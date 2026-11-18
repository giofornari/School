# Stile del prof (slide 18-54 + tests/riferimenti di node-al-pettine)

1. **CommonJS**: `const http = require("http");` poi `fs`, `path`, `qs = require("querystring")` (slide 18, 31, 51). Niente npm, niente Express.
2. **Costanti in testa**: `const hostname = "127.0.0.1";` e `const port = 3000;` (slide 18, 31).
3. **`mimeTypes`**: oggetto estensione → tipo, chiavi tra apici `'.html': 'text/html; charset=utf-8'` (slide 27, 31).
4. **`allowedURLPaths`**: URL → file con `./` davanti; tutto il resto è rifiutato (slide 31).
5. **`function requestHandler(req, res)`**: funzione con nome, non arrow, passata a `http.createServer(requestHandler)` (slide 18, 23).
6. Prima riga del gestore: `console.log(req.url)` (o `req.method + ' ' + req.url` nei riferimenti).
7. **Metodo prima di tutto**: `if (req.method !== 'GET' && req.method !== 'HEAD')` → **405** e `return` (slide 32, 51).
8. **Routing** con `allowedURLPaths.hasOwnProperty(req.url)`, altrimenti **404** "Pagina non trovata" (slide 32, 35).
9. **Statici con stream**: `fs.createReadStream(filePath)`, su `'open'` → `writeHead(200)` + `fileStream.pipe(res)` (slide 35).
10. Su `'error'`: se `!res.headersSent` → `ENOENT` 404, altro 500 "Errore interno del server"; se no `res.destroy()` (slide 35-36).
11. **POST**: `let body = "";` → `request.on('data', function (data) { body += data; })` → `on('end')` → `qs.parse(body)` (slide 51).
12. Nomi: `body`, `post` (risultato di qs.parse), `data` (chunk), `error`, `fileStream`, `filePath`, `contentType` (slide 35, 51).
13. Callback scritte `function (...) {` (slide). Le arrow solo dove le usa lui: `listen(..., () => ...)` (slide 29, 51).
14. **Header**: `res.writeHead(stato, { 'Content-Type': '...' })` poi `res.end(...)`; `end()` chiude sempre, va su ogni ramo (slide 26, 43).
15. **charset=utf-8** su text/html e text/plain: senza, "è" diventa spazzatura (slide 23).
16. **Codici**: 200 ok, 400 parametri mancanti, 401 credenziali non valide, 404, 405, 500 (slide 32, 44, 51). 413 non è sulle slide: è RFC 9110, lo aggiungo io.
17. **Form**: `action="/recuperadati"` o simile, `method="POST"`, `<label for>` + `id`, `name="nome"` / `name="pass"` (slide 52).
18. **Pagine generate** con template literal `` `...${nome}...` `` (slide 46); nei riferimenti c'è `paginaRisposta(titolo, contenuto)`.
19. **Validazione** dei riferimenti: `String(dati.x || '').trim()`, poi `=== ''` → messaggio, poi regola; errori in un array (contatti-*.server.js).
20. `listen(port, hostname, function () { console.log(\`Server running at http://${hostname}:${port}/\`); })` (slide 18).
21. Indentazione 4 spazi, doppi apici per require, apici singoli dentro gli oggetti.

**Cosa i riferimenti NON fanno e io sì** (lo chiedi tu, e il prof lo premia a voce):
- escape dell'output: i riferimenti stampano `${dati[campo]}` crudo, quindi XSS;
- 405 sulla rotta del form;
- limite sul body (413);
- `path.join(__dirname, ...)`, che sta nella slide 31 ma che lui non usa nei server.
