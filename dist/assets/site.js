/* accessibilitenumerique.eu — interactions */
(function () {
  'use strict';
  var toggles = Array.prototype.slice.call(document.querySelectorAll('[data-toggle]'));
  function close(btn) {
    var el = document.getElementById(btn.getAttribute('aria-controls'));
    btn.setAttribute('aria-expanded', 'false');
    if (el) el.hidden = true;
  }
  function closeAll(except) {
    toggles.forEach(function (b) { if (b !== except && b.getAttribute('aria-expanded') === 'true') close(b); });
  }
  toggles.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = btn.getAttribute('aria-expanded') === 'true';
      closeAll(btn);
      var el = document.getElementById(btn.getAttribute('aria-controls'));
      btn.setAttribute('aria-expanded', open ? 'false' : 'true');
      if (el) el.hidden = open;
    });
  });
  document.addEventListener('click', function (e) {
    toggles.forEach(function (b) {
      var el = document.getElementById(b.getAttribute('aria-controls'));
      if (b.getAttribute('aria-expanded') === 'true' && el && !el.contains(e.target) && b.getAttribute('data-toggle') !== 'mob') close(b);
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    toggles.forEach(function (b) {
      if (b.getAttribute('aria-expanded') === 'true') { close(b); b.focus(); }
    });
  });

  /* Onglets (accueil) */
  Array.prototype.forEach.call(document.querySelectorAll('[role=tablist]'), function (list) {
    var tabs = Array.prototype.slice.call(list.querySelectorAll('[role=tab]'));
    function select(tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
        var p = document.getElementById(t.getAttribute('aria-controls'));
        if (p) p.hidden = !on;
      });
      if (focus) tab.focus();
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(t); });
      t.addEventListener('keydown', function (e) {
        var k = e.key, n = null;
        if (k === 'ArrowRight') n = tabs[(i + 1) % tabs.length];
        if (k === 'ArrowLeft') n = tabs[(i - 1 + tabs.length) % tabs.length];
        if (k === 'Home') n = tabs[0];
        if (k === 'End') n = tabs[tabs.length - 1];
        if (n) { e.preventDefault(); select(n, true); }
      });
    });
    select(tabs[0]);
  });

  /* Filtres (ressources) */
  Array.prototype.forEach.call(document.querySelectorAll('[data-filters]'), function (box) {
    var btns = Array.prototype.slice.call(box.querySelectorAll('button'));
    var items = Array.prototype.slice.call(document.querySelectorAll('[data-cat]'));
    var status = document.getElementById(box.getAttribute('data-status'));
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        var f = b.getAttribute('data-filter');
        btns.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        var n = 0;
        items.forEach(function (it) {
          var show = f === 'all' || it.getAttribute('data-cat') === f;
          it.hidden = !show; if (show) n++;
        });
        if (status) status.textContent = status.getAttribute('data-tpl').replace('%n', n);
      });
    });
  });

  /* Formulaire de contact */
  var form = document.querySelector('form[data-contact]');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var err = form.querySelector('.err');
      var req = Array.prototype.slice.call(form.querySelectorAll('[required]'));
      var bad = req.filter(function (f) { return f.type === 'checkbox' ? !f.checked : !f.value.trim(); });
      req.forEach(function (f) { f.setAttribute('aria-invalid', bad.indexOf(f) >= 0 ? 'true' : 'false'); });
      if (bad.length) { err.hidden = false; bad[0].focus(); return; }
      err.hidden = true;
      var data = {};
      new FormData(form).forEach(function (v, k) { data[k] = v; });
      data.site = 'accessibilitenumerique.eu'; data.page = location.href.split('#')[0]; data.langue = document.documentElement.lang.toUpperCase();
      var url = form.getAttribute('data-endpoint');
      var done = function () {
        var ok = document.getElementById('form-ok');
        form.hidden = true; ok.hidden = false; ok.focus();
      };
      if (!url) { done(); return; }
      fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { if (!r.ok) throw new Error(); done(); })
        .catch(function () { err.textContent = form.getAttribute('data-neterr'); err.hidden = false; });
    });
  }
})();
