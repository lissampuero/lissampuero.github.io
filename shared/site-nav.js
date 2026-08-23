(function () {
  'use strict';

  var menuBtn = document.querySelector('.site-header__menu-btn');
  var nav = document.getElementById('site-nav');

  if (!menuBtn || !nav) return;

  function closeNav() {
    nav.classList.remove('is-open');
    menuBtn.setAttribute('aria-expanded', 'false');
  }

  function openNav() {
    nav.classList.add('is-open');
    menuBtn.setAttribute('aria-expanded', 'true');
    var firstLink = nav.querySelector('.site-header__links a, .site-header__cta');
    if (firstLink) firstLink.focus();
  }

  menuBtn.addEventListener('click', function () {
    if (nav.classList.contains('is-open')) {
      closeNav();
      menuBtn.focus();
    } else {
      openNav();
    }
  });

  document.addEventListener('click', function (e) {
    if (!e.target.closest('.site-header') && nav.classList.contains('is-open')) {
      closeNav();
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav.classList.contains('is-open')) {
      closeNav();
      menuBtn.focus();
    }
  });

  nav.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', function () {
      if (nav.classList.contains('is-open')) closeNav();
    });
  });
})();
