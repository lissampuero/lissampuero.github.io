(function () {
  'use strict';

  var lightbox = document.getElementById('stn-lightbox');
  var stage = lightbox ? lightbox.querySelector('.stn-lightbox__image') : null;

  document.querySelectorAll('[data-lightbox-src]').forEach(function (trigger) {
    trigger.addEventListener('click', function () {
      if (!lightbox || !stage) return;
      stage.src = trigger.getAttribute('data-lightbox-src');
      stage.alt = trigger.getAttribute('data-lightbox-alt') || '';
      lightbox.classList.remove('is-zoomed');
    }, true);
  });

  document.querySelectorAll('.stn-fan__issue').forEach(function (issue) {
    issue.addEventListener('click', function (e) {
      if (e.target.closest('[data-lightbox-open]')) return;
      var inner = issue.querySelector('[data-lightbox-open]');
      if (inner) inner.click();
    });
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
