/**
 * Privacy-friendly analytics — Plausible (no cookies).
 * Create a site at plausible.io for lissampuero.com to activate.
 */
(function () {
  'use strict';
  if (document.location.hostname === 'localhost' || document.location.protocol === 'file:') return;

  var s = document.createElement('script');
  s.defer = true;
  s.dataset.domain = 'lissampuero.com';
  s.src = 'https://plausible.io/js/script.js';
  document.head.appendChild(s);
})();
