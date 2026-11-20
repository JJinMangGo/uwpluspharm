# 유원플러스팜 홈페이지 퍼블리싱

정적 HTML/CSS/JS. 그누보드 테마로 옮기기 전 퍼블 결과물.

## 구조
- `*.html` — 빌드된 페이지 (직접 수정하지 말고 `_src`에서 수정 후 빌드)
- `_src/pages/` — 페이지 본문
- `_src/partials/` — 공통 조각 (header → head.php, footer → tail.php, contact-form 등)
- `_src/build.py` — 헤더·푸터·조각을 끼워 루트에 HTML 생성. 이메일·전화·카카오 링크는 맨 위 `SITE`에서만 수정
- `css/tokens.css` — 피그마 컬러 변수와 1:1
- `css/common.css`, `css/main.css` — 공통 / 메인
- `js/common.js`, `js/main.js` — 공통 / 메인 (Swiper 11, `js/vendor`)

## 빌드
```
python3 _src/build.py
```
