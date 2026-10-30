#!/usr/bin/env python3
"""
Genera le varianti della planimetria da un'unica sorgente.

sfondo_planimetria.svg  =  la pianta pulita, senza marker
   |
   +--> sfondo_planimetria.png        1600x1000  sfondo per Packet Tracer
   +--> sfondo_planimetria_1200.png   1200x750   idem, schermi piccoli
   +--> ../planimetria.svg / .png                versione annotata per la relazione

Una sola architettura, due usi: se sposti un muro, tutte le varianti si
aggiornano rilanciando questo script.

    python3 genera_varianti.py
"""
import os
import re

QUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(QUI, "sfondo_planimetria.svg")
DOC_SVG = os.path.join(QUI, "..", "planimetria.svg")

# VLAN -> colore del marker
COL = {0: "#6b7680",   # 0 = fuori dal piano VLAN (rete dell'operatore)
       10: "#4a5f8e", 20: "#2e7d5b", 30: "#b3701f", 40: "#8a4a86",
       50: "#a03a3a", 60: "#1f6f78"}

# (x, y, etichetta, vlan) - le coordinate sono quelle del viewBox 1600x1000
MARKER = [
    # --- soggiorno ---
    (200, 740, "1", 30), (320, 740, "2", 30),
    (200, 850, "3", 30), (320, 850, "4", 30), (470, 850, "A", 20),
    # --- cucina ---
    (560, 320, "5", 30), (680, 320, "6", 30),
    # --- ingresso ---
    (180, 310, "7", 30), (300, 310, "8", 30), (180, 420, "9", 30),
    # --- bagno e lavanderia ---
    (880, 320, "10", 30), (990, 320, "11", 30),
    # --- camera matrimoniale ---
    (1180, 330, "12", 30), (1300, 330, "13", 30),
    # --- corridoio: sirena + LAP a soffitto (posizione baricentrica) ---
    (700, 555, "15", 30), (900, 555, "LAP", 60),
    # --- studio ---
    (670, 800, "14", 30), (790, 800, "B", 20),
    # --- camera singola ---
    (1020, 800, "C", 20),
    # --- locale tecnico (ora e' una stanza vera): 3 colonne x 4 righe,
    #     sotto l'etichetta della stanza per non sovrapporsi.
    #     MOD = modem DSL: e' il punto di ingresso della linea, sta in casa ---
    (1250, 765, "MOD", 0), (1340, 765, "R", 10), (1430, 765, "SW", 10),
    (1250, 822, "WLC", 60), (1340, 822, "APio", 30), (1430, 822, "APgs", 40),
    (1250, 879, "IoT", 50), (1340, 879, "WEB", 50), (1430, 879, "DHCP", 50),
    (1250, 928, "RAD", 50), (1340, 928, "DNS", 50),
    # --- giardino ---
    (640, 1140, "16", 30), (860, 1140, "17", 30),
    (1080, 1140, "18", 30), (1300, 1140, "19", 30),
    # --- cantina ---
    (1700, 600, "20", 30), (1790, 600, "21", 30),
    # --- rete dell'operatore: la catena di accesso ---
    (1620, 840, "ISP", 0), (1730, 840, "CLD", 0),
    (1840, 840, "WEB", 0), (1950, 840, "DNS", 0), (2050, 840, "PC", 0),
]

LEGENDA = [
    ("Categoria Home", None),
    ("1 Smart Lamp · 2 Ceiling Fan · 3 Window · 4 Home Speaker", None),
    ("5 Smoke Detector · 6 Fire Sprinkler · 7 Smart Door", None),
    ("8 Motion Detector · 9 Webcam (telecamera IP)", None),
    ("10 Water Level Monitor · 11 Drain Actuator", None),
    ("12 Air Conditioner · 13 Humiture Monitor", None),
    ("14 Furnace · 15 Siren", None),
    ("", None),
    ("Categoria Power Grid", None),
    ("16 Solar Panel · 20 Battery · 21 Power Meter", None),
    ("", None),
    ("Categoria Industrial / esterni", None),
    ("17 Photo Sensor · 18 Lawn Sprinkler · 19 MCU-PT", None),
    ("", None),
    ("Apparati di rete", None),
    ("MOD modem DSL · R router di casa · SW switch", None),
    ("WLC controller wireless · LAP access point gestito (MyHome)", None),
    ("APio APgs access point autonomi (IoT, Ospiti)", None),
    ("IoT WEB DHCP RAD DNS i cinque server · A/B/C PC di famiglia", None),
    ("", None),
    ("Rete dell'operatore", None),
    ("ISP router del provider · CLD nuvola di accesso (DSLAM)", None),
    ("WEB DNS server pubblici · PC client remoto", None),
]


def marker_svg(x, y, testo, vlan):
    r = 13 if len(testo) <= 2 else 17
    forma = (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{COL[vlan]}" '
             f'stroke="#fff" stroke-width="2"/>')
    fs = 10 if len(testo) <= 2 else 8.5
    return (forma + f'<text x="{x}" y="{y + 3.5}" font-size="{fs}" '
            f'font-weight="700" fill="#fff" text-anchor="middle">{testo}</text>')


def main():
    with open(BASE, encoding="utf-8") as f:
        svg = f.read()

    if "</svg>" not in svg:
        raise SystemExit("sorgente SVG non valida")

    pezzi = ['\n<!-- ===== marker dei dispositivi (versione per la relazione) ===== -->',
             '<g id="marker">']
    pezzi += [marker_svg(*m) for m in MARKER]
    pezzi.append("</g>")

    # legenda in basso a destra, dove non c'e' disegno
    pezzi.append('<g id="legenda" font-family="DejaVu Sans, Helvetica, sans-serif">')
    pezzi.append('<text x="90" y="1290" font-size="14" font-weight="700" '
                 'fill="#7d868e">LEGENDA DEI MARKER</text>')
    x, y = 90, 1314
    for i, (riga, _) in enumerate(LEGENDA):
        if i == 8:      # inizio colonna 2: "Categoria Power Grid"
            x, y = 800, 1314
        elif i == 11:   # inizio colonna 3: "Categoria Industrial / esterni"
            x, y = 1500, 1314
        if not riga:
            continue
        peso = "700" if not riga[0].isdigit() and "·" not in riga else "400"
        col = "#7d868e" if peso == "700" else "#a9b2b9"
        pezzi.append(f'<text x="{x}" y="{y}" font-size="12.5" font-weight="{peso}" '
                     f'fill="{col}">{riga}</text>')
        y += 17
    pezzi.append("</g>")

    doc = svg.replace("</svg>", "\n".join(pezzi) + "\n</svg>")
    # il sottotitolo cambia: questa variante non e' uno sfondo
    doc = doc.replace("Villa su un piano · pianta e aree di posa degli apparati",
                      "Villa su un piano · posizione dei 21 dispositivi IoT "
                      "e degli apparati di rete")
    # piu' spazio in basso per la legenda
    doc = doc.replace('height="1300" viewBox="0 0 2200 1300"',
                      'height="1400" viewBox="0 0 2200 1400"', 1)
    doc = doc.replace('<rect fill="#ffffff" x="0" y="0" width="2200" height="1300"/>',
                      '<rect fill="#ffffff" x="0" y="0" width="2200" height="1400"/>')

    with open(DOC_SVG, "w", encoding="utf-8") as f:
        f.write(doc)
    print("scritto", os.path.normpath(DOC_SVG))

    try:
        import cairosvg
        from PIL import Image
    except ImportError:
        print("cairosvg/Pillow non installati: salto i PNG "
              "(pip install cairosvg pillow)")
        return

    uscite = [
        (BASE, os.path.join(QUI, "sfondo_planimetria.png"), 2200, 1300),
        (BASE, os.path.join(QUI, "sfondo_planimetria_1600.png"), 1600, 945),
        (DOC_SVG, os.path.join(QUI, "..", "planimetria.png"), 2200, 1400),
    ]
    for src, dst, w, h in uscite:
        cairosvg.svg2png(url=src, write_to=dst, output_width=w,
                         output_height=h, background_color="white")
        Image.open(dst).convert("RGB").save(dst)
        print(f"scritto {os.path.normpath(dst)}  {w}x{h}")


if __name__ == "__main__":
    main()
