/**
 * Services CTA contact menus — keyboard accessible, ARIA synced.
 */
(function () {
  'use strict';

  var wraps = document.querySelectorAll('.svc-cta-button-wrap');

  function closeAll() {
    document.querySelectorAll('.svc-contact-menu').forEach(function (menu) {
      menu.classList.remove('is-open');
      var btnId = menu.id.replace('menu-', '');
      var btn = document.querySelector('[aria-controls="' + menu.id + '"]');
      if (btn) btn.setAttribute('aria-expanded', 'false');
    });
  }

  wraps.forEach(function (wrap) {
    var btn = wrap.querySelector('.svc-cta-btn');
    var menu = wrap.querySelector('.svc-contact-menu');
    if (!btn || !menu) return;

    var menuId = menu.id;
    btn.setAttribute('aria-haspopup', 'true');
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-controls', menuId);

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var isOpen = menu.classList.contains('is-open');
      closeAll();
      if (!isOpen) {
        menu.classList.add('is-open');
        btn.setAttribute('aria-expanded', 'true');
        var first = menu.querySelector('.svc-contact-option');
        if (first) first.focus();
      }
    });
  });

  document.addEventListener('click', function (e) {
    if (!e.target.closest('.svc-cta-button-wrap')) closeAll();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeAll();
  });
})();
