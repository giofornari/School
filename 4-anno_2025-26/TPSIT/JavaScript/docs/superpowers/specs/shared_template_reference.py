#!/usr/bin/env python3
"""
Shared HTML template for all four repo sites.
Copy render_page() and highlight_*() into each repo's generate-site.py.
Design system: Charcoal (v4 approved 2026-05-13)
Nav URLs: update per-repo (active_nav selects the current site).
"""

import re
import html as html_lib

# ── NAV CONFIG ────────────────────────────────────────────────────────────────
NAV_LINKS = [
    ("Java",       "https://bigbrodyg.github.io/JavaProjects/"),
    ("JavaScript", "https://bigbrodyg.github.io/DIYJavaScript/"),
    ("Python",     "https://bigbrodyg.github.io/PythonAlmostSelfLearned/"),
    ("GApps",      "https://bigbrodyg.github.io/GAppProjects/"),
]

# ── SYNTAX HIGHLIGHTING ───────────────────────────────────────────────────────

def highlight_java(code: str) -> str:
    """Minimal Java syntax highlighting. Returns HTML-escaped string with span tags."""
    KEYWORDS = {
        'public', 'private', 'protected', 'static', 'void', 'class', 'interface',
        'extends', 'implements', 'new', 'return', 'if', 'else', 'for', 'while',
        'do', 'switch', 'case', 'break', 'continue', 'try', 'catch', 'finally',
        'throw', 'throws', 'import', 'package', 'final', 'abstract', 'boolean',
        'int', 'double', 'float', 'long', 'char', 'byte', 'short', 'String',
        'true', 'false', 'null', 'this', 'super', 'instanceof'
    }
    escaped = html_lib.escape(code)
    escaped = re.sub(r'(//[^\n]*)', r'<span class="cm">\1</span>', escaped)
    escaped = re.sub(r'(/\*.*?\*/)', r'<span class="cm">\1</span>', escaped, flags=re.DOTALL)
    escaped = re.sub(r'(&quot;[^&]*?&quot;)', r'<span class="str">\1</span>', escaped)
    escaped = re.sub(r'\b([A-Z][a-zA-Z0-9]+)\b(?![^<]*>)', r'<span class="cl">\1</span>', escaped)
    for kw in KEYWORDS:
        escaped = re.sub(rf'\b({re.escape(kw)})\b(?![^<]*>)', r'<span class="kw">\1</span>', escaped)
    return escaped


def highlight_python(code: str) -> str:
    """Minimal Python syntax highlighting."""
    KEYWORDS = {
        'def', 'class', 'import', 'from', 'return', 'if', 'elif', 'else',
        'for', 'while', 'in', 'not', 'and', 'or', 'True', 'False', 'None',
        'with', 'as', 'try', 'except', 'raise', 'finally', 'pass', 'break',
        'continue', 'lambda', 'yield', 'global', 'nonlocal', 'del', 'assert',
        'is', 'print', 'len', 'range', 'int', 'str', 'float', 'list', 'dict',
        'set', 'tuple', 'open', 'type'
    }
    escaped = html_lib.escape(code)
    escaped = re.sub(r'(#[^\n]*)', r'<span class="cm">\1</span>', escaped)
    escaped = re.sub(r'(&quot;[^&]*?&quot;|&#x27;[^&]*?&#x27;)', r'<span class="str">\1</span>', escaped)
    escaped = re.sub(r'\b([A-Z][a-zA-Z0-9]+)\b(?![^<]*>)', r'<span class="cl">\1</span>', escaped)
    for kw in KEYWORDS:
        escaped = re.sub(rf'\b({re.escape(kw)})\b(?![^<]*>)', r'<span class="kw">\1</span>', escaped)
    return escaped


def highlight_dart(code: str) -> str:
    """Minimal Dart syntax highlighting."""
    KEYWORDS = {
        'class', 'void', 'var', 'final', 'const', 'static', 'return', 'if',
        'else', 'for', 'while', 'new', 'import', 'export', 'extends', 'implements',
        'abstract', 'String', 'int', 'double', 'bool', 'List', 'Map', 'Set',
        'Future', 'Stream', 'async', 'await', 'true', 'false', 'null', 'this',
        'super', 'try', 'catch', 'throw', 'rethrow', 'in', 'is', 'as', 'late',
        'required', 'dynamic', 'Widget', 'BuildContext', 'override'
    }
    escaped = html_lib.escape(code)
    escaped = re.sub(r'(//[^\n]*)', r'<span class="cm">\1</span>', escaped)
    escaped = re.sub(r'(&quot;[^&]*?&quot;|&#x27;[^&]*?&#x27;)', r'<span class="str">\1</span>', escaped)
    escaped = re.sub(r'\b([A-Z][a-zA-Z0-9]+)\b(?![^<]*>)', r'<span class="cl">\1</span>', escaped)
    for kw in KEYWORDS:
        escaped = re.sub(rf'\b({re.escape(kw)})\b(?![^<]*>)', r'<span class="kw">\1</span>', escaped)
    return escaped


def highlight_js(code: str) -> str:
    """Minimal JS syntax highlighting."""
    KEYWORDS = {
        'const', 'let', 'var', 'function', 'return', 'if', 'else', 'for',
        'while', 'class', 'new', 'import', 'export', 'default', 'extends',
        'static', 'async', 'await', 'true', 'false', 'null', 'undefined',
        'this', 'super', 'try', 'catch', 'throw', 'typeof', 'instanceof',
        'in', 'of', 'from', 'document', 'window', 'console'
    }
    escaped = html_lib.escape(code)
    escaped = re.sub(r'(//[^\n]*)', r'<span class="cm">\1</span>', escaped)
    escaped = re.sub(r'(&quot;[^&]*?&quot;|&#x27;[^&]*?&#x27;|`[^`]*`)', r'<span class="str">\1</span>', escaped)
    escaped = re.sub(r'\b([A-Z][a-zA-Z0-9]+)\b(?![^<]*>)', r'<span class="cl">\1</span>', escaped)
    for kw in KEYWORDS:
        escaped = re.sub(rf'\b({re.escape(kw)})\b(?![^<]*>)', r'<span class="kw">\1</span>', escaped)
    return escaped


def slugify(name: str) -> str:
    """Convert project name to a safe HTML id."""
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


# ── CARD + DETAIL PANEL RENDERERS ─────────────────────────────────────────────

def render_card(project: dict, index: int) -> str:
    slug = slugify(project['name'])
    active = 'active' if index == 0 else ''
    cat = html_lib.escape(project['category'])
    onclick = f"toggleDetail(this,'{slug}')"

    if project['has_output']:
        output_preview = project['output'][:60].replace('\n', ' ').strip()
        footer = f'<span class="output-pill">{html_lib.escape(output_preview)}</span>'
    else:
        footer = '<a class="source-link" href="#">⟶ view source</a>'

    return f'''
    <div class="project-card {active}" data-category="{cat}" onclick="{onclick}">
      <span class="expand-icon">⌄</span>
      <div class="project-name">{html_lib.escape(project["name"])}</div>
      <div class="project-path">{html_lib.escape(project["path"])}</div>
      {footer}
    </div>'''


def render_detail_panel(project: dict, index: int, highlighter) -> str:
    slug = slugify(project['name'])
    visible = 'visible' if index == 0 else ''
    highlighted = highlighter(project['source_content'])

    if project['has_output']:
        output_pane = f'''
      <div class="pane">
        <div class="pane-label">Output</div>
        <div class="output-block">{html_lib.escape(project["output"])}</div>
      </div>'''
        grid_cols = 'grid-template-columns: 1fr 1fr'
    else:
        output_pane = ''
        grid_cols = 'grid-template-columns: 1fr'

    return f'''
  <div class="detail-panel {visible}" id="detail-{slug}">
    <div class="detail-header">
      <span class="detail-filename">{html_lib.escape(project["source_file"])}</span>
      <span class="detail-close" onclick="closeDetail()">close ✕</span>
    </div>
    <div class="detail-body" style="{grid_cols}">
      <div class="pane">
        <div class="pane-label">Source</div>
        <pre>{highlighted}</pre>
      </div>{output_pane}
    </div>
  </div>'''


# ── MAIN RENDER ───────────────────────────────────────────────────────────────

def render_page(
    repo_title: str,
    repo_desc: str,
    active_nav: str,
    projects: list,
    highlighter,
) -> str:
    """
    Render a complete index.html page.

    projects: list of dicts with keys:
      name, path, category, source_file, source_content, output (str|None), has_output (bool)
    highlighter: one of highlight_java / highlight_python / highlight_dart / highlight_js
    active_nav: one of "Java" | "JavaScript" | "Python" | "GApps"
    """
    categories = sorted({p['category'] for p in projects})
    has_output_count = sum(1 for p in projects if p['has_output'])

    nav_items_parts = []
    for label, url in NAV_LINKS:
        active_attr = ' class="active"' if label == active_nav else ''
        nav_items_parts.append(f'    <li><a href="{url}"{active_attr}>{label}</a></li>')
    nav_items = '\n'.join(nav_items_parts)

    tab_all = f'<div class="tab active" onclick="setTab(this,\'all\')">All <span class="tab-count">{len(projects)}</span></div>'
    tab_cats = '\n'.join(
        f'<div class="tab" onclick="setTab(this,\'{html_lib.escape(cat)}\')">{html_lib.escape(cat)} <span class="tab-count">{sum(1 for p in projects if p["category"]==cat)}</span></div>'
        for cat in categories
    )

    cards = '\n'.join(render_card(p, i) for i, p in enumerate(projects))
    detail_panels = '\n'.join(render_detail_panel(p, i, highlighter) for i, p in enumerate(projects))
    panel_open_class = 'panel-open' if projects else ''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_lib.escape(repo_title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg:#141414;--surface:#1d1d1d;--surface-hi:#252525;
    --border:#2c2c2c;--border-hi:#3c3c3c;
    --text-1:#ededed;--text-2:#a5a5a5;--text-3:#717171;--text-4:#565656;
    --green:#22c55e;--green-dim:rgba(34,197,94,.07);--green-border:rgba(34,197,94,.20);
    --blue:#60a5fa;--blue-dim:rgba(96,165,250,.08);--blue-border:rgba(96,165,250,.22);
    --font-sans:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
    --font-mono:'JetBrains Mono','Fira Code',monospace;
  }}
  *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
  body{{background:var(--bg);color:var(--text-1);font-family:var(--font-sans);min-height:100vh;font-size:14px;line-height:1.5;-webkit-font-smoothing:antialiased}}
  nav{{border-bottom:1px solid var(--border);padding:0 56px;height:50px;display:flex;align-items:center;justify-content:flex-end;position:sticky;top:0;background:rgba(20,20,20,.92);backdrop-filter:blur(16px);z-index:10}}
  .nav-links{{display:flex;gap:2px;list-style:none}}
  .nav-links a{{font-size:12px;color:var(--text-3);text-decoration:none;font-weight:500;padding:5px 11px;border-radius:5px;transition:color .12s,background .12s}}
  .nav-links a:hover{{color:var(--text-2);background:var(--surface)}}
  .nav-links a.active{{color:var(--text-1);background:var(--surface-hi)}}
  .hero{{padding:72px 56px 44px;border-bottom:1px solid var(--border)}}
  .hero-eyebrow{{display:flex;align-items:center;gap:10px;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.13em;color:var(--text-3);margin-bottom:22px}}
  .hero-eyebrow-dot{{width:4px;height:4px;border-radius:50%;background:var(--green);flex-shrink:0}}
  .hero-title{{font-size:64px;font-weight:800;letter-spacing:-2.5px;line-height:1;color:#fff;margin-bottom:20px}}
  .hero-desc{{font-size:14px;color:var(--text-2);max-width:440px;line-height:1.75;margin-bottom:32px}}
  .hero-meta{{display:flex;align-items:center;gap:18px;flex-wrap:wrap}}
  .meta-stat{{font-size:12px;color:var(--text-3)}}
  .meta-stat strong{{color:var(--text-2);font-weight:600}}
  .meta-divider{{width:1px;height:12px;background:var(--border-hi);flex-shrink:0}}
  .content{{padding:0 56px}}
  .filter-row{{display:flex;align-items:center;justify-content:space-between;padding:22px 0 18px;border-bottom:1px solid var(--border);margin-bottom:20px}}
  .tabs{{display:flex;gap:2px}}
  .tab{{font-size:12px;font-weight:500;padding:5px 12px;border-radius:5px;color:var(--text-3);cursor:pointer;transition:color .12s,background .12s;user-select:none}}
  .tab:hover{{color:var(--text-2);background:var(--surface)}}
  .tab.active{{color:var(--text-1);background:var(--surface-hi)}}
  .tab-count{{display:inline-block;font-size:10px;color:var(--text-4);margin-left:4px;font-variant-numeric:tabular-nums}}
  .tab.active .tab-count{{color:var(--text-3)}}
  .filter-right{{font-size:11px;color:var(--text-3);display:flex;align-items:center;gap:6px;font-weight:500}}
  .filter-dot{{width:6px;height:6px;border-radius:50%;background:var(--green);flex-shrink:0}}
  .projects{{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--border);border:1px solid var(--border);border-radius:8px;overflow:hidden}}
  .projects.panel-open{{border-radius:8px 8px 0 0;border-bottom-color:transparent}}
  .project-card{{background:var(--bg);padding:22px 24px 20px;cursor:pointer;transition:background .1s;position:relative;min-height:100px}}
  .project-card[data-category]{{display:block}}
  .project-card.hidden{{display:none}}
  .project-card:hover{{background:var(--surface)}}
  .project-card.active{{background:var(--surface-hi);border-top:2px solid var(--border-hi);padding-top:20px}}
  .expand-icon{{position:absolute;top:22px;right:18px;font-size:11px;color:var(--text-4);transition:color .1s,transform .15s;line-height:1}}
  .project-card:hover .expand-icon{{color:var(--text-3)}}
  .project-card.active .expand-icon{{color:var(--text-3);transform:rotate(180deg)}}
  .project-name{{font-size:13px;font-weight:600;color:var(--text-1);margin-bottom:5px;padding-right:28px;letter-spacing:-.1px}}
  .project-path{{font-family:var(--font-mono);font-size:10px;color:var(--text-3);margin-bottom:14px}}
  .output-pill{{display:inline-flex;align-items:center;gap:5px;font-family:var(--font-mono);font-size:10px;color:var(--green);background:var(--green-dim);border:1px solid var(--green-border);padding:3px 8px;border-radius:3px;max-width:210px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
  .output-pill::before{{content:'▶';font-size:7px;flex-shrink:0}}
  .source-link{{font-size:10px;font-weight:500;color:var(--text-3);text-decoration:none;display:inline-flex;align-items:center;gap:4px;transition:color .1s}}
  .source-link:hover{{color:var(--text-2)}}
  .detail-panel{{border:1px solid var(--border);border-top:none;border-radius:0 0 8px 8px;overflow:hidden;margin-bottom:52px;display:none}}
  .detail-panel.visible{{display:block}}
  .detail-header{{background:var(--surface);border-bottom:1px solid var(--border);padding:12px 22px;display:flex;align-items:center;justify-content:space-between}}
  .detail-filename{{font-family:var(--font-mono);font-size:11.5px;font-weight:500;color:var(--text-2);display:flex;align-items:center;gap:8px}}
  .detail-filename::before{{content:'';display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--green);flex-shrink:0;opacity:.8}}
  .detail-close{{font-size:11px;color:var(--text-4);cursor:pointer;padding:3px 8px;border-radius:4px;transition:color .12s,background .12s;font-weight:500}}
  .detail-close:hover{{color:var(--text-1);background:var(--surface-hi)}}
  .detail-body{{display:grid}}
  .pane{{padding:24px 26px}}
  .pane:first-child{{border-right:1px solid var(--border)}}
  .pane-label{{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.14em;color:var(--text-4);margin-bottom:16px}}
  pre{{font-family:var(--font-mono);font-size:11.5px;color:var(--text-2);line-height:1.9;white-space:pre-wrap}}
  pre .kw{{color:#93c5fd}}pre .cl{{color:#f9a8d4}}pre .cm{{color:var(--text-3);font-style:italic}}pre .str{{color:#86efac}}
  .output-block{{font-family:var(--font-mono);font-size:12px;color:var(--green);background:#101d14;border:1px solid var(--green-border);border-radius:6px;padding:18px 20px;line-height:2.1;white-space:pre-wrap}}
</style>
</head>
<body>
<nav>
  <ul class="nav-links">
{nav_items}
  </ul>
</nav>
<div class="hero">
  <div class="hero-eyebrow"><span class="hero-eyebrow-dot"></span>School projects · Giordano Fornari</div>
  <h1 class="hero-title">{html_lib.escape(repo_title)}</h1>
  <p class="hero-desc">{html_lib.escape(repo_desc)}</p>
  <div class="hero-meta">
    <span class="meta-stat"><strong>{len(projects)}</strong> projects</span>
    <span class="meta-divider"></span>
    <span class="meta-stat"><strong>{has_output_count}</strong> with output</span>
  </div>
</div>
<div class="content">
  <div class="filter-row">
    <div class="tabs">
      {tab_all}
      {tab_cats}
    </div>
    <div class="filter-right"><span class="filter-dot"></span>{has_output_count} with live output</div>
  </div>
  <div class="projects {panel_open_class}" id="grid">
{cards}
  </div>
{detail_panels}
</div>
<script>
function setTab(el, cat) {{
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  document.querySelectorAll('.project-card').forEach(c => {{
    c.classList.toggle('hidden', cat !== 'all' && c.dataset.category !== cat);
  }});
}}
function toggleDetail(card, id) {{
  const wasActive = card.classList.contains('active');
  document.querySelectorAll('.project-card').forEach(c => c.classList.remove('active'));
  document.querySelectorAll('.detail-panel').forEach(p => p.classList.remove('visible'));
  const grid = document.getElementById('grid');
  if (!wasActive) {{
    card.classList.add('active');
    if (grid) grid.classList.add('panel-open');
    const panel = document.getElementById('detail-' + id);
    if (panel) {{ panel.classList.add('visible'); panel.scrollIntoView({{behavior:'smooth',block:'nearest'}}); }}
  }} else {{
    if (grid) grid.classList.remove('panel-open');
  }}
}}
function closeDetail() {{
  document.querySelectorAll('.project-card').forEach(c => c.classList.remove('active'));
  document.querySelectorAll('.detail-panel').forEach(p => p.classList.remove('visible'));
  const grid = document.getElementById('grid');
  if (grid) grid.classList.remove('panel-open');
}}
</script>
</body>
</html>'''