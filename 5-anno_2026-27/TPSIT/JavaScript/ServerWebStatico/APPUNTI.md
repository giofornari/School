# server.js spiegato

**Come usarlo:** cerca la riga nella tabella qui sotto e clicca. Ogni sezione si apre con **⚡**, la frase da dire a voce, e sotto c'è il dettaglio.
In VS Code: `Ctrl+Shift+V` apre l'anteprima, il pannello **Outline** mostra le sezioni.

<a id="indice"></a>

## Trova per riga

| Righe | Cosa c'è | Sezione |
|---|---|---|
| 1-5 | `require` dei moduli | [1. Import](#1-import) |
| 7-16 | `PORT`, dizionario `tipi` | [2. Costanti](#2-costanti) |
| 18-21 | `errore404` | [3. errore404](#3-errore404) |
| 25-27 | `finito` | [4. finito](#4-finito) |
| 30-43 | `inviaPezzo` (video) | [5. inviaPezzo](#5-inviapezzo) |
| 45 | `http.createServer` | [6. createServer](#6-createserver) |
| 49 | `/` → `/index.html` | [7. Home](#7-home) |
| 52 | blocco di `..` | [8. Sicurezza](#8-sicurezza) |
| 55-57 | da URL a file | [9. Da URL a file](#9-da-url-a-file) |
| 60-61 | `fs.stat` | [10. fs.stat](#10-fsstat) |
| 63 | tipo MIME | [11. Tipo di file](#11-tipo-di-file) |
| 66 | strada 1: Range | [12. Strada 1: Range](#12-strada-1-range) |
| 69-73 | strada 2: gzip | [13. Strada 2: gzip](#13-strada-2-gzip) |
| 76-77 | strada 3: il resto | [14. Strada 3: il resto](#14-strada-3-il-resto) |
| 81-83 | `server.listen` | [15. listen](#15-listen) |

**Concetti trasversali**
- [0. Il quadro generale](#0-il-quadro-generale)
- [16. Stream e pipeline](#16-stream-e-pipeline)
- [17. Perché .pipe lascia il file aperto](#17-perché-pipe-lascia-il-file-aperto)
- [18. Tre richieste dall'inizio alla fine](#18-tre-richieste-dallinizio-alla-fine)
- [19. Glossario](#19-glossario)
- [20. Codici e header HTTP](#20-codici-e-header-http)

---

## 0. Il quadro generale

> ⚡ **Prima scarto ciò che non va (`..`, file inesistente). Poi capisco cosa mi chiedono (tipo di file, Range, gzip). Infine scelgo il tubo giusto. Il file non viene mai caricato tutto in RAM.**

**Due momenti distinti**
- **All'avvio, una volta sola:** le righe 1-43 *definiscono* moduli, costanti e funzioni. La riga 45 *crea* il server, la riga 81 lo *accende*.
- **A ogni richiesta:** Node esegue la funzione `(req, res) => {…}` della riga 45.

È un programma **a eventi**: non va dall'alto in basso e finisce, ma reagisce quando arriva una richiesta.

**Il flusso di una richiesta**
```
richiesta → "/"? → contiene ".."? → percorso del file → fs.stat (esiste?) → tipo MIME
          → Range?  → 206 pezzo           (strada 1)
          → testo?  → 200 file→gzip→client (strada 2)
          → altro   → 200 file→client      (strada 3)
```

**Le uscite anticipate** (`return errore404`) stanno in cima. Le tre strade vanno dalla più specifica (Range) alla più generica (tutto il resto).

[↑ indice](#indice)

---

## 1. Import

[server.js:1-5](server.js#L1-L5)
```js
const http = require('http');
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');
const { pipeline } = require('stream');
```

> ⚡ **Moduli interni di Node, niente npm.**

| Modulo | Serve per | Cosa usi |
|---|---|---|
| `http` | Creare il server | `createServer` |
| `fs` | Il disco | `stat`, `createReadStream` |
| `path` | Costruire percorsi | `join`, `extname` |
| `zlib` | Comprimere | `createGzip` |
| `stream` | Collegare gli stream | `pipeline` |

- **`require('x')`** carica il modulo e restituisce un oggetto con dentro le funzioni.
- **`const { pipeline } = …`** è **destructuring**: prende solo `pipeline`. Equivale a `require('stream').pipeline`.

[↑ indice](#indice)

---

## 2. Costanti

[server.js:7-16](server.js#L7-L16)
```js
const PORT = 3000;
const tipi = { '.html': 'text/html; charset=utf-8', '.css': …, '.png': …, '.jpg': …, '.mp4': … };
```

> ⚡ **`tipi` è un dizionario che associa un'estensione a un tipo MIME. Il browser decide come mostrare un file guardando l'header `Content-Type`, non l'estensione.**

- **`PORT`**: la porta su cui il server ascolta, da cui l'indirizzo `localhost:3000`.
- **`charset=utf-8`**: serve a mostrare bene le lettere accentate.
- **Senza il tipo giusto:** un HTML etichettato `text/plain` verrebbe mostrato come testo grezzo.

[↑ indice](#indice)

---

## 3. errore404

[server.js:18-21](server.js#L18-L21)
```js
function errore404(res) {
    res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end('<h1>404 - Risorsa non trovata</h1>');
}
```

> ⚡ **Risponde "non trovato". È una funzione perché la uso in tre punti.**

- **`res.writeHead(codice, headers)`** manda il codice di stato e gli header. Si chiama **una volta sola**, prima del contenuto.
- **`res.end(testo)`** manda il contenuto e **chiude** la risposta. Senza `end` il browser resta in attesa per sempre.

[↑ indice](#indice)

---

## 4. finito

[server.js:25-27](server.js#L25-L27)
```js
function finito(err) {
    if (err) console.log('invio interrotto:', err.code);
}
```

> ⚡ **È la callback di `pipeline`. Viene chiamata quando l'invio finisce; se c'è stato un errore lo stampa. A quel punto `pipeline` ha già chiuso il file.**

- **Callback:** una funzione che non chiami tu. La passi a `pipeline`, che la chiamerà alla fine.
- **Invio andato bene:** `err` è `undefined` e non succede niente.
- **L'utente ha chiuso la pagina a metà:** `err.code` vale di solito `ERR_STREAM_PREMATURE_CLOSE`.

[↑ indice](#indice)

---

## 5. inviaPezzo

[server.js:30-43](server.js#L30-L43)
```js
function inviaPezzo(res, file, info, tipo, range) {
    const [a, b] = range.replace('bytes=', '').split('-');
    const inizio = Number(a);
    const fine = b ? Number(b) : info.size - 1;
    if (isNaN(inizio)) return errore404(res);

    res.writeHead(206, {
        'Content-Type': tipo,
        'Content-Length': fine - inizio + 1,
        'Content-Range': 'bytes ' + inizio + '-' + fine + '/' + info.size,
        'Accept-Ranges': 'bytes'
    });
    pipeline(fs.createReadStream(file, { start: inizio, end: fine }), res, finito);
}
```

> ⚡ **Quando sposti la barra del video, il browser chiede solo un pezzo del file. Leggo solo quei byte dal disco e rispondo 206.**

**Parametri**

| Nome | Cos'è |
|---|---|
| `res` | La risposta |
| `file` | Il percorso del file sul disco |
| `info` | Il risultato di `fs.stat` (serve `info.size`) |
| `tipo` | Il tipo MIME |
| `range` | L'header ricevuto, per esempio `"bytes=1000-1999"` |

**Passo 1: leggere l'header**

`"bytes=1000-1999"` → `.replace` → `"1000-1999"` → `.split('-')` → `["1000", "1999"]` → `a = "1000"`, `b = "1999"`

`const [a, b] = …` è destructuring di un array.

**Passo 2: trasformare in numeri**

| Header | `a` | `b` | inizio | fine |
|---|---|---|---|---|
| `bytes=0-999` | `"0"` | `"999"` | 0 | 999 |
| `bytes=50000-` | `"50000"` | `""` | 50000 | `info.size - 1` |
| `bytes=abc` | `"abc"` | – | NaN | → **404** |

- **`Number(a)`**: gli header sono testo, quindi i numeri vanno convertiti.
- **`b ? X : Y`**: operatore ternario. Se `b` è vuoto vale "falso", e quindi la fine è l'ultimo byte del file.
- **`- 1`**: i byte si contano da 0. Un file da 100 byte va dal byte 0 al byte 99.
- **`isNaN(inizio)`**: se l'header è scritto male, rispondo 404. Senza questo controllo `createReadStream` riceverebbe NaN e il server andrebbe in crash (`ERR_OUT_OF_RANGE`).

**Passo 3: gli header**
- **`206 Partial Content`**: "ti mando solo una parte".
- **`Content-Length: fine - inizio + 1`**: il **+1** c'è perché inizio e fine sono entrambi inclusi. Da 0 a 999 sono 1000 byte.
- **`Content-Range: bytes 0-999/87167`**: quale pezzo è, e su quanti byte totali.
- **`Accept-Ranges: bytes`**: "puoi chiedermi dei pezzi".

**Passo 4: mandare il pezzo**

`createReadStream(file, { start, end })` legge **solo** quei byte (`end` è incluso). `pipeline` li collega a `res`.

[↑ indice](#indice)

---

## 6. createServer

[server.js:45](server.js#L45)
```js
const server = http.createServer((req, res) => { … });
```

> ⚡ **Crea il server. La funzione che gli passo viene eseguita a ogni richiesta, sempre con due argomenti: `req`, cioè cosa chiede il browser, e `res`, cioè cosa rispondo.**

| | Cos'è | Cosa usi |
|---|---|---|
| **`req`** | La richiesta | `req.url`, per esempio `/img/mare.jpg`. `req.headers`, con i nomi **in minuscolo** |
| **`res`** | La risposta. È anche uno **stream scrivibile** | `writeHead`, `end`, e lo usi come fine del tubo |

`(req, res) => {…}` è una **arrow function**, una forma più corta di `function (req, res) {…}`.

[↑ indice](#indice)

---

## 7. Home

[server.js:46-49](server.js#L46-L49)
```js
let url = req.url;
if (url === '/') url = '/index.html';
```

> ⚡ **Il browser chiede `/`, ma sul disco quel file non esiste: lo sostituisco con `index.html`.**

Si usa `let` e non `const` perché il valore può cambiare.

[↑ indice](#indice)

---

## 8. Sicurezza

[server.js:52](server.js#L52)
```js
if (url.includes('..')) return errore404(res);
```

> ⚡ **Blocco il path traversal: con `/../server.js` uno uscirebbe da `public` e si leggerebbe il mio codice.**

- **`.includes('..')`**: `true` se il testo contiene `..`.
- **`return`**: uscita anticipata. Risponde 404 e ferma la funzione.
- **Perché il controllo sta prima di `path.join`:** `path.join` risolve i `..` da solo. Dopo non li vedresti più.

[↑ indice](#indice)

---

## 9. Da URL a file

[server.js:55-57](server.js#L55-L57)
```js
let file;
if (url.startsWith('/Css/')) file = path.join(__dirname, url);
else file = path.join(__dirname, 'public', url);
```

> ⚡ **Trasformo l'URL in un percorso sul disco: il CSS sta nella cartella `Css`, tutto il resto in `public`.**

- **`__dirname`**: la cartella in cui si trova `server.js`. Così il server funziona da qualunque cartella lo lanci.
- **`path.join`**: unisce i pezzi con il separatore giusto (`/` su Linux, `\` su Windows).
- **Esempi:** `/Css/style.css` → `…/Css/style.css`, mentre `/img/mare.jpg` → `…/public/img/mare.jpg`.
- Il disco non è ancora stato toccato: è solo una stringa.

[↑ indice](#indice)

---

## 10. fs.stat

[server.js:60-61](server.js#L60-L61)
```js
fs.stat(file, (err, info) => {
    if (err || !info.isFile()) return errore404(res);
```

> ⚡ **Chiedo al sistema operativo se il file esiste e quanto pesa, senza leggerlo. È asincrona: mentre il disco risponde, Node serve altri utenti.**

- **`err`**: c'è se il file non esiste (codice `ENOENT`).
- **`info.isFile()`**: è falso per una cartella, per esempio `/img`, e allora rispondo 404.
- **`info.size`**: la dimensione in byte, che serve per `Content-Length` e per il Range.
- **Short-circuit:** se `err` c'è, la parte dopo `||` non viene eseguita. È importante, perché in quel caso `info` non esiste.
- **Perché il resto del codice sta dentro la callback:** senza la risposta del disco non si può andare avanti.

[↑ indice](#indice)

---

## 11. Tipo di file

[server.js:63](server.js#L63)
```js
const tipo = tipi[path.extname(file)] || 'text/plain';
```

> ⚡ **Dall'estensione ricavo il tipo MIME. Se non lo conosco, uso `text/plain`.**

`path.extname('…/mare.jpg')` → `'.jpg'` → `tipi['.jpg']` → `'image/jpeg'`. Se l'estensione non c'è nel dizionario, il risultato è `undefined` e scatta il valore di riserva dopo `||`.

[↑ indice](#indice)

---

## 12. Strada 1: Range

[server.js:66](server.js#L66)
```js
if (req.headers.range) return inviaPezzo(res, file, info, tipo, req.headers.range);
```

> ⚡ **Se il browser chiede un pezzo (il tag video lo fa), passo tutto a `inviaPezzo`. È la prima strada perché una richiesta parziale non va né compressa né mandata intera.**

→ dettagli in [5. inviaPezzo](#5-inviapezzo)

[↑ indice](#indice)

---

## 13. Strada 2: gzip

[server.js:69-73](server.js#L69-L73)
```js
const accetta = req.headers['accept-encoding'] || '';
if (tipo.startsWith('text/') && accetta.includes('gzip')) {
    res.writeHead(200, { 'Content-Type': tipo, 'Content-Encoding': 'gzip' });
    return pipeline(fs.createReadStream(file), zlib.createGzip(), res, finito);
}
```

> ⚡ **Se è testo e il browser sa decomprimere, comprimo al volo: basta aggiungere un pezzo al tubo, file → gzip → client.**

- **`['accept-encoding']`**: parentesi quadre e non il punto, perché nel nome c'è un trattino.
- **`|| ''`**: curl non manda questo header. Senza il valore di riserva, `undefined.includes` manderebbe in crash il server.
- **`&&`**: devono essere vere tutte e due le condizioni.
- **Solo per il testo:** JPG, PNG e MP4 sono già compressi, ricomprimerli costerebbe CPU per niente.
- **`Content-Encoding: gzip`**: avvisa il browser che deve decomprimere.
- **Niente `Content-Length`:** la dimensione compressa non si conosce in anticipo, quindi Node manda a blocchi (`Transfer-Encoding: chunked`).

[↑ indice](#indice)

---

## 14. Strada 3: il resto

[server.js:76-77](server.js#L76-L77)
```js
res.writeHead(200, { 'Content-Type': tipo, 'Content-Length': info.size, 'Accept-Ranges': 'bytes' });
pipeline(fs.createReadStream(file), res, finito);
```

> ⚡ **Le immagini vanno così come sono: file → client, 64 KB alla volta. La dimensione la conosco grazie a `fs.stat`.**

Il `return` non serve, perché questa è l'ultima istruzione.

[↑ indice](#indice)

---

## 15. listen

[server.js:81-83](server.js#L81-L83)
```js
server.listen(PORT, () => {
    console.log('server avviato su http://localhost:' + PORT);
});
```

> ⚡ **Accende il server sulla porta 3000. La callback viene chiamata quando è pronto.**

[↑ indice](#indice)

---

## 16. Stream e pipeline

> ⚡ **Uno stream è un tubo: il file viaggia a pezzi da 64 KB e in RAM c'è sempre un solo pezzo. Se il client è lento, la lettura si mette in pausa da sola (backpressure).**

**I tre tipi di stream, tutti usati in server.js**

| Tipo | Ruolo | Qui |
|---|---|---|
| **Readable** | Fonte dei dati | `fs.createReadStream` |
| **Transform** | Trasforma i dati mentre passano | `zlib.createGzip` |
| **Writable** | Destinazione | `res` |

**`pipeline(a, b, …, callback)`**
1. **Collega** gli stream in fila.
2. **Gestisce la backpressure:** se `res` si riempie, mette in pausa la lettura dal disco.
3. **Gestisce gli errori:** se un pezzo si rompe, chiama `destroy()` su **tutti** gli stream e poi chiama la callback con l'errore.
4. **Fine normale:** chiama la callback senza errore.

**`fs.createReadStream(path, opzioni)`**
- **Pezzi da 64 KB**, il valore predefinito (si chiama `highWaterMark`).
- **`{ start, end }`**: legge solo un intervallo, con `end` incluso.
- **`autoClose`**: chiude il file da solo alla fine della lettura o in caso di errore.

**Rispetto a `readFile`**
- **Il primo byte parte subito.** Con `readFile` parte solo dopo aver letto tutto il file.
- **Nessun limite di dimensione.** `readFile` oltre i 2 GiB dà l'errore `ERR_FS_FILE_TOO_LARGE`.

[↑ indice](#indice)

---

## 17. Perché .pipe lascia il file aperto

> ⚡ **Quando il client chiude a metà, `.pipe()` scollega il tubo ma non lo distrugge. Il file resta aperto e fermo per sempre. `pipeline` invece chiama `destroy()` su tutti gli stream, e il file si chiude.**

**Passo per passo con `.pipe()`**
1. Si apre il file e il sistema operativo assegna un **file descriptor**, una risorsa limitata.
2. Lo stream manda pezzi da 64 KB a `res`.
3. L'utente chiude la pagina, e `res` emette l'evento `'close'`.
4. `.pipe()` chiama `unpipe()`: il file non ha più nessuno a cui mandare dati e **si mette in pausa**.
5. **Nessuno chiama `destroy()`**, quindi il file resta aperto.

**"Ma `autoClose` non chiude il file da solo?"** No: scatta solo alla **fine della lettura** (evento `'end'`) o in caso di **errore** (evento `'error'`). Uno stream in pausa a metà non è in nessuno dei due casi.

**Cosa fa `pipeline` al posto tuo**
```js
stream.pipe(res);
res.on('close', () => stream.destroy());   // con .pipe() devi ricordartelo tu
stream.on('error', () => res.destroy());   // anche il caso opposto
```

**Il caso opposto:** se è il file a dare errore, `.pipe()` non chiude `res`, e il browser resta con la rotellina che gira.

**Perché è grave**
- Ogni utente che chiude la pagina lascia **un file aperto in più**, più fino a 64 KB di buffer in memoria.
- Al limite dei file aperti consentiti dal sistema arriva **`EMFILE: too many open files`**. Il server resta acceso ma non riesce più a servire nessun file.

**La frase da dire:** "Con `.pipe()` la pulizia è compito tuo, con `pipeline` è garantita."

[↑ indice](#indice)

---

## 18. Tre richieste dall'inizio alla fine

**Apri `localhost:3000`**
`/` → `/index.html` → nessun `..` → `public/index.html` → `stat` ok → `text/html` → niente Range → testo con gzip → **200 compresso**.
Il browser legge l'HTML, trova `<link href="/Css/style.css">` e fa una **seconda richiesta** → cartella `Css/` → anche il CSS arriva compresso.

**Clicchi "Mare"**
`/pagina2.html` (testo compresso), poi `/img/mare.jpg` → `image/jpeg` → non è testo → strada 3 → **200 con `Content-Length`**.

**Sposti la barra del video**
`<video>` manda `Range: bytes=0-` → **206** con tutto il file. Quando sposti la barra arriva `Range: bytes=50000-` → **206**, e vengono letti solo i byte dal 50000 in poi.
Per mostrarlo: F12 → **Network** → richieste con stato 206.

[↑ indice](#indice)

---

## 19. Glossario

| Cosa | Significato | Riga |
|---|---|---|
| `require('x')` | Carica un modulo | 1-5 |
| `const { a } = obj` | Destructuring: prende una proprietà | 5 |
| `const [a, b] = arr` | Destructuring di array | 31 |
| `res.writeHead(code, headers)` | Codice di stato e header, una volta sola | 19, 36, 71, 76 |
| `res.end(testo)` | Manda il contenuto e chiude | 20 |
| `.replace(x, y)` | Sostituisce un pezzo di testo | 31 |
| `.split('-')` | Spezza il testo in un array | 31 |
| `Number(x)` | Da testo a numero | 32-33 |
| `c ? x : y` | Operatore ternario, un if/else in una riga | 33 |
| `isNaN(x)` | "Non è un numero valido?" | 34 |
| `fs.createReadStream(p, {start, end})` | Stream di lettura da 64 KB | 42, 72, 77 |
| `pipeline(…, cb)` | Collega gli stream e chiude tutto in caso di errore | 42, 72, 77 |
| `http.createServer(fn)` | Crea il server; `fn(req, res)` viene eseguita a ogni richiesta | 45 |
| `req.url` / `req.headers` | Percorso chiesto / header della richiesta | 46, 66, 69 |
| `(a, b) => {…}` | Arrow function | 45, 60 |
| `.includes(x)` | "Contiene?" | 52, 70 |
| `.startsWith(x)` | "Inizia con?" | 56, 70 |
| `__dirname` | Cartella di `server.js` | 56-57 |
| `path.join(…)` | Unisce pezzi di percorso | 56-57 |
| `fs.stat(p, cb)` | Informazioni sul file senza leggerlo, asincrona | 60 |
| `info.isFile()` / `info.size` | È un file? / Dimensione in byte | 61, 76 |
| `a \|\| b` | "Oppure" nelle condizioni; valore di riserva negli assegnamenti | 61, 63, 69 |
| `path.extname(p)` | Estensione: `'.jpg'` | 63 |
| `zlib.createGzip()` | Stream che comprime | 72 |
| `server.listen(port, cb)` | Accende il server | 81 |

[↑ indice](#indice)

---

## 20. Codici e header HTTP

| Codice | Quando |
|---|---|
| **200** | File inviato intero |
| **206** | Inviato solo un pezzo (Range) |
| **404** | File inesistente, cartella, `..` nell'URL o Range scritto male |

| Header | Direzione | A cosa serve |
|---|---|---|
| `Content-Type` | risposta | Tipo di file (MIME) |
| `Content-Length` | risposta | Quanti byte arrivano |
| `Accept-Encoding` | richiesta | "So decomprimere gzip" |
| `Content-Encoding: gzip` | risposta | "È compresso" |
| `Transfer-Encoding: chunked` | risposta | A blocchi, perché la dimensione non è nota (lo fa Node) |
| `Range: bytes=1000-` | richiesta | "Voglio solo questo pezzo" |
| `Content-Range: bytes 0-999/87167` | risposta | "Ecco il pezzo, su 87167 byte totali" |
| `Accept-Ranges: bytes` | risposta | "Puoi chiedermi dei pezzi" |

[↑ indice](#indice)
