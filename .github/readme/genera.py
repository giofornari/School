#!/usr/bin/env python3
"""Banner e mappa del percorso scolastico per chi visita la repository.

uv run --with fonttools --with brotli python .github/readme/genera.py
Riferimento: sistema/montaggio.md e produzione/src/ds/tokens.ts del corso
Security Awareness. Carta a quadretti, Instrument Sans, Cormorant corsivo,
un fuoco per tavola, segni che spiegano relazioni fra contenuti reali.
"""
import xml.etree.ElementTree as ET
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen

QUI = Path(__file__).resolve().parent
RADICE = QUI.parent.parent
CARTA, INCHIOSTRO, SECONDARIO = "#F4F7FA", "#0D0D26", "#4D5870"
NAVY, FILETTO, GIALLO, BIANCO = "#164573", "#DCE3EC", "#FFE27A", "#FFFFFF"
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

def frase(y, prima, parola, corpo=56, x=None):
    a = larghezza(prima + " ", corpo, 600)
    b = larghezza(parola, corpo * 1.2, 600, "serif")
    if x is None: x = (1200 - a - b) / 2
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
    print(f"{nome:<30} {len(doc)/1024:6.1f} KB")

ANNI = [
    ("3-anno_2024-25", "TERZO", "2024–25", "Le", "basi",
     "Imparare a risolvere problemi.",
     "Algoritmi e programmazione procedurale", "Primi concetti di rete e web", "Python / C / HTML"),
    ("4-anno_2025-26", "QUARTO", "2025–26", "Oggetti e", "interfacce",
     "Organizzare il codice in applicazioni.",
     "Classi, ereditarietà e strutture dati", "Interfacce, applicazioni e sviluppo web", "Java / Python / JavaScript / Dart"),
    ("5-anno_2026-27", "QUINTO", "2026–27", "Applicazioni e", "reti",
     "Collegare software e sistemi. In corso.",
     "Applicazioni desktop e servizi web", "Subnetting, progettazione di reti e IoT", "C# / Node.js / Packet Tracer"),
]


def hero():
    c = testo(64, 48, "ITIS LEONARDO DA VINCI / PARMA", 22, colore=SECONDARIO)
    c += testo(60, 170, "School", 112, 700)
    c += testo(64, 248, "GIORDANO FORNARI / INFORMATICA / 2024–2027", 22, colore=SECONDARIO)
    c += testo(656, 112, "Dalle basi alle applicazioni", 33)
    c += frase(170, "e alle", "reti", 43, x=656)
    c += sottolinea(656, 198, 392)
    c += testo(656, 248, "Terzo, quarto e quinto anno", 27, colore=SECONDARIO)
    tavola("banner-school.svg", 300, c, "School: tre anni di informatica, 2024–2027",
           "Percorso scolastico di Giordano Fornari all’ITIS Leonardo da Vinci di Parma: dalle basi della programmazione alle applicazioni e alle reti.")


def banner_anni():
    for i, (_, ordinale, periodo, prima, parola, sintesi, tema1, tema2, tecnologie) in enumerate(ANNI):
        c = testo(64, 47, f"{ordinale} ANNO / {periodo}", 22, colore=SECONDARIO)
        c += frase(125, prima, parola, 43, x=64)
        c += testo(64, 192, sintesi, 24, colore=SECONDARIO)
        c += testo(654, 80, tema1, 25)
        c += testo(654, 125, tema2, 25)
        c += testo(654, 192, tecnologie, 22, 500, colore=SECONDARIO)
        tavola(f"banner-anno-{i+3}.svg", 240, c,
               f"{ordinale.capitalize()} anno {periodo}: {prima} {parola}",
               f"{sintesi} {tema1}. {tema2}. Tecnologie: {tecnologie}.")


def percorso():
    c = frase(76, "Come cresce il", "percorso", 47)
    fasi = [
        ("3ª / 2024–25", "Risolvere", "Capire un problema", "e tradurlo in un algoritmo."),
        ("4ª / 2025–26", "Strutturare", "Organizzare dati e codice", "in applicazioni con interfacce."),
        ("5ª / 2026–27", "Integrare", "Collegare applicazioni,", "servizi e reti. Anno in corso."),
    ]
    for i, (anno, verbo, riga1, riga2) in enumerate(fasi):
        x = 64+i*376
        c += testo(x, 151, anno, 23, colore=SECONDARIO)
        c += testo(x, 222, verbo, 40, 600)
        c += sottolinea(x, 239, larghezza(verbo, 40, 600))
        c += testo(x, 294, riga1, 25)
        c += testo(x, 332, riga2, 25)
        if i < 2: c += freccia(x+278, 205, x+341, 205)
    tavola("mappa-percorso.svg", 390, c, "La progressione dei tre anni",
           "Terzo anno: capire un problema e tradurlo in un algoritmo. Quarto: organizzare dati e codice in applicazioni con interfacce. Quinto, in corso: collegare applicazioni, servizi e reti.")


if __name__ == "__main__":
    assert all((RADICE/a[0]).is_dir() for a in ANNI)
    hero(); banner_anni(); percorso()
