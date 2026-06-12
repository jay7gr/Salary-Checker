/*
 * embed-promo.js — slim, dismissible top bar promoting the free embeddable
 * widgets. Included on the homepage, tool pages and blog articles.
 *
 * Deliberately self-contained (no deps) and defensive:
 *  - Never shows inside an embedded widget (?embed=1 / .embed-mode), otherwise
 *    embeds would advertise "embed me" to their own visitors.
 *  - Hidden once dismissed (localStorage), so it's a one-time nudge.
 *  - Rendered as a normal top-of-body block (not fixed), so it pushes in-flow
 *    content down with no overlap and scrolls away as the visitor uses the tool.
 *  - Mobile-safe: on phones the app chrome (hamburger, theme toggle, stats
 *    burger) is position:fixed at the very top, so it would float OVER the bar.
 *    We measure the bar height and push that fixed chrome down by it (mobile
 *    only), keeping everything aligned.
 */
(function () {
  'use strict';
  try {
    var params = new URLSearchParams(location.search);
    if (params.get('embed') === '1' ||
        document.documentElement.classList.contains('embed-mode')) return;
    if (localStorage.getItem('embedPromoDismissed') === '1') return;
  } catch (e) { /* if storage/URL is unavailable, fail open and still show */ }

  var bar, onResize;

  function setHeight() {
    if (bar) document.documentElement.style.setProperty('--embed-promo-h', bar.offsetHeight + 'px');
  }

  function injectOffsetStyle() {
    if (document.getElementById('embedPromoOffsetStyle')) return;
    var st = document.createElement('style');
    st.id = 'embedPromoOffsetStyle';
    // On mobile, the top chrome is position:fixed (viewport-anchored) so the
    // in-flow bar slides under it. Shift it down by the bar height. translateY
    // is independent of each element's own top value, so we don't need to know
    // whether it's 16px or 23px. Desktop (chrome is in-flow) is untouched.
    st.textContent =
      '@media (max-width:768px){' +
        'html.embed-promo-on .nav-burger,' +
        'html.embed-promo-on .theme-toggle,' +
        'html.embed-promo-on .sidebar-burger{' +
          'transform:translateY(var(--embed-promo-h,0px))!important;' +
        '}' +
      '}';
    (document.head || document.documentElement).appendChild(st);
  }

  function init() {
    if (document.getElementById('embedPromoBar')) return;

    bar = document.createElement('div');
    bar.id = 'embedPromoBar';
    bar.setAttribute('role', 'region');
    bar.setAttribute('aria-label', 'Add our free calculators to your website');
    bar.style.cssText = [
      'box-sizing:border-box', 'width:100%', 'max-width:100%', 'overflow-wrap:break-word',
      'background:#2563eb', 'color:#fff',
      'font:500 13px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif',
      'padding:9px 48px', 'text-align:center', 'position:relative', 'z-index:2147483600'
    ].join(';') + ';';

    // Short copy keeps it to ~1 line on phones; the CTA never breaks mid-phrase.
    bar.innerHTML =
      '🧩 <strong>Run a website?</strong> Embed these calculators free — ' +
      '<a href="/widget" style="color:#fff;text-decoration:underline;font-weight:600;white-space:nowrap;">get the code →</a>' +
      '<button type="button" id="embedPromoClose" aria-label="Dismiss" ' +
      'style="position:absolute;top:0;right:0;height:100%;width:44px;background:none;border:0;' +
      'color:#fff;font-size:22px;line-height:1;cursor:pointer;opacity:0.85;padding:0;">×</button>';

    document.body.insertBefore(bar, document.body.firstChild);

    injectOffsetStyle();
    document.documentElement.classList.add('embed-promo-on');
    setHeight();
    onResize = function () { setHeight(); };
    window.addEventListener('resize', onResize);
    window.addEventListener('orientationchange', onResize);

    var closeBtn = document.getElementById('embedPromoClose');
    if (closeBtn) {
      closeBtn.addEventListener('click', function () {
        if (bar && bar.parentNode) bar.parentNode.removeChild(bar);
        document.documentElement.classList.remove('embed-promo-on');
        document.documentElement.style.removeProperty('--embed-promo-h');
        if (onResize) {
          window.removeEventListener('resize', onResize);
          window.removeEventListener('orientationchange', onResize);
        }
        try { localStorage.setItem('embedPromoDismissed', '1'); } catch (e) {}
      });
    }

    var link = bar.querySelector('a');
    if (link) {
      link.addEventListener('click', function () {
        try { if (typeof gtag === 'function') gtag('event', 'embed_promo_click', { page_path: location.pathname }); } catch (e) {}
      });
    }
  }

  if (document.body) init();
  else document.addEventListener('DOMContentLoaded', init);
})();
