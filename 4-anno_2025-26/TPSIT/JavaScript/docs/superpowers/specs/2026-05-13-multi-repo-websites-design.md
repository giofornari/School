# Multi-Repo Websites — Design Spec
*2026-05-13 · Giordano Fornari*

## What We're Building

Four static portfolio sites, one per school repo, each auto-built and deployed to GitHub Pages on every commit. Every site shares the same design system and generator pattern but is deployed independently with its own CI pipeline.

**Repos:**
| Repo | Content type | Live output |
|------|-------------|-------------|
| JavaProjects | Java OOP exercises, labs, verifiche | Compiled + run on CI |
| GAppProjects | Google Apps Script projects | Source only |
| DIYJavaScript | DOM/vanilla JS exercises | JS eval in-browser (existing) |
| PythonAlmostSelfLearned | Python scripts | Run on CI, captured to `.txt` |

---

## Architecture

### Deployment

- Each repo gets its own `gh-pages` branch (or `docs/` folder) served by GitHub Pages
- Sites are independent — no shared CDN, no cross-repo dependencies at runtime
- Each site is a single `index.html` + optional `style.css` generated from repo contents

### Generator Pattern

Each repo has a `generate-site.py` (or equivalent) script that:
1. Scans the repo directory structure
2. Reads source files
3. Reads pre-captured output files (`.txt` from CI runs) where available
4. Emits a static `index.html` using the shared design token values (hardcoded, no external CSS deps)

Generator produces fully self-contained HTML — no external dependencies except Google Fonts (optional, graceful fallback stack included).

### CI Pipeline per Repo

**JavaProjects** (`auto-update-site.yml`):
1. Compile all `.java` files with `javac`
2. Run each `main()`, capture stdout to `docs/{ProjectName}.txt`
3. Run `generate-site.py`
4. Commit updated `docs/` + deploy to GitHub Pages

**PythonAlmostSelfLearned**:
1. Run each `.py` script with `python3`, capture stdout to `docs/{script}.txt`
2. Run `generate-site.py`
3. Deploy

**GAppProjects**:
1. No compilation — source only
2. Run `generate-site.py` (reads `.gs`/`.js` files)
3. Deploy

**DIYJavaScript** (existing, update):
1. Run `generate_index.py` (existing pattern)
2. Deploy (existing `deploy-pages.yml`)

---

## Design System

### Palette — Charcoal

```css
--bg:          #141414;   /* page background */
--surface:     #1d1d1d;   /* card background */
--surface-hi:  #252525;   /* active/hover state */
--border:      #2c2c2c;   /* dividers */
--border-hi:   #3c3c3c;   /* active borders */
--text-1:      #ededed;   /* primary content — 14.8:1 */
--text-2:      #a5a5a5;   /* secondary / descriptions — 7.1:1 */
--text-3:      #717171;   /* muted / labels — 4.1:1 */
--text-4:      #565656;   /* decorative only — 2.8:1 */
--green:       #22c55e;   /* live output accent */
--green-dim:   rgba(34,197,94,0.07);
--green-border:rgba(34,197,94,0.20);
--blue:        #60a5fa;   /* language/category badge */
--blue-dim:    rgba(96,165,250,0.08);
--blue-border: rgba(96,165,250,0.22);
```

### Typography

- Body: `Inter` (400/500/600/700/800), fallback: `-apple-system, BlinkMacSystemFont, Segoe UI, Roboto`
- Mono: `JetBrains Mono`, fallback: `Fira Code, monospace`
- Base: 14px / 1.5 line-height
- `-webkit-font-smoothing: antialiased`

---

## Layout — Page Structure

```
┌─ NAV (50px sticky) ────────────────────────────────────┐
│  [nav links: Java | JavaScript | Python | GApps]        │
├─ HERO ──────────────────────────────────────────────────┤
│  eyebrow: • School projects · Name                      │
│  title: 64px/800w/−2.5px tracking                      │
│  desc: 14px/1.75lh max-width 440px                      │
│  meta: N projects  N with output                        │
├─ CONTENT (0 56px padding) ──────────────────────────────┤
│  FILTER ROW: [All N] [Cat A N] [Cat B N]  • N with output│
│  ┌──────────────────────────────────────────────────┐   │
│  │ PROJECTS GRID (3 col, 1px gap, border-radius 8px)│   │
│  │ [card] [card] [card]                             │   │
│  │ [card] [card] [card]                             │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │ DETAIL PANEL (visible when card active)          │   │
│  │ header: filename  [close ✕]                      │   │
│  │ ┌────────────────┬─────────────────────────────┐ │   │
│  │ │ SOURCE pane    │ OUTPUT pane                 │ │   │
│  │ │ <pre> syntax   │ <div class=output-block>    │ │   │
│  │ └────────────────┴─────────────────────────────┘ │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Card States

- **Default**: `background: --bg`
- **Hover**: `background: --surface`
- **Active** (detail open): `background: --surface-hi; border-top: 2px solid --border-hi; padding-top: 20px`
- Grid gains `.panel-open` class → `border-radius: 8px 8px 0 0; border-bottom: transparent` (seamless join to panel)

### Card Content

```
project-name    (13px/600w, --text-1)
project-path    (10px mono, --text-3)
output-pill     (if has output: ▶ truncated output, green)
source-link     (if no output: ⟶ view source, --text-3)
expand-icon ⌄   (absolute top-right, rotates 180° when active)
```

### Detail Panel

- Header: `• filename.ext` (green dot indicator) + `close ✕`
- Body: 50/50 split — SOURCE left, OUTPUT right
- Source: syntax-highlighted `<pre>` with `.kw`/`.cl`/`.cm`/`.str` spans
- Output: `<div class="output-block">` — mono, green on `#101d14` bg, `white-space: pre-wrap`

---

## File Interaction

**Always available:**
- View source in detail panel (syntax highlighted)
- Expand/collapse per project card

**When output exists (CI captured):**
- Output pill on card (truncated preview)
- Full output in detail panel right pane

**No output (source-only):**
- "⟶ view source" link in card footer
- Detail panel shows source pane only (output pane hidden)

---

## Nav — Cross-Site Links

The nav links point to the live GitHub Pages URLs of the other 3 repos. Active link = current site. These are hardcoded per-site in the generator.

| Site | Nav label |
|------|-----------|
| JavaProjects | Java |
| DIYJavaScript | JavaScript |
| PythonAlmostSelfLearned | Python |
| GAppProjects | GApps |

---

## Generator — Data Model

Each project entry fed to the template:

```python
{
  "name": "Cerchio",
  "path": "Esercizi/Cerchio/",
  "category": "Esercizi",        # derived from directory name
  "source_file": "Cerchio.java", # primary source file
  "source_content": "...",       # raw source text
  "output": "Area = 78.54\n...", # from .txt file, None if absent
  "has_output": True
}
```

Categories derived from top-level directory names in each repo. Filter tabs generated dynamically from distinct categories.

---

## Error Handling

- Compilation fails: card shows no output pill, source still displayed
- Source file missing: card still shown with name + path, no expand
- Output file empty: treated as no-output (source-only)
- Generator crash: CI step fails, previous `index.html` remains on Pages (no regression)

---

## Out of Scope

- Search across projects
- Authentication / private repos
- Dark/light mode toggle
- Mobile-specific layout (responsive via natural content flow, not custom mobile layout)
- Comments, social features
