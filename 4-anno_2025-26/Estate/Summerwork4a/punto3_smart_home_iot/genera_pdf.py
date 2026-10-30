#!/usr/bin/env python3
"""
Genera il PDF della relazione progettuale da relazione_progettuale.md.

    pip install markdown2 weasyprint
    python3 genera_pdf.py

Cosa fa oltre alla conversione:
  - trasforma i link fra documenti in semplice codice: su carta non si cliccano
  - inserisce la planimetria dove il testo la cita
  - impagina in A4 con numerazione, tabelle non spezzate e blocchi di codice
    che vanno a capo invece di uscire dal foglio
"""
import pathlib
import re
import sys

QUI = pathlib.Path(__file__).parent
SORGENTE = QUI / "relazione_progettuale.md"
USCITA = QUI / "Relazione_progettuale_CPT_Domotica_IoT.pdf"
PIANTA = QUI / "planimetria.png"

INTESTAZIONE = """
<div class="frontespizio">
  <div class="istituto">ITIS &middot; Sistemi e Reti &middot; Lavoro estivo</div>
  <div class="autore">Studente: S. Giordano Fornari &nbsp;&middot;&nbsp; Classe: ____</div>
</div>
"""

CSS = """
@page { size: A4; margin: 20mm 18mm 18mm 18mm;
  @bottom-center { content: counter(page) " / " counter(pages);
                   font-family: Helvetica, sans-serif; font-size: 8pt; color: #999; } }
body { font-family: "DejaVu Sans", Helvetica, sans-serif; font-size: 9.6pt;
       line-height: 1.45; color: #1c1c1a; }
.frontespizio { font-size: 8.5pt; color: #8b949c; margin-bottom: 14px;
                border-bottom: 1px solid #e4e8eb; padding-bottom: 6px; }
.frontespizio .autore { margin-top: 2px; }
h1 { font-size: 20pt; color: #2b3640; border-bottom: 2.5px solid #2b3640;
     padding-bottom: 5px; margin: 0 0 4px; }
h1 + h2 { border: 0; color: #6b757e; font-size: 12pt; margin-top: 0; font-weight: 400; }
h2 { font-size: 13pt; color: #2b3640; margin-top: 20px; margin-bottom: 6px;
     border-bottom: 1px solid #d8dde1; padding-bottom: 3px; page-break-after: avoid; }
h3 { font-size: 10.6pt; color: #3d4a55; margin-top: 14px; margin-bottom: 4px;
     page-break-after: avoid; }
p { margin: 5px 0; text-align: justify; }
table { border-collapse: collapse; width: 100%; margin: 9px 0; font-size: 8.4pt;
        page-break-inside: avoid; }
th { background: #eef1f3; text-align: left; padding: 4px 6px;
     border: 1px solid #ccd3d8; font-weight: 700; color: #2b3640; }
td { padding: 4px 6px; border: 1px solid #dde2e6; vertical-align: top; }
tr:nth-child(even) td { background: #fafbfc; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 8.2pt;
       background: #f2f4f6; padding: 0.5px 3px; border-radius: 2px; }
pre { background: #f7f8f9; border: 1px solid #dde2e6; border-left: 3px solid #7a8791;
      padding: 7px 9px; font-size: 7.6pt; line-height: 1.35;
      white-space: pre-wrap; page-break-inside: avoid; }
pre code { background: none; padding: 0; font-size: 7.6pt; }
blockquote { border-left: 3px solid #c3ccd3; margin: 8px 0; padding: 2px 0 2px 11px;
             color: #4a555e; }
strong { color: #16202a; }
hr { border: 0; border-top: 1px solid #dde2e6; margin: 16px 0; }
ul, ol { margin: 5px 0; padding-left: 19px; }
li { margin: 2px 0; }
figure { margin: 12px 0; page-break-inside: avoid; text-align: center; }
figure img { width: 100%; border: 1px solid #dde2e6; }
figcaption { font-size: 8pt; color: #8b949c; margin-top: 4px; }
"""


def main():
    try:
        import markdown2
        import weasyprint
    except ImportError as e:
        sys.exit(f"manca una dipendenza ({e.name}): "
                 "pip install markdown2 weasyprint")

    md = SORGENTE.read_text(encoding="utf-8")

    # i rimandi fra documenti su carta non si cliccano: restano solo i nomi file
    md = re.sub(r"\[`([^`]+)`\]\([^)]+\)", r"`\1`", md)
    md = re.sub(r"\[([^\]]+)\]\((?!http)[^)]+\)", r"\1", md)

    # la planimetria va inserita dove il testo la cita
    ancora = "Planimetria annotata in `planimetria.svg`."
    if ancora in md and PIANTA.exists():
        figura = (ancora + "\n\n<figure><img src=\"planimetria.png\">"
                  "<figcaption>Pianta della villa con la posizione dei 21 "
                  "dispositivi IoT e degli apparati di rete. Il colore del "
                  "marker indica la VLAN di appartenenza.</figcaption></figure>\n")
        md = md.replace(ancora, figura, 1)
    elif not PIANTA.exists():
        print("nota: planimetria.png non trovata, il PDF esce senza pianta")

    html = markdown2.markdown(
        md, extras=["tables", "fenced-code-blocks", "cuddled-lists"])

    doc = ('<!doctype html><html lang="it"><head><meta charset="utf-8">'
           f"<style>{CSS}</style></head><body>{INTESTAZIONE}{html}</body></html>")

    pagine = weasyprint.HTML(string=doc, base_url=str(QUI)).render()
    pagine.write_pdf(USCITA)
    print(f"scritto {USCITA.name} — {len(pagine.pages)} pagine, "
          f"{USCITA.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
