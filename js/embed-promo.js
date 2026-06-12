/*
 * embed-promo.js — slim, dismissible top bar promoting the free embeddable
 * widgets. Included on the homepage, tool pages and blog articles.
 *
 * Deliberately self-contained (no deps) and defensive:
 *  - Never shows inside an embedded widget (?embed=1 / .embed-mode), otherwise
 *    embeds would advertise "embed me" to their own visitors.
 *  - Hidden once dismissed (localStorage), so it's a one-time nudge.
 *  - Rendered as a normal top-of-body block (not fixed), so it pushes content
 *    down with no overlap and scrolls away as the visitor uses the tool — i.e.
 *    visible on load without permanently stealing space from the core action.
 */
(function () {
  'use strict';
  try {
    var params = new URLSearchParams(location.search);
    if (params.get('embed') === '1' ||
        document.documentElement.classList.contains('embed-mode')) return;
    if (localStorage.getItem('embedPromoDismissed') === '1') return;
  } catch (e) { /* if storage/URL is unavailable, fail open and still show */ }

  function init() {
    if (document.getElementById('embedPromoBar')) return;

    var bar = document.createElement('div');
    bar.id = 'embedPromoBar';
    bar.setAttribute('role', 'region');
    bar.setAttribute('aria-label', 'Add our free calculators to your website');
    bar.style.cssText = [
      'box-sizing:border-box', 'width:100%', 'max-width:100%', 'overflow-wrap:break-word',
      'background:#2563eb', 'color:#fff',
      'font:500 13px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif',
      'padding:8px 46px 8px 14px', 'text-align:center', 'position:relative'
    ].join(';') + ';';

    // Short copy keeps it to ~1 line on phones; the CTA never breaks mid-phrase.
    bar.innerHTML =
      '🧩 <strong>Run a website?</strong> Embed these calculators free — ' +
      '<a href="/widget" style="color:#fff;text-decoration:underline;font-weight:600;white-space:nowrap;">get the code →</a>' +
      '<button type="button" id="embedPromoClose" aria-label="Dismiss" ' +
      'style="position:absolute;top:0;right:0;height:100%;min-width:44px;background:none;border:0;' +
      'color:#fff;font-size:20px;line-height:1;cursor:pointer;opacity:0.85;padding:0 12px;">×</button>';

    document.body.insertBefore(bar, document.body.firstChild);

    var closeBtn = document.getElementById('embedPromoClose');
    if (closeBtn) {
      closeBtn.addEventListener('click', function () {
        bar.parentNode && bar.parentNode.removeChild(bar);
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
