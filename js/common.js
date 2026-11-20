/* UWPLUSPHARM common.js — vanilla, no dependency */
(function () {
  'use strict';
  var header = document.querySelector('.header');
  var dim = document.querySelector('.dim');
  var pcQuery = window.matchMedia('(min-width:1025px)');

  /* 스크롤 시 헤더 배경 */
  function onScroll() {
    if (!header) return;
    header.classList.toggle('is-scrolled', window.scrollY > 10);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* PC 풀네비: 각 컬럼을 GNB 항목 중앙에 맞춤 */
  var gnbItems = document.querySelectorAll('.gnb__item');
  var cols = document.querySelectorAll('.fullnav__col');
  function placeCols() {
    if (!header || !cols.length) return;
    var base = header.getBoundingClientRect().left;
    gnbItems.forEach(function (item, i) {
      if (!cols[i]) return;
      var r = item.getBoundingClientRect();
      cols[i].style.left = (r.left - base + r.width / 2) + 'px';
    });
  }
  window.addEventListener('resize', placeCols);
  window.addEventListener('load', placeCols);
  placeCols();

  function openNav() {
    if (!pcQuery.matches) return;
    placeCols();
    header.classList.add('is-open');
    dim && dim.classList.add('is-on');
  }
  function closeNav() {
    header.classList.remove('is-open');
    dim && dim.classList.remove('is-on');
    cols.forEach(function (c) { c.classList.remove('is-hover'); });
  }
  var gnb = document.querySelector('.gnb');
  var fullnav = document.querySelector('.fullnav');
  if (gnb && fullnav) {
    gnb.addEventListener('mouseenter', openNav);
    gnb.addEventListener('focusin', openNav);
    header.addEventListener('mouseleave', closeNav);
    fullnav.addEventListener('focusout', function (e) {
      if (!header.contains(e.relatedTarget)) closeNav();
    });
    gnbItems.forEach(function (item, i) {
      item.addEventListener('mouseenter', function () {
        cols.forEach(function (c, j) { c.classList.toggle('is-hover', i === j); });
      });
    });
    cols.forEach(function (col) {
      col.addEventListener('mouseenter', function () {
        cols.forEach(function (c) { c.classList.toggle('is-hover', c === col); });
      });
    });
  }

  /* 모바일 메뉴 */
  var btnMenu = document.querySelector('.btn-menu');
  if (btnMenu) {
    btnMenu.addEventListener('click', function () {
      var open = !document.body.classList.contains('is-mopen');
      document.body.classList.toggle('is-mopen', open);
      header.classList.toggle('is-open', open);
      dim && dim.classList.toggle('is-on', open);
      btnMenu.setAttribute('aria-expanded', open);
      document.body.style.overflow = open ? 'hidden' : '';
    });
  }
  document.querySelectorAll('.mnav__btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.parentElement;
      var open = !item.classList.contains('is-open');
      item.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', open);
    });
  });
  if (dim) {
    dim.addEventListener('click', function () {
      document.body.classList.remove('is-mopen');
      document.body.style.overflow = '';
      closeNav();
    });
  }
  pcQuery.addEventListener && pcQuery.addEventListener('change', function () {
    document.body.classList.remove('is-mopen');
    document.body.style.overflow = '';
    closeNav();
  });

  /* 스크롤 등장 */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.15 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  }
})();

/* 모달 (개인정보 전문 보기 등) */
(function () {
  var last;
  function open(id) {
    var m = document.getElementById('modal-' + id);
    if (!m) return;
    last = document.activeElement;
    m.hidden = false;
    var b = m.querySelector('[data-modal-close]'); b && b.focus();
  }
  function close(m) { m.hidden = true; last && last.focus(); }
  document.addEventListener('click', function (e) {
    var o = e.target.closest('[data-modal-open]');
    if (o) { open(o.getAttribute('data-modal-open')); return; }
    var c = e.target.closest('[data-modal-close]');
    if (c) { close(c.closest('.modal')); return; }
    if (e.target.classList && e.target.classList.contains('modal')) close(e.target);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    document.querySelectorAll('.modal:not([hidden])').forEach(close);
  });
})();
