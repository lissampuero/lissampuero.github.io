(function () {
  'use strict';

  document.querySelectorAll('.hm-smart-img[data-asset]').forEach(function (img) {
    var src = img.getAttribute('data-asset');
    if (!src) return;
    var probe = new Image();
    probe.onload = function () { img.src = src; };
    probe.src = src;
  });

  var lightbox = document.getElementById('hm-lightbox');
  var stage = lightbox ? lightbox.querySelector('.hm-lightbox__image') : null;

  document.querySelectorAll('[data-lightbox-src]').forEach(function (trigger) {
    trigger.addEventListener('click', function () {
      if (!lightbox || !stage) return;
      stage.src = trigger.getAttribute('data-lightbox-src');
      stage.alt = trigger.getAttribute('data-lightbox-alt') || '';
      lightbox.classList.remove('is-zoomed');
    }, true);
  });

  if (!lightbox || !stage) return;

  stage.addEventListener('click', function (e) {
    e.stopPropagation();
    lightbox.classList.toggle('is-zoomed');
  });

  function resetZoom() {
    lightbox.classList.remove('is-zoomed');
  }

  lightbox.querySelectorAll('[data-lightbox-close]').forEach(function (el) {
    el.addEventListener('click', resetZoom);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') resetZoom();
  });
})();
