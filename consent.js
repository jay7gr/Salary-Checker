/**
 * Consent Management Platform (CMP) for salary-converter.com
 *
 * Consent Mode v2:
 * - In strict consent regions (EU/EEA, UK, CH, BR, CA): analytics + ads denied
 *   until the user accepts (or grants via More Options).
 * - Elsewhere: analytics + ads granted by default (no banner).
 * - Essential: sc_consent preference cookie only after interaction.
 */
(function() {
    'use strict';

    var COOKIE_NAME = 'sc_consent';
    var COOKIE_DAYS = 365;
    var GEO_API = 'https://api.country.is/';
    var GEO_TIMEOUT = 2000;

    var CMP_REGIONS = [
        'AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR',
        'DE','GR','HU','IE','IT','LV','LT','LU','MT','NL',
        'PL','PT','RO','SK','SI','ES','SE',
        'IS','LI','NO',
        'GB','CH','BR','CA'
    ];

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
        obj.v = 2;
        obj.ts = Math.floor(Date.now() / 1000);
        setCookie(COOKIE_NAME, encodeURIComponent(JSON.stringify(obj)), COOKIE_DAYS);
    }

    function applyConsent(obj) {
        if (typeof gtag !== 'function') return;
        gtag('consent', 'update', {
            'ad_storage': obj.ad_storage || 'denied',
            'ad_user_data': obj.ad_user_data || 'denied',
            'ad_personalization': obj.ad_personalization || 'denied',
            'analytics_storage': obj.analytics_storage || 'denied'
        });
    }

    function consentPayload(ad, analytics) {
        var a = ad ? 'granted' : 'denied';
        var g = analytics ? 'granted' : 'denied';
        return {
            ad_storage: a,
            ad_user_data: a,
            ad_personalization: a,
            analytics_storage: g
        };
    }

    function acceptAll() {
        var c = consentPayload(true, true);
        applyConsent(c);
        storeConsent(c);
        destroyBanner();
    }

    function declineAll() {
        var c = consentPayload(false, false);
        applyConsent(c);
        storeConsent(c);
        destroyBanner();
    }

    function savePreferences(adEnabled, analyticsEnabled) {
        var c = consentPayload(!!adEnabled, !!analyticsEnabled);
        applyConsent(c);
        storeConsent(c);
        destroyBanner();
    }

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
            if (tz.indexOf('America/Sao_Paulo') === 0 || tz.indexOf('America/Fortaleza') === 0 ||
                tz.indexOf('America/Recife') === 0 || tz.indexOf('America/Bahia') === 0 ||
                tz.indexOf('America/Manaus') === 0 || tz.indexOf('America/Belem') === 0 ||
                tz.indexOf('America/Cuiaba') === 0 || tz.indexOf('America/Rio_Branco') === 0) return 'BR';
            if (tz.indexOf('America/Toronto') === 0 || tz.indexOf('America/Vancouver') === 0 ||
                tz.indexOf('America/Edmonton') === 0 || tz.indexOf('America/Winnipeg') === 0 ||
                tz.indexOf('America/Halifax') === 0 || tz.indexOf('America/St_Johns') === 0 ||
                tz.indexOf('America/Regina') === 0 || tz.indexOf('America/Moncton') === 0) return 'CA';
            if (tz === 'Atlantic/Reykjavik') return 'IS';
            return null;
        } catch(e) { return null; }
    }

    function isConsentRequired(code) {
        if (!code) return false;
        if (code === 'EU_LIKELY') return true;
        return CMP_REGIONS.indexOf(code.toUpperCase()) !== -1;
    }

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
            '.sc-cb-actions{display:flex;gap:10px;flex-shrink:0;flex-wrap:wrap}',
            '.sc-cb-btn{border:none;padding:10px 20px;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer;transition:opacity .2s}',
            '.sc-cb-btn:hover{opacity:0.85}',
            '.sc-cb-accept{background:var(--accent,#2563eb);color:#fff}',
            '.sc-cb-more{background:var(--tag-bg,#f0f0f2);color:var(--text-primary,#1d1d1f)}',
            '.sc-cb-decline{background:var(--tag-bg,#f0f0f2);color:var(--text-primary,#1d1d1f)}',
            '.sc-cb-t2{display:none;padding-top:16px}',
            '.sc-cb-t2.sc-cb-t2-show{display:block}',
            '.sc-cb-heading{margin:0 0 14px;font-size:16px;font-weight:700;color:var(--text-primary,#1d1d1f)}',
            '.sc-cb-option{display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid var(--border,#e5e5ea)}',
            '.sc-cb-option:last-of-type{border-bottom:none}',
            '.sc-cb-opt-info{flex:1}',
            '.sc-cb-opt-label{display:block;font-size:14px;font-weight:600;color:var(--text-primary,#1d1d1f)}',
            '.sc-cb-opt-desc{display:block;font-size:12px;color:var(--text-secondary,#86868b);margin-top:2px}',
            '.sc-cb-toggle{position:relative;width:44px;height:24px;flex-shrink:0;margin-left:12px}',
            '.sc-cb-toggle input{opacity:0;width:0;height:0;position:absolute}',
            '.sc-cb-slider{position:absolute;inset:0;background:var(--border-mid,#d2d2d7);border-radius:24px;cursor:pointer;transition:background .2s}',
            '.sc-cb-slider::before{content:"";position:absolute;left:2px;top:2px;width:20px;height:20px;background:#fff;border-radius:50%;transition:transform .2s}',
            '.sc-cb-toggle input:checked+.sc-cb-slider{background:var(--accent,#2563eb)}',
            '.sc-cb-toggle input:checked+.sc-cb-slider::before{transform:translateX(20px)}',
            '.sc-cb-t2-actions{display:flex;gap:10px;margin-top:16px;justify-content:flex-end;flex-wrap:wrap}',
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

    function createOption(label, desc, checked) {
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
        toggle.className = 'sc-cb-toggle';
        var input = document.createElement('input');
        input.type = 'checkbox';
        input.checked = checked;
        var slider = document.createElement('span');
        slider.className = 'sc-cb-slider';
        toggle.appendChild(input);
        toggle.appendChild(slider);
        opt.appendChild(info);
        opt.appendChild(toggle);
        return opt;
    }

    function showBanner() {
        bannerEl = document.createElement('div');
        bannerEl.id = 'sc-consent-banner';
        bannerEl.className = 'sc-cb';
        bannerEl.setAttribute('role', 'dialog');
        bannerEl.setAttribute('aria-label', 'Cookie consent');

        var t1 = document.createElement('div');
        t1.className = 'sc-cb-t1';

        var text = document.createElement('p');
        text.className = 'sc-cb-text';
        text.innerHTML = 'We use cookies for analytics and advertising. You can accept, reject, or choose preferences. ' +
            '<a href="/privacy/" class="sc-cb-link">Privacy Policy</a>';

        var actions1 = document.createElement('div');
        actions1.className = 'sc-cb-actions';

        var btnAccept = document.createElement('button');
        btnAccept.className = 'sc-cb-btn sc-cb-accept';
        btnAccept.textContent = 'Accept all';
        btnAccept.addEventListener('click', acceptAll);

        var btnReject = document.createElement('button');
        btnReject.className = 'sc-cb-btn sc-cb-decline';
        btnReject.textContent = 'Reject all';
        btnReject.addEventListener('click', declineAll);

        var btnMore = document.createElement('button');
        btnMore.className = 'sc-cb-btn sc-cb-more';
        btnMore.textContent = 'More options';
        btnMore.addEventListener('click', function() {
            t1.style.display = 'none';
            t2.classList.add('sc-cb-t2-show');
        });

        actions1.appendChild(btnAccept);
        actions1.appendChild(btnReject);
        actions1.appendChild(btnMore);
        t1.appendChild(text);
        t1.appendChild(actions1);

        var t2 = document.createElement('div');
        t2.className = 'sc-cb-t2';

        var heading = document.createElement('h3');
        heading.className = 'sc-cb-heading';
        heading.textContent = 'Cookie preferences';

        var optAnalytics = createOption(
            'Analytics',
            'Helps us understand site usage (Google Analytics). Off by default in your region until you opt in.',
            false
        );
        var optAd = createOption(
            'Advertising',
            'Used for Google AdSense ad measurement and personalization.',
            false
        );
        var analyticsInput = optAnalytics.querySelector('input');
        var adInput = optAd.querySelector('input');

        var actions2 = document.createElement('div');
        actions2.className = 'sc-cb-t2-actions';

        var btnSave = document.createElement('button');
        btnSave.className = 'sc-cb-btn sc-cb-accept';
        btnSave.textContent = 'Save preferences';
        btnSave.addEventListener('click', function() {
            savePreferences(adInput && adInput.checked, analyticsInput && analyticsInput.checked);
        });

        var btnDecline2 = document.createElement('button');
        btnDecline2.className = 'sc-cb-btn sc-cb-decline';
        btnDecline2.textContent = 'Reject all';
        btnDecline2.addEventListener('click', declineAll);

        actions2.appendChild(btnSave);
        actions2.appendChild(btnDecline2);

        t2.appendChild(heading);
        t2.appendChild(optAnalytics);
        t2.appendChild(optAd);
        t2.appendChild(actions2);

        bannerEl.appendChild(t1);
        bannerEl.appendChild(t2);
        document.body.appendChild(bannerEl);

        requestAnimationFrame(function() {
            requestAnimationFrame(function() {
                bannerEl.classList.add('sc-cb-show');
            });
        });
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

    function main() {
        var stored = getStoredConsent();
        if (stored) {
            // Migrate v1 cookies (no analytics_storage) → treat analytics as granted if any ads were granted
            if (!stored.analytics_storage) {
                stored.analytics_storage = (stored.ad_storage === 'granted') ? 'granted' : 'denied';
            }
            applyConsent(stored);
            return;
        }

        detectRegion().then(function(country) {
            var region = country || getTimezoneRegion();
            if (isConsentRequired(region)) {
                // Keep defaults denied until user chooses (set in page head Consent Mode defaults)
                injectStyles();
                showBanner();
            }
            // Non-CMP regions: page head defaults already grant analytics + ads
        });
    }

    main();
})();
