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

# 서브 비주얼 (메뉴별)
VISUAL = {
    'company':  ('ABOUT US', '회사소개', '무독성 의료용 접착 기술로 상처 보호의 새로운 기준을 만듭니다'),
    'business': ('BUSINESS', '사업분야', '국내 병원·약국부터 해외 수출까지, 일상을 지키는 제품을 공급합니다'),
    'product':  ('PRODUCTS', '제품안내', '일상을 보호하는 유원플러스팜의 제품을 소개합니다'),
    'support':  ('SUPPORT', '고객지원', '제품 도입·수출 상담과 회사 소개 자료를 안내합니다'),
}
MENU_NAME = {'company': '회사소개', 'business': '사업분야', 'product': '제품안내', 'support': '고객지원'}
# 서브 탭 (pill)
TABS = {
    'company': [('company.html', '회사개요'), ('cert.html', '인증현황'), ('location.html', '오시는 길')],
    'support': [('contact.html', '문의하기'), ('brochure.html', '영문 소개서')],
    'product': [('products.html', '전체', ''), ('products.html?sca=액상밴드', '액상밴드', '액상밴드'),
                ('products.html?sca=창상피복제', '창상피복제', '창상피복제'), ('products.html?sca=리튬이온 소화기', '리튬이온 소화기', '리튬이온 소화기')],
}

# 제품 카드 데이터 (그누보드에서는 갤러리 게시판 목록으로 대체)
# key, 분류, 뱃지, 제품명, 판매처, 한줄설명, 이미지, 출시예정
PRODUCTS = [
    ('pianna', '액상밴드', '일반 생활용품', '피안나', '온라인 · 일반 도소매', '크고 작은 상처를 물로부터 지켜주는 바르는 액상밴드', 'product-pianna.png', False),
    ('dermaglue', '액상밴드', '의료기기 3등급', '더마글루', '병원 · 약국', '땀과 물에 강한 방수 피막, 인체 무독성 피부 접착제', 'product-dermaglue.png', False),
    ('quickguard', '액상밴드', '수출용', '퀵가드', '수출용', '바르는 즉시 밀착, 움직여도 갈라지지 않는 피막', 'product-quickguard.png', False),
    ('waterbioskin', '창상피복제', '창상피복제', '워터바이오스킨', '병원 수술실 · 비급여 BM5000JZ', '상처 부위를 덮어 보호하는 창상피복제 (1g · 2g)', 'product-waterbioskin.png', False),
    ('toktok', '창상피복제', '의료기기 2등급', '상처N 톡톡', '피부과 · 약국 (판매 예정)', '톡톡 바르면 끝, 샤워와 화장도 가능한 액상밴드', 'product-toktok.png', False),
    ('cellubond', '창상피복제', '의료기기 3등급', '셀루본드', '병원 · 약국', '의료기기 3등급 승인을 받은 신제품', 'product-cellubond.png', False),
    ('spray', '창상피복제', '출시 예정', '상처N 스프레이', 'Coming soon', '상처N 톡톡의 후속 모델로 출시 예정입니다.', '', True),
    ('fo-lia', '리튬이온 소화기', 'KFI 형식인증', 'FO-LIA', '강화액 8.0L · KFI 형식인증', '리튬이온 배터리 화재용 소화기. N2 축압식 스테인리스, 사용온도 -20~+40℃', 'product-fo-lia.png', False),
    ('fo-liab', '리튬이온 소화기', 'KFI 형식인증', 'FO-LIAB', '강화액 4.0L · KFI 형식인증', '리튬이온 배터리 화재용 소화기. N2 축압식 스테인리스, 사용온도 -20~+40℃', 'product-fo-liab.png', False),
]

def card(p):
    key, ca, badge, name, use, desc, img, soon = p
    if soon:
        return (f'<div class="p-card p-card--soon" data-ca="{ca}">\n'
                f'  <div class="p-card__img p-card__img--soon">COMING SOON</div>\n'
                f'  <div class="p-card__body"><span class="badge">{badge}</span><h3 class="p-card__name">{name}</h3>'
                f'<p class="p-card__use">{use}</p><p class="p-card__desc">{desc}</p><span class="link-more p-card__more">출시 예정</span></div>\n</div>')
    return (f'<a class="p-card" href="product-view.html?p={key}" data-ca="{ca}">\n'
            f'  <div class="p-card__img"><img src="images/product/{img}" alt="{name}" loading="lazy"></div>\n'
            f'  <div class="p-card__body"><span class="badge">{badge}</span><h3 class="p-card__name">{name}</h3>'
            f'<p class="p-card__use">{use}</p><p class="p-card__desc">{desc}</p><span class="link-more p-card__more">자세히 보기</span></div>\n</a>')

def cards(arg):
    # all | 분류명 | related:key
    if arg == 'all':
        items = PRODUCTS
    elif arg.startswith('related:'):
        k = arg.split(':', 1)[1]
        me = next(p for p in PRODUCTS if p[0] == k)
        items = [p for p in PRODUCTS if p[1] == me[1] and p[0] != k and not p[7]][:4]
    else:
        items = [p for p in PRODUCTS if p[1] == arg]
    return '\n'.join(card(p) for p in items)

def sub_visual(meta, menu):
    label, title, desc = VISUAL[menu]
    crumb = meta.get('crumb', '')
    lis = f'<li>HOME</li><li>{MENU_NAME[menu]}</li>' + (f'<li>{crumb}</li>' if crumb else '')
    return (f'<section class="sub-visual">\n  <div class="sub-visual__inner">\n'
            f'    <span class="sub-visual__label">{label}</span>\n    <h2 class="sub-visual__title">{title}</h2>\n'
            f'    <p class="sub-visual__desc">{desc}</p>\n    <ol class="breadcrumb" aria-label="현재 위치">{lis}</ol>\n  </div>\n</section>\n')

def sub_tabs(menu, current):
    if menu not in TABS:
        return ''
    out = []
    for t in TABS[menu]:
        href, name = t[0], t[1]
        extra = f' data-sca="{t[2]}"' if len(t) > 2 else ''
        on = (name == current) and len(t) == 2
        out.append(f'<li><a class="sub-tabs__link{" is-active" if on else ""}" href="{href}"{extra}{" aria-current=\"page\"" if on else ""}>{name}</a></li>')
    return '<nav class="sub-tabs" aria-label="하위 메뉴"><ul class="sub-tabs__list">' + ''.join(out) + '</ul></nav>\n'

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
    if meta.get('menu') in VISUAL and page.stem != 'index':
        tabs_html = '' if meta.get('tabs') == 'no' else sub_tabs(meta['menu'], meta.get('crumb', ''))
        raw = sub_visual(meta, meta['menu']) + tabs_html + raw
    raw = re.sub(r'<!--\s*cards:([^\s]+)\s*-->', lambda m: cards(m.group(1)), raw)
    css = ''.join(f'<link rel="stylesheet" href="css/{c.strip()}.css">\n' for c in meta.get('css', '').split(',') if c.strip())
    js = ''.join(f'<script src="js/{j.strip()}.js"></script>\n' for j in meta.get('js', '').split(',') if j.strip())
    out = TPL.format(title=title, css=css, js=js, vcss=vcss, vjs=vjs, body=meta.get('body', 'sub'),
                     header=h.rstrip(), content=raw.rstrip(), footer=footer.rstrip())
    (ROOT / page.name).write_text(fill(include(out)), encoding='utf-8')
    print('built', page.name)
