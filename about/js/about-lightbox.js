(function () {
  'use strict';

  var bound = {};

  function focusQuiet(el) {
    if (!el || typeof el.focus !== 'function') return;
    try {
      el.focus({ preventScroll: true });
    } catch (err) {
      el.focus();
    }
  }

  document.querySelectorAll('[data-lightbox-open]').forEach(function (trigger) {
    var id = trigger.getAttribute('data-lightbox-open');
    var lightbox = document.getElementById(id);
    if (!lightbox) return;

    if (!bound[id]) {
      bound[id] = { lastTrigger: null, scrollX: 0, scrollY: 0 };

      function close() {
        var opener = bound[id].lastTrigger;
        var x = bound[id].scrollX;
        var y = bound[id].scrollY;

        if (opener) focusQuiet(opener);
        else if (document.activeElement && lightbox.contains(document.activeElement)) {
          document.activeElement.blur();
        }

        lightbox.hidden = true;
        document.body.style.overflow = '';
        clearOverlays(lightbox);
        document.removeEventListener('keydown', onKeydown);
        window.scrollTo(x, y);
      }

      function onKeydown(e) {
        if (e.key === 'Escape') close();
      }

      bound[id].onKeydown = onKeydown;

      lightbox.querySelectorAll('[data-lightbox-close]').forEach(function (el) {
        el.addEventListener('click', close);
      });
      var panel = lightbox.querySelector('[class*="__panel"]');
      if (panel) {
        panel.addEventListener('click', function (e) {
          e.stopPropagation();
        });
      }
    }

    trigger.addEventListener('click', function () {
      var img = lightbox.querySelector('.storytelling-lightbox__image');
      var src = trigger.getAttribute('data-lightbox-src');
      var alt = trigger.getAttribute('data-lightbox-alt');
      if (img && src) img.src = src;
      if (img && alt !== null) img.alt = alt || '';
      if (img) {
        img.classList.toggle('is-screen', trigger.hasAttribute('data-lightbox-screen'));
      }
      syncOverlays(trigger, lightbox);
      bound[id].lastTrigger = trigger;
      bound[id].scrollX = window.scrollX;
      bound[id].scrollY = window.scrollY;
      lightbox.hidden = false;
      document.body.style.overflow = 'hidden';
      focusQuiet(lightbox.querySelector('.storytelling-lightbox__close'));
      document.addEventListener('keydown', bound[id].onKeydown);
    });
  });

  function clearOverlays(lightbox) {
    var holder = lightbox.querySelector('.storytelling-lightbox__overlays');
    var stage = lightbox.querySelector('.storytelling-lightbox__stage');
    if (holder) holder.replaceChildren();
    if (stage) stage.classList.remove('storytelling-lightbox__stage--cta');
  }

  function syncOverlays(trigger, lightbox) {
    clearOverlays(lightbox);
    var band = trigger.closest('.about-cta-band');
    var stage = lightbox.querySelector('.storytelling-lightbox__stage');
    var holder = lightbox.querySelector('.storytelling-lightbox__overlays');
    if (!band || !stage || !holder) return;
    var heading = band.querySelector('.about-cta-band__heading');
    if (!heading) return;
    stage.classList.add('storytelling-lightbox__stage--cta');
    holder.appendChild(heading.cloneNode(true));
  }
})();
