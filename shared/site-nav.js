(function () {
  'use strict';

  var menuBtn = document.querySelector('.site-header__menu-btn');
  var nav = document.getElementById('site-nav');

  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    document.addEventListener('click', function (e) {
      if (!e.target.closest('.site-header') && nav.classList.contains('is-open')) {
        nav.classList.remove('is-open');
        menuBtn.setAttribute('aria-expanded', 'false');
      }
    });
  }
})();
