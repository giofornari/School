#!/usr/bin/env python3
"""Rigenera le grafiche del README dalla history della repo.

uv run --with fonttools --with brotli python .github/readme/genera.py

Stile ripreso dal design system DCS Academy: fondale petrolio → verde con onde di luce,
Poppins, eyebrow maiuscoli, anello in tre segmenti, icone lineari su cerchio petrolio.
"""
import base64, collections, datetime as dt, io, math, os, random, subprocess
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools import subset

QUI = Path(__file__).resolve().parent
RADICE = QUI.parent.parent
OGGI = dt.date.today().isoformat()

# palette DCS Academy
PETROLIO, TURCHESE, VERDE, VERDE_SCURO = "#05343E", "#1BA79C", "#66C26B", "#137E6C"
NAVY, MENTA, SUPERFICIE, BIANCO = "#1B263A", "#97F3E9", "#E8F5EE", "#FFFFFF"
P70, P16, B75 = "#507178", "#D7DFE0", "#C0CCCF"
SCURO, MEDIO, CHIARO, LUCE = "#014554", "#0E6F67", "#1E9F7A", "#29B589"
ACQUA, VERDINO = "#2AE2CA", "#88EC8A"
SEG = ("#004A58", "#1CAC9E", "#64C26A")  # segmenti dell'anello

ANNI = [  # cartella, ordinale, periodo, titolo, colore
    ("3-anno_2024-25", "3ª", "2024–25", "Le fondamenta", SEG[0]),
    ("4-anno_2025-26", "4ª", "2025–26", "L’anno degli oggetti", SEG[1]),
    ("5-anno_2026-27", "5ª", "2026–27", "Reti e server", SEG[2]),
]

# ---------- font ----------
PESI = {900: "Poppins-Black", 700: "Poppins-Bold", 500: "Poppins-Medium", 400: "Poppins-Regular"}
CARATTERI = "".join(chr(c) for c in range(32, 127)) + "àèéìòùÀÈÉÌÒÙ’‘«»–—·•×→←ªº°…“”"
_ttf, _woff = {}, {}

def ttf(peso):
    if peso not in _ttf:
        _ttf[peso] = TTFont(QUI / "font" / f"{PESI[peso]}.ttf")
    return _ttf[peso]

def woff2(peso):
    if peso not in _woff:
        opt = subset.Options(); opt.flavor = "woff2"; opt.layout_features = ["kern", "liga"]
        f = TTFont(QUI / "font" / f"{PESI[peso]}.ttf")
        s = subset.Subsetter(opt); s.populate(text=CARATTERI); s.subset(f)
        buf = io.BytesIO(); f.flavor = "woff2"; f.save(buf)
        _woff[peso] = base64.b64encode(buf.getvalue()).decode()
    return _woff[peso]

def larghezza(testo, peso, corpo, spaziatura=0.0):
    f = ttf(peso); cmap = f.getBestCmap(); hmtx = f["hmtx"]; upm = f["head"].unitsPerEm
    w = sum(hmtx[cmap.get(ord(c), cmap[32])][0] for c in testo)
    return w * corpo / upm + spaziatura * corpo * len(testo)

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def testo(x, y, s, peso=400, corpo=16, colore=PETROLIO, anchor="start", spaziatura=0.0, extra=""):
    ls = f' letter-spacing="{spaziatura * corpo:.2f}"' if spaziatura else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="P{peso}" font-size="{corpo}" fill="{colore}"'
            f' text-anchor="{anchor}"{ls}{extra}>{esc(s)}</text>')

def svg(w, h, corpo, pesi, titolo):
    font = "".join(f"@font-face{{font-family:P{p};src:url(data:font/woff2;base64,{woff2(p)}) format('woff2')}}" for p in sorted(pesi))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
            f'<title>{esc(titolo)}</title><style>{font}</style>{corpo}</svg>')

def salva(nome, contenuto):
    (QUI / nome).write_text(contenuto, encoding="utf-8")
    print(f"{nome:<22} {len(contenuto) / 1024:6.1f} KB")

# ---------- fondale ----------
def gradiente(id_, angolo, fermate):
    a = math.radians(angolo - 90)  # angolo CSS → vettore SVG
    dx, dy = math.cos(a) / 2, math.sin(a) / 2
    stop = "".join(f'<stop offset="{o}%" stop-color="{c}"/>' for o, c in fermate)
    return (f'<linearGradient id="{id_}" x1="{.5 - dx:.3f}" y1="{.5 - dy:.3f}" x2="{.5 + dx:.3f}" y2="{.5 + dy:.3f}">{stop}</linearGradient>')

TESTATA = [(0, SCURO), (46, SCURO), (66, MEDIO), (86, CHIARO), (100, LUCE)]
COPERTINA = [(0, SCURO), (52, SCURO), (72, MEDIO), (90, CHIARO), (100, LUCE)]
RETRO = [(0, SCURO), (58, SCURO), (100, PETROLIO)]

def onde(w, h, seme, da=0.45, n=9, ampiezza=None):
    """Onde di luce disegnate: linee sottili e bagliori sfocati, sfumati verso la zona dei testi."""
    rnd = random.Random(seme); ampiezza = ampiezza or h * 0.18
    linee, bagliori = [], []
    for i in range(n):
        y0 = h * (0.25 + 0.6 * i / n) + rnd.uniform(-20, 20)
        f1, f2, fase = rnd.uniform(.6, 1.4), rnd.uniform(1.5, 3), rnd.uniform(0, 6.28)
        inclin = rnd.uniform(-.25, .12) * h
        pts = []
        for k in range(0, 101):
            t = k / 100; x = w * (da - .1) + t * w * (1.1 - da + .1)
            y = y0 + inclin * t + ampiezza * (.6 * math.sin(f1 * 3.1 * t + fase) + .25 * math.sin(f2 * 6.2 * t + fase * 2))
            pts.append(f"{x:.1f},{y:.1f}")
        d = "M" + " L".join(pts)
        linee.append(f'<path d="{d}" stroke="{BIANCO}" stroke-opacity="{rnd.uniform(.10, .32):.2f}" stroke-width="{rnd.uniform(.8, 2.2):.1f}" fill="none"/>')
        if i % 3 == 0:
            bagliori.append(f'<path d="{d}" stroke="{MENTA}" stroke-opacity=".16" stroke-width="{rnd.uniform(14, 34):.0f}" fill="none" stroke-linecap="round"/>')
    return (f'<defs><linearGradient id="mo{seme}" x1="0" x2="1" y1="0" y2="0"><stop offset="{da}" stop-color="#fff" stop-opacity="0"/>'
            f'<stop offset="{min(da + .28, 1)}" stop-color="#fff" stop-opacity="1"/></linearGradient>'
            f'<mask id="m{seme}"><rect width="{w}" height="{h}" fill="url(#mo{seme})"/></mask>'
            f'<filter id="b{seme}" x="-10%" y="-50%" width="120%" height="200%"><feGaussianBlur stdDeviation="14"/></filter></defs>'
            f'<g mask="url(#m{seme})"><g filter="url(#b{seme})">{"".join(bagliori)}</g>{"".join(linee)}</g>')

# ---------- icone ----------
def icona(nome, cx, cy, r):
    """Icone lineari acqua/verdino su cerchio petrolio, disegnate su griglia 64."""
    s = r / 32
    a = f'stroke="{ACQUA}" stroke-width="{2.4:.1f}" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    v = f'stroke="{VERDINO}" stroke-width="{2.4:.1f}" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    g = {
        "informatica": f'<path d="M23 22 L13 32 L23 42 M41 22 L51 32 L41 42" {a}/><path d="M36 18 L28 46" {v}/>',
        "sistemi": f'<path d="M32 21 L19 41 M32 21 L45 41 M19 43 L45 43" {v}/><circle cx="32" cy="18" r="5" {a}/><circle cx="17" cy="44" r="5" {a}/><circle cx="47" cy="44" r="5" {a}/>',
        "tpsit": f'<rect x="16" y="15" width="32" height="9" rx="2.5" {a}/><rect x="16" y="28" width="32" height="9" rx="2.5" {a}/><rect x="16" y="41" width="32" height="9" rx="2.5" {a}/><path d="M21 19.5h.1M21 32.5h.1M21 45.5h.1M26 19.5h.1M26 32.5h.1M26 45.5h.1" {v} stroke-width="3.2"/><path d="M36 19.5h7M36 32.5h7M36 45.5h7" {v}/>',
        "attacco-difesa": f'<path d="M32 12 L48 18 V31 C48 41 41 48 32 52 C23 48 16 41 16 31 V18 Z" {a}/><path d="M27 41 V23 M27 24 H39 L36 28.5 L39 33 H27" {v}/>',
        "pcto": f'<path d="M32 16 L54 26 L32 36 L10 26 Z" {a}/><path d="M19 30 V40 C19 44 26 47 32 47 C38 47 45 44 45 40 V30" {a}/><path d="M54 26 V38" {v}/><circle cx="54" cy="41" r="2.5" {v}/>',
        "estate": f'<circle cx="32" cy="32" r="9" {a}/><path d="M32 13v5M32 46v5M13 32h5M46 32h5M18.6 18.6l3.5 3.5M41.9 41.9l3.5 3.5M18.6 45.4l3.5-3.5M41.9 22.1l3.5-3.5" {v}/>',
        "laboratorio": f'<path d="M27 14 H37 M29 14 V27 L17 47 C16 49 17.5 51 20 51 H44 C46.5 51 48 49 47 47 L35 27 V14" {a}/><path d="M22 41 H42" {v}/><circle cx="29" cy="46" r="1.6" {v}/><circle cx="36" cy="44" r="1.2" {v}/>',
        "anno": "",
    }[nome]
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{PETROLIO}"/>'
            f'<g transform="translate({cx - r:.1f} {cy - r:.1f}) scale({s:.4f})">{g}</g>')

ICONE = ["informatica", "sistemi", "tpsit", "attacco-difesa", "pcto", "estate", "laboratorio"]

# ---------- dati ----------
def git(*a):
    return subprocess.run(["git", "-C", str(RADICE), *a], capture_output=True, text=True, check=True).stdout

def anno_scolastico(mese):  # "2025-10" → indice 0/1/2 (settembre–agosto)
    y, m = map(int, mese.split("-"))
    return max(0, min(2, (y if m >= 9 else y - 1) - 2024))

def dati():
    righe = git("log", "--format=%ad|%s", "--date=format:%Y-%m-%d").splitlines()
    # i commit che hanno assemblato School (merge, import, README) non sono lavoro scolastico
    commit = [r.split("|", 1)[0][:7] for r in righe if r[:10] < "2026-10-30"]
    mesi = collections.Counter(commit)
    primo, ultimo = min(mesi), max(max(mesi), dt.date.today().strftime("%Y-%m"))
    asse, (y, m) = [], map(int, primo.split("-"))
    while f"{y}-{m:02d}" <= ultimo:
        asse.append(f"{y}-{m:02d}"); m += 1
        if m > 12: y, m = y + 1, 1
    per_anno = [0, 0, 0]
    for k, n in mesi.items(): per_anno[anno_scolastico(k)] += n
    file = git("ls-files").splitlines()
    return dict(commit=len(commit), mesi=mesi, asse=asse, per_anno=per_anno, file=len(file),
                elenco=file, progetti=len({"/".join(f.split("/")[:3]) for f in file if f.count("/") >= 3}))

LINGUAGGI = {".java": "Java", ".py": "Python", ".c": "C", ".h": "C", ".js": "JavaScript", ".mjs": "JavaScript",
             ".cs": "C#", ".html": "HTML", ".css": "CSS", ".dart": "Dart", ".sh": "Shell", ".bat": "Batch"}
GENERATI = ("/ios/", "/android/", "/windows/", "/linux/", "/macos/", "/web/", "/docs/", "/node_modules/", "/build/", ".min.")

def righe_per_linguaggio(elenco):
    c = collections.Counter()
    for f in elenco:
        lang = LINGUAGGI.get(os.path.splitext(f)[1].lower())
        if not lang or any(g in "/" + f for g in GENERATI): continue
        try: c[lang] += sum(1 for r in open(RADICE / f, errors="ignore") if r.strip())
        except OSError: pass
    return c

# ---------- grafiche ----------
def hero(d):
    W, H = 1600, 620
    tot = sum(d["per_anno"]) or 1
    cx, cy, r, sp = 1262, 318, 150, 46
    circ = 2 * math.pi * r; gap = 10; ang = 0; seg = ""
    for i, n in enumerate(d["per_anno"]):
        l = max(circ * n / tot - gap, 2)
        seg += (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{SEG[i]}" stroke-width="{sp}"'
                f' stroke-dasharray="{l:.1f} {circ:.1f}" stroke-dashoffset="{-ang:.1f}" transform="rotate(-90 {cx} {cy})">'
                f'<animate attributeName="stroke-dasharray" from="0 {circ:.1f}" to="{l:.1f} {circ:.1f}" dur="1.2s" begin="{.25 + i * .35:.2f}s" fill="freeze" calcMode="spline" keySplines=".2 .7 .2 1"/></circle>')
        ang += circ * n / tot
    # etichette dei tre anni accanto all'anello, come i verbi accanto all'infografica DCS
    eti = ""
    for i, (_, o, per, _, _) in enumerate(ANNI):
        y = 196 + i * 92
        eti += (f'<rect x="1448" y="{y - 30}" width="6" height="44" rx="3" fill="{SEG[i] if i else MENTA}"/>'
                + testo(1468, y - 6, f"{o} · {per}", 700, 15, MENTA, spaziatura=.08)
                + testo(1468, y + 16, f"{d['per_anno'][i]} commit", 900, 22, BIANCO))
    corpo = (f'<defs>{gradiente("g", 104, COPERTINA)}<clipPath id="c"><rect width="{W}" height="{H}" rx="28"/></clipPath></defs>'
             f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="url(#g)"/>{onde(W, H, 7, da=.42, n=11)}'
             f'<circle cx="{cx}" cy="{cy}" r="{r + sp / 2 + 18}" fill="{SCURO}" fill-opacity=".35"/>{seg}'
             f'{icona("pcto", cx, cy, 92)}{eti}'
             + testo(96, 104, "GIOFORNARI / SCHOOL", 700, 18, BIANCO, spaziatura=.12)
             + f'<rect x="96" y="124" width="64" height="4" rx="2" fill="{VERDE}"/>'
             + testo(96, 228, "ITIS LEONARDO DA VINCI · PARMA · INFORMATICA", 700, 17, MENTA, spaziatura=.08)
             + testo(90, 372, "School", 900, 168, BIANCO, spaziatura=-.01)
             + testo(96, 436, "Tre anni di codice, una sola storia.", 900, 34, VERDE)
             + f'<text x="96" y="490" font-family="P900" font-size="24"><tspan fill="{BIANCO}">Terzo</tspan><tspan fill="{B75}"> · </tspan>'
               f'<tspan fill="{TURCHESE}">Quarto</tspan><tspan fill="{B75}"> · </tspan><tspan fill="{VERDE}">Quinto</tspan></text>'
             + testo(96, 560, f"{d['commit']} commit da 12 sorgenti, riordinati per anno e materia.", 500, 18, BIANCO)
             + "</g>")
    salva("hero.svg", svg(W, H, corpo, {900, 700, 500}, "School: tre anni di codice all’ITIS Leonardo da Vinci di Parma"))

def numeri(d):
    W, H = 1600, 260
    voci = [("COMMIT", f"{d['commit']}", "dal primo all’ultimo, history intatta"),
            ("SORGENTI", "12", "9 repository e 3 cartelle locali"),
            ("PROGETTI", f"{d['progetti']}", "cartelle di lavoro sotto le materie"),
            ("FILE", f"{d['file']:,}".replace(",", "."), "tutto quello che è stato consegnato")]
    col = W / 4; corpo = f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="28" fill="{BIANCO}" stroke="{P16}" stroke-width="2"/>'
    for i, (e, n, c) in enumerate(voci):
        x = 64 + i * col
        if i: corpo += f'<rect x="{i * col:.0f}" y="56" width="2" height="{H - 112}" fill="{P16}"/>'
        corpo += (f'<rect x="{x}" y="58" width="36" height="5" rx="2.5" fill="{SEG[min(i, 2)] if i < 3 else VERDE_SCURO}"/>'
                  + testo(x, 98, e, 700, 15, P70, spaziatura=.1)
                  + f'<text x="{x - 4}" y="178" font-family="P900" font-size="80" fill="{VERDE_SCURO}" opacity="0">{esc(n)}'
                    f'<animate attributeName="opacity" from="0" to="1" dur=".6s" begin="{.15 * i:.2f}s" fill="freeze"/></text>'
                  + testo(x, 214, c, 400, 17, P70))
    salva("numeri.svg", svg(W, H, corpo, {900, 700, 400}, "School in numeri"))

def percorso(d):
    W, H = 1600, 640; L, R, T, B = 96, 64, 190, 520
    asse, mesi = d["asse"], d["mesi"]; n = len(asse); passo = (W - L - R) / n; bw = passo * .62
    mx = max(mesi.values()); scala = (B - T) / (mx * 1.1)
    corpo = f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="28" fill="{BIANCO}" stroke="{P16}" stroke-width="2"/>'
    corpo += testo(L, 82, "IL PERCORSO", 700, 15, VERDE_SCURO, spaziatura=.1) + testo(L, 132, "Commit mese per mese", 900, 40, PETROLIO)
    for v in range(0, int(mx * 1.1), 20):  # griglia
        y = B - v * scala
        corpo += f'<rect x="{L}" y="{y:.1f}" width="{W - L - R}" height="1.2" fill="{P16}"/>' + testo(L - 14, y + 5, str(v), 500, 13, P70, "end")
    # fasce degli anni sotto l'asse
    for i, (_, o, per, tit, _) in enumerate(ANNI):
        idx = [j for j, m in enumerate(asse) if anno_scolastico(m) == i]
        if not idx: continue
        x0, x1 = L + idx[0] * passo + 4, L + (idx[-1] + 1) * passo - 4
        corpo += (f'<rect x="{x0:.1f}" y="{B + 18}" width="{x1 - x0:.1f}" height="8" rx="4" fill="{SEG[i]}"/>'
                  + testo(x0, B + 56, f"{o} ANNO · {per}", 700, 14, PETROLIO, spaziatura=.08)
                  + testo(x0, B + 80, tit, 400, 15, P70))
    for j, m in enumerate(asse):
        v = mesi.get(m, 0); h = max(v * scala, 3 if v else 0); x = L + j * passo + (passo - bw) / 2
        if v:
            corpo += (f'<rect x="{x:.1f}" y="{B - h:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="6" fill="{SEG[anno_scolastico(m)]}">'
                      f'<animate attributeName="height" from="0" to="{h:.1f}" dur=".7s" begin="{j * .04:.2f}s" fill="freeze"/>'
                      f'<animate attributeName="y" from="{B}" to="{B - h:.1f}" dur=".7s" begin="{j * .04:.2f}s" fill="freeze"/></rect>'
                      + testo(x + bw / 2, B - h - 10, str(v), 700, 14, PETROLIO, "middle"))
        lab = ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"][int(m[5:]) - 1]
        corpo += testo(x + bw / 2, B + 0 - 6 + 0, "", 400, 1) if False else ""
        if m[5:] in ("01", "09") or j == 0:
            corpo += testo(x + bw / 2, T - 26, f"{lab} {m[2:4]}", 700, 13, P70, "middle", .06)
            corpo += f'<rect x="{x + bw / 2 - .6:.1f}" y="{T - 18}" width="1.2" height="{B - T + 18}" fill="{P16}"/>'
    # tappe: etichette sopra le barre
    tappe = [("2025-03", "School_journey"), ("2025-05", "ISO/OSI in C"), ("2025-10", "Java e JavaScript"),
             ("2026-04", "Flutter"), ("2026-08", "ROUTER-GUI"), ("2026-10", "C# e SmartSerra")]
    for m, t in tappe:
        if m not in asse: continue
        j = asse.index(m); x = L + j * passo + passo / 2; v = mesi.get(m, 0); y = B - v * scala - 40
        w = larghezza(t, 700, 13) + 22; x0 = min(max(x - w / 2, L), W - R - w)
        corpo += (f'<rect x="{x0:.1f}" y="{y - 24:.1f}" width="{w:.1f}" height="26" rx="13" fill="{PETROLIO}"/>'
                  + testo(x0 + w / 2, y - 6, t, 700, 13, MENTA, "middle"))
    salva("percorso.svg", svg(W, H, corpo, {900, 700, 500, 400}, "Commit mese per mese, colorati per anno scolastico"))

FONTI = [  # nome, tipo, commit (dopo la pulizia), anni
    ("School_journey", "repo", 60, [0]), ("C-ISO-OSI", "repo", 30, [0]), ("py_uni", "repo", 5, [0]),
    ("CUgolot", "repo", 11, [0, 1, 2]), ("PythonAlmostSelfLearned", "repo", 21, [0, 1]),
    ("JavaProjects", "repo", 115, [1, 2]), ("DIYJavaScript", "repo", 78, [1, 2]), ("GAppProjects", "repo", 13, [1]),
    ("ROUTER-GUI", "repo", 20, [1]), ("Summerwork4a", "cartella", 0, [1]), ("Csharp", "cartella", 0, [2]), ("SmartSerra", "cartella", 0, [2]),
]

def confluenza(d):
    W, H = 1600, 900; x0, pw, ph, top, gap = 96, 400, 50, 170, 10
    xa, aw = 1180, 324; ah = 190; atop = 190
    corpo = f'<defs>{gradiente("g", 170, RETRO)}<clipPath id="c"><rect width="{W}" height="{H}" rx="28"/></clipPath></defs><g clip-path="url(#c)">'
    corpo += f'<rect width="{W}" height="{H}" fill="url(#g)"/>{onde(W, H, 3, da=.55, n=7, ampiezza=60)}'
    corpo += testo(x0, 82, "DA DOVE VIENE", 700, 15, MENTA, spaziatura=.1) + testo(x0, 132, "Dodici sorgenti, una repository", 900, 40, BIANCO)
    ya = [atop + i * (ah + 40) for i in range(3)]
    flussi, pill = "", ""
    for k, (nome, tipo, n, anni) in enumerate(FONTI):
        y = top + k * (ph + gap)
        pill += (f'<rect x="{x0}" y="{y}" width="{pw}" height="{ph}" rx="12" fill="{PETROLIO}" stroke="{MEDIO}" stroke-width="1.5"/>'
                 + testo(x0 + 22, y + 32, nome, 700, 18, BIANCO)
                 + testo(x0 + pw - 22, y + 31, f"{n} commit" if n else "cartella", 500, 14, MENTA if n else B75, "end"))
        for j, a in enumerate(anni):
            ys = y + ph / 2 + (j - (len(anni) - 1) / 2) * 8
            ye = ya[a] + 50 + (k % 6) * 22
            cxm = (x0 + pw + xa) / 2
            flussi += (f'<path d="M{x0 + pw} {ys:.1f} C{cxm} {ys:.1f} {cxm} {ye:.1f} {xa} {ye:.1f}" stroke="{SEG[a] if a else TURCHESE}"'
                       f' stroke-opacity="{.55 if a else .35}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    blocchi = ""
    for i, (_, o, per, tit, _) in enumerate(ANNI):
        y = ya[i]
        blocchi += (f'<rect x="{xa}" y="{y}" width="{aw}" height="{ah}" rx="20" fill="{BIANCO}"/>'
                    f'<rect x="{xa}" y="{y}" width="12" height="{ah}" rx="6" fill="{SEG[i]}"/>'
                    + testo(xa + 40, y + 52, f"{o} ANNO · {per}", 700, 14, P70, spaziatura=.08)
                    + testo(xa + 40, y + 98, tit, 900, 26 if len(tit) < 18 else 23, PETROLIO)
                    + testo(xa + 40, y + 148, f"{d['per_anno'][i]} commit", 900, 30, VERDE_SCURO))
    corpo += flussi + pill + blocchi + "</g>"
    salva("confluenza.svg", svg(W, H, corpo, {900, 700, 500}, "Le dodici sorgenti confluite nei tre anni"))

def linguaggi(d):
    W, H = 1600, 360; L = 96
    c = righe_per_linguaggio(d["elenco"]); top = c.most_common(7)
    altro = sum(c.values()) - sum(v for _, v in top)
    if altro > 0: top.append(("Altro", altro))
    tot = sum(v for _, v in top)
    col = [PETROLIO, VERDE_SCURO, TURCHESE, VERDE, NAVY, MENTA, P70, P16]
    corpo = f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="28" fill="{BIANCO}" stroke="{P16}" stroke-width="2"/>'
    corpo += testo(L, 82, "LINGUAGGI", 700, 15, VERDE_SCURO, spaziatura=.1)
    corpo += testo(L, 132, f"{tot:,} righe scritte a mano".replace(",", "."), 900, 40, PETROLIO)
    x, bw = L, W - 2 * L
    corpo += f'<clipPath id="b"><rect x="{L}" y="168" width="{bw}" height="40" rx="12"/></clipPath><g clip-path="url(#b)">'
    for i, (k, v) in enumerate(top):
        w = bw * v / tot
        corpo += f'<rect x="{x:.1f}" y="168" width="{w + .5:.1f}" height="40" fill="{col[i]}"/>'
        x += w
    corpo += "</g>"
    lx, ly = L, 264
    for i, (k, v) in enumerate(top):
        pct = f"{100 * v / tot:.0f}%"
        w = 22 + larghezza(k, 700, 18) + 10 + larghezza(pct, 400, 16) + 44
        if lx + w > W - L: lx, ly = L, ly + 44
        corpo += (f'<rect x="{lx}" y="{ly - 15}" width="14" height="14" rx="4" fill="{col[i]}" stroke="{P16 if col[i] in (MENTA, P16) else col[i]}"/>'
                  + testo(lx + 24, ly - 2, k, 700, 18, PETROLIO) + testo(lx + 24 + larghezza(k, 700, 18) + 10, ly - 2, pct, 400, 16, P70))
        lx += w
    salva("linguaggi.svg", svg(W, H, corpo, {900, 700, 400}, "Righe di codice per linguaggio"))

MATERIE_ANNO = {0: ["informatica", "sistemi", "tpsit", "attacco-difesa", "pcto", "estate"],
                1: ["informatica", "laboratorio", "sistemi", "tpsit", "estate"],
                2: ["informatica", "sistemi", "tpsit"]}

def testate(d):
    W, H = 1600, 300
    for i, (cart, o, per, tit, _) in enumerate(ANNI):
        corpo = (f'<defs>{gradiente("g", 98, TESTATA)}<clipPath id="c"><rect width="{W}" height="{H}" rx="28"/></clipPath></defs>'
                 f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="url(#g)"/>{onde(W, H, 20 + i, da=.4, n=8, ampiezza=50)}'
                 f'<rect x="0" y="0" width="14" height="{H}" fill="{SEG[i] if i else MENTA}"/>'
                 + testo(96, 118, f"{['TERZO', 'QUARTO', 'QUINTO'][i]} ANNO · {per}", 700, 17, VERDE, spaziatura=.08)
                 + testo(92, 196, tit, 900, 72, BIANCO, spaziatura=-.01)
                 + testo(96, 246, f"{d['per_anno'][i]} commit · {len(MATERIE_ANNO[i])} aree", 500, 19, BIANCO))
        r, x = 34, W - 96 - 34
        for m in reversed(MATERIE_ANNO[i]):
            corpo += icona(m, x, 214, r) ; x -= 2 * r + 14
        corpo += (f'<circle cx="{W - 140}" cy="{104}" r="62" fill="{PETROLIO}"/>'
                  + testo(W - 140, 128, o, 900, 64, MENTA, "middle") + "</g>")
        salva(f"anno-{i + 3}.svg", svg(W, H, corpo, {900, 700, 500}, f"{['Terzo', 'Quarto', 'Quinto'][i]} anno, {per}: {tit}"))

def icone():
    for m in ICONE:
        salva(f"icona-{m}.svg", f'<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64" role="img"><title>{m}</title>{icona(m, 32, 32, 32)}</svg>')

def chiusura(d):
    W, H = 1600, 320
    corpo = (f'<defs>{gradiente("g", 170, RETRO)}<clipPath id="c"><rect width="{W}" height="{H}" rx="28"/></clipPath></defs>'
             f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="url(#g)"/>{onde(W, H, 11, da=.6, n=6, ampiezza=40)}'
             + testo(W / 2, 128, "Dal primo printf a un router simulato nel browser", 900, 44, BIANCO, "middle")
             + f'<text x="{W / 2}" y="186" font-family="P900" font-size="24" text-anchor="middle"><tspan fill="{BIANCO}">Terzo</tspan><tspan fill="{B75}"> · </tspan>'
               f'<tspan fill="{TURCHESE}">Quarto</tspan><tspan fill="{B75}"> · </tspan><tspan fill="{VERDE}">Quinto</tspan></text>'
             + testo(W / 2, 262, "Giordano Fornari · 5ª C Informatica · ITIS Leonardo da Vinci, Parma", 500, 17, B75, "middle", .02)
             + "</g>")
    salva("chiusura.svg", svg(W, H, corpo, {900, 500}, "Dal primo printf a un router simulato nel browser"))

if __name__ == "__main__":
    d = dati()
    print(f"commit {d['commit']} · per anno {d['per_anno']} · file {d['file']} · progetti {d['progetti']}")
    hero(d); numeri(d); percorso(d); confluenza(d); linguaggi(d); testate(d); icone(); chiusura(d)
