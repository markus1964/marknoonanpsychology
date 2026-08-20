// Theme toggle, sticky header hairline, mobile contact bar. That is the whole of the JS.
(function () {
  var root = document.documentElement;

  document.querySelector('.theme-toggle').addEventListener('click', function () {
    var dark = root.dataset.theme
      ? root.dataset.theme === 'dark'
      : matchMedia('(prefers-color-scheme: dark)').matches;
    var next = dark ? 'light' : 'dark';
    root.dataset.theme = next;
    try { localStorage.setItem('theme', next); } catch (e) {}
  });

  var header = document.querySelector('.site-header');
  var bar = document.querySelector('.mobile-bar');
  var hero = document.querySelector('.hero');

  function onScroll() {
    header.classList.toggle('scrolled', window.scrollY > 8);
    bar.hidden = window.scrollY < hero.offsetHeight * 0.6;
  }
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Modality terms: one open at a time, closed on load so the prose reads clean.
  document.querySelectorAll('.term').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var panel = document.getElementById(btn.getAttribute('aria-controls'));
      var open = btn.getAttribute('aria-expanded') === 'true';
      document.querySelectorAll('.term').forEach(function (other) {
        other.setAttribute('aria-expanded', 'false');
        document.getElementById(other.getAttribute('aria-controls')).hidden = true;
      });
      btn.setAttribute('aria-expanded', String(!open));
      panel.hidden = open;
    });
  });

  document.getElementById('year').textContent = new Date().getFullYear();
})();
