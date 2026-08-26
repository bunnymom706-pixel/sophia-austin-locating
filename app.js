/*
 * app.js — sophia-austin-locating
 * One IIFE, no globals. Every module null-checks its DOM so a partial page
 * never throws. The site works with JS disabled: all CTA links are valid
 * plain hrefs before this file runs; we only enhance them.
 */
(function () {
  'use strict';

  var PHONE = '5126761215';
  var SPARK_URL = 'https://sparkapt.com/inquiry/sophia-reddehase859';
  var EMAIL = 'Sophia.Reddehases@spiritre.com';
  var STORAGE_KEY = 'sophia-search-starter-v1';

  /* Question keys in DOM order of the fieldset.starter-q blocks. */
  var Q_KEYS = ['area', 'budget', 'beds', 'move'];

  /* Short URL-safe values for the Spark query string. Unknown labels fall
     back to a generic slug so a copy tweak by another agent can't break us. */
  var SHORT_VALUES = {
    area: {
      'Downtown & Central Austin': 'downtown-central',
      'The Domain & North Austin': 'domain-north',
      'East Austin': 'east',
      'South Austin & South Congress': 'south-soco',
      'Round Rock & Cedar Park': 'roundrock-cedarpark',
      'Bee Cave & Southwest Austin': 'beecave-sw',
      'Not sure yet': 'unsure'
    },
    budget: {
      'Under $1,300': 'under-1300',
      '$1,300–1,700': '1300-1700',
      '$1,700–2,200': '1700-2200',
      '$2,200–3,000': '2200-3000',
      '$3,000+': '3000-plus'
    },
    beds: {
      'Studio': 'studio',
      '1': '1',
      '2': '2',
      '3+': '3plus'
    },
    move: {
      'ASAP': 'asap',
      'Within 30 days': '30-days',
      '1–2 months': '1-2-months',
      '3+ months': '3-plus-months'
    }
  };

  function slugify(value) {
    return String(value)
      .toLowerCase()
      .replace(/\$/g, '')
      .replace(/,/g, '')
      .replace(/\+/g, 'plus')
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '') || 'na';
  }

  function shortValue(key, label) {
    var table = SHORT_VALUES[key];
    if (table && Object.prototype.hasOwnProperty.call(table, label)) {
      return table[label];
    }
    return slugify(label);
  }

  /* ---------------------------------------------------------------- *
   * 1. Sticky header shadow on scroll (passive listener)
   * ---------------------------------------------------------------- */
  function initHeaderShadow() {
    var header = document.querySelector('header.site-header') ||
      document.querySelector('.site-header');
    if (!header) return;

    var shadowed = false;
    function update() {
      var wantShadow = (window.pageYOffset || document.documentElement.scrollTop || 0) > 4;
      if (wantShadow === shadowed) return;
      shadowed = wantShadow;
      if (wantShadow) {
        header.classList.add('is-scrolled');
        header.style.boxShadow = '0 1px 3px rgba(0,0,0,.08)';
      } else {
        header.classList.remove('is-scrolled');
        header.style.boxShadow = '';
      }
    }
    window.addEventListener('scroll', update, { passive: true });
    update();
  }

  /* ---------------------------------------------------------------- *
   * 2. Mobile nav toggle (#nav-toggle, aria-expanded)
   * ---------------------------------------------------------------- */
  function initNavToggle() {
    var toggle = document.getElementById('nav-toggle');
    if (!toggle) return;
    var header = toggle.closest('header') || document.querySelector('.site-header');
    var nav = (header && header.querySelector('nav')) || document.querySelector('nav');

    function setOpen(open) {
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (header) header.classList.toggle('nav-open', open);
      if (nav) nav.classList.toggle('is-open', open);
    }

    if (!toggle.hasAttribute('aria-expanded')) {
      toggle.setAttribute('aria-expanded', 'false');
    }

    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });

    /* Close after choosing a nav link, and on Escape. */
    if (nav) {
      nav.addEventListener('click', function (e) {
        var link = e.target && e.target.closest ? e.target.closest('a') : null;
        if (link) setOpen(false);
      });
    }
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setOpen(false);
      }
    });
  }

  /* ---------------------------------------------------------------- *
   * 3. Search starter (4 questions) + CTA rewriting + clipboard +
   *    localStorage persistence
   * ---------------------------------------------------------------- */

  function readStored() {
    try {
      var raw = window.localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      var parsed = JSON.parse(raw);
      if (!parsed || typeof parsed !== 'object') return null;
      for (var i = 0; i < Q_KEYS.length; i++) {
        var key = Q_KEYS[i];
        if (key in parsed && typeof parsed[key] !== 'string') return null;
      }
      return parsed;
    } catch (err) {
      return null;
    }
  }

  function writeStored(answers) {
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(answers));
    } catch (err) {
      /* Storage unavailable (private mode, disabled) — feature still works. */
    }
  }

  function buildSummary(answers) {
    var bedsPart = answers.beds === 'Studio' ? 'Studio' : answers.beds + ' bed';
    var movePart = answers.move === 'ASAP'
      ? 'ASAP'
      : answers.move.charAt(0).toLowerCase() + answers.move.slice(1);
    return 'Area: ' + answers.area +
      ' · Budget: ' + answers.budget +
      ' · ' + bedsPart +
      ' · Move: ' + movePart +
      ' — sent from Sophia’s site';
  }

  function buildSparkHref(answers) {
    return SPARK_URL +
      '?ref=site' +
      '&area=' + encodeURIComponent(shortValue('area', answers.area)) +
      '&budget=' + encodeURIComponent(shortValue('budget', answers.budget)) +
      '&beds=' + encodeURIComponent(shortValue('beds', answers.beds)) +
      '&move=' + encodeURIComponent(shortValue('move', answers.move));
  }

  function buildSmsHref(summary) {
    return 'sms:' + PHONE + '?&body=' + encodeURIComponent(summary);
  }

  function buildMailtoHref(summary) {
    return 'mailto:' + EMAIL +
      '?subject=' + encodeURIComponent('Apartment search') +
      '&body=' + encodeURIComponent(summary);
  }

  function findCopyNote(results) {
    if (!results) return null;
    var note = results.querySelector('.copy-note, [data-copy-note]');
    if (note) return note;
    var candidates = results.querySelectorAll('p, span, small, div');
    for (var i = 0; i < candidates.length; i++) {
      if (/^copied\b/i.test((candidates[i].textContent || '').trim())) {
        return candidates[i];
      }
    }
    return null;
  }

  function showCopyNote(results) {
    var note = findCopyNote(results);
    if (!note) return;
    note.classList.remove('is-hidden');
    note.removeAttribute('hidden');
  }

  /* Most recently built summary, kept so the CTA click handlers (added by
     initCtaClipboard) can copy it at click time without rebuilding it. */
  var currentSummary = '';

  /* Copy with navigator.clipboard, falling back to execCommand.
     The "copied" note is shown only when a copy actually succeeded. */
  function copySummary(summary, results) {
    var copied = false;
    try {
      if (navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {
        navigator.clipboard.writeText(summary).then(function () {
          showCopyNote(results);
        }).catch(function () {
          if (copyViaExecCommand(summary)) showCopyNote(results);
        });
        return;
      }
    } catch (err) {
      /* fall through to legacy path */
    }
    try {
      copied = copyViaExecCommand(summary);
    } catch (err) {
      copied = false;
    }
    if (copied) showCopyNote(results);
  }

  function copyViaExecCommand(text) {
    var ok = false;
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.position = 'fixed';
    ta.style.top = '-1000px';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    try {
      ta.select();
      ta.setSelectionRange(0, ta.value.length);
      ok = document.execCommand('copy');
    } catch (err) {
      ok = false;
    }
    if (ta.parentNode) ta.parentNode.removeChild(ta);
    return ok;
  }

  function initSearchStarter() {
    var fieldsets = document.querySelectorAll('fieldset.starter-q');
    if (!fieldsets.length) {
      /* Still give the sticky bar / results whatever a previous visit stored. */
      applyAnswers(readStored());
      initCtaClipboard();
      return;
    }

    var answers = readStored() || {};

    Array.prototype.forEach.call(fieldsets, function (fieldset, index) {
      var key = fieldset.getAttribute('data-q') || Q_KEYS[index];
      if (!key) return;
      var options = fieldset.querySelectorAll('button.starter-opt');

      Array.prototype.forEach.call(options, function (btn) {
        /* Make sure a stray unset type never submits a form. */
        if (!btn.getAttribute('type')) btn.setAttribute('type', 'button');
        if (!btn.hasAttribute('aria-pressed')) btn.setAttribute('aria-pressed', 'false');

        var label = (btn.getAttribute('data-value') || btn.textContent || '').trim();

        /* Hydrate selection state from a previous visit. */
        if (answers[key] && answers[key] === label) {
          markSelected(fieldset, btn);
        }

        btn.addEventListener('click', function () {
          answers[key] = label;
          markSelected(fieldset, btn);
          writeStored(answers);
          if (allAnswered(answers)) {
            applyAnswers(answers);
          }
        });
      });
    });

    /* Hydration: if a previous visit finished the quiz, restore the results. */
    if (allAnswered(answers)) {
      applyAnswers(answers);
    }

    initCtaClipboard();
  }

  function markSelected(fieldset, chosen) {
    var options = fieldset.querySelectorAll('button.starter-opt');
    Array.prototype.forEach.call(options, function (btn) {
      var selected = btn === chosen;
      btn.setAttribute('aria-pressed', selected ? 'true' : 'false');
      btn.classList.toggle('is-selected', selected);
    });
  }

  function allAnswered(answers) {
    if (!answers) return false;
    for (var i = 0; i < Q_KEYS.length; i++) {
      if (!answers[Q_KEYS[i]]) return false;
    }
    return true;
  }

  /* Build the summary, reveal results, rewrite CTA hrefs, update sticky bar.
     Never copies to the clipboard here — that only happens from a CTA click
     (see initCtaClipboard), so it always has a real user gesture behind it. */
  function applyAnswers(answers) {
    if (!allAnswered(answers)) return;

    var summary = buildSummary(answers);
    currentSummary = summary;
    var results = document.getElementById('quiz-results');
    var summaryEl = document.getElementById('quiz-summary');
    var smsCta = document.getElementById('quiz-cta-sms');
    var sparkCta = document.getElementById('quiz-cta-spark');
    var emailCta = document.getElementById('quiz-cta-email');
    var stickySms = document.getElementById('sticky-sms');

    if (summaryEl) summaryEl.textContent = summary;
    if (smsCta) smsCta.setAttribute('href', buildSmsHref(summary));
    if (sparkCta) sparkCta.setAttribute('href', buildSparkHref(answers));
    if (emailCta) emailCta.setAttribute('href', buildMailtoHref(summary));
    if (stickySms) stickySms.setAttribute('href', buildSmsHref(summary));

    if (results) {
      results.classList.remove('is-hidden');
      results.removeAttribute('hidden');
    }
  }

  /* Copy the summary to the clipboard only when a visitor actively clicks
     one of the three quiz CTAs — never automatically. Navigation is left
     alone (no preventDefault): the copy just piggybacks on the click, and
     the "Copied" note (via copySummary -> showCopyNote) only appears once
     that click-triggered copy actually succeeds. */
  function initCtaClipboard() {
    var results = document.getElementById('quiz-results');
    var ctaIds = ['quiz-cta-sms', 'quiz-cta-spark', 'quiz-cta-email'];
    Array.prototype.forEach.call(ctaIds, function (id) {
      var cta = document.getElementById(id);
      if (!cta) return;
      cta.addEventListener('click', function () {
        if (currentSummary) copySummary(currentSummary, results);
      });
    });
  }

  /* ---------------------------------------------------------------- *
   * 5. Footer year
   * ---------------------------------------------------------------- */
  function initYear() {
    var yearEl = document.getElementById('year');
    if (yearEl) yearEl.textContent = String(new Date().getFullYear());
  }

  function init() {
    initHeaderShadow();
    initNavToggle();
    initSearchStarter();
    initYear();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
