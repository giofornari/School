# Server Web Statico

Autore: **Giordano Fornari**

Server web statico scritto in Node.js usando solo i moduli nativi (`http`, `fs`, `path`), senza Express.

## Struttura

```
ServerWebStatico/
├── server.js          # il server
├── public/            # pagine HTML
│   ├── index.html     # home, servita su "/"
│   ├── pagina1.html   # pagina con l'immagine della montagna
│   ├── pagina2.html   # pagina con l'immagine del mare
│   └── 404.html       # pagina mostrata quando una risorsa non esiste
├── css/
│   └── style.css      # foglio di stile, servito su /css/style.css
└── img/
    ├── montagna.png
    └── mare.jpg
```

## Avvio

```bash
cd ServerWebStatico
node server.js
```

Poi apri <http://localhost:3000>.

## Come funziona

| Richiesta              | Cartella  | Risposta                         |
|------------------------|-----------|----------------------------------|
| `/`                    | `public/` | `index.html` (200)               |
| `/pagina1.html`        | `public/` | pagina HTML (200)                |
| `/css/style.css`       | `css/`    | foglio di stile (200)            |
| `/img/montagna.png`    | `img/`    | immagine (200)                   |
| `/qualcosa-che-non-c-e`| —         | `public/404.html` con codice 404 |

Il `Content-Type` viene scelto in base all'estensione del file (`.html`, `.css`, `.png`, `.jpg`, ...).
Le richieste che provano a uscire dalle cartelle (es. `/css/..%2F..%2Fserver.js`) vengono bloccate con un 404.
Ogni richiesta viene stampata in console con il suo codice di risposta.
