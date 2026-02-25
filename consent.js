/**
 * Consent Management Platform (CMP) for salary-converter.com
 *
 * - Analytics (GA4) always runs — no consent needed
 * - Only gates ad signals (ad_storage, ad_user_data, ad_personalization)
 * - Banner shown ONLY in strict consent regions (EU/EEA, UK, CH, BR, CA)
 * - Two-tier UI: Accept + More Options → toggles + Save/Decline All
 */
(function() {
    'use strict';

    var COOKIE_NAME = 'sc_consent';
    var COOKIE_DAYS = 365;
    var GEO_API = 'https://api.country.is/';
    var GEO_TIMEOUT = 2000;

    // Regions where banner is shown (ISO 3166-1 alpha-2)
    var CMP_REGIONS = [
        'AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR',
        'DE','GR','HU','IE','IT','LV','LT','LU','MT','NL',
        'PL','PT','RO','SK','SI','ES','SE',
        'IS','LI','NO',
        'GB','CH','BR','CA'
    ];

    // --- Cookie Manager ---

    function getCookie(name) {
        var match = document.cookie.match(new RegExp('(?:^|; )' + name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '=([^;]*)'));
        return match ? match[1] : null;
    }

    function setCookie(name, value, days) {
        var d = new Date();
        d.setTime(d.getTime() + days * 86400000);
        document.cookie = name + '=' + value + ';expires=' + d.toUTCString() + ';path=/;SameSite=Lax';
    }

    function getStoredConsent() {
        var raw = getCookie(COOKIE_NAME);
        if (!raw) return null;
        try { return JSON.parse(decodeURIComponent(raw)); } catch(e) { return null; }
    }

    function storeConsent(obj) {
        obj.v = 1;
        obj.ts = Math.floor(Date.now() / 1000);
        setCookie(COOKIE_NAME, encodeURIComponent(JSON.stringify(obj)), COOKIE_DAYS);
    }

    // --- Consent Engine ---

    function applyConsent(obj) {
        if (typeof gtag === 'function') {
            gtag('consent', 'update', {
                'ad_storage': obj.ad_storage || 'denied',
                'ad_user_data': obj.ad_user_data || 'denied',
                'ad_personalization': obj.ad_personalization || 'denied'
            });
        }
    }

    function acceptAll() {
        var c = { ad_storage: 'granted', ad_user_data: 'granted', ad_personalization: 'granted' };
        applyConsent(c);
        storeConsent(c);
        destroyBanner();
    }

    function declineAll() {
        var c = { ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' };
        applyConsent(c);
        storeConsent(c);
        destroyBanner();
    }

    function savePreferences(adEnabled) {
        var val = adEnabled ? 'granted' : 'denied';
        var c = { ad_storage: val, ad_user_data: val, ad_personalization: val };
        applyConsent(c);
        storeConsent(c);
        destroyBanner();
    }

    // --- Region Detection ---

    function detectRegion() {
        return new Promise(function(resolve) {
            var timer = setTimeout(function() { resolve(null); }, GEO_TIMEOUT);
            fetch(GEO_API).then(function(r) {
                return r.json();
            }).then(function(data) {
                clearTimeout(timer);
                resolve(data && data.country ? data.country : null);
            }).catch(function() {
                clearTimeout(timer);
                resolve(null);
            });
        });
    }

    function getTimezoneRegion() {
        try {
            var tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
            if (!tz) return null;
            var parts = tz.split('/');
            if (parts[0] === 'Europe') return 'EU_LIKELY';
            // Brazil
            if (tz === 'America/Sao_Paulo' || tz === 'America/Fortaleza' || tz === 'America/Recife' ||
                tz === 'America/Bahia' || tz === 'America/Belem' || tz === 'America/Manaus' ||
                tz === 'America/Cuiaba' || tz === 'America/Porto_Velho' || tz === 'America/Boa_Vista' ||
                tz === 'America/Campo_Grande' || tz === 'America/Araguaina' || tz === 'America/Maceio' ||
                tz === 'America/Noronha' || tz === 'America/Rio_Branco') return 'BR';
            // Canada
            if (tz === 'America/Toronto' || tz === 'America/Vancouver' || tz === 'America/Edmonton' ||
                tz === 'America/Winnipeg' || tz === 'America/Halifax' || tz === 'America/St_Johns' ||
                tz === 'America/Regina' || tz === 'America/Moncton' || tz === 'America/Thunder_Bay' ||
                tz === 'America/Iqaluit' || tz === 'America/Whitehorse' || tz === 'America/Yellowknife') return 'CA';
            // UK (covers Atlantic/Reykjavik too which is Iceland)
            if (tz === 'Atlantic/Reykjavik') return 'IS';
            return null;
        } catch(e) { return null; }
    }

    function isConsentRequired(code) {
        if (!code) return false;
        if (code === 'EU_LIKELY') return true;
        return CMP_REGIONS.indexOf(code.toUpperCase()) !== -1;
    }

    // --- Banner Renderer ---

    var bannerEl = null;

    function injectStyles() {
        var style = document.createElement('style');
        style.textContent = [
            '.sc-cb{position:fixed;bottom:0;left:0;right:0;z-index:99999;',
            'background:var(--card-bg,#fff);border-top:1px solid var(--border,#e5e5ea);',
            'box-shadow:0 -2px 20px rgba(0,0,0,0.08);padding:16px 24px;',
            'font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;',
            'transform:translateY(100%);transition:transform .3s ease;',
            'color:var(--text-primary,#1d1d1f)}',

            '.sc-cb.sc-cb-show{transform:translateY(0)}',

            '.sc-cb-t1{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap}',
            '.sc-cb-text{margin:0;font-size:14px;color:var(--text-body,#4a4a4c);flex:1 1 300px;line-height:1.5}',
            '.sc-cb-link{color:var(--accent,#2563eb);text-decoration:underline}',
            '.sc-cb-actions{display:flex;gap:10px;flex-shrink:0}',

            '.sc-cb-btn{border:none;padding:10px 20px;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer;transition:opacity .2s}',
            '.sc-cb-btn:hover{opacity:0.85}',
            '.sc-cb-accept{background:var(--accent,#2563eb);color:#fff}',
            '.sc-cb-more{background:var(--tag-bg,#f0f0f2);color:var(--text-primary,#1d1d1f)}',
            '.sc-cb-save{background:var(--accent,#2563eb);color:#fff}',
            '.sc-cb-decline{background:var(--tag-bg,#f0f0f2);color:var(--text-primary,#1d1d1f)}',

            '.sc-cb-t2{display:none;padding-top:16px}',
            '.sc-cb-t2.sc-cb-t2-show{display:block}',
            '.sc-cb-heading{margin:0 0 14px;font-size:16px;font-weight:700;color:var(--text-primary,#1d1d1f)}',

            '.sc-cb-option{display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid var(--border,#e5e5ea)}',
            '.sc-cb-option:last-of-type{border-bottom:none}',
            '.sc-cb-opt-info{flex:1}',
            '.sc-cb-opt-label{display:block;font-size:14px;font-weight:600;color:var(--text-primary,#1d1d1f)}',
            '.sc-cb-opt-desc{display:block;font-size:12px;color:var(--text-secondary,#86868b);margin-top:2px}',

            // Toggle switch
            '.sc-cb-toggle{position:relative;width:44px;height:24px;flex-shrink:0;margin-left:12px}',
            '.sc-cb-toggle input{opacity:0;width:0;height:0;position:absolute}',
            '.sc-cb-slider{position:absolute;inset:0;background:var(--border-mid,#d2d2d7);border-radius:24px;cursor:pointer;transition:background .2s}',
            '.sc-cb-slider::before{content:"";position:absolute;left:2px;top:2px;width:20px;height:20px;background:#fff;border-radius:50%;transition:transform .2s}',
            '.sc-cb-toggle input:checked+.sc-cb-slider{background:var(--accent,#2563eb)}',
            '.sc-cb-toggle input:checked+.sc-cb-slider::before{transform:translateX(20px)}',
            '.sc-cb-toggle.sc-cb-disabled{opacity:0.5}',
            '.sc-cb-toggle.sc-cb-disabled .sc-cb-slider{cursor:not-allowed}',

            '.sc-cb-t2-actions{display:flex;gap:10px;margin-top:16px;justify-content:flex-end}',

            // Mobile
            '@media(max-width:600px){',
            '.sc-cb{padding:14px 16px}',
            '.sc-cb-t1{flex-direction:column;align-items:stretch;gap:12px}',
            '.sc-cb-actions{justify-content:stretch}',
            '.sc-cb-btn{flex:1;text-align:center}',
            '.sc-cb-t2-actions{flex-direction:column}',
            '}'
        ].join('');
        document.head.appendChild(style);
    }

    function showBanner() {
        bannerEl = document.createElement('div');
        bannerEl.id = 'sc-consent-banner';
        bannerEl.className = 'sc-cb';
        bannerEl.setAttribute('role', 'dialog');
        bannerEl.setAttribute('aria-label', 'Cookie consent');

        // Tier 1
        var t1 = document.createElement('div');
        t1.className = 'sc-cb-t1';

        var text = document.createElement('p');
        text.className = 'sc-cb-text';
        text.innerHTML = 'We use cookies to improve your experience and for advertising personalization. ' +
            '<a href="/privacy/" class="sc-cb-link">Learn more</a>';

        var actions1 = document.createElement('div');
        actions1.className = 'sc-cb-actions';

        var btnAccept = document.createElement('button');
        btnAccept.className = 'sc-cb-btn sc-cb-accept';
        btnAccept.textContent = 'Accept';
        btnAccept.addEventListener('click', acceptAll);

        var btnMore = document.createElement('button');
        btnMore.className = 'sc-cb-btn sc-cb-more';
        btnMore.textContent = 'More Options';
        btnMore.addEventListener('click', function() {
            t1.style.display = 'none';
            t2.classList.add('sc-cb-t2-show');
        });

        actions1.appendChild(btnAccept);
        actions1.appendChild(btnMore);
        t1.appendChild(text);
        t1.appendChild(actions1);

        // Tier 2
        var t2 = document.createElement('div');
        t2.className = 'sc-cb-t2';

        var heading = document.createElement('h3');
        heading.className = 'sc-cb-heading';
        heading.textContent = 'Cookie Preferences';

        // Advertising option (defaults ON — user can toggle off)
        var adToggleInput = null;
        var optAd = createOption('Advertising & Personalization', 'Used for ad targeting and personalization', true, false);
        adToggleInput = optAd.querySelector('input');

        var actions2 = document.createElement('div');
        actions2.className = 'sc-cb-t2-actions';

        var btnAcceptAll = document.createElement('button');
        btnAcceptAll.className = 'sc-cb-btn sc-cb-accept';
        btnAcceptAll.textContent = 'Accept All';
        btnAcceptAll.addEventListener('click', function() {
            savePreferences(adToggleInput && adToggleInput.checked);
        });

        var btnReject = document.createElement('button');
        btnReject.className = 'sc-cb-btn sc-cb-decline';
        btnReject.textContent = 'Reject All';
        btnReject.addEventListener('click', declineAll);

        actions2.appendChild(btnAcceptAll);
        actions2.appendChild(btnReject);

        t2.appendChild(heading);
        t2.appendChild(optAd);
        t2.appendChild(actions2);

        bannerEl.appendChild(t1);
        bannerEl.appendChild(t2);
        document.body.appendChild(bannerEl);

        // Trigger animation
        requestAnimationFrame(function() {
            requestAnimationFrame(function() {
                bannerEl.classList.add('sc-cb-show');
            });
        });
    }

    function createOption(label, desc, checked, disabled) {
        var opt = document.createElement('div');
        opt.className = 'sc-cb-option';

        var info = document.createElement('div');
        info.className = 'sc-cb-opt-info';
        var lbl = document.createElement('span');
        lbl.className = 'sc-cb-opt-label';
        lbl.textContent = label;
        var d = document.createElement('span');
        d.className = 'sc-cb-opt-desc';
        d.textContent = desc;
        info.appendChild(lbl);
        info.appendChild(d);

        var toggle = document.createElement('label');
        toggle.className = 'sc-cb-toggle' + (disabled ? ' sc-cb-disabled' : '');
        var input = document.createElement('input');
        input.type = 'checkbox';
        input.checked = checked;
        if (disabled) input.disabled = true;
        var slider = document.createElement('span');
        slider.className = 'sc-cb-slider';
        toggle.appendChild(input);
        toggle.appendChild(slider);

        opt.appendChild(info);
        opt.appendChild(toggle);
        return opt;
    }

    function destroyBanner() {
        if (bannerEl) {
            bannerEl.classList.remove('sc-cb-show');
            setTimeout(function() {
                if (bannerEl && bannerEl.parentNode) {
                    bannerEl.parentNode.removeChild(bannerEl);
                }
                bannerEl = null;
            }, 350);
        }
    }

    // --- Init ---

    function main() {
        // 1. Check stored consent
        var stored = getStoredConsent();
        if (stored) {
            applyConsent(stored);
            return;
        }

        // 2. Detect region
        detectRegion().then(function(country) {
            var region = country;
            if (!region) {
                region = getTimezoneRegion();
            }
            if (isConsentRequired(region)) {
                injectStyles();
                showBanner();
            }
        });
    }

    // Script is deferred, DOM is ready
    main();
})();
