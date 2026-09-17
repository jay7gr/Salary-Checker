/**
 * Keep-result: quiet local Recent (localStorage only).
 * Keys: sc.recent.main | sc.recent.oe — cap 5, {id,ts,label,url}.
 */
(function (global) {
  'use strict';

  var CAP = 5;
  var KEYS = { main: 'sc.recent.main', oe: 'sc.recent.oe' };

  function storageKey(tool) {
    return KEYS[tool] || null;
  }

  function safeRead(tool) {
    var key = storageKey(tool);
    if (!key) return [];
    try {
      var raw = localStorage.getItem(key);
      if (!raw) return [];
      var arr = JSON.parse(raw);
      if (!Array.isArray(arr)) return [];
      return arr.filter(function (e) {
        return e && typeof e.url === 'string' && e.url.length > 0;
      }).slice(0, CAP);
    } catch (e) {
      return [];
    }
  }

  function safeWrite(tool, list) {
    var key = storageKey(tool);
    if (!key) return false;
    try {
      localStorage.setItem(key, JSON.stringify(list.slice(0, CAP)));
      return true;
    } catch (e) {
      return false;
    }
  }

  /** Dedupe key: pathname (no trailing slash except root) + search */
  function urlKey(url) {
    try {
      var u = new URL(url, location.origin);
      var path = u.pathname;
      if (path.length > 1 && path.endsWith('/')) path = path.slice(0, -1);
      return path + u.search;
    } catch (e) {
      return String(url || '');
    }
  }

  function makeId() {
    return Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
  }

  function add(tool, entry) {
    if (!entry || !entry.url) return safeRead(tool);
    var list = safeRead(tool);
    var key = urlKey(entry.url);
    list = list.filter(function (e) { return urlKey(e.url) !== key; });
    list.unshift({
      id: entry.id || makeId(),
      ts: typeof entry.ts === 'number' ? entry.ts : Date.now(),
      label: String(entry.label || 'Recent').slice(0, 120),
      url: entry.url
    });
    if (list.length > CAP) list = list.slice(0, CAP);
    safeWrite(tool, list);
    return list;
  }

  function remove(tool, id) {
    var list = safeRead(tool).filter(function (e) { return e.id !== id; });
    safeWrite(tool, list);
    return list;
  }

  function clear(tool) {
    safeWrite(tool, []);
    return [];
  }

  function relativeTime(ts) {
    if (!ts) return '';
    var diff = Date.now() - ts;
    if (diff < 0) diff = 0;
    var sec = Math.floor(diff / 1000);
    if (sec < 60) return 'just now';
    var min = Math.floor(sec / 60);
    if (min < 60) return min + 'm ago';
    var hr = Math.floor(min / 60);
    if (hr < 48) return hr + 'h ago';
    var day = Math.floor(hr / 24);
    if (day < 14) return day + 'd ago';
    try {
      return new Date(ts).toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
    } catch (e) {
      return '';
    }
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  var _mounted = {};

  function render(tool) {
    var state = _mounted[tool];
    if (!state || !state.root) return;
    var root = state.root;
    var list = safeRead(tool);
    var n = list.length;

    if (n === 0) {
      root.hidden = true;
      root.setAttribute('hidden', '');
      root.innerHTML = '';
      return;
    }

    root.hidden = false;
    root.removeAttribute('hidden');

    var wasOpen = !!(state.details && state.details.open);
    var rows = list.map(function (e) {
      var time = relativeTime(e.ts);
      return (
        '<li class="sc-recent-row" data-id="' + escapeHtml(e.id) + '">' +
          '<button type="button" class="sc-recent-open" data-url="' + escapeHtml(e.url) + '">' +
            '<span class="sc-recent-label">' + escapeHtml(e.label) + '</span>' +
            (time ? '<span class="sc-recent-time">' + escapeHtml(time) + '</span>' : '') +
          '</button>' +
          '<button type="button" class="sc-recent-remove" aria-label="Remove from Recent" data-id="' + escapeHtml(e.id) + '" title="Remove">' +
            '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 6L6 18M6 6l12 12"/></svg>' +
          '</button>' +
        '</li>'
      );
    }).join('');

    root.innerHTML =
      '<details class="sc-recent-details"' + (wasOpen ? ' open' : '') + '>' +
        '<summary class="sc-recent-summary">Recent on this device (' + n + ')</summary>' +
        '<div class="sc-recent-body">' +
          '<p class="sc-recent-privacy">Stored only in this browser. Clearing site data removes it.</p>' +
          '<ul class="sc-recent-list" role="list">' + rows + '</ul>' +
          '<div class="sc-recent-footer">' +
            '<button type="button" class="sc-recent-clear">Clear all</button>' +
          '</div>' +
        '</div>' +
      '</details>';

    state.details = root.querySelector('.sc-recent-details');

    root.querySelectorAll('.sc-recent-open').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var url = btn.getAttribute('data-url');
        if (url) location.assign(url);
      });
    });

    root.querySelectorAll('.sc-recent-remove').forEach(function (btn) {
      btn.addEventListener('click', function (ev) {
        ev.preventDefault();
        ev.stopPropagation();
        var id = btn.getAttribute('data-id');
        if (!id) return;
        remove(tool, id);
        render(tool);
      });
    });

    var clearBtn = root.querySelector('.sc-recent-clear');
    if (clearBtn) {
      clearBtn.addEventListener('click', function () {
        if (!window.confirm('Clear recent on this device?')) return;
        clear(tool);
        render(tool);
      });
    }
  }

  function mount(tool, rootEl) {
    if (!rootEl || !storageKey(tool)) return;
    _mounted[tool] = { root: rootEl, details: null };
    render(tool);
  }

  function refresh(tool) {
    if (_mounted[tool]) render(tool);
  }

  function compactSalary(amount, currency) {
    var n = Number(amount);
    if (!isFinite(n) || n <= 0) return '';
    try {
      return new Intl.NumberFormat('en', {
        style: 'currency',
        currency: currency || 'USD',
        notation: 'compact',
        maximumFractionDigits: n >= 10000 ? 0 : 1
      }).format(n);
    } catch (e) {
      if (n >= 1000) return Math.round(n / 1000) + 'k';
      return String(Math.round(n));
    }
  }

  global.SCRecent = {
    add: add,
    remove: remove,
    clear: clear,
    list: safeRead,
    mount: mount,
    refresh: refresh,
    relativeTime: relativeTime,
    compactSalary: compactSalary,
    CAP: CAP
  };
})(typeof window !== 'undefined' ? window : this);
