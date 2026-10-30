# Grafiche di School

Sette SVG nello stile **lavagna del corso Security Awareness / Ariele**: carta `#F4F7FA`, quadretti `#DCE3EC`, inchiostro `#0D0D26`, tratto navy `#164573`, evidenziatore `#FFE27A`. Instrument Sans per il testo, una parola in Cormorant corsivo per tavola, JetBrains Mono per codice e dati.

Riferimenti locali: `corsi/security-awareness/sistema/montaggio.md`, `produzione/src/ds/tokens.ts`, `produzione/src/ds/components/Lavagna.tsx` e i fotogrammi del modulo 5 nella repo DCS Academy. Si adatta il registro di spiegazione su carta, con le stesse famiglie tipografiche e gerarchie, a immagini statiche.

| Tavola | Utilità |
| :--- | :--- |
| `hero.svg` | Associa ciascuna cartella annuale ai temi che contiene. |
| `anno-3.svg` | Spiega la conversione 13 → 1101 del programma C `dectobin.c`. |
| `anno-4.svg` | Mostra l’ereditarietà delle classi reali di Biblioteca. |
| `anno-5.svg` | Segue richiesta, lettura del file e risposta di ServerWebStatico. |
| `percorso.svg` | Distribuisce la history importata per mese e anno scolastico. |
| `linguaggi.svg` | Confronta il materiale presente per linguaggio, con conteggi e percentuali. |
| `confluenza.svg` | Indica gli anni e le aree in cui ritrovare ciascuna sorgente originale. |

## Rigenerazione

Dalla radice della repository, con Python e [uv](https://docs.astral.sh/uv/):

```bash
uv run --with fonttools --with brotli python .github/readme/genera.py
```

I font WOFF2 sono in `font/`, insieme alla [licenza OFL e alle attribuzioni](font/OFL.txt). Il generatore istanzia i pesi e converte i glifi in tracciati: gli SVG non richiedono font installati, font web o servizi esterni. Le immagini sono statiche e hanno titolo e descrizione; il README fornisce descrizioni alternative e collegamenti agli esempi. Le etichette dettagliate si consultano ingrandendo l’immagine; percorsi ed esempi restano disponibili anche come testo nel README.

Non ci sono icone generiche, fondali luminosi o una tavola finale ornamentale. I diagrammi sono semplificazioni didattiche verificate sui file collegati: non sostituiscono il codice completo.

## Dati e limiti

- **Commit:** fotografia della history importata prima del 30 ottobre 2026. Sono esclusi i commit di assemblaggio, importazione e documentazione di quel giorno e quelli successivi. Totale: 353; per anno scolastico: 94, 237, 22. Il grafico usa la data autore e settembre come inizio dell’anno.
- **Sorgenti:** 9 repository e 3 cartelle locali. La tabella `FONTI` conserva i conteggi originali dopo la pulizia della history, senza i commit di unificazione.
- **File:** file tracciati da Git nelle tre cartelle annuali; le grafiche del README sono escluse. I file nuovi entrano nel conteggio dopo `git add`.
- **Linguaggi:** righe non vuote dei file tracciati con estensione riconosciuta, inclusi commenti e markup. Il filtro `GENERATI` esclude cartelle di piattaforma Flutter, dipendenze, build, docs e file minificati riconoscibili dal percorso. Non attribuisce la paternità del codice e non rileva automaticamente ogni file generato.

Le statistiche sono statiche: rieseguire il generatore per aggiornare file e linguaggi. La history importata resta una fotografia dell’unificazione; per trasformarla in un grafico dell’attività corrente occorre aggiornare anche il filtro delle date e le relative didascalie.
