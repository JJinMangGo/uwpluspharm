/* UWPLUSPHARM main.js — Swiper 11 (CDN: jsdelivr swiper@11) */
(function () {
  'use strict';
  if (typeof Swiper === 'undefined') return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var pad = function (n) { return ('0' + n).slice(-2); };

  /* ---------- Hero: fade + loop + autoplay 5s ---------- */
  var heroEl = document.querySelector('.hero');
  if (heroEl) {
    var DELAY = 5000;
    var cur = heroEl.querySelector('.hero__cur');
    var bar = heroEl.querySelector('.hero__bar i');
    var btnPause = heroEl.querySelector('.hero__pause');
    heroEl.style.setProperty('--hero-delay', DELAY / 1000 + 's');
    var runBar = function () {
      bar.classList.remove('is-run'); void bar.offsetWidth;
      if (!heroEl.classList.contains('is-paused')) bar.classList.add('is-run');
    };
    var hero = new Swiper(heroEl, {
      effect: 'fade',
      fadeEffect: { crossFade: true },
      speed: 800,
      loop: true,
      autoplay: reduce ? false : { delay: DELAY, disableOnInteraction: false },
      on: {
        slideChange: function (sw) { cur.textContent = pad(sw.realIndex + 1); runBar(); }
      }
    });
    if (reduce) heroEl.classList.add('is-paused');
    runBar();
    btnPause.addEventListener('click', function () {
      var paused = !heroEl.classList.contains('is-paused');
      heroEl.classList.toggle('is-paused', paused);
      btnPause.setAttribute('aria-label', paused ? '자동 넘김 재생' : '자동 넘김 정지');
      if (paused) hero.autoplay.stop(); else { hero.autoplay.start(); runBar(); }
    });
  }

  /* ---------- 사업분야: 제품군 탭마다 Swiper 하나, loop ---------- */
  var biz = document.querySelector('[data-biz]');
  if (biz) {
    var tabs = biz.querySelectorAll('.m-biz__tab');
    var countCur = biz.querySelector('.m-biz__count b');
    var countAll = biz.querySelector('.m-biz__count span');
    var swipers = {};
    var active = null;

    var updateCount = function (sw) {
      var total = sw.el.getAttribute('data-total') * 1;
      countCur.textContent = pad(sw.realIndex % total + 1);
      countAll.textContent = pad(total);
    };
    var make = function (el) {
      var wrap = el.querySelector('.swiper-wrapper');
      var orig = [].slice.call(wrap.children);
      el.setAttribute('data-total', orig.length);
      /* 슬라이드가 적으면 loop + 오른쪽 미리보기가 비지 않도록 복제 */
      var copies = Math.ceil(6 / orig.length) - 1;
      for (var c = 0; c < copies; c++) {
        orig.forEach(function (s) {
          var cl = s.cloneNode(true);
          cl.setAttribute('aria-hidden', 'true');
          wrap.appendChild(cl);
        });
      }
      /* 옆에 보이는 슬라이드 클릭은 링크 이동 대신 그 슬라이드로 넘김 */
      el.addEventListener('click', function (e) {
        var sl = e.target.closest('.swiper-slide');
        if (sl && !sl.classList.contains('swiper-slide-active')) e.preventDefault();
      }, true);
      return new Swiper(el, {
        slidesPerView: 'auto',
        grabCursor: true,
        spaceBetween: 40,
        speed: 600,
        loop: true,
        slideToClickedSlide: true,
        breakpoints: { 0: { spaceBetween: 16 }, 769: { spaceBetween: 24 }, 1101: { spaceBetween: 40 } },
        on: { slideChange: updateCount, init: updateCount }
      });
    };
    var setGroup = function (g) {
      tabs.forEach(function (t) {
        var on = t.getAttribute('data-group') === g;
        t.classList.toggle('is-active', on);
        t.setAttribute('aria-selected', on);
      });
      biz.querySelectorAll('.m-biz__swiper').forEach(function (el) {
        el.hidden = el.getAttribute('data-group') !== g;
      });
      if (!swipers[g]) swipers[g] = make(biz.querySelector('.m-biz__swiper[data-group="' + g + '"]'));
      active = swipers[g];
      active.update();
      active.slideToLoop(0, 0);
      updateCount(active);
    };
    tabs.forEach(function (t) { t.addEventListener('click', function () { setGroup(t.getAttribute('data-group')); }); });
    biz.querySelector('[data-dir="-1"]').addEventListener('click', function () { active && active.slidePrev(); });
    biz.querySelector('[data-dir="1"]').addEventListener('click', function () { active && active.slideNext(); });
    setGroup('liquid');
  }
})();
