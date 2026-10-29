"""Build the two deep-dive pages of the story dashboard (output.html, networks.html) and its themed profile
explorer (explorer.html) from the full dashboard in ../index.html and ../explorer.html.

Every panel, chart and table of the full dashboard is kept; only the shell changes: the sidebar becomes the story
page's top bar, the colours and type follow the story page's tokens, and each page carries only its own sections.
The full dashboard's script runs unchanged apart from a lookup that tolerates panels living on the other page.

Run after the full dashboard changes:  python Dashboard/site/mohit/build_full.py
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "index.html"
EXP = HERE.parent / "explorer.html"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;'
         '12..96,500;12..96,600;12..96,700;12..96,800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&display=swap">')

# The full dashboard's token names, given the story page's values (light, then dark).
LIGHT = """
  --paper:#f5f7fa; --sheet:#ffffff; --ink:#14213d; --ink-2:#4a5570; --ink-3:#7b849a; --rule:#dfe4ec; --grid:#e9edf3; --tint:#eaf0f8;
  --unseen:#f3eefb; --unseen-ink:#5b3f8c; --unseen-rule:#d9cdef;
  --bg:var(--paper); --band:var(--paper); --card:var(--sheet); --fg:var(--ink); --fg2:var(--ink-2); --fg3:var(--ink-3);
  --line:#cdd4e0; --hair:var(--grid); --link:var(--ink); --nav:rgba(245,247,250,.88);
  --kgp:#2a78d6; --rkg:#eb6834; --joint:#8a8fa3; --muted-node:#c3c9d6;
  --q1:#1c5cab; --q2:#3987e5; --q3:#86b6ef; --q4:#cde2fb;
  --c1:#1baf7a; --c2:#eda100; --c3:#e87ba4; --c4:#008300; --c5:#4a3aa7; --c6:#e34948;
  --thumb:#ffffff; --shadow:0 1px 2px rgba(20,33,61,.05), 0 8px 24px rgba(20,33,61,.07);
  --font-display:"Bricolage Grotesque", "Segoe UI", system-ui, sans-serif;
  --font-text:"Bricolage Grotesque", "Segoe UI", system-ui, sans-serif;
  --serif:"Newsreader", Georgia, "Times New Roman", serif;
  --radius:16px; --ease:cubic-bezier(0.28, 0.11, 0.32, 1);
  color-scheme:light;"""
DARK = """
    --paper:#10162a; --sheet:#161e36; --ink:#e8ecf6; --ink-2:#aab3c9; --ink-3:#7d87a0; --rule:#2a3452; --grid:#222b46; --tint:#1a2440;
    --unseen:#211b38; --unseen-ink:#cdb8f5; --unseen-rule:#3e3366;
    --line:#34405f; --nav:rgba(16,22,42,.86);
    --kgp:#4b93ea; --rkg:#e8622e; --joint:#8d93a8; --muted-node:#3a4566;
    --q1:#9ec5f4; --q2:#5598e7; --q3:#2a78d6; --q4:#184f95;
    --c1:#199e70; --c2:#c98500; --c3:#d55181; --c4:#2f9a2f; --c5:#9085e9; --c6:#e66767;
    --thumb:#2c3757; --shadow:0 1px 2px rgba(0,0,0,.4), 0 8px 24px rgba(0,0,0,.35);
    color-scheme:dark;"""
TOKENS = (":root{" + LIGHT + "\n}\n@media (prefers-color-scheme: dark){\n  :root:not([data-theme=\"light\"]){" + DARK +
          "\n  }\n}\n:root[data-theme=\"dark\"]{" + DARK + "\n}\n")

# Story-page shell, laid over the full dashboard's own rules.
SHELL = """
body{font-size:17px; letter-spacing:0; overflow-x:hidden}
main, footer{margin-left:0}
html{scroll-padding-top:120px}
.side, .mbar, .scrim{display:none!important}
a{text-decoration:underline; text-decoration-color:var(--ink-3); text-underline-offset:3px}
a:hover{text-decoration-color:currentColor}
.rank .t a, .lk, .menu a, .bar a, .back a{text-decoration:none}
.lede, .cap, .method p, .findings li, .inspector .hint, details > p, .card > p{font-family:var(--serif)}
.lede{font-size:clamp(19px,2vw,22px); line-height:1.45; letter-spacing:0}
.cap{font-size:15.5px; line-height:1.5}
h1{font-weight:800; letter-spacing:-.035em}
h2{font-weight:700; letter-spacing:-.03em}
section{padding-block:88px; border-top:1px solid var(--rule)}
section.alt{background:var(--paper)}
section:first-of-type{border-top:0}
.card, .kpi, .stat, .inspector, .facpapers{border:1px solid var(--rule)}
section:not(.alt) .card, section:not(.alt) .kpi, section:not(.alt) .stat, section:not(.alt) .inspector, section.alt .kpi{background:var(--sheet)}
section.alt .facpapers, .facpapers{background:var(--paper)}
.eyebrow{font-weight:500; color:var(--ink-3); font-size:15px}
.seg{background:var(--grid)}
.btn{color:var(--ink); border-color:var(--line)}
.btn:hover:not(:disabled){border-color:var(--ink)}
details summary{color:var(--ink); text-decoration:underline; text-decoration-color:var(--ink-3); text-underline-offset:3px}

.bar{position:sticky; top:0; z-index:50; background:var(--nav); backdrop-filter:saturate(1.4) blur(10px); -webkit-backdrop-filter:saturate(1.4) blur(10px); border-bottom:1px solid var(--rule)}
.bar-in{max-width:1180px; margin:0 auto; padding:10px 22px 0; display:flex; align-items:center; gap:16px; flex-wrap:wrap}
.bar .brand{font:800 17px var(--font-display); letter-spacing:-.01em; color:var(--ink); white-space:nowrap}
.bar .crumb{font:500 15px var(--font-display); color:var(--ink-3); white-space:nowrap}
.bar .sp{flex:1}
.bar .menu{flex-basis:100%; flex-direction:row; gap:4px; overflow-x:auto; scrollbar-width:none; padding:6px 0 8px; margin:0 -4px}
.bar .menu a{white-space:nowrap; padding:5px 11px; border-radius:999px; font-size:14px; color:var(--ink-2)}
.bar .menu a:hover{background:var(--grid)}
.bar .menu a.on{background:var(--ink); color:var(--paper); font-weight:500}
.theme{border:1px solid var(--rule); background:var(--sheet); border-radius:999px; width:36px; height:36px; cursor:pointer; display:grid; place-items:center; flex:none; color:var(--ink)}
.theme svg{width:18px; height:18px}
@media (max-width:640px){ .bar .crumb{display:none} .bar-in{padding:8px 16px 0; gap:10px} .seg button{padding:5px 8px} }
.ch-tag{display:flex; align-items:baseline; gap:18px; margin-bottom:6px}
.ch-tag b{font:800 76px/.8 var(--font-display); letter-spacing:-.06em; color:transparent; -webkit-text-stroke:1.5px var(--ink-3)}
.ch-tag span{font:500 15px var(--font-display); color:var(--ink-3)}
.back{display:flex; flex-wrap:wrap; gap:14px; margin-top:8px}
.back a{display:inline-flex; align-items:center; gap:10px; font:600 16px var(--font-display); border:1.5px solid var(--ink); border-radius:999px; padding:10px 20px; color:var(--ink)}
.back a:hover{background:var(--ink); color:var(--paper)}
.back a.quiet{border-color:var(--rule)}
footer{border-top:1px solid var(--rule)}
"""

THEME_BTN = ('<button type="button" class="theme themeBtn" aria-label="Switch light or dark theme">'
             '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4.2"/>'
             '<path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M5.3 18.7l1.6-1.6M17.1 6.9l1.6-1.6"/></svg></button>')
INST_SEG = ('<div class="seg" id="instSeg" role="group" aria-label="Institute"><span class="thumb"></span>'
            '<button type="button" data-inst="both" aria-pressed="true">Both</button>'
            '<button type="button" data-inst="IIT Kharagpur" aria-pressed="false"><span class="dot k"></span>Kharagpur</button>'
            '<button type="button" data-inst="IIT Roorkee" aria-pressed="false"><span class="dot r"></span>Roorkee</button></div>')

PAGES = {
    "output.html": {
        "title": "Output in Full", "no": "1", "crumb": "Chapter 1 in full: data analysis",
        "desc": "Every data-analysis panel for IIT Kharagpur and IIT Roorkee, 2016-2026: output, journal quality, people, most cited and big-team papers.",
        "sections": [("overview", "Overview"), ("output", "Output"), ("quality", "Quality"), ("people", "People"),
                     ("papers", "Most cited"), ("teams", "Big-team papers")],
        "next": ('networks.html', 'Chapter 2 in full: networks'),
        "back": ('./#networks', 'Back to the story: chapter 2'),
    },
    "networks.html": {
        "title": "Networks in Full", "no": "2", "crumb": "Chapter 2 in full: network analysis",
        "desc": "Every network-analysis panel for IIT Kharagpur and IIT Roorkee: citations, Indian links, collaboration, dynamics, higher-order structure, two layers and partners.",
        "sections": [("citations", "Citation network"), ("flow", "Indian links"), ("collaboration", "Collaboration"),
                     ("dynamics", "Dynamics"), ("beyond", "Beyond pairs"), ("layers", "Two layers"),
                     ("partners", "Partners"), ("method", "Method")],
        "next": ('output.html', 'Chapter 1 in full: output'),
        "back": ('./#making', 'Back to the story: chapter 3'),
    },
}


def theme_storage(js):
    """Share the story page's theme setting (rm_mohit_theme, stored as JSON)."""
    js = js.replace('localStorage.getItem("irm-theme")', 'JSON.parse(localStorage.getItem("rm_mohit_theme"))')
    return js.replace('localStorage.setItem("irm-theme", root.dataset.theme)',
                      'localStorage.setItem("rm_mohit_theme", JSON.stringify(root.dataset.theme))')


def strip_tokens(css):
    """Drop the source's own :root token blocks (everything before the first `* {` rule)."""
    i = css.index("* { box-sizing")
    return css[i:]


def build_pages():
    html = SRC.read_text(encoding="utf-8")
    css = re.search(r"<style>(.*?)</style>", html, re.S).group(1)
    js = re.search(r'<script src="https://cdnjs[^"]+"></script>\s*<script>(.*?)</script>', html, re.S).group(1)
    sections = {m.group(1): m.group(0) for m in re.finditer(r'<section id="([a-z]+)"[^>]*>.*?\n</section>', html, re.S)}

    # panels that live on the other page resolve to a detached element, so the script runs unchanged
    js = js.replace("document.getElementById(", "$id(").replace("document.querySelector(", "$q(")
    js = js.replace("(() => {", "(() => {\n  const $id = id => document.getElementById(id) || Object.assign(document.createElement(\"div\"), { value: \"\" });\n"
                    "  const $q = s => document.querySelector(s) || document.createElement(\"tbody\");", 1)
    js = js.replace('sc.src = "papers.js"', 'sc.src = "../papers.js"')
    js = theme_storage(js)

    for name, P in PAGES.items():
        body = "\n\n".join(sections[s] for s, _ in P["sections"])
        if name == "output.html":
            body = body.replace('<p class="eyebrow">Research mapping · 2016 – 2026</p>\n    <h1>Two IITs.<br>A decade of research.</h1>',
                                '<div class="ch-tag"><b aria-hidden="true">1</b><span>Data analysis, every panel</span></div>\n'
                                '    <h1>What they publish, in full.</h1>')
            body = body.replace('<p class="lede">Every confirmed publication',
                                '<p class="lede">The story page shows the five charts that carry the argument. This page keeps every panel, table and paper list behind them. Every confirmed publication', 1)
        else:
            body = body.replace('<section id="citations">', '<section id="citations">\n  <div class="wrap"><div class="ch-tag"><b aria-hidden="true">2</b><span>Network analysis, every panel</span></div></div>', 1)
        body = body.replace('<select class="field" id=', '<select class="combo" data-noun="departments" id=')
        nav = "".join(f'<a href="#{s}">{t}</a>' for s, t in P["sections"])
        page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{P['title']}</title>
<meta name="description" content="{P['desc']}">
<!-- Generated by build_full.py from ../index.html. Edit that file (or the shell in build_full.py), then rebuild. -->
{FONTS}
<style>
{TOKENS}{strip_tokens(css)}{SHELL}</style>
</head>
<body>
<header class="bar">
  <div class="bar-in">
    <a class="brand" href="./">Two IITs, ten years</a>
    <span class="crumb">{P['crumb']}</span>
    <span class="sp"></span>
    {INST_SEG}
    {THEME_BTN}
    <nav class="menu" aria-label="Sections">{nav}</nav>
  </div>
</header>
<main>
{body}

<section id="more-{P['no']}">
  <div class="wrap">
    <div class="back">
      <a href="{P['back'][0]}">{P['back'][1]}</a>
      <a class="quiet" href="{P['next'][0]}">{P['next'][1]}</a>
      <a class="quiet" href="explorer.html">Profile explorer</a>
    </div>
  </div>
</section>
</main>
<footer>
  <div class="wrap">
    <p>DPCN Research Mapping Project, Group 3. IIT Kharagpur and IIT Roorkee, 2016–2026.</p>
    <p>Sources: Crossref, Europe PMC, DOAJ, ORCID, DBLP, OpenAlex, Scimago Journal Rank, CORE. Data collected October 2026.</p>
  </div>
</footer>
<script src="../data.js"></script>
<script src="combo.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/echarts/5.5.0/echarts.min.js"></script>
<script>{js}</script>
</body>
</html>
"""
        (HERE / name).write_text(page, encoding="utf-8", newline="\n")
        print("wrote", name, len(page), "bytes")


def build_explorer():
    html = EXP.read_text(encoding="utf-8")
    html = re.sub(r'<link rel="preconnect".*?display=swap">', FONTS, html, count=1, flags=re.S)
    css = re.search(r"<style>(.*?)</style>", html, re.S).group(1)
    shell = """
.lede, header.top p{font-family:var(--serif); font-size:17px}
a{color:var(--ink); text-decoration:underline; text-decoration-color:var(--ink-3); text-underline-offset:3px}
.card{border:1px solid var(--rule); background:var(--sheet); box-shadow:none}
body{background:var(--paper)}
header.top h1{font:800 34px/1.05 var(--font-display); letter-spacing:-.03em}
.sbar{position:sticky; top:0; z-index:50; background:var(--nav); backdrop-filter:blur(10px); -webkit-backdrop-filter:blur(10px); border-bottom:1px solid var(--rule)}
.sbar-in{max-width:1240px; margin:0 auto; padding:12px 16px; display:flex; gap:16px; align-items:baseline}
.sbar .brand{font:800 17px var(--font-display); color:var(--ink); text-decoration:none}
.row .cbx{flex:1}
.sbar .crumb{font:500 15px var(--font-display); color:var(--ink-3)}
.cbx-btn{min-height:40px; border-radius:10px}
.controls label, th{text-transform:none; letter-spacing:0}
.controls label{font-size:13px}
"""
    html = html.replace(css, "\n" + TOKENS + strip_tokens(css) + shell)
    html = html.replace('href="index.html"', 'href="./"')
    html = re.sub(r'(["\'])profiles\.js\1', r'\1../profiles.js\1', html)
    html = theme_storage(html)
    for i in ("dept", "fac", "cmpA", "cmpB"):
        html = html.replace(f'<select id="{i}"', f'<select class="combo" id="{i}"')
    html = html.replace('<script src="https://cdnjs', '<script src="combo.js"></script>\n<script src="https://cdnjs', 1)
    html = html.replace('<div class="wrap">\n  <header class="top">', '<header class="sbar"><div class="sbar-in"><a class="brand" href="./">Two IITs, ten years</a>'
                        '<span class="crumb">Profile explorer</span></div></header>\n<div class="wrap">\n  <header class="top">', 1)
    (HERE / "explorer.html").write_text(html, encoding="utf-8", newline="\n")
    print("wrote explorer.html", len(html), "bytes")


if __name__ == "__main__":
    build_pages()
    build_explorer()
