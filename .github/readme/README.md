# Sorgenti delle grafiche

Il README presenta il percorso dei tre anni a chi arriva nella repository: quattro banner orizzontali e una mappa della progressione. I banner misurano 1200 × 300 e 1200 × 240 px; la mappa misura 1200 × 390 px. Non contengono esempi di singoli progetti o statistiche della history.

Lo stile riprende la lavagna del corso Security Awareness: carta `#F4F7FA`, quadretti `#DCE3EC`, inchiostro `#0D0D26`, tratto navy `#164573`, evidenziatore `#FFE27A`, Instrument Sans e Cormorant corsivo. Riferimenti: `sistema/montaggio.md`, `produzione/src/ds/tokens.ts` e `produzione/src/ds/components/Lavagna.tsx` nella cartella del corso DCS Academy.

I font locali e le attribuzioni sono in [font/OFL.txt](font/OFL.txt). I glifi sono convertiti in tracciati per mantenere la tipografia nei renderer SVG. Ogni immagine include titolo e descrizione; il README contiene anche testo alternativo.

Per aggiornare le grafiche dalla radice della repository:

```bash
uv run --with fonttools --with brotli python .github/readme/genera.py
```

Il generatore verifica l’esistenza delle cartelle annuali e la validità XML degli SVG. Se cambiano immagini già pubblicate, aggiornare anche il nome del file e il relativo riferimento nel README per evitare la cache raw di GitHub.
