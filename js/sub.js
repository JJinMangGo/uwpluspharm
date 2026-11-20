/* UWPLUSPHARM sub.js */
(function () {
  'use strict';

  /* 사업분야 폴더 탭: 페이지가 바뀌어도 스크롤 위치 유지 */
  var KEY = 'uw-folder-scroll';
  try {
    var saved = sessionStorage.getItem(KEY);
    if (saved !== null) {
      sessionStorage.removeItem(KEY);
      if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
      window.scrollTo(0, +saved);
    }
  } catch (e) {}
  document.querySelectorAll('.folder-tabs__link').forEach(function (a) {
    a.addEventListener('click', function () {
      try { sessionStorage.setItem(KEY, window.scrollY); } catch (e) {}
    });
  });

  /* 인증서 라이트박스 */
  var lb = document.querySelector('.lightbox');
  if (lb) {
    var lbImg = lb.querySelector('img');
    var lbClose = lb.querySelector('.lightbox__close');
    var last;
    var close = function () { lb.hidden = true; document.body.style.overflow = ''; last && last.focus(); };
    document.querySelectorAll('[data-lightbox]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        last = btn;
        lbImg.src = btn.getAttribute('data-lightbox');
        lbImg.alt = btn.getAttribute('data-title') || '';
        lb.hidden = false;
        document.body.style.overflow = 'hidden';
        lbClose.focus();
      });
    });
    lbClose.addEventListener('click', close);
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !lb.hidden) close(); });
  }

  /* 제품 상세 갤러리: 썸네일 클릭 시 큰 이미지 교체 */
  var main = document.querySelector('.pview__main img');
  if (main) {
    var thumbs = document.querySelectorAll('.pview__thumb');
    thumbs.forEach(function (t) {
      t.addEventListener('click', function () {
        main.src = t.querySelector('img').src;
        thumbs.forEach(function (o) { o.classList.toggle('is-active', o === t); o.setAttribute('aria-current', o === t); });
      });
    });
  }

  /* 제품 목록 분류 (정적 미리보기용 — 그누보드에서는 sca 파라미터로 서버가 걸러줌) */
  var grid = document.querySelector('[data-plist]');
  if (grid) {
    var sca = new URLSearchParams(location.search).get('sca') || '';
    var cards = grid.querySelectorAll('.p-card');
    var n = 0;
    cards.forEach(function (c) {
      var show = !sca || c.getAttribute('data-ca') === sca;
      c.hidden = !show; if (show) n++;
    });
    document.querySelectorAll('[data-sca]').forEach(function (a) {
      var on = a.getAttribute('data-sca') === sca;
      a.classList.toggle('is-active', on);
      if (on) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
    });
    var title = document.querySelector('.plist__head h2');
    var count = document.querySelector('.plist__head b');
    if (title) title.textContent = sca ? sca + ' 제품' : '전체 제품';
    if (count) count.textContent = n;
  }
})();
