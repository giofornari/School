# Scheletro da memoria: login in Node.js

È `server.js` senza commenti, nell'ordine in cui lo scrivi. Ogni riga di codice qui sotto è identica a una di `server.js` o `index.html` (lo controlla `node test/verifica.js`).
Tempo indicativo: HTML 5 minuti, server 25 minuti, prova con browser 5 minuti.

## 0 · Prima di scrivere (30 secondi)
Fissa i nomi e non cambiarli più: rotta `/login`, campi `nome` e `pass`, max 30 caratteri, utente `mario` / `Rossi2026`.

## 1 · index.html
```html
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
    <link rel="stylesheet" href="/stile.css">
</head>
<body>
    <main>
        <h1>Login</h1>
        <form action="/login" method="POST">
            <label for="nome">Username</label>
            <input type="text" id="nome" name="nome" value="" maxlength="30" required>
            <label for="pass">Password</label>
            <input type="password" id="pass" name="pass" maxlength="30" required>
            <button type="submit">Accedi</button>
        </form>
    </main>
</body>
</html>
```
`for` = `id` (il label clicca il campo), `name` = la chiave che arriva al server.

## 2 · require e costanti
```js
const http = require("http");
const fs = require("fs");
const path = require("path");
const qs = require("querystring");

const hostname = "127.0.0.1";
const port = 3000;
const MAX_BODY = 1024;
const MAX_CAMPO = 30;

const mimeTypes = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8'
};

const allowedURLPaths = {
    '/': './index.html',
    '/stile.css': './stile.css'
};

const utenti = [
    { nome: "mario", pass: "Rossi2026" },
    { nome: "anna", pass: "Verdi2026" }
];
```

## 3 · escapeHtml e pagine generate
```js
function escapeHtml(testo) {
    return String(testo)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
}
```
`&` va per **primo**, se no rovini le entità appena create.

`pagina(titolo, contenuto)` restituisce il template HTML intero con `${titolo}` e `${contenuto}`.
`paginaLogin(messaggio, nome)` è il form di index.html con due differenze:
```html
        <p class="errore">${messaggio}</p>
            <input type="text" id="nome" name="nome" value="${escapeHtml(nome)}" maxlength="30" required>
```
Il campo password resta **senza** `value`.

## 4 · requestHandler: metodo, routing, 404/405
```js
function requestHandler(req, res) {
    console.log(req.method + " " + req.url);

    if (req.url === "/login") {
        if (req.method !== "POST") {
            res.writeHead(405, { 'Content-Type': 'text/plain; charset=utf-8', 'Allow': 'POST' });
            res.end("Metodo non consentito");
            return;
        }
        riceviLogin(req, res);
        return;
    }

    if (req.method !== "GET" && req.method !== "HEAD") {
        res.writeHead(405, { 'Content-Type': 'text/plain; charset=utf-8', 'Allow': 'GET, HEAD' });
        res.end("Metodo non consentito");
        return;
    }

    if (allowedURLPaths.hasOwnProperty(req.url)) {
        inviaFileStatico(res, allowedURLPaths[req.url]);
    } else {
        res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
        res.end("Pagina non trovata");
    }
}
```

## 5 · File statici (stream + pipe)
```js
function inviaFileStatico(res, filePath) {
    const contentType = mimeTypes[path.extname(filePath)] || 'application/octet-stream';
    const fileStream = fs.createReadStream(path.join(__dirname, filePath));

    fileStream.on('open', function () {
        res.writeHead(200, { 'Content-Type': contentType });
        fileStream.pipe(res);
    });

    fileStream.on('error', function (error) {
        console.error("Errore nella lettura del file: " + error.message);
        if (!res.headersSent) {
            if (error.code === 'ENOENT') {
                res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
                res.end("File non trovato");
            } else {
                res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
                res.end("Errore interno del server");
            }
        } else {
            res.destroy();
        }
    });
}
```

## 6 · Ricezione POST
```js
function riceviLogin(req, res) {
    let body = "";
    let troppoGrande = false;

    req.on('data', function (data) {
        if (body.length + data.length > MAX_BODY) {
            troppoGrande = true;
        } else {
            body += data;
        }
    });

    req.on('end', function () {
        if (troppoGrande) {
            res.writeHead(413, { 'Content-Type': 'text/plain; charset=utf-8' });
            res.end("Dati troppo grandi");
            return;
        }

        const post = qs.parse(body);
        const nome = String(post.nome || "").trim();
        const pass = String(post.pass || "");
```

## 7 · Validazione e controllo utenti
```js
        if (nome === "" || pass === "") {
            res.writeHead(400, { 'Content-Type': 'text/html; charset=utf-8' });
            res.end(paginaLogin("Compila username e password.", nome));
            return;
        }

        if (nome.length > MAX_CAMPO || pass.length > MAX_CAMPO) {
            res.writeHead(400, { 'Content-Type': 'text/html; charset=utf-8' });
            res.end(paginaLogin("Username o password troppo lunghi.", ""));
            return;
        }

        const utente = utenti.find(function (u) {
            return u.nome === nome && u.pass === pass;
        });
```

## 8 · Risposte
```js
        if (!utente) {
            res.writeHead(401, { 'Content-Type': 'text/html; charset=utf-8' });
            res.end(paginaLogin("Username o password errati.", nome));
            return;
        }

        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(pagina("Benvenuto", `<h1>Benvenuto ${escapeHtml(utente.nome)}!</h1>
        <p><a href="/">Esci</a></p>`));
    });
}
```

## 9 · Avvio
```js
const server = http.createServer(requestHandler);
server.listen(port, hostname, function () {
    console.log(`Server running at http://${hostname}:${port}/`);
});
```
Prova: `node server.js`, poi http://127.0.0.1:3000, un login giusto, uno sbagliato, uno vuoto.

## I 10 errori che costano punti
1. **Nessun `res.end()` su un ramo**: il browser gira all'infinito. Ogni `writeHead` ha il suo `end` (o il `pipe`).
2. **`writeHead` dopo `end` o due risposte** (manca il `return` dopo un errore): `ERR_HTTP_HEADERS_SENT` e il server muore.
3. **`qs.parse(body)` fuori da `on('end')`**: il body è ancora vuoto, perché `data` arriva dopo.
4. **Niente 405**: `/login` in GET deve dire 405, non fare il login né rispondere 404.
5. **Nessun limite al body**: chiunque ti manda 1 GB e il server finisce la RAM. Senza 413 il controllo è a metà.
6. **Fidarsi di `required`/`maxlength`**: con curl si aggirano. Trim, vuoti e lunghezza vanno ricontrollati sul server, con 400.
7. **Messaggio diverso per utente e password** ("utente inesistente"): così dici a un attaccante quali username esistono. Un solo 401.
8. **Nome stampato senza escape** (`${nome}` crudo): `<script>` nel campo diventa codice, cioè XSS. Vale anche per il `value` del form.
9. **Content-Type senza `charset=utf-8`** o sbagliato (`text/plain` per l'HTML): accenti rotti, oppure la pagina appare come testo.
10. **`readFileSync` nel gestore** al posto dello stream: blocca tutto il server (slide 26: "non è corretta"). E i nomi non coincidono: `name="pass"` nel form ma `post.password` nel server, così arriva `undefined`.
