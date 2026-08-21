/**
 * Generic lightbox trigger — works with any element carrying [data-lightbox-open="targetId"],
 * as long as the target contains [data-lightbox-close] elements and a "*__panel" wrapper.
 *
 * One close handler per lightbox (not per trigger). Closing restores the scroll
 * and focus to the image that opened the popup, instead of jumping to the
 * lightbox markup at the end of the document.
 */
(function () {
  'use strict';

  var states = {};

  function focusQuiet(el) {
    if (!el || typeof el.focus !== 'function') return;
    try {
      el.focus({ preventScroll: true });
    } catch (err) {
      el.focus();
    }
  }

  function closeLightbox(id) {
    var state = states[id];
    if (!state) return;
    var lightbox = state.el;
    var opener = state.lastTrigger;
    var x = state.scrollX;
    var y = state.scrollY;

    if (opener) focusQuiet(opener);
    else if (document.activeElement && lightbox.contains(document.activeElement)) {
      document.activeElement.blur();
    }

    lightbox.hidden = true;
    document.body.style.overflow = '';
    document.removeEventListener('keydown', state.onKeydown);
    window.scrollTo(x, y);
  }

  document.querySelectorAll('[data-lightbox-open]').forEach(function (trigger) {
    var id = trigger.getAttribute('data-lightbox-open');
    var lightbox = document.getElementById(id);
    if (!lightbox) return;

    if (!states[id]) {
      states[id] = {
        el: lightbox,
        lastTrigger: null,
        scrollX: 0,
        scrollY: 0
      };

      states[id].onKeydown = function (e) {
        if (e.key === 'Escape') closeLightbox(id);
      };

      lightbox.querySelectorAll('[data-lightbox-close]').forEach(function (el) {
        el.addEventListener('click', function () {
          closeLightbox(id);
        });
      });

      var panel = lightbox.querySelector('[class*="__panel"]');
      if (panel) {
        panel.addEventListener('click', function (e) {
          e.stopPropagation();
        });
      }
    }

    trigger.addEventListener('click', function () {
      var state = states[id];
      state.lastTrigger = trigger;
      state.scrollX = window.scrollX;
      state.scrollY = window.scrollY;
      lightbox.hidden = false;
      document.body.style.overflow = 'hidden';
      focusQuiet(lightbox.querySelector('[class*="__close"]'));
      document.addEventListener('keydown', state.onKeydown);
    });
  });
})();
