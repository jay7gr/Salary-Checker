/**
 * Flagged Wise affiliate CTA (shared).
 * WISE_AFFILIATE_URL empty = flag OFF — mount is a no-op (nothing rendered).
 * Scope: /compare/* (via Functions inject) and /offer-evaluator/ only.
 * Never runs meaningful UI inside embeds.
 */
(function () {
  'use strict';

  // Flag: empty string = off. Do not commit a live tracking URL.
  var WISE_AFFILIATE_URL = '';

  var ROOT_ID = 'sc-wise-affiliate';

  function isEmbedContext() {
    try {
      if (window.self !== window.top) return true;
    } catch (e) {
      return true;
    }
    var path = (location.pathname || '').toLowerCase();
    if (path.indexOf('embed') !== -1) return true;
    if (/(?:^|[?&])embed=1(?:&|$)/.test(location.search || '')) return true;
    return false;
  }

  function clear() {
    var el = document.getElementById(ROOT_ID);
    if (el && el.parentNode) el.parentNode.removeChild(el);
  }

  function ensureStyles() {
    if (document.getElementById('sc-wise-affiliate-style')) return;
    var style = document.createElement('style');
    style.id = 'sc-wise-affiliate-style';
    style.textContent =
      '#' + ROOT_ID + '{' +
        'margin:14px 0 18px;' +
        'padding:0;' +
        'font-size:0.88rem;' +
        'line-height:1.45;' +
        'color:var(--text-secondary,#86868b);' +
        'display:flex;' +
        'flex-wrap:wrap;' +
        'align-items:baseline;' +
        'gap:8px 10px;' +
      '}' +
      '#' + ROOT_ID + ' a{' +
        'color:var(--accent,#2563eb);' +
        'text-decoration:underline;' +
        'text-underline-offset:2px;' +
        'font-weight:600;' +
      '}' +
      '#' + ROOT_ID + ' a:hover{color:var(--accent-hover,#1d4ed8)}' +
      '#' + ROOT_ID + ' .sc-wise-affiliate-label{' +
        'font-size:0.72rem;' +
        'font-weight:600;' +
        'letter-spacing:0.02em;' +
        'text-transform:uppercase;' +
        'color:var(--text-secondary,#86868b);' +
        'opacity:0.85;' +
      '}';
    document.head.appendChild(style);
  }

  /**
   * @param {{pageType:'compare'|'offer_evaluator', currencyA:string, currencyB:string, anchor:Element|null, position?:'after'|'append'}} opts
   */
  function mount(opts) {
    clear();
    if (!WISE_AFFILIATE_URL || typeof WISE_AFFILIATE_URL !== 'string') return;
    if (isEmbedContext()) return;
    if (!opts || !opts.pageType) return;

    var a = String(opts.currencyA || '').trim().toUpperCase();
    var b = String(opts.currencyB || '').trim().toUpperCase();
    if (!a || !b || a === b) return;

    var anchor = opts.anchor;
    if (!anchor || !anchor.parentNode) return;

    ensureStyles();

    var wrap = document.createElement('div');
    wrap.id = ROOT_ID;
    wrap.setAttribute('data-partner', 'wise');
    wrap.setAttribute('data-page-type', opts.pageType);

    var link = document.createElement('a');
    link.href = WISE_AFFILIATE_URL;
    link.target = '_blank';
    link.rel = 'sponsored nofollow noopener';
    link.textContent = 'Moving money between these currencies? Compare Wise fees';
    link.addEventListener('click', function () {
      try {
        if (typeof gtag === 'function') {
          gtag('event', 'affiliate_click', {
            partner: 'wise',
            page_type: opts.pageType
          });
        }
      } catch (err) { /* ignore */ }
    });

    var label = document.createElement('span');
    label.className = 'sc-wise-affiliate-label';
    label.textContent = 'Affiliate link';

    wrap.appendChild(link);
    wrap.appendChild(label);

    if (opts.position === 'append') {
      anchor.appendChild(wrap);
    } else {
      anchor.parentNode.insertBefore(wrap, anchor.nextSibling);
    }
  }

  function currenciesFromCompareDom() {
    var out = [];
    var stats = document.querySelectorAll('.compare-stat');
    for (var i = 0; i < stats.length; i++) {
      var label = stats[i].querySelector('.label');
      var value = stats[i].querySelector('.value');
      if (!label || !value) continue;
      if (!/^\s*currency\s*$/i.test(label.textContent || '')) continue;
      var code = String(value.textContent || '').trim().toUpperCase();
      if (/^[A-Z]{3}$/.test(code)) out.push(code);
    }
    return out;
  }

  function initComparePage() {
    var path = location.pathname || '';
    if (path.indexOf('/compare/') === -1) return;
    if (isEmbedContext()) return;

    var codes = currenciesFromCompareDom();
    if (codes.length < 2) return;

    var anchor =
      document.querySelector('.hero .share-bar') ||
      document.querySelector('section.hero') ||
      document.querySelector('.compare-grid');
    if (!anchor) return;

    mount({
      pageType: 'compare',
      currencyA: codes[0],
      currencyB: codes[1],
      anchor: anchor,
      position: 'after'
    });
  }

  window.SCWiseAffiliate = {
    url: WISE_AFFILIATE_URL,
    mount: mount,
    clear: clear,
    isEmbedContext: isEmbedContext
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initComparePage);
  } else {
    initComparePage();
  }
})();
