# Multi-Repo Websites Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Four static portfolio sites (one per school repo) that auto-build and deploy to GitHub Pages on every commit, sharing a Charcoal design system.

**Architecture:** Each repo gets a `generate-site.py` script + GitHub Actions workflow. The generator scans the repo, reads source files + pre-captured output `.txt` files, and emits a fully self-contained `docs/index.html`. All four sites link to each other via a shared nav. No shared runtime dependencies — each site is independent.

**Tech Stack:** Python 3.x (generator), GitHub Actions (CI), GitHub Pages (hosting), inline CSS (no build step), Google Fonts (optional, graceful fallback).

**Repos and local paths:**
| Repo | Local path | GitHub Pages URL |
|------|-----------|-----------------|
| DIYJavaScript | `/home/giordi/Repos/DIYJavaScript/` | `https://bigbrodyg.github.io/DIYJavaScript/` |
| JavaProjects | `/home/giordi/Repos/JavaProjects/` | `https://bigbrodyg.github.io/JavaProjects/` |
| PythonAlmostSelfLearned | `/home/giordi/Repos/1_School/PythonAlmostSelfLearned/` | `https://bigbrodyg.github.io/PythonAlmostSelfLearned/` |
| GAppProjects | `/home/giordi/Repos/1_School/GAppProjects/` | `https://bigbrodyg.github.io/GAppProjects/` |

**Note on GAppProjects:** The repo contains Flutter/Dart projects (not Google Apps Script despite the name). Generator scans `.dart` and `.js` files. Source-only display (no CI execution).

---

## File Structure

```
DIYJavaScript/
  generate_index.py                    REPLACE — rewrite with Charcoal template

JavaProjects/
  .github/scripts/generate-site.py    REPLACE — rewrite with Charcoal template
  .github/workflows/auto-update-site.yml  KEEP — already compiles Java + calls generator

1_School/PythonAlmostSelfLearned/
  .github/scripts/generate-site.py    CREATE
  .github/workflows/auto-update-site.yml  CREATE
  docs/                                CREATE dir

1_School/GAppProjects/
  .github/scripts/generate-site.py    CREATE
  .github/workflows/auto-update-site.yml  CREATE
  docs/                                CREATE dir
```

---

## Task 1: Write shared HTML template function

This is the core of the whole plan. All four generators use this same `render_page()` function — copy it verbatim into each `generate-site.py`.

**Files:**
- Reference: `/home/giordi/Repos/DIYJavaScript/docs/superpowers/specs/shared_template_reference.py` (not deployed — local reference only)

- [ ] **Step 1: Create the reference template file**

```python
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
    # Comments (// and /* */) — must run first to avoid mangling keyword spans inside comments
    escaped = re.sub(r'(//[^\n]*)', r'<span class="cm">\1</span>', escaped)
    escaped = re.sub(r'(/\*.*?\*/)', r'<span class="cm">\1</span>', escaped, flags=re.DOTALL)
    # String literals
    escaped = re.sub(r'(&quot;[^&]*?&quot;)', r'<span class="str">\1</span>', escaped)
    # Class names (CapitalCase words not already wrapped)
    escaped = re.sub(r'\b([A-Z][a-zA-Z0-9]+)\b(?![^<]*>)', r'<span class="cl">\1</span>', escaped)
    # Keywords
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
    onclick = f"toggleDetail(this,'{slug}')"

    if project['has_output']:
        output_preview = project['output'][:60].replace('\n', ' ').strip()
        footer = f'<span class="output-pill">{html_lib.escape(output_preview)}</span>'
    else:
        footer = '<a class="source-link" href="#">⟶ view source</a>'

    return f'''
    <div class="project-card {active}" onclick="{onclick}">
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

    nav_items = '\n'.join(
        f'    <li><a href="{url}"{"class=\"active\"" if label == active_nav else ""}>{label}</a></li>'
        for label, url in NAV_LINKS
    )

    tab_all = f'<div class="tab active" onclick="setTab(this,\'all\')">All <span class="tab-count">{len(projects)}</span></div>'
    tab_cats = '\n'.join(
        f'<div class="tab" onclick="setTab(this,\'{html_lib.escape(cat)}\')">{html_lib.escape(cat)} <span class="tab-count">{sum(1 for p in projects if p["category"]==cat)}</span></div>'
        for cat in categories
    )

    cards = '\n'.join(render_card(p, i) for i, p in enumerate(projects))
    detail_panels = '\n'.join(render_detail_panel(p, i, highlighter) for i, p in enumerate(projects))

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
  <div class="projects{'panel-open' if projects else ''}" id="grid">
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
```

- [ ] **Step 2: Save the file**

```bash
# file already written in step 1 — verify it exists
python3 -c "import ast; ast.parse(open('docs/superpowers/specs/shared_template_reference.py').read()); print('syntax OK')"
```

Expected: `syntax OK`

- [ ] **Step 3: Commit**

```bash
cd /home/giordi/Repos/DIYJavaScript
git add docs/superpowers/specs/shared_template_reference.py
git commit -m "docs: add shared HTML template reference for all repo sites"
```

---

## Task 2: Rewrite DIYJavaScript generator

Replace the existing `generate_index.py` with a new version that uses the Charcoal design. The new generator scans for HTML/JS/Python project directories (same as before) but emits the new template.

**Files:**
- Replace: `/home/giordi/Repos/DIYJavaScript/generate_index.py`

- [ ] **Step 1: Write the new generator**

```python
#!/usr/bin/env python3
"""Generate index.html for DIYJavaScript using the Charcoal design system."""

import os
import re
import html as html_lib
from pathlib import Path
from datetime import datetime

# ── COPY THESE FROM shared_template_reference.py ──────────────────────────────
NAV_LINKS = [
    ("Java",       "https://bigbrodyg.github.io/JavaProjects/"),
    ("JavaScript", "https://bigbrodyg.github.io/DIYJavaScript/"),
    ("Python",     "https://bigbrodyg.github.io/PythonAlmostSelfLearned/"),
    ("GApps",      "https://bigbrodyg.github.io/GAppProjects/"),
]

def slugify(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

def highlight_js(code):
    KEYWORDS = {
        'const','let','var','function','return','if','else','for','while','class',
        'new','import','export','default','extends','static','async','await',
        'true','false','null','undefined','this','super','try','catch','throw',
        'typeof','instanceof','in','of','from','document','window','console'
    }
    escaped = html_lib.escape(code)
    escaped = re.sub(r'(//[^\n]*)', r'<span class="cm">\1</span>', escaped)
    escaped = re.sub(r'(&quot;[^&]*?&quot;|&#x27;[^&]*?&#x27;|`[^`]*`)', r'<span class="str">\1</span>', escaped)
    escaped = re.sub(r'\b([A-Z][a-zA-Z0-9]+)\b(?![^<]*>)', r'<span class="cl">\1</span>', escaped)
    for kw in KEYWORDS:
        escaped = re.sub(rf'\b({re.escape(kw)})\b(?![^<]*>)', r'<span class="kw">\1</span>', escaped)
    return escaped

# ── SCANNING ──────────────────────────────────────────────────────────────────

IGNORED_DIRS = {'.git','__pycache__','node_modules','.vscode','venv','dist','build','sdfiles','.superpowers','docs','functons'}
SOURCE_EXTENSIONS = {'.js', '.html', '.py'}

def find_projects(base: Path) -> list:
    """Each top-level directory with at least one source file is a project."""
    projects = []
    for item in sorted(base.iterdir()):
        if not item.is_dir() or item.name in IGNORED_DIRS or item.name.startswith('.'):
            continue
        source_files = list(item.rglob('*.js')) + list(item.rglob('*.html')) + list(item.rglob('*.py'))
        if not source_files:
            continue
        # Primary source: prefer .js > .html > .py
        primary = next((f for f in source_files if f.suffix == '.js'), None) \
               or next((f for f in source_files if f.suffix == '.html'), None) \
               or source_files[0]
        try:
            source_content = primary.read_text(encoding='utf-8', errors='replace')
        except Exception:
            source_content = ''
        # Category: first segment of path relative to base
        rel = item.relative_to(base)
        category = rel.parts[0] if rel.parts else 'Other'
        projects.append({
            'name': item.name,
            'path': str(rel) + '/',
            'category': category,
            'source_file': primary.name,
            'source_content': source_content,
            'output': None,
            'has_output': False,
        })
    return projects

# ── PASTE render_card, render_detail_panel, render_page FROM shared_template_reference.py ──

def render_card(project, index):
    slug = slugify(project['name'])
    active = 'active' if index == 0 else ''
    cat = html_lib.escape(project['category'])
    if project['has_output']:
        preview = project['output'][:60].replace('\n',' ').strip()
        footer = f'<span class="output-pill">{html_lib.escape(preview)}</span>'
    else:
        footer = '<a class="source-link" href="#">⟶ view source</a>'
    return f'''
    <div class="project-card {active}" data-category="{cat}" onclick="toggleDetail(this,\'{slug}\')">
      <span class="expand-icon">⌄</span>
      <div class="project-name">{html_lib.escape(project["name"])}</div>
      <div class="project-path">{html_lib.escape(project["path"])}</div>
      {footer}
    </div>'''

def render_detail_panel(project, index, highlighter):
    slug = slugify(project['name'])
    visible = 'visible' if index == 0 else ''
    highlighted = highlighter(project['source_content'])
    if project['has_output']:
        output_pane = f'<div class="pane"><div class="pane-label">Output</div><div class="output-block">{html_lib.escape(project["output"])}</div></div>'
        grid_cols = 'grid-template-columns:1fr 1fr'
    else:
        output_pane = ''
        grid_cols = 'grid-template-columns:1fr'
    return f'''
  <div class="detail-panel {visible}" id="detail-{slug}">
    <div class="detail-header">
      <span class="detail-filename">{html_lib.escape(project["source_file"])}</span>
      <span class="detail-close" onclick="closeDetail()">close ✕</span>
    </div>
    <div class="detail-body" style="{grid_cols}">
      <div class="pane"><div class="pane-label">Source</div><pre>{highlighted}</pre></div>
      {output_pane}
    </div>
  </div>'''

def render_page(repo_title, repo_desc, active_nav, projects, highlighter):
    categories = sorted({p['category'] for p in projects})
    has_output_count = sum(1 for p in projects if p['has_output'])
    nav_items = '\n'.join(
        f'    <li><a href="{url}"{"class=\"active\"" if label == active_nav else ""}>{label}</a></li>'
        for label, url in NAV_LINKS
    )
    tab_all = f'<div class="tab active" onclick="setTab(this,\'all\')">All <span class="tab-count">{len(projects)}</span></div>'
    tab_cats = '\n'.join(
        f'<div class="tab" onclick="setTab(this,\'{html_lib.escape(cat)}\')">{html_lib.escape(cat)} <span class="tab-count">{sum(1 for p in projects if p["category"]==cat)}</span></div>'
        for cat in categories
    )
    cards = '\n'.join(render_card(p, i) for i, p in enumerate(projects))
    panels = '\n'.join(render_detail_panel(p, i, highlighter) for i, p in enumerate(projects))
    panel_open_class = 'panel-open' if projects else ''
    # [PASTE THE CSS AND FULL HTML TEMPLATE FROM shared_template_reference.py render_page() HERE]
    # Replace the return f'''...''' block with the one from shared_template_reference.py,
    # substituting the variables above.
    pass  # remove this line after pasting

# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    base = Path(__file__).parent
    projects = find_projects(base)
    html = render_page(
        repo_title='DIYJavaScript',
        repo_desc='DOM manipulation, vanilla JS exercises, and browser experiments.',
        active_nav='JavaScript',
        projects=projects,
        highlighter=highlight_js,
    )
    out = base / 'docs' / 'index.html'
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding='utf-8')
    print(f'Generated {out} ({len(projects)} projects)')
```

**Note:** The `render_page()` body (the large CSS + HTML string) must be copied from `shared_template_reference.py`. Remove the `pass` placeholder.

- [ ] **Step 2: Run the generator locally and verify**

```bash
cd /home/giordi/Repos/DIYJavaScript
python3 generate_index.py
```

Expected output: `Generated docs/index.html (N projects)` where N > 0.

```bash
wc -l docs/index.html   # should be > 100 lines
grep -c 'project-card' docs/index.html  # should equal N
```

- [ ] **Step 3: Open and visually verify**

```bash
xdg-open docs/index.html
# OR: python3 -m http.server 8080 --directory docs/ then open http://localhost:8080
```

Check: nav shows 4 links, hero title is "DIYJavaScript", cards show project names, clicking a card expands source pane.

- [ ] **Step 4: Commit**

```bash
cd /home/giordi/Repos/DIYJavaScript
git add generate_index.py docs/index.html
git commit -m "feat: rewrite generator with Charcoal design system"
```

---

## Task 3: Rewrite JavaProjects generator

Replace `/home/giordi/Repos/JavaProjects/.github/scripts/generate-site.py` with a clean version using the Charcoal design. The CI workflow (`auto-update-site.yml`) already compiles Java and captures output to `docs/{name}-output.txt` — the generator just reads those files.

**Files:**
- Replace: `/home/giordi/Repos/JavaProjects/.github/scripts/generate-site.py`

- [ ] **Step 1: Understand the existing output file naming convention**

```bash
ls /home/giordi/Repos/JavaProjects/docs/*.txt 2>/dev/null | head -10
# Output files are named like: cerchio-output.txt, convertitorexml-output.txt
# Project dirs are: Cerchio/, ConvertitoreXML/, Laboratorio/Esercizio1/, etc.
```

- [ ] **Step 2: Write the new generator**

```python
#!/usr/bin/env python3
"""Generate index.html for JavaProjects using the Charcoal design system.
Run by CI after javac compilation. Reads docs/{project}-output.txt files.
"""

import os
import re
import html as html_lib
from pathlib import Path

NAV_LINKS = [
    ("Java",       "https://bigbrodyg.github.io/JavaProjects/"),
    ("JavaScript", "https://bigbrodyg.github.io/DIYJavaScript/"),
    ("Python",     "https://bigbrodyg.github.io/PythonAlmostSelfLearned/"),
    ("GApps",      "https://bigbrodyg.github.io/GAppProjects/"),
]

IGNORED_DIRS = {'.git','docs','.github','bin','build','.vscode'}
JAVA_CATEGORIES = {'Esercizi', 'Laboratorio', 'Verifiche'}

def slugify(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

def highlight_java(code):
    KEYWORDS = {
        'public','private','protected','static','void','class','interface',
        'extends','implements','new','return','if','else','for','while',
        'do','switch','case','break','continue','try','catch','finally',
        'throw','throws','import','package','final','abstract','boolean',
        'int','double','float','long','char','byte','short','String',
        'true','false','null','this','super','instanceof'
    }
    escaped = html_lib.escape(code)
    escaped = re.sub(r'(//[^\n]*)', r'<span class="cm">\1</span>', escaped)
    escaped = re.sub(r'(/\*.*?\*/)', r'<span class="cm">\1</span>', escaped, flags=re.DOTALL)
    escaped = re.sub(r'(&quot;[^&]*?&quot;)', r'<span class="str">\1</span>', escaped)
    escaped = re.sub(r'\b([A-Z][a-zA-Z0-9]+)\b(?![^<]*>)', r'<span class="cl">\1</span>', escaped)
    for kw in KEYWORDS:
        escaped = re.sub(rf'\b({re.escape(kw)})\b(?![^<]*>)', r'<span class="kw">\1</span>', escaped)
    return escaped

def find_projects(base: Path) -> list:
    """Scan Java project dirs. Category from first parent dir matching JAVA_CATEGORIES."""
    docs_dir = base / 'docs'
    projects = []

    def scan_dir(dir_path: Path, category: str):
        # Find Java files in src/ subdirectory
        src = dir_path / 'src'
        if not src.exists():
            return
        java_files = sorted(src.glob('*.java'))
        if not java_files:
            return
        name = dir_path.name
        slug = slugify(name)
        # Read primary source (first .java file, prefer one matching dir name)
        primary = next((f for f in java_files if f.stem.lower() == name.lower()), java_files[0])
        try:
            source_content = primary.read_text(encoding='utf-8', errors='replace')
        except Exception:
            source_content = ''
        # Read output if captured by CI
        output_file = docs_dir / f'{slug}-output.txt'
        if not output_file.exists():
            output_file = docs_dir / f'{name.lower()}-output.txt'
        output = None
        has_output = False
        if output_file.exists():
            raw = output_file.read_text(encoding='utf-8', errors='replace').strip()
            if raw and 'No main method' not in raw and 'error:' not in raw.lower()[:50]:
                output = raw
                has_output = True
        rel_path = dir_path.relative_to(base)
        projects.append({
            'name': name,
            'path': str(rel_path) + '/',
            'category': category,
            'source_file': primary.name,
            'source_content': source_content,
            'output': output,
            'has_output': has_output,
        })

    # Scan top-level dirs and categorized subdirs
    for item in sorted(base.iterdir()):
        if not item.is_dir() or item.name in IGNORED_DIRS or item.name.startswith('.'):
            continue
        if item.name in JAVA_CATEGORIES:
            for sub in sorted(item.iterdir()):
                if sub.is_dir():
                    scan_dir(sub, item.name)
        else:
            # Top-level project (old structure)
            scan_dir(item, 'Progetti')

    return projects

# [PASTE render_card, render_detail_panel, render_page FROM shared_template_reference.py]

if __name__ == '__main__':
    base = Path(__file__).parent.parent.parent  # repo root (scripts/ is 2 levels deep)
    projects = find_projects(base)
    html = render_page(
        repo_title='JavaProjects',
        repo_desc='Object-oriented exercises, lab assignments, and verifiche. Compiled and run on every commit.',
        active_nav='Java',
        projects=projects,
        highlighter=highlight_java,
    )
    out = base / 'docs' / 'index.html'
    out.write_text(html, encoding='utf-8')
    print(f'Generated {out} ({len(projects)} projects, {sum(1 for p in projects if p["has_output"])} with output)')
```

- [ ] **Step 3: Run locally and verify**

```bash
cd /home/giordi/Repos/JavaProjects
python3 .github/scripts/generate-site.py
```

Expected: `Generated .../docs/index.html (N projects, M with output)`

```bash
grep -c 'project-card' docs/index.html
xdg-open docs/index.html
```

Check: cards show Java project names, output pills on projects with `docs/*-output.txt` files, source pane shows Java code with syntax highlighting.

- [ ] **Step 4: Commit**

```bash
cd /home/giordi/Repos/JavaProjects
git add .github/scripts/generate-site.py docs/index.html
git commit -m "feat: rewrite generator with Charcoal design system"
```

---

## Task 4: PythonAlmostSelfLearned — generator + CI

Repo at `/home/giordi/Repos/1_School/PythonAlmostSelfLearned/`. Structure: `Year3/` and `Year4/` directories with `.py` scripts. CI will run each script and capture stdout.

**Files:**
- Create: `/home/giordi/Repos/1_School/PythonAlmostSelfLearned/.github/scripts/generate-site.py`
- Create: `/home/giordi/Repos/1_School/PythonAlmostSelfLearned/.github/workflows/auto-update-site.yml`
- Create: `/home/giordi/Repos/1_School/PythonAlmostSelfLearned/docs/` (dir)

- [ ] **Step 1: Create the generator**

```python
#!/usr/bin/env python3
"""Generate index.html for PythonAlmostSelfLearned."""

import os
import re
import html as html_lib
from pathlib import Path

NAV_LINKS = [
    ("Java",       "https://bigbrodyg.github.io/JavaProjects/"),
    ("JavaScript", "https://bigbrodyg.github.io/DIYJavaScript/"),
    ("Python",     "https://bigbrodyg.github.io/PythonAlmostSelfLearned/"),
    ("GApps",      "https://bigbrodyg.github.io/GAppProjects/"),
]

IGNORED_DIRS = {'.git','docs','.github','__pycache__','venv','.venv','node_modules'}
IGNORED_FILES = {'utils.md', 'README.md', 'CLAUDE.md'}

def slugify(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

def highlight_python(code):
    KEYWORDS = {
        'def','class','import','from','return','if','elif','else','for','while',
        'in','not','and','or','True','False','None','with','as','try','except',
        'raise','finally','pass','break','continue','lambda','yield','global',
        'nonlocal','del','assert','is','print','len','range','int','str',
        'float','list','dict','set','tuple','open','type'
    }
    escaped = html_lib.escape(code)
    escaped = re.sub(r'(#[^\n]*)', r'<span class="cm">\1</span>', escaped)
    escaped = re.sub(r'(&quot;[^&]*?&quot;|&#x27;[^&]*?&#x27;)', r'<span class="str">\1</span>', escaped)
    escaped = re.sub(r'\b([A-Z][a-zA-Z0-9]+)\b(?![^<]*>)', r'<span class="cl">\1</span>', escaped)
    for kw in KEYWORDS:
        escaped = re.sub(rf'\b({re.escape(kw)})\b(?![^<]*>)', r'<span class="kw">\1</span>', escaped)
    return escaped

def find_projects(base: Path) -> list:
    """Scan Year3/ and Year4/ for .py scripts. Category = year dir name."""
    docs_dir = base / 'docs'
    projects = []
    for year_dir in sorted(base.iterdir()):
        if not year_dir.is_dir() or year_dir.name in IGNORED_DIRS or year_dir.name.startswith('.'):
            continue
        category = year_dir.name  # Year3, Year4
        # Collect .py files (flat and in subdirs)
        for py_file in sorted(year_dir.rglob('*.py')):
            if py_file.name.startswith('_'):
                continue
            try:
                source_content = py_file.read_text(encoding='utf-8', errors='replace')
            except Exception:
                source_content = ''
            name = py_file.stem
            rel_path = py_file.parent.relative_to(base)
            slug = slugify(str(py_file.relative_to(base)).replace('/', '-').replace('.py', ''))
            # Check for captured output
            output_file = docs_dir / f'{slug}-output.txt'
            output = None
            has_output = False
            if output_file.exists():
                raw = output_file.read_text(encoding='utf-8', errors='replace').strip()
                if raw and not raw.lower().startswith('error'):
                    output = raw
                    has_output = True
            projects.append({
                'name': name,
                'path': str(rel_path) + '/',
                'category': category,
                'source_file': py_file.name,
                'source_content': source_content,
                'output': output,
                'has_output': has_output,
            })
    return projects

# [PASTE render_card, render_detail_panel, render_page FROM shared_template_reference.py]

if __name__ == '__main__':
    base = Path(__file__).parent.parent.parent
    projects = find_projects(base)
    html = render_page(
        repo_title='Python',
        repo_desc='Python scripts from Year 3 and Year 4. Scripts, Codewars katas, and data projects.',
        active_nav='Python',
        projects=projects,
        highlighter=highlight_python,
    )
    out = base / 'docs' / 'index.html'
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding='utf-8')
    print(f'Generated {out} ({len(projects)} projects)')
```

- [ ] **Step 2: Create the CI workflow**

```yaml
# /home/giordi/Repos/1_School/PythonAlmostSelfLearned/.github/workflows/auto-update-site.yml
name: Auto-Update Python Showcase

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: write
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Create docs dir
        run: mkdir -p docs

      - name: Run Python scripts and capture output
        run: |
          find Year3 Year4 -name "*.py" ! -name "_*" | while read script; do
            slug=$(echo "$script" | sed 's|/|-|g' | sed 's|\.py$||')
            echo "Running $script -> docs/${slug}-output.txt"
            timeout 10 python3 "$script" > "docs/${slug}-output.txt" 2>&1 || true
            # Blank output = treat as no output (remove file)
            [ -s "docs/${slug}-output.txt" ] || rm -f "docs/${slug}-output.txt"
          done

      - name: Generate site
        run: python3 .github/scripts/generate-site.py

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: docs

  deploy:
    if: github.ref == 'refs/heads/main'
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build-and-deploy
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 3: Run generator locally and verify**

```bash
cd /home/giordi/Repos/1_School/PythonAlmostSelfLearned
mkdir -p .github/scripts .github/workflows docs
# (files written in steps 1 and 2)
python3 .github/scripts/generate-site.py
```

Expected: `Generated .../docs/index.html (N projects)`

```bash
grep -c 'project-card' docs/index.html  # should be > 0
xdg-open docs/index.html
```

Check: Year3 and Year4 filter tabs appear, scripts listed with Python source in detail pane.

- [ ] **Step 4: Enable GitHub Pages on the repo**

Go to: https://github.com/bigBrodyG/PythonAlmostSelfLearned/settings/pages

Set source to: **GitHub Actions**

- [ ] **Step 5: Commit and push**

```bash
cd /home/giordi/Repos/1_School/PythonAlmostSelfLearned
git add .github/scripts/generate-site.py .github/workflows/auto-update-site.yml docs/index.html
git commit -m "feat: add Charcoal site generator and GitHub Pages CI"
git push
```

Expected: GitHub Actions runs, site deploys to `https://bigbrodyg.github.io/PythonAlmostSelfLearned/`.

---

## Task 5: GAppProjects — generator + CI (source-only)

Repo at `/home/giordi/Repos/1_School/GAppProjects/`. Contains Flutter/Dart projects. Source-only display — no CI execution (Flutter apps don't produce simple stdout output). Generator scans `.dart` files.

**Files:**
- Create: `/home/giordi/Repos/1_School/GAppProjects/.github/scripts/generate-site.py`
- Create: `/home/giordi/Repos/1_School/GAppProjects/.github/workflows/auto-update-site.yml`
- Create: `/home/giordi/Repos/1_School/GAppProjects/docs/` (dir)

- [ ] **Step 1: Create the generator**

```python
#!/usr/bin/env python3
"""Generate index.html for GAppProjects (Flutter/Dart projects). Source-only."""

import os
import re
import html as html_lib
from pathlib import Path

NAV_LINKS = [
    ("Java",       "https://bigbrodyg.github.io/JavaProjects/"),
    ("JavaScript", "https://bigbrodyg.github.io/DIYJavaScript/"),
    ("Python",     "https://bigbrodyg.github.io/PythonAlmostSelfLearned/"),
    ("GApps",      "https://bigbrodyg.github.io/GAppProjects/"),
]

IGNORED_DIRS = {'.git','docs','.github','.remember','TestFolder','build','.dart_tool','.pub-cache'}

def slugify(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

def highlight_dart(code):
    KEYWORDS = {
        'class','void','var','final','const','static','return','if','else','for',
        'while','new','import','export','extends','implements','abstract',
        'String','int','double','bool','List','Map','Set','Future','Stream',
        'async','await','true','false','null','this','super','try','catch',
        'throw','rethrow','in','is','as','late','required','dynamic',
        'Widget','BuildContext','override'
    }
    escaped = html_lib.escape(code)
    escaped = re.sub(r'(//[^\n]*)', r'<span class="cm">\1</span>', escaped)
    escaped = re.sub(r'(&quot;[^&]*?&quot;|&#x27;[^&]*?&#x27;)', r'<span class="str">\1</span>', escaped)
    escaped = re.sub(r'\b([A-Z][a-zA-Z0-9]+)\b(?![^<]*>)', r'<span class="cl">\1</span>', escaped)
    for kw in KEYWORDS:
        escaped = re.sub(rf'\b({re.escape(kw)})\b(?![^<]*>)', r'<span class="kw">\1</span>', escaped)
    return escaped

def find_projects(base: Path) -> list:
    """Each top-level dir with .dart files is a project. Category = parent dir name."""
    projects = []
    for top_dir in sorted(base.iterdir()):
        if not top_dir.is_dir() or top_dir.name in IGNORED_DIRS or top_dir.name.startswith('.'):
            continue
        category = top_dir.name  # Flutter, Dart, etc.
        for proj_dir in sorted(top_dir.iterdir()):
            if not proj_dir.is_dir() or proj_dir.name.startswith('.'):
                continue
            dart_files = list(proj_dir.rglob('*.dart'))
            if not dart_files:
                continue
            # Prefer lib/main.dart as primary source
            primary = next((f for f in dart_files if f.name == 'main.dart'), dart_files[0])
            try:
                source_content = primary.read_text(encoding='utf-8', errors='replace')
            except Exception:
                source_content = ''
            rel_path = proj_dir.relative_to(base)
            projects.append({
                'name': proj_dir.name,
                'path': str(rel_path) + '/',
                'category': category,
                'source_file': primary.name,
                'source_content': source_content,
                'output': None,
                'has_output': False,
            })
    return projects

# [PASTE render_card, render_detail_panel, render_page FROM shared_template_reference.py]

if __name__ == '__main__':
    base = Path(__file__).parent.parent.parent
    projects = find_projects(base)
    html = render_page(
        repo_title='GAppProjects',
        repo_desc='Flutter and Dart school projects.',
        active_nav='GApps',
        projects=projects,
        highlighter=highlight_dart,
    )
    out = base / 'docs' / 'index.html'
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding='utf-8')
    print(f'Generated {out} ({len(projects)} projects)')
```

- [ ] **Step 2: Create the CI workflow**

```yaml
# /home/giordi/Repos/1_School/GAppProjects/.github/workflows/auto-update-site.yml
name: Auto-Update GApps Showcase

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: write
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - name: Generate site
        run: |
          mkdir -p docs
          python3 .github/scripts/generate-site.py
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: docs

  deploy:
    if: github.ref == 'refs/heads/main'
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build-and-deploy
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 3: Run generator locally and verify**

```bash
cd /home/giordi/Repos/1_School/GAppProjects
mkdir -p .github/scripts .github/workflows docs
python3 .github/scripts/generate-site.py
```

Expected: `Generated .../docs/index.html (N projects)` where N ≥ 1 (Flutter/Dart subdirs found).

```bash
xdg-open docs/index.html
```

Check: Flutter, Dart filter tabs, projects listed with source-link (no output pills since source-only).

- [ ] **Step 4: Enable GitHub Pages on the repo**

Go to: https://github.com/bigBrodyG/GAppProjects/settings/pages

Set source to: **GitHub Actions**

- [ ] **Step 5: Commit and push**

```bash
cd /home/giordi/Repos/1_School/GAppProjects
git add .github/scripts/generate-site.py .github/workflows/auto-update-site.yml docs/index.html
git commit -m "feat: add Charcoal site generator and GitHub Pages CI"
git push
```

---

## Task 6: Verify cross-site navigation

After all four sites are deployed, verify that the nav links work across sites.

- [ ] **Step 1: Confirm all four Pages deployments are live**

```
https://bigbrodyg.github.io/JavaProjects/
https://bigbrodyg.github.io/DIYJavaScript/
https://bigbrodyg.github.io/PythonAlmostSelfLearned/
https://bigbrodyg.github.io/GAppProjects/
```

Each should load with the Charcoal design, nav links present.

- [ ] **Step 2: Click each nav link from each site**

From JavaProjects → click JavaScript → should land on DIYJavaScript site.
From DIYJavaScript → click Python → should land on PythonAlmostSelfLearned.
From Python → click GApps → GAppProjects. From GApps → click Java → JavaProjects.

- [ ] **Step 3: Verify active nav highlights correctly on each site**

The current site's nav link should be styled `.active` (lighter background). The other three links should be muted (`--text-3` color).

- [ ] **Step 4: Trigger a push to JavaProjects and verify auto-rebuild**

```bash
cd /home/giordi/Repos/JavaProjects
echo "# test" >> README.md
git add README.md && git commit -m "test: trigger CI rebuild"
git push
```

Watch GitHub Actions: https://github.com/bigBrodyG/JavaProjects/actions

Expected: workflow runs, site updates within ~2 minutes.

---

## Self-Review Notes

**Spec coverage:**
- ✅ 4 repos with individual generators
- ✅ Shared Charcoal design system (same CSS in all 4)
- ✅ GitHub Actions CI per repo
- ✅ GitHub Pages deployment
- ✅ File interaction: view source always, output when available
- ✅ Filter tabs by category
- ✅ Cross-site nav links
- ✅ Auto-rebuild on push
- ✅ Error handling: empty/errored output files excluded, generator crash leaves previous index.html

**Known gaps:**
- DIYJavaScript has no output capture (JS exercises run in-browser, not on CI). All cards will be source-only unless the existing in-browser runner is wired in. This is acceptable per spec ("view source always").
- PythonAlmostSelfLearned scripts that require input (`input()`) will hang on CI — the `timeout 10` in the workflow handles this by killing them and producing partial/no output.
- The `render_page()` function body must be manually copy-pasted into Tasks 2-5 from the reference. This duplication is intentional since the repos cannot share Python modules at runtime.

## GSTACK REVIEW REPORT

| Review | Trigger | Why | Runs | Status | Findings |
|--------|---------|-----|------|--------|----------|
| CEO Review | `/plan-ceo-review` | Scope & strategy | 0 | — | — |
| Codex Review | `/codex review` | Independent 2nd opinion | 0 | — | — |
| Eng Review | `/plan-eng-review` | Architecture & tests (required) | 0 | — | — |
| Design Review | `/plan-design-review` | UI/UX gaps | 0 | — | — |
| DX Review | `/plan-devex-review` | Developer experience gaps | 0 | — | — |

**VERDICT:** NO REVIEWS YET
