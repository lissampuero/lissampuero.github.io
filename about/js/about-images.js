(function () {
  'use strict';

  document.querySelectorAll('[data-asset]').forEach(function (img) {
    var asset = img.getAttribute('data-asset');
    if (!asset) return;

    var probe = new Image();
    probe.onload = function () {
      img.src = asset;
    };
    probe.src = asset;
  });
})();
