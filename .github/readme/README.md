# Grafiche di School

16 SVG: copertina, quattro infografiche, tre testate annuali, sette icone e chiusura. Palette petrolio/turchese/verde, onde di luce, Poppins e icone lineari riprendono il lavoro iniziato da Claude sullo stile DCS Academy.

## Rigenerazione

Dalla radice della repository, con Python e [uv](https://docs.astral.sh/uv/):

```bash
uv run --with fonttools --with brotli python .github/readme/genera.py
```

I font sono già in `font/`, insieme alla [licenza OFL](font/Poppins-OFL.txt). Gli SVG incorporano un sottoinsieme WOFF2: non richiedono font installati o servizi esterni. Le immagini sono statiche e hanno un titolo; il README fornisce descrizioni alternative e collegamenti testuali.

## Dati e limiti

- **Commit:** fotografia della history importata prima del 30 ottobre 2026. Sono esclusi i commit di assemblaggio, importazione e documentazione di quel giorno e quelli successivi. Totale: 353; per anno scolastico: 94, 237, 22. Il grafico usa la data autore e settembre come inizio dell’anno.
- **Sorgenti:** 9 repository e 3 cartelle locali. La tabella `FONTI` conserva i conteggi originali dopo la pulizia della history, senza i commit di unificazione.
- **File:** file tracciati da Git nelle tre cartelle annuali; le grafiche del README sono escluse. I file nuovi entrano nel conteggio dopo `git add`.
- **Linguaggi:** righe non vuote dei file tracciati con estensione riconosciuta, inclusi commenti e markup. Il filtro `GENERATI` esclude cartelle di piattaforma Flutter, dipendenze, build, docs e file minificati riconoscibili dal percorso. Non attribuisce la paternità del codice e non rileva automaticamente ogni file generato.

Le statistiche sono statiche: rieseguire il generatore per aggiornare file e linguaggi. La history importata resta una fotografia dell’unificazione; per trasformarla in un grafico dell’attività corrente occorre aggiornare anche il filtro delle date e le relative didascalie.
