/* =========================================================================
   Adelaide Confident Driving Academy — site behaviour
   Vanilla, no dependencies, deferred. Everything degrades gracefully.
   ========================================================================= */
(function () {
  'use strict';

  /* --- Config: the single source of truth for the WhatsApp destination --- */
  var WA_NUMBER = '61423457296';          // international format, no +, no spaces
  var TEL_NUMBER = '+61423457296';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* =======================================================================
     1. Preloader
     ===================================================================== */
  (function preloader() {
    var el = $('#preloader');
    if (!el) return;
    var hide = function () { el.classList.add('is-done'); setTimeout(function () { el.remove(); }, 1000); };
    if (reduceMotion) { el.remove(); return; }
    if (document.readyState === 'complete') setTimeout(hide, 420);
    else window.addEventListener('load', function () { setTimeout(hide, 420); });
    // Never let a stalled asset trap the visitor behind the overlay.
    setTimeout(hide, 2600);
  })();

  /* =======================================================================
     2. Navigation
     ===================================================================== */
  (function nav() {
    var toggle = $('.nav-toggle');
    var links  = $('#nav-links');
    var header = $('.site-header');

    if (toggle && links) {
      toggle.addEventListener('click', function () {
        var open = toggle.getAttribute('aria-expanded') === 'true';
        toggle.setAttribute('aria-expanded', String(!open));
        links.classList.toggle('is-open', !open);
        document.body.style.overflow = !open ? 'hidden' : '';
      });
      links.addEventListener('click', function (e) {
        if (e.target.closest('a')) {
          toggle.setAttribute('aria-expanded', 'false');
          links.classList.remove('is-open');
          document.body.style.overflow = '';
        }
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && links.classList.contains('is-open')) toggle.click();
      });
    }

    if (header) {
      var onScroll = function () { header.classList.toggle('is-stuck', window.scrollY > 12); };
      onScroll();
      window.addEventListener('scroll', onScroll, { passive: true });
    }
  })();

  /* =======================================================================
     3. Scroll reveal + counters
     ===================================================================== */
  (function reveal() {
    var items = $$('.reveal');
    if (!items.length) return;
    if (reduceMotion || !('IntersectionObserver' in window)) {
      items.forEach(function (n) { n.classList.add('is-in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var delay = parseInt(el.getAttribute('data-delay') || '0', 10);
        setTimeout(function () { el.classList.add('is-in'); }, delay);
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (n) { io.observe(n); });
  })();

  (function counters() {
    var nums = $$('[data-count]');
    if (!nums.length) return;
    if (reduceMotion || !('IntersectionObserver' in window)) {
      nums.forEach(function (n) { n.textContent = n.getAttribute('data-count') + (n.getAttribute('data-suffix') || ''); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var target = parseFloat(el.getAttribute('data-count'));
        var suffix = el.getAttribute('data-suffix') || '';
        var dec = (el.getAttribute('data-count').split('.')[1] || '').length;
        var start = null, dur = 1100;
        var tick = function (ts) {
          if (!start) start = ts;
          var p = Math.min((ts - start) / dur, 1);
          var eased = 1 - Math.pow(1 - p, 3);
          el.textContent = (target * eased).toFixed(dec) + suffix;
          if (p < 1) requestAnimationFrame(tick);
          else el.textContent = target.toFixed(dec) + suffix;
        };
        requestAnimationFrame(tick);
        io.unobserve(el);
      });
    }, { threshold: 0.4 });
    nums.forEach(function (n) { io.observe(n); });
  })();

  /* =======================================================================
     4. Review filter
     ===================================================================== */
  (function reviewFilter() {
    var bar = $('#review-filter');
    if (!bar) return;
    var cards = $$('#review-grid .review');
    var live = $('#review-count');

    bar.addEventListener('click', function (e) {
      var btn = e.target.closest('.filter-btn');
      if (!btn) return;
      var tag = btn.getAttribute('data-filter');
      $$('.filter-btn', bar).forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
      var shown = 0;
      cards.forEach(function (card) {
        var tags = (card.getAttribute('data-tags') || '').split('|');
        var match = tag === 'all' || tags.indexOf(tag) !== -1;
        card.hidden = !match;
        if (match) shown++;
      });
      if (live) live.textContent = 'Showing ' + shown + ' of ' + cards.length + ' reviews.';
    });
  })();

  /* =======================================================================
     5. WhatsApp booking funnel
     ===================================================================== */
  (function booking() {
    var form = $('#booking-form');
    if (!form) return;

    var steps    = $$('.step', form);
    var bar      = $('#booking-progress');
    var counter  = $('#booking-step-count');
    var backBtn  = $('#booking-back');
    var nextBtn  = $('#booking-next');
    var errorBox = $('#booking-error');
    var summary  = $('#booking-summary');
    var index    = 0;

    var LABELS = { route: 'Training path', gearbox: 'Transmission', suburb: 'Suburb', timing: 'Preferred timing' };

    function value(name) {
      var checked = form.querySelector('input[name="' + name + '"]:checked');
      if (checked) return checked.value;
      var text = form.querySelector('[name="' + name + '"]');
      return text ? text.value.trim() : '';
    }

    function render() {
      steps.forEach(function (s, i) { s.classList.toggle('is-active', i === index); });
      if (bar) bar.style.width = ((index + 1) / steps.length * 100) + '%';
      if (counter) counter.textContent = 'Step ' + (index + 1) + ' of ' + steps.length;
      if (backBtn) backBtn.hidden = index === 0;
      if (nextBtn) nextBtn.innerHTML = index === steps.length - 1
        ? waIcon() + ' Send on WhatsApp'
        : 'Continue';
      if (nextBtn) nextBtn.className = index === steps.length - 1 ? 'btn btn--whatsapp' : 'btn btn--primary';
      if (errorBox) errorBox.hidden = true;
      if (summary) summary.hidden = index !== steps.length - 1;
      if (index === steps.length - 1) buildSummary();
      var focusTarget = steps[index].querySelector('input, button');
      if (focusTarget && index > 0) focusTarget.focus({ preventScroll: true });
    }

    function waIcon() {
      return '<svg aria-hidden="true" width="19" height="19" viewBox="0 0 24 24" fill="currentColor">' +
        '<path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.87 9.87 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2Zm5.8 14.17c-.24.68-1.4 1.3-1.95 1.35-.5.05-1.13.07-1.83-.11-.42-.11-.96-.29-1.65-.59-2.9-1.25-4.8-4.17-4.94-4.36-.15-.19-1.19-1.58-1.19-3.02s.76-2.14 1.03-2.44c.27-.29.58-.37.78-.37h.56c.18 0 .42-.07.66.5.24.59.83 2.03.9 2.18.07.15.12.32.02.51-.09.19-.14.31-.28.48-.14.17-.29.37-.42.5-.14.14-.28.29-.12.57.16.29.71 1.17 1.53 1.9 1.05.94 1.94 1.23 2.22 1.37.27.14.43.12.59-.07.16-.19.68-.79.86-1.07.18-.27.36-.22.61-.13.24.09 1.55.73 1.82.86.27.14.44.2.5.32.07.11.07.65-.17 1.33Z"/></svg>';
    }

    function buildSummary() {
      if (!summary) return;
      var dl = $('dl', summary);
      if (!dl) return;
      dl.innerHTML = '';
      ['route', 'gearbox', 'suburb', 'timing'].forEach(function (k) {
        var v = value(k);
        if (!v) return;
        var dt = document.createElement('dt'); dt.textContent = LABELS[k];
        var dd = document.createElement('dd'); dd.textContent = v;
        dl.appendChild(dt); dl.appendChild(dd);
      });
    }

    function validate() {
      var step = steps[index];
      var required = step.getAttribute('data-require');
      if (!required) return true;
      if (value(required)) return true;
      if (errorBox) {
        errorBox.textContent = step.getAttribute('data-error') || 'Please choose an option to continue.';
        errorBox.hidden = false;
      }
      return false;
    }

    /* Builds the pre-filled WhatsApp message. Asterisks are WhatsApp bold. */
    function buildLink() {
      var lines = [
        "Hi Gopi, I'm booking through the Adelaide Confident Driving Academy website.",
        '',
        '*Training path:* ' + (value('route') || 'Not specified'),
        '*Transmission:* ' + (value('gearbox') || 'Not specified'),
        '*Suburb:* ' + (value('suburb') || 'Not specified'),
        '*Preferred timing:* ' + (value('timing') || 'Not specified'),
        '',
        'Could you let me know your next available slots?'
      ];
      return 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(lines.join('\n'));
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!validate()) return;
      if (index < steps.length - 1) { index++; render(); return; }
      var url = buildLink();
      var out = $('#booking-result');
      if (out) {
        out.innerHTML = 'If WhatsApp did not open, <a href="' + url + '" rel="noopener">tap here to send your enquiry</a> ' +
          'or call <a href="tel:' + TEL_NUMBER + '">0423 457 296</a>.';
        out.hidden = false;
      }
      window.open(url, '_blank', 'noopener');
    });

    if (backBtn) backBtn.addEventListener('click', function () { if (index > 0) { index--; render(); } });

    // Choosing an option auto-advances on the single-choice steps.
    form.addEventListener('change', function (e) {
      if (errorBox) errorBox.hidden = true;
      // Keep the confirmation summary in step with the current answers.
      if (index === steps.length - 1) buildSummary();
      if (e.target.type !== 'radio') return;
      var step = steps[index];
      if (!step || !step.getAttribute('data-autoadvance')) return;
      if (index < steps.length - 1) setTimeout(function () { index++; render(); }, 190);
    });

    form.addEventListener('input', function () {
      if (errorBox) errorBox.hidden = true;
      if (index === steps.length - 1) buildSummary();
    });

    // Suburb quick-pick chips
    $$('.suburb-hints button', form).forEach(function (b) {
      b.addEventListener('click', function () {
        var input = form.querySelector('[name="suburb"]');
        if (input) { input.value = b.textContent.trim(); input.focus(); }
      });
    });

    render();
  })();

  /* =======================================================================
     6. Plain WhatsApp links elsewhere on the page
     ===================================================================== */
  (function genericWa() {
    $$('[data-wa]').forEach(function (a) {
      var msg = a.getAttribute('data-wa');
      a.setAttribute('href', 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(msg));
    });
  })();

  /* =======================================================================
     7. Current year in the footer
     ===================================================================== */
  $$('[data-year]').forEach(function (n) { n.textContent = String(new Date().getFullYear()); });
})();
