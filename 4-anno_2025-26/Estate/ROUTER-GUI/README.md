# ROUTER-GUI

Simulatore grafico di un router IPv4 e della sua Tabella di Instradamento (TDI), fatto in JavaScript per il progetto di Reti.

Dalla pagina si vede la TDI completa, si aggiungono ed eliminano route e interfacce, e si salva o carica la configurazione da file. Scrivendo un IP di destinazione il programma confronta l'IP con ogni route (IP AND mask), sceglie con il Longest Prefix Match e colora la tabella: in verde la route scelta, in ambra i fallback numerati, barrate le route che passano da un'interfaccia down. Sotto la tabella c'è il motivo della scelta.

Versione online: https://bigbrodyg.github.io/ROUTER-GUI/

## Avvio in locale

Serve Node.js. I moduli ES non partono aprendo `index.html` con doppio click, quindi la pagina va servita da un server locale.

```bash
npm install
npm run build
npx serve .
```

Poi si apre l'indirizzo che stampa `serve` (di solito http://localhost:3000). Mentre si modificano le classi CSS conviene lasciare `npm run dev` acceso in un altro terminale, così Tailwind rigenera `assets/styles.css` a ogni salvataggio.

## Formato della configurazione

Il pulsante "salva su file" scarica `router-config.json`, che si può ricaricare con "carica da file". Un esempio completo è in [esempi/router-esempio.json](esempi/router-esempio.json).

```json
{
    "name": "R1",
    "interfaces": [
        { "name": "eth0", "ip": "192.168.1.1", "mask": "255.255.255.0", "up": true }
    ],
    "routes": [
        { "network": "192.168.1.0", "mask": "255.255.255.0", "nextHop": null, "iface": "eth0", "metric": 0 },
        { "network": "0.0.0.0", "mask": "0.0.0.0", "nextHop": "192.168.1.254", "iface": "eth0", "metric": 1 }
    ]
}
```

`nextHop` vale `null` per le reti direttamente connesse. `iface` è il nome di un'interfaccia presente nella lista `interfaces`, e `metric` è un intero da 0 in su. Il file viene caricato solo se è tutto valido: al primo errore la configurazione attuale resta com'è e compare il messaggio con la posizione, per esempio `route 3: netmask non contigua: 255.0.255.0`.

Ogni modifica viene salvata anche nel `localStorage` del browser, quindi ricaricando la pagina si ritrova l'ultima configurazione. "ripristina esempio" torna al file di esempio.

## Documenti

- [docs/UML.md](docs/UML.md): diagramma delle classi
- [docs/RELAZIONE.md](docs/RELAZIONE.md): relazione tecnica
