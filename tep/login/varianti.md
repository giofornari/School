# Varianti della soluzione base

Ogni variante è un diff rispetto a `server.js` / `index.html` di questa cartella (righe con `-` tolte, `+` aggiunte). Le ho applicate e provate con curl una per una; l'esito è sotto ogni titolo.

Quando usarle: se la consegna dice "metodo GET", "usa readFile", "gli utenti stanno in un file" o "la pagina di benvenuto è un file HTML". Altrimenti scrivi la base.

## 1 · GET con il modulo `url`

Con GET il form non ha body: i campi arrivano nella querystring. Quindi spariscono `querystring`, `on('data')`/`on('end')` e il 413, e la validazione va in una funzione che riceve la query. Il routing va fatto su `pathname`, perché `req.url` contiene anche `?nome=...`.

**Da dire a voce**: la password finisce nell'URL, nella cronologia e nei log del server (slide 46). Per un login è la scelta sbagliata, va bene solo se la consegna la impone. `url.parse` è deprecato: l'alternativa moderna è ``new URL(req.url, `http://${req.headers.host}`)`` con `searchParams.get("nome")` (slide 46).

Provata: login giusto 200, password errata 401, campi vuoti 400, POST su /login 405, URL inesistente 404, `<script>` escapato.

```diff
--- a/index.html
+++ b/index.html
@@ -9,7 +9,7 @@
 <body>
     <main>
         <h1>Login</h1>
-        <form action="/login" method="POST">
+        <form action="/login" method="GET">
             <label for="nome">Username</label>
             <input type="text" id="nome" name="nome" value="" maxlength="30" required>
             <label for="pass">Password</label>
--- a/server.js
+++ b/server.js
@@ -2,13 +2,11 @@
 const http = require("http");
 const fs = require("fs");
 const path = require("path");
-const qs = require("querystring");
+const url = require("url");
 
 const hostname = "127.0.0.1";
 const port = 3000;
 
-// tetto al body del POST: senza, un client può riempire la RAM del server
-const MAX_BODY = 1024;
 // stesso valore del maxlength nel form: il controllo del browser si aggira con curl
 const MAX_CAMPO = 30;
 
@@ -61,7 +59,7 @@
 function paginaLogin(messaggio, nome) {
     return pagina("Login", `<h1>Login</h1>
         <p class="errore">${messaggio}</p>
-        <form action="/login" method="POST">
+        <form action="/login" method="GET">
             <label for="nome">Username</label>
             <input type="text" id="nome" name="nome" value="${escapeHtml(nome)}" maxlength="30" required>
             <label for="pass">Password</label>
@@ -98,73 +96,55 @@
     });
 }
 
-function riceviLogin(req, res) {
-    let body = "";
-    let troppoGrande = false;
-
-    // il body arriva a pezzi (chunk): li accumulo finché stanno sotto il tetto
-    req.on('data', function (data) {
-        if (body.length + data.length > MAX_BODY) {
-            troppoGrande = true;
-        } else {
-            body += data;
-        }
-    });
-
-    // 'end' scatta una volta sola, quando il body è arrivato tutto
-    req.on('end', function () {
-        if (troppoGrande) {
-            res.writeHead(413, { 'Content-Type': 'text/plain; charset=utf-8' });
-            res.end("Dati troppo grandi");
-            return;
-        }
+// con GET non c'è body: i dati sono già nella querystring, niente 'data'/'end'
+function controllaLogin(res, query) {
+    // || "" copre il campo mancante; la password non si trimma: lo spazio può farne parte
+    const nome = String(query.nome || "").trim();
+    const pass = String(query.pass || "");
+
+    // validazione lato server: il required del browser non basta
+    if (nome === "" || pass === "") {
+        res.writeHead(400, { 'Content-Type': 'text/html; charset=utf-8' });
+        res.end(paginaLogin("Compila username e password.", nome));
+        return;
+    }
 
-        const post = qs.parse(body);
-        // || "" copre il campo mancante; la password non si trimma: lo spazio può farne parte
-        const nome = String(post.nome || "").trim();
-        const pass = String(post.pass || "");
-
-        // validazione lato server: il required del browser non basta
-        if (nome === "" || pass === "") {
-            res.writeHead(400, { 'Content-Type': 'text/html; charset=utf-8' });
-            res.end(paginaLogin("Compila username e password.", nome));
-            return;
-        }
+    if (nome.length > MAX_CAMPO || pass.length > MAX_CAMPO) {
+        res.writeHead(400, { 'Content-Type': 'text/html; charset=utf-8' });
+        res.end(paginaLogin("Username o password troppo lunghi.", ""));
+        return;
+    }
 
-        if (nome.length > MAX_CAMPO || pass.length > MAX_CAMPO) {
-            res.writeHead(400, { 'Content-Type': 'text/html; charset=utf-8' });
-            res.end(paginaLogin("Username o password troppo lunghi.", ""));
-            return;
-        }
+    const utente = utenti.find(function (u) {
+        return u.nome === nome && u.pass === pass;
+    });
 
-        const utente = utenti.find(function (u) {
-            return u.nome === nome && u.pass === pass;
-        });
-
-        // messaggio unico: non dico quale dei due è sbagliato
-        if (!utente) {
-            res.writeHead(401, { 'Content-Type': 'text/html; charset=utf-8' });
-            res.end(paginaLogin("Username o password errati.", nome));
-            return;
-        }
+    // messaggio unico: non dico quale dei due è sbagliato
+    if (!utente) {
+        res.writeHead(401, { 'Content-Type': 'text/html; charset=utf-8' });
+        res.end(paginaLogin("Username o password errati.", nome));
+        return;
+    }
 
-        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
-        res.end(pagina("Benvenuto", `<h1>Benvenuto ${escapeHtml(utente.nome)}!</h1>
-        <p><a href="/">Esci</a></p>`));
-    });
+    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
+    res.end(pagina("Benvenuto", `<h1>Benvenuto ${escapeHtml(utente.nome)}!</h1>
+    <p><a href="/">Esci</a></p>`));
 }
 
 function requestHandler(req, res) {
     console.log(req.method + " " + req.url);
-
-    if (req.url === "/login") {
-        // il login si accetta solo in POST: con GET la password finirebbe nell'URL
-        if (req.method !== "POST") {
-            res.writeHead(405, { 'Content-Type': 'text/plain; charset=utf-8', 'Allow': 'POST' });
+    // true: la query arriva già come oggetto { nome: ..., pass: ... } (slide 46)
+    const oggettourl = url.parse(req.url, true);
+    const pathname = oggettourl.pathname;
+
+    if (pathname === "/login") {
+        // ATTENZIONE: con GET la password resta nell'URL, nella cronologia e nei log
+        if (req.method !== "GET") {
+            res.writeHead(405, { 'Content-Type': 'text/plain; charset=utf-8', 'Allow': 'GET' });
             res.end("Metodo non consentito");
             return;
         }
-        riceviLogin(req, res);
+        controllaLogin(res, oggettourl.query);
         return;
     }
 
@@ -175,8 +155,8 @@
         return;
     }
 
-    if (allowedURLPaths.hasOwnProperty(req.url)) {
-        inviaFileStatico(res, allowedURLPaths[req.url]);
+    if (allowedURLPaths.hasOwnProperty(pathname)) {
+        inviaFileStatico(res, allowedURLPaths[pathname]);
     } else {
         res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
         res.end("Pagina non trovata");
```

## 2a · File statici con `readFile`

La versione della slide 32: legge tutto il file in memoria e poi lo manda. Più corta, ma con un file grande occupa tutta la RAM (slide 34). Sparisce la distinzione 404/500 perché `readFile` non ha l'evento `open`: qualunque errore è 500, dato che l'URL era già in `allowedURLPaths`.

Provata: index 200, stile.css 200 con `text/css; charset=utf-8`, 622 byte su 622.

```diff
--- a/server.js
+++ b/server.js
@@ -71,29 +71,15 @@
 }
 
 function inviaFileStatico(res, filePath) {
-    const contentType = mimeTypes[path.extname(filePath)] || 'application/octet-stream';
-    // __dirname: il file si trova anche se avvio node da un'altra cartella
-    const fileStream = fs.createReadStream(path.join(__dirname, filePath));
-
-    // il 200 parte solo quando il file è davvero aperto
-    fileStream.on('open', function () {
-        res.writeHead(200, { 'Content-Type': contentType });
-        fileStream.pipe(res);
-    });
-
-    fileStream.on('error', function (error) {
-        console.error("Errore nella lettura del file: " + error.message);
-        if (!res.headersSent) {
-            if (error.code === 'ENOENT') {
-                res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
-                res.end("File non trovato");
-            } else {
-                res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
-                res.end("Errore interno del server");
-            }
+    // readFile carica tutto il file in RAM: va bene per file piccoli (slide 32)
+    fs.readFile(path.join(__dirname, filePath), function (error, data) {
+        if (error) {
+            console.error("Errore nella lettura del file: " + error.message);
+            res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
+            res.end("Errore interno del server");
         } else {
-            // header già partiti: chiudo la connessione per non lasciare il client in attesa
-            res.destroy();
+            res.writeHead(200, { 'Content-Type': mimeTypes[path.extname(filePath)] || 'application/octet-stream' });
+            res.end(data);
         }
     });
 }
```

## 2b · File statici con gli eventi `data` / `end`

La versione "a mano" della slide 36: al posto di `pipe` scrivi tu ogni chunk con `res.write` e chiudi con `res.end` su `'end'`. Il gestore `'error'` resta uguale.

Provata: index 200, stile.css 200, 622 byte su 622.

```diff
--- a/server.js
+++ b/server.js
@@ -78,7 +78,16 @@
     // il 200 parte solo quando il file è davvero aperto
     fileStream.on('open', function () {
         res.writeHead(200, { 'Content-Type': contentType });
-        fileStream.pipe(res);
+    });
+
+    // ogni chunk letto va subito al client (slide 36)
+    fileStream.on('data', function (chunk) {
+        res.write(chunk);
+    });
+
+    // fine file: senza pipe, end() lo chiami tu
+    fileStream.on('end', function () {
+        res.end();
     });
 
     fileStream.on('error', function (error) {
```

## 3 · Utenti letti da `utenti.json` con `fs`

`utenti.json`:

```json
[
    { "nome": "mario", "pass": "Rossi2026" },
    { "nome": "anna", "pass": "Verdi2026" }
]
```

Il file si rilegge a ogni login con `fs.readFile` (asincrono, come vuole il prof), e `JSON.parse` sta in un `try` perché un JSON rotto lancerebbe un'eccezione e farebbe cadere il server. Il file non va mai in `allowedURLPaths`.

Provata: login giusto 200, password errata 401, GET /utenti.json 404, file mancante 500, JSON rotto 500.

```diff
--- a/server.js
+++ b/server.js
@@ -24,11 +24,8 @@
     '/stile.css': './stile.css'
 };
 
-// utenti abilitati (in verifica basta un array, come nella slide 48)
-const utenti = [
-    { nome: "mario", pass: "Rossi2026" },
-    { nome: "anna", pass: "Verdi2026" }
-];
+// utenti.json NON va in allowedURLPaths: chiunque scaricherebbe le password
+const fileUtenti = path.join(__dirname, "utenti.json");
 
 // trasforma i caratteri speciali in entità: <script> diventa testo, non codice (niente XSS)
 function escapeHtml(testo) {
@@ -137,20 +134,35 @@
             return;
         }
 
-        const utente = utenti.find(function (u) {
-            return u.nome === nome && u.pass === pass;
-        });
+        // letto a ogni login: se modifichi il file non serve riavviare il server
+        fs.readFile(fileUtenti, "utf8", function (error, testo) {
+            let utenti;
+            try {
+                if (error) throw error;
+                utenti = JSON.parse(testo);
+            } catch (e) {
+                // file mancante o JSON rotto: è colpa del server, non dell'utente
+                console.error("utenti.json illeggibile: " + e.message);
+                res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
+                res.end("Errore interno del server");
+                return;
+            }
 
-        // messaggio unico: non dico quale dei due è sbagliato
-        if (!utente) {
-            res.writeHead(401, { 'Content-Type': 'text/html; charset=utf-8' });
-            res.end(paginaLogin("Username o password errati.", nome));
-            return;
-        }
+            const utente = utenti.find(function (u) {
+                return u.nome === nome && u.pass === pass;
+            });
+
+            // messaggio unico: non dico quale dei due è sbagliato
+            if (!utente) {
+                res.writeHead(401, { 'Content-Type': 'text/html; charset=utf-8' });
+                res.end(paginaLogin("Username o password errati.", nome));
+                return;
+            }
 
-        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
-        res.end(pagina("Benvenuto", `<h1>Benvenuto ${escapeHtml(utente.nome)}!</h1>
-        <p><a href="/">Esci</a></p>`));
+            res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
+            res.end(pagina("Benvenuto", `<h1>Benvenuto ${escapeHtml(utente.nome)}!</h1>
+            <p><a href="/">Esci</a></p>`));
+        });
     });
 }
 
```

## 4 · Pagina di benvenuto servita da file

`benvenuto.html` (stessa cartella, **non** in `allowedURLPaths`, altrimenti si vedrebbe `{{nome}}`):

```html
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Benvenuto</title>
    <link rel="stylesheet" href="/stile.css">
</head>
<body>
    <main>
        <h1>Benvenuto {{nome}}!</h1>
        <p><a href="/">Esci</a></p>
    </main>
</body>
</html>
```

Il server legge il file e sostituisce `{{nome}}` con il nome **escapato**. `replace` riceve una funzione e non una stringa: in una stringa di sostituzione `$&` e `$1` hanno un significato speciale, e un nome che li contiene sporcherebbe la pagina.

Provata: login giusto 200 con `<h1>Benvenuto mario!</h1>`, GET /benvenuto.html 404.

```diff
--- a/server.js
+++ b/server.js
@@ -148,9 +148,19 @@
             return;
         }
 
-        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
-        res.end(pagina("Benvenuto", `<h1>Benvenuto ${escapeHtml(utente.nome)}!</h1>
-        <p><a href="/">Esci</a></p>`));
+        // la pagina è un file con il segnaposto {{nome}}; non è in allowedURLPaths
+        fs.readFile(path.join(__dirname, "benvenuto.html"), "utf8", function (error, html) {
+            if (error) {
+                res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
+                res.end("Errore interno del server");
+                return;
+            }
+            res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
+            // funzione come secondo argomento: un $ nel nome non viene interpretato da replace
+            res.end(html.replace("{{nome}}", function () {
+                return escapeHtml(utente.nome);
+            }));
+        });
     });
 }
 
```
