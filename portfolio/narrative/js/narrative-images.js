/**
 * Smart image loader — swaps to final WebP when available.
 * LoLo manuscript: seven-spread internal book.
 */
(function () {
  'use strict';

  document.querySelectorAll('.nar-smart-img[data-asset]').forEach(function (img) {
    var assetSrc = img.getAttribute('data-asset');
    if (!assetSrc) return;

    var probe = new Image();
    probe.onload = function () {
      img.src = assetSrc;
    };
    probe.src = assetSrc;
  });

  document.querySelectorAll('[data-lightbox-src]').forEach(function (trigger) {
    trigger.addEventListener('click', function () {
      var lightbox = document.getElementById(trigger.getAttribute('data-lightbox-open'));
      if (!lightbox) return;
      var img = lightbox.querySelector('.nar-lightbox__image');
      if (!img) return;
      img.src = trigger.getAttribute('data-lightbox-src');
      img.alt = trigger.getAttribute('data-lightbox-alt') || '';
      syncLightboxOverlays(trigger, lightbox);
    });
  });

  function clearLightboxOverlays(lightbox) {
    var holder = lightbox.querySelector('.nar-lightbox__overlays');
    var stage = lightbox.querySelector('.nar-lightbox__stage');
    if (holder) holder.replaceChildren();
    if (!stage) return;
    stage.className = 'nar-lightbox__stage';
    stage.style.width = '';
    stage.style.containerType = '';
  }

  function lockLightboxStage(img, stage) {
    function apply() {
      var width = img.getBoundingClientRect().width;
      if (!width) return;
      stage.style.width = Math.round(width) + 'px';
      stage.style.containerType = 'inline-size';
    }
    apply();
    if (!img.complete) img.addEventListener('load', apply, { once: true });
    else img.addEventListener('load', apply, { once: true });
  }

  function syncLightboxOverlays(trigger, lightbox) {
    clearLightboxOverlays(lightbox);
    var plate = trigger.closest('.nar-plate') || trigger.closest('.lolo-plate');
    var stage = lightbox.querySelector('.nar-lightbox__stage');
    var holder = lightbox.querySelector('.nar-lightbox__overlays');
    var img = lightbox.querySelector('.nar-lightbox__image');
    if (!img || !stage) return;

    if (!plate || !holder) {
      lockLightboxStage(img, stage);
      return;
    }

    var plateImg = plate.querySelector('.nar-plate__img') || plate.querySelector('.lolo-stage img');
    if (plateImg) {
      if (plateImg.getAttribute('width')) img.setAttribute('width', plateImg.getAttribute('width'));
      if (plateImg.getAttribute('height')) img.setAttribute('height', plateImg.getAttribute('height'));
    }

    plate.classList.forEach(function (name) {
      if (name.indexOf('nar-plate--') === 0) stage.classList.add(name);
      if (name.indexOf('lolo-plate--') === 0 && name !== 'lolo-plate--overlay') {
        stage.classList.add(name);
      }
    });

    if (stage.classList.contains('lolo-plate--highlights') || stage.classList.contains('lolo-plate--sheet')) {
      stage.style.width = '';
      stage.style.containerType = 'inline-size';
    } else {
      lockLightboxStage(img, stage);
    }

    plate.querySelectorAll('.nar-plate__text, .lolo-float, .lolo-glints').forEach(function (node) {
      holder.appendChild(node.cloneNode(true));
    });
  }

  var sharedLightbox = document.getElementById('nar-lightbox');
  if (sharedLightbox) {
    sharedLightbox.querySelectorAll('[data-lightbox-close]').forEach(function (el) {
      el.addEventListener('click', function () {
        clearLightboxOverlays(sharedLightbox);
      });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') clearLightboxOverlays(sharedLightbox);
    });
  }

  document.querySelectorAll('[data-lolo-book]').forEach(function (book) {
    var thumbs = Array.prototype.slice.call(book.querySelectorAll('.lolo-book__thumb'));
    var pageBtn = book.querySelector('.lolo-book__page');
    var img = book.querySelector('.lolo-book__img');
    var folio = book.querySelector('[data-lolo-folio]');
    var caption = book.querySelector('[data-lolo-caption]');
    var prev = book.querySelector('[data-lolo-prev]');
    var next = book.querySelector('[data-lolo-next]');
    var lightbox = document.getElementById('nar-lightbox');
    var total = thumbs.length;
    var index = 0;

    if (!thumbs.length || !pageBtn || !img) return;

    function pad(n) {
      return n < 10 ? '0' + n : String(n);
    }

    function preload(i) {
      if (i < 0 || i >= total) return;
      var src = thumbs[i].getAttribute('data-src');
      if (!src) return;
      var probe = new Image();
      probe.src = src;
    }

    function show(i) {
      if (i < 0) i = 0;
      if (i > total - 1) i = total - 1;
      index = i;
      var thumb = thumbs[index];
      var src = thumb.getAttribute('data-src');
      var src2x = thumb.getAttribute('data-src2x') || src;
      var alt = thumb.getAttribute('data-alt') || '';

      img.src = src;
      img.srcset = src + ' 1100w, ' + src2x + ' 1600w';
      img.sizes = '(min-width: 80rem) 80rem, 92vw';
      img.alt = alt;
      img.setAttribute('width', thumb.getAttribute('data-width') || '1800');
      img.setAttribute('height', thumb.getAttribute('data-height') || '1349');

      pageBtn.setAttribute('data-lightbox-src', src2x);
      pageBtn.setAttribute('data-lightbox-alt', alt);

      if (folio) folio.textContent = pad(index + 1);
      if (caption) caption.textContent = thumb.getAttribute('data-caption') || '';

      thumbs.forEach(function (t, n) {
        if (n === index) t.setAttribute('aria-current', 'true');
        else t.removeAttribute('aria-current');
      });

      if (prev) prev.disabled = index === 0;
      if (next) next.disabled = index === total - 1;

      preload(index + 1);
      preload(index - 1);
    }

    thumbs.forEach(function (thumb, i) {
      thumb.addEventListener('click', function () {
        show(i);
      });
    });

    if (prev) prev.addEventListener('click', function () { show(index - 1); });
    if (next) next.addEventListener('click', function () { show(index + 1); });

    document.addEventListener('keydown', function (e) {
      if (lightbox && !lightbox.hidden) return;
      if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
      var rect = book.getBoundingClientRect();
      var inView = rect.top < window.innerHeight * 0.78 && rect.bottom > window.innerHeight * 0.22;
      if (!inView && !book.contains(document.activeElement)) return;
      e.preventDefault();
      show(e.key === 'ArrowRight' ? index + 1 : index - 1);
    });

    show(0);
  });
})();
