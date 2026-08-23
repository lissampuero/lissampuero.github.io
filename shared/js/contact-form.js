/**
 * Formspree AJAX submit — keeps users on-page with accessible feedback.
 */
(function () {
  'use strict';

  document.querySelectorAll('.hm-contact-form[data-formspree]').forEach(function (form) {
    var status = form.querySelector('[data-form-status]');
    var submitBtn = form.querySelector('[type="submit"]');
    var defaultLabel = submitBtn ? submitBtn.textContent : '';

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!submitBtn) return;

      submitBtn.disabled = true;
      if (status) {
        status.hidden = false;
        status.className = 'hm-form-status hm-form-status--loading';
        status.textContent = form.getAttribute('data-msg-sending') || 'Sending…';
      }

      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' }
      })
        .then(function (res) {
          if (!res.ok) throw new Error('submit failed');
          if (status) {
            status.className = 'hm-form-status hm-form-status--success';
            status.textContent = form.getAttribute('data-msg-success') ||
              'Thank you — your message is on its way. I\'ll reply soon.';
          }
          form.reset();
        })
        .catch(function () {
          if (status) {
            status.className = 'hm-form-status hm-form-status--error';
            status.textContent = form.getAttribute('data-msg-error') ||
              'Something went wrong. Please email lissampuero@outlook.com directly.';
          }
        })
        .finally(function () {
          submitBtn.disabled = false;
          submitBtn.textContent = defaultLabel;
        });
    });
  });
})();
