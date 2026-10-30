#!/usr/bin/env python3
"""Lavagne statiche del README: percorsi, esempi reali e history importata.

uv run --with fonttools --with brotli python .github/readme/genera.py
Riferimento: sistema/montaggio.md e produzione/src/ds/tokens.ts del corso
Security Awareness. Carta a quadretti, Instrument Sans, Cormorant corsivo,
un fuoco per tavola, segni che spiegano relazioni fra contenuti reali.
"""
import collections
import os
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen

QUI = Path(__file__).resolve().parent
RADICE = QUI.parent.parent
CARTA, INCHIOSTRO, SECONDARIO = "#F4F7FA", "#0D0D26", "#4D5870"
NAVY, FILETTO, GIALLO, BIANCO = "#164573", "#DCE3EC", "#FFE27A", "#FFFFFF"
ANNI = [
    ("3-anno_2024-25", "3ª", "2024–25", "Le fondamenta"),
    ("4-anno_2025-26", "4ª", "2025–26", "L’anno degli oggetti"),
    ("5-anno_2026-27", "5ª", "2026–27", "Reti e server"),
]
_font = {}

def font(stile, peso):
    key = (stile, peso)
    if key not in _font:
        nome = {"sans": "InstrumentSans", "serif": "Cormorant-Italic", "mono": "JetBrainsMono"}[stile]
        f = TTFont(QUI / "font" / f"{nome}.woff2", recalcTimestamp=False)
        assi = {a.axisTag: peso if a.axisTag == "wght" else a.defaultValue for a in f["fvar"].axes}
        _font[key] = instantiateVariableFont(f, assi, inplace=True)
    return _font[key]

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def larghezza(s, corpo, peso=560, stile="sans"):
    f = font(stile, peso); cmap = f.getBestCmap()
    assert all(ord(c) in cmap for c in s), f"Glifo mancante: {s}"
    return sum(f["hmtx"][cmap[ord(c)]][0] for c in s) * corpo / f["head"].unitsPerEm

def testo(x, y, s, corpo=28, peso=560, colore=INCHIOSTRO, anchor="start", stile="sans"):
    # I contorni mantengono i font del corso anche nei renderer SVG senza font web.
    f = font(stile, peso); cmap = f.getBestCmap(); gs = f.getGlyphSet(); k = corpo / f["head"].unitsPerEm
    w = larghezza(s, corpo, peso, stile)
    x -= w / 2 if anchor == "middle" else w if anchor == "end" else 0
    parti, pos = [], 0
    for c in s:
        nome = cmap[ord(c)]; pen = SVGPathPen(gs); gs[nome].draw(pen)
        if pen.getCommands(): parti.append(f'<path transform="translate({pos} 0)" d="{pen.getCommands()}"/>')
        pos += f["hmtx"][nome][0]
    return f'<g aria-label="{esc(s)}" data-text="{esc(s)}" fill="{colore}" transform="translate({x:.2f} {y}) scale({k:.6f} {-k:.6f})">{"".join(parti)}</g>'

def linea(d, colore=NAVY, spessore=2.5, extra=""):
    return f'<path d="{d}" stroke="{colore}" stroke-width="{spessore}" fill="none" stroke-linecap="round" stroke-linejoin="round" {extra}/>'

def rett(x, y, w, h, fill=BIANCO, stroke=FILETTO, r=6):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'

def freccia(x1, y1, x2, y2):
    return linea(f"M{x1} {y1} L{x2} {y2}", extra='marker-end="url(#punta)"')

def sottolinea(x, y, w):
    return linea(f"M{x} {y} Q{x+w*.45} {y+5} {x+w} {y-2}", spessore=3)

def frase(y, prima, parola, corpo=56):
    a = larghezza(prima + " ", corpo, 600)
    b = larghezza(parola, corpo * 1.2, 600, "serif")
    x = (1200 - a - b) / 2
    return (f'<path d="M{x+a-3:.1f} {y-corpo*.53:.1f} l{b+9:.1f} -3 l-2 {corpo*.62:.1f} l{-b-6:.1f} 3 Z" fill="{GIALLO}"/>'
            + testo(x, y, prima + " ", corpo, 600)
            + testo(x+a, y, parola, corpo*1.2, 600, stile="serif"))

def tavola(nome, h, corpo, titolo, descrizione):
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{h}" viewBox="0 0 1200 {h}" role="img" aria-labelledby="titolo descrizione">'
           f'<title id="titolo">{esc(titolo)}</title><desc id="descrizione">{esc(descrizione)}</desc>'
           f'<defs><pattern id="quadretti" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{FILETTO}" stroke-width="1" opacity=".7"/></pattern>'
           f'<marker id="punta" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M1 1L9 5L1 9" fill="none" stroke="{NAVY}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>'
           f'<rect width="1200" height="{h}" fill="{CARTA}"/><rect width="1200" height="{h}" fill="url(#quadretti)"/>{corpo}</svg>')
    ET.fromstring(doc)
    (QUI / nome).write_text(doc, encoding="utf-8")
    print(f"{nome:<22} {len(doc)/1024:6.1f} KB")

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
    primo, ultimo = min(mesi), "2026-10"
    asse, (y, m) = [], map(int, primo.split("-"))
    while f"{y}-{m:02d}" <= ultimo:
        asse.append(f"{y}-{m:02d}"); m += 1
        if m > 12: y, m = y + 1, 1
    per_anno = [0, 0, 0]
    for k, n in mesi.items(): per_anno[anno_scolastico(k)] += n
    file = git("-c", "core.quotepath=false", "ls-files", "--", *(a[0] for a in ANNI)).splitlines()
    return dict(commit=len(commit), mesi=mesi, asse=asse, per_anno=per_anno, file=len(file),
                elenco=file)

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


FONTI = [  # nome, tipo, commit (dopo la pulizia), anni
    ("School_journey", "repo", 60, [0]), ("C-ISO-OSI", "repo", 30, [0]), ("py_uni", "repo", 5, [0]),
    ("CUgolot", "repo", 11, [0, 1, 2]), ("PythonAlmostSelfLearned", "repo", 21, [0, 1]),
    ("JavaProjects", "repo", 115, [1, 2]), ("DIYJavaScript", "repo", 78, [1, 2]), ("GAppProjects", "repo", 13, [1]),
    ("ROUTER-GUI", "repo", 20, [1]), ("Summerwork4a", "cartella", 0, [1]), ("Csharp", "cartella", 0, [2]), ("SmartSerra", "cartella", 0, [2]),
]

def hero(d):
    c = testo(600, 58, "GIORDANO FORNARI / ITIS LEONARDO DA VINCI, PARMA", 21, colore=SECONDARIO, anchor="middle")
    c += testo(600, 174, "School", 112, 700, anchor="middle") + frase(251, "Tre anni di", "codice", 48)
    c += testo(112, 343, "School/", 30, 500, stile="mono")
    c += linea("M130 363 V559 M130 399 H169 M130 479 H169 M130 559 H169", spessore=2)
    temi = ["C, Python, primi algoritmi", "Java, oggetti, interfacce", "C#, Node.js, reti"]
    for i, (cart, _, _, _) in enumerate(ANNI):
        y = 409 + i * 80
        c += testo(188, y, cart + "/", 30, 500, stile="mono")
        c += testo(696, y, temi[i], 27, colore=SECONDARIO)
    c += testo(600, 655, "Scegli l’anno, poi la materia, poi il progetto.", 30, anchor="middle")
    tavola("hero.svg", 710, c, "School: mappa dei tre anni", "Cartelle reali: 3-anno_2024-25, 4-anno_2025-26, 5-anno_2026-27. C e Python, poi oggetti e interfacce, infine reti e server.")


def testate(d):
    intestazioni = [("Le", "fondamenta"), ("L’anno degli", "oggetti"), ("Reti e", "server")]
    for i, (_, o, periodo, titolo) in enumerate(ANNI):
        c = testo(600, 58, f"{o} ANNO / {periodo}", 25, colore=SECONDARIO, anchor="middle")
        c += frase(148, *intestazioni[i])
        if i == 0:
            c += testo(600, 219, "Da un numero decimale alla sua rappresentazione binaria", 27, anchor="middle")
            c += rett(94, 285, 214, 174, stroke=NAVY)
            c += testo(201, 330, "INPUT", 22, colore=SECONDARIO, anchor="middle")
            c += testo(201, 417, "13", 76, 600, anchor="middle", stile="mono")
            c += freccia(335, 372, 550, 372)
            c += testo(443, 340, "dectobin.c", 22, 500, anchor="middle", stile="mono")
            c += testo(848, 269, "OUTPUT BINARIO", 22, colore=SECONDARIO, anchor="middle")
            for j, (bit, valore) in enumerate(zip("1101", (8, 4, 2, 1))):
                x = 594 + j * 128
                c += rett(x, 285, 116, 174, fill=BIANCO if bit == "1" else CARTA, stroke=NAVY)
                c += testo(x+58, 400, bit, 74, 600, anchor="middle", stile="mono")
                c += testo(x+58, 501, str(valore), 27, colore=SECONDARIO, anchor="middle")
            c += testo(848, 550, "8 + 4 + 0 + 1 = 13", 28, 500, anchor="middle", stile="mono")
            c += testo(600, 610, "Il bit indica se includere quel valore nella somma.", 26, colore=SECONDARIO, anchor="middle")
            desc = "Esempio reale: dectobin.c. L’input 13 diventa 1101: i bit corrispondono ai valori 8, 4, 2, 1; 8 + 4 + 0 + 1 = 13."
        elif i == 1:
            c += testo(600, 219, "Biblioteca: ciò che è comune si eredita", 28, anchor="middle")
            c += rett(384, 261, 432, 116, stroke=NAVY)
            c += testo(600, 305, "Pubblicazione", 33, 600, anchor="middle")
            c += testo(600, 347, "titolo · data · numeroPagine", 24, colore=SECONDARIO, anchor="middle")
            c += linea("M600 393 V431 M294 468 V431 H906 V468")
            c += f'<path d="M589 395 L600 379 L611 395 Z" fill="{CARTA}" stroke="{NAVY}" stroke-width="2.5"/>'
            for x, nome, campi in [(94, "Libro", "isbn · autore"), (706, "Rivista", "numeroVolume · periodicita")]:
                c += rett(x, 469, 400, 112, stroke=NAVY)
                c += testo(x+200, 513, nome, 34, 600, anchor="middle")
                c += testo(x+200, 555, campi, 24, colore=SECONDARIO, anchor="middle")
            c += testo(600, 630, "Due classi diverse, la stessa base astratta.", 26, colore=SECONDARIO, anchor="middle")
            desc = "Diagramma delle classi reali di Biblioteca: Libro e Rivista estendono la classe astratta Pubblicazione, che contiene titolo, data e numero di pagine. Libro aggiunge ISBN e autore; Rivista volume e periodicità."
        else:
            c += testo(600, 219, "ServerWebStatico: il viaggio di una pagina", 28, anchor="middle")
            c += rett(84, 275, 294, 171, stroke=NAVY)
            c += testo(231, 330, "Browser", 38, 600, anchor="middle")
            c += testo(231, 403, "localhost:3000", 24, 500, colore=SECONDARIO, anchor="middle", stile="mono")
            c += rett(782, 275, 334, 171, stroke=NAVY)
            c += testo(949, 330, "server.js", 35, 500, anchor="middle", stile="mono")
            c += testo(949, 403, "Node.js / http", 26, colore=SECONDARIO, anchor="middle")
            c += freccia(405, 302, 750, 302) + testo(578, 282, "GET /", 28, 500, anchor="middle", stile="mono")
            c += freccia(750, 407, 405, 407) + testo(578, 387, "200 + HTML", 28, 500, anchor="middle", stile="mono")
            c += freccia(949, 477, 949, 536)
            c += testo(920, 510, "legge il file", 24, colore=SECONDARIO, anchor="end")
            c += rett(782, 557, 334, 64, stroke=NAVY)
            c += testo(949, 599, "public/index.html", 24, 500, anchor="middle", stile="mono")
            c += testo(84, 539, "La richiesta sceglie la risorsa.", 27)
            c += testo(84, 581, "Lo stream la invia al browser.", 27)
            desc = "Flusso del server reale ServerWebStatico: il browser richiede GET / a localhost:3000; server.js legge public/index.html e lo invia tramite stream con risposta 200 e contenuto HTML. Schema semplificato del caso senza gzip o Range."
        tavola(f"anno-{i+3}.svg", 675, c, f"{o} anno {periodo}: {titolo}", desc)


def percorso(d):
    asse, mesi = d["asse"], d["mesi"]
    c = frase(98, "La storia nel", "tempo", 54)
    c += testo(600, 157, "353 commit importati / date autore / marzo 2025–ottobre 2026", 24, colore=SECONDARIO, anchor="middle")
    l, b, passo = 90, 476, 1040 / len(asse)
    scala = 230 / max(mesi.values())
    for v in range(0, max(mesi.values())+1, 20):
        y = b - v*scala
        c += linea(f"M{l} {y} H1130", FILETTO, 1.5)
        c += testo(l-16, y+7, str(v), 21, colore=SECONDARIO, anchor="end")
    for j, m in enumerate(asse):
        v = mesi.get(m, 0); x = l + j*passo
        if v:
            c += rett(round(x+9, 2), round(b-v*scala, 2), round(passo-18, 2), round(v*scala, 2), NAVY, NAVY, 1)
            c += testo(x+passo/2, b-v*scala-12, str(v), 22, anchor="middle")
        lab = ["g", "f", "m", "a", "m", "g", "l", "a", "s", "o", "n", "d"][int(m[5:])-1]
        c += testo(x+passo/2, b+31, lab, 21, colore=SECONDARIO, anchor="middle")
    for i, (_, o, periodo, _) in enumerate(ANNI):
        idx = [j for j, m in enumerate(asse) if anno_scolastico(m) == i]
        x0, x1 = l+idx[0]*passo+5, l+(idx[-1]+1)*passo-5
        c += linea(f"M{x0} 535 V545 H{x1} V535", spessore=2)
        c += testo((x0+x1)/2, 583, f"{o} / {periodo}", 24, anchor="middle")
        c += testo((x0+x1)/2, 622, f"{d['per_anno'][i]} commit", 25, 650, anchor="middle")
    c += testo(600, 686, "La lunghezza delle barre conta i commit, non le ore di studio.", 24, colore=SECONDARIO, anchor="middle")
    tavola("percorso.svg", 730, c, "Commit importati per mese e anno scolastico", "History precedente al 30 ottobre 2026: 94 commit nel terzo anno, 237 nel quarto, 22 nel quinto. Ogni barra rappresenta un mese; gli anni scolastici iniziano a settembre.")


def linguaggi(d):
    conti = righe_per_linguaggio(d["elenco"])
    top = conti.most_common(7)
    top.append(("Altro", sum(conti.values())-sum(v for _, v in top)))
    tot, mx = sum(conti.values()), top[0][1]
    c = frase(98, "Di cosa è fatto il", "codice", 54)
    c += testo(600, 157, f"{tot:,} righe non vuote, inclusi commenti e markup".replace(",", ".", 1), 25, colore=SECONDARIO, anchor="middle")
    for i, (nome, n) in enumerate(top):
        y = 226+i*52
        c += testo(64, y+22, nome, 27)
        c += rett(258, y, 580, 27, FILETTO, FILETTO, 1)
        c += rett(258, y, round(580*n/mx, 2), 27, NAVY, NAVY, 1)
        c += testo(990, y+22, f"{n:,}".replace(",", "."), 26, 500, anchor="end", stile="mono")
        c += testo(1136, y+22, f"{100*n/tot:.0f}%", 26, colore=SECONDARIO, anchor="end")
    c += testo(600, 702, "File didattici tracciati; cartelle generate riconoscibili escluse.", 24, colore=SECONDARIO, anchor="middle")
    tavola("linguaggi.svg", 745, c, "Distribuzione del materiale per linguaggio", "; ".join(f"{nome}: {n} righe" for nome, n in top)+". Il conteggio include commenti e markup e non misura la paternità o l’esperienza.")


def confluenza(d):
    destinazioni = [
        ("4 materie", "", ""), ("Sistemi", "", ""), ("PCTO", "", ""),
        ("Sistemi, Estate", "Sistemi/C", "Subnet-Tool"),
        ("Inf./Python", "Inf./Python", ""), ("", "Inf./Java", "Inf./Java"),
        ("", "TPSIT/JS", "TPSIT/JS"), ("", "Lab/Flutter", ""),
        ("", "Estate", ""), ("", "Estate", ""),
        ("", "", "Inf./CSharp"), ("", "", "Sistemi"),
    ]
    c = frase(98, "Dove è finito il", "materiale", 54)
    c += testo(600, 157, "La mappa delle sorgenti, prima e dopo l’unificazione", 26, colore=SECONDARIO, anchor="middle")
    c += testo(64, 230, "SORGENTE", 22, colore=SECONDARIO)
    c += testo(480, 230, "COMMIT", 22, colore=SECONDARIO, anchor="end")
    for j, (_, o, periodo, _) in enumerate(ANNI):
        c += testo(620+j*204, 214, o+" ANNO", 25, 650, anchor="middle")
        c += testo(620+j*204, 244, periodo, 21, colore=SECONDARIO, anchor="middle")
    for i, ((nome, tipo, n, anni), celle) in enumerate(zip(FONTI, destinazioni)):
        assert [j for j, cella in enumerate(celle) if cella] == anni
        y = 287+i*51
        c += linea(f"M64 {y+22} H1136", FILETTO, 1)
        c += testo(64, y, nome, 24, 600)
        c += testo(480, y, str(n) if n else "locale", 23, colore=SECONDARIO, anchor="end")
        for j, cella in enumerate(celle):
            c += testo(620+j*204, y, cella or "—", 22, colore=INCHIOSTRO if cella else SECONDARIO, anchor="middle")
    c += testo(600, 956, "Inf. = Informatica / JS = JavaScript / trattino = nessun materiale", 23, colore=SECONDARIO, anchor="middle")
    c += testo(600, 997, "I percorsi completi sono nella tabella del README.", 24, anchor="middle")
    tavola("confluenza.svg", 1040, c, "Origini e destinazioni del materiale", "Nove repository con 353 commit e tre cartelle locali. Per ogni sorgente la matrice mostra gli anni e le aree di destinazione; un trattino indica che non c’è materiale.")


if __name__ == "__main__":
    d = dati()
    assert sum(d["per_anno"]) == d["commit"] == sum(f[2] for f in FONTI)
    assert anno_scolastico("2025-08") == 0 and anno_scolastico("2025-09") == 1
    assert all((RADICE/f).exists() for f in d["elenco"])
    hero(d); testate(d); percorso(d); linguaggi(d); confluenza(d)
