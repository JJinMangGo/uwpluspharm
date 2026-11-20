"""정적 페이지 조립 스크립트.
_src/pages/*.html 의 첫 줄 주석에 메타를 적고, 헤더/푸터를 끼워 루트에 출력한다.
  <!-- title: 회사개요 | menu: company | header: solid -->
그누보드 테마 전환 시: partials/header.html → head.php, footer.html → tail.php
공통 값(이메일·카카오 링크)은 아래 SITE 한 곳에서만 바꾼다.
"""
import re, pathlib

SITE = {
    'EMAIL': 'plus-1220@naver.com',   # 회사 도메인 메일 확정되면 여기만 교체
    'KAKAO_URL': '#',                 # 카카오톡 채널 URL 확정되면 교체
    'TEL': '031-778-6186',
    'FAX': '031-697-8907',
    'ADDR': '경기도 성남시 수정구 복정로 101, 2층',
    'HOURS': '평일 09:00 – 18:00 (점심 12:00 – 13:00)',
}
MENUS = ['company', 'business', 'product', 'support']

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / '_src'
header = (SRC / 'partials/header.html').read_text(encoding='utf-8')
footer = (SRC / 'partials/footer.html').read_text(encoding='utf-8')

TPL = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="유원플러스팜 — 액상밴드·창상피복제·리튬이온 소화기 전문기업">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
{vcss}<link rel="stylesheet" href="css/tokens.css">
<link rel="stylesheet" href="css/common.css">
{css}</head>
<body class="{body}">
{header}
<main id="main">
{content}
</main>
{footer}
{vjs}<script src="js/common.js"></script>
{js}</body>
</html>
'''

def include(s):
    # <!-- include:name --> → partials/name.html
    return re.sub(r'<!--\s*include:([\w-]+)\s*-->',
                  lambda m: (SRC / 'partials' / (m.group(1) + '.html')).read_text(encoding='utf-8').rstrip(), s)

def fill(s):
    for k, v in SITE.items():
        s = s.replace('{{' + k + '}}', v)
    return s

for page in sorted((SRC / 'pages').glob('*.html')):
    raw = page.read_text(encoding='utf-8')
    m = re.match(r'\s*<!--(.*?)-->\s*', raw, re.S)
    meta = {}
    if m:
        for part in m.group(1).split('|'):
            if ':' in part:
                k, v = part.split(':', 1)
                meta[k.strip()] = v.strip()
        raw = raw[m.end():]
    h = header.replace('{{HEADER_CLASS}}', ' header--solid' if meta.get('header') == 'solid' else '')
    for mn in MENUS:
        h = h.replace('{{ON_' + mn + '}}', ' is-active' if meta.get('menu') == mn else '')
    title = '유원플러스팜' if page.stem == 'index' else f"{meta.get('title', '')} | 유원플러스팜"
    swiper = 'swiper' in meta.get('lib', '')
    vcss = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css">\n' if swiper else ''
    vjs = '<script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>\n' if swiper else ''
    css = ''.join(f'<link rel="stylesheet" href="css/{c.strip()}.css">\n' for c in meta.get('css', '').split(',') if c.strip())
    js = ''.join(f'<script src="js/{j.strip()}.js"></script>\n' for j in meta.get('js', '').split(',') if j.strip())
    out = TPL.format(title=title, css=css, js=js, vcss=vcss, vjs=vjs, body=meta.get('body', 'sub'),
                     header=h.rstrip(), content=raw.rstrip(), footer=footer.rstrip())
    (ROOT / page.name).write_text(fill(include(out)), encoding='utf-8')
    print('built', page.name)
