(function () {
  'use strict';

  document.querySelectorAll('.ed-smart-img[data-asset]').forEach(function (img) {
    var assetSrc = img.getAttribute('data-asset');
    if (!assetSrc) return;
    var probe = new Image();
    probe.onload = function () { img.src = assetSrc; };
    probe.src = assetSrc;
  });

  document.querySelectorAll('[data-lightbox-src]').forEach(function (trigger) {
    trigger.addEventListener('click', function () {
      var lightbox = document.getElementById(trigger.getAttribute('data-lightbox-open'));
      if (!lightbox) return;
      var img = lightbox.querySelector('.ed-lightbox__image');
      if (!img) return;
      img.src = trigger.getAttribute('data-lightbox-src');
      img.alt = trigger.getAttribute('data-lightbox-alt') || '';
      var pair = lightbox.querySelector('.ed-lightbox__image--pair');
      var src2 = trigger.getAttribute('data-lightbox-src2');
      if (pair) {
        if (src2) {
          pair.hidden = false;
          pair.src = src2;
          pair.alt = trigger.getAttribute('data-lightbox-alt2') || '';
          lightbox.classList.add('is-spread');
        } else {
          pair.hidden = true;
          pair.removeAttribute('src');
          lightbox.classList.remove('is-spread');
        }
      }
    });
  });
})();
