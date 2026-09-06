(function () {
  'use strict';

  var popup = document.getElementById('svc-deliverables-popup');
  if (!popup) return;

  var titleEl = popup.querySelector('.svc-deliverables-popup__title');
  var textEl = popup.querySelector('.svc-deliverables-popup__text');
  var closeBtn = popup.querySelector('.svc-deliverables-popup__close');
  var lastTrigger = null;
  var scrollX = 0;
  var scrollY = 0;

  function focusQuiet(el) {
    if (!el || typeof el.focus !== 'function') return;
    try {
      el.focus({ preventScroll: true });
    } catch (err) {
      el.focus();
    }
  }

  function close() {
    if (lastTrigger) {
      lastTrigger.setAttribute('aria-expanded', 'false');
      focusQuiet(lastTrigger);
    } else if (document.activeElement && popup.contains(document.activeElement)) {
      document.activeElement.blur();
    }

    popup.hidden = true;
    document.body.style.overflow = '';
    document.removeEventListener('keydown', onKeydown);
    window.scrollTo(scrollX, scrollY);
    lastTrigger = null;
  }

  function onKeydown(e) {
    if (e.key === 'Escape') close();
  }

  function open(trigger) {
    var title = trigger.querySelector('.svc-category__title');
    var deliverables = trigger.querySelector('.svc-category__deliverables');
    if (!title || !deliverables) return;

    lastTrigger = trigger;
    scrollX = window.scrollX;
    scrollY = window.scrollY;

    titleEl.textContent = title.textContent;
    textEl.textContent = deliverables.textContent;

    trigger.setAttribute('aria-expanded', 'true');
    popup.hidden = false;
    document.body.style.overflow = 'hidden';
    focusQuiet(closeBtn);
    document.addEventListener('keydown', onKeydown);
  }

  popup.querySelectorAll('[data-deliverables-close]').forEach(function (el) {
    el.addEventListener('click', close);
  });

  var panel = popup.querySelector('.svc-deliverables-popup__panel');
  if (panel) {
    panel.addEventListener('click', function (e) {
      e.stopPropagation();
    });
  }

  document.querySelectorAll('[data-deliverables-trigger]').forEach(function (trigger) {
    trigger.addEventListener('click', function () {
      open(trigger);
    });
  });
})();
