(function () {
  'use strict';

  document.querySelectorAll('.ed-smart-img[data-asset]').forEach(function (img) {
    var assetSrc = img.getAttribute('data-asset');
    if (!assetSrc) return;
    var probe = new Image();
    probe.onload = function () { img.src = assetSrc; };
    probe.src = assetSrc;
  });

  function clearPair(pair, lightbox) {
    if (!pair) return;
    pair.hidden = true;
    pair.removeAttribute('src');
    pair.alt = '';
    lightbox.classList.remove('is-spread');
  }

  document.querySelectorAll('[data-lightbox-src]').forEach(function (trigger) {
    trigger.addEventListener('click', function () {
      var lightbox = document.getElementById(trigger.getAttribute('data-lightbox-open'));
      if (!lightbox) return;

      var img = lightbox.querySelector('.ed-lightbox__image:not(.ed-lightbox__image--pair)');
      if (!img) return;

      var panel = lightbox.querySelector('.ed-lightbox__panel');
      if (panel && !panel.dataset.lightboxLabel) {
        panel.dataset.lightboxLabel = panel.getAttribute('aria-label') || 'Illustration, full size';
      }
      var fallbackLabel = (panel && panel.dataset.lightboxLabel) || 'Illustration, full size';
      var alt = trigger.getAttribute('data-lightbox-alt') || '';

      img.src = trigger.getAttribute('data-lightbox-src');
      // Keep alt empty in the dialog so a stale/broken pair never paints a wrong caption.
      // Description lives on the dialog label instead.
      img.alt = '';

      var pair = lightbox.querySelector('.ed-lightbox__image--pair');
      var src2 = trigger.getAttribute('data-lightbox-src2');
      if (src2 && pair) {
        pair.hidden = false;
        pair.src = src2;
        pair.alt = '';
        lightbox.classList.add('is-spread');
        if (panel) {
          var alt2 = trigger.getAttribute('data-lightbox-alt2');
          panel.setAttribute('aria-label', alt2 ? alt + '. ' + alt2 : (alt || fallbackLabel));
        }
      } else {
        clearPair(pair, lightbox);
        if (panel) panel.setAttribute('aria-label', alt || fallbackLabel);
      }
    });
  });
})();
