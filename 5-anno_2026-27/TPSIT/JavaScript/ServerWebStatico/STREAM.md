# Server statico con gli stream

## Il problema
`fs.readFile` carica **tutto** il file in RAM e solo dopo inizia a mandarlo.
File da 500 MB × 10 utenti insieme = 5 GB di RAM. Il server muore.

## L'idea
Uno stream è un **tubo**: il file viene letto e mandato **a pezzi da 64 KB**.
In RAM c'è sempre solo un pezzo alla volta, qualunque sia la dimensione del file.
Se il client è lento, lo stream rallenta da solo la lettura (*backpressure*).

```js
fs.createReadStream(file).pipe(res);      // modo "classico"
pipeline(fs.createReadStream(file), res, finito);   // modo giusto
```

## Perché `pipeline` e non `.pipe()`
`.pipe()` ha un difetto: se il client chiude la pagina a metà, **il file resta aperto**.
Ogni utente che chiude la pagina = un file aperto in più, per sempre (leak).
`pipeline` (Node 10+) chiude tutti gli stream se uno si rompe, e dà l'errore nella callback.
È quello che consiglia la documentazione di Node.

## Cosa fa server.js
1. `fs.stat` → controlla che il file esista e quanto pesa, **senza leggerlo**
2. **Testo (html, css)** → `file → gzip → client`: compresso al volo, basta aggiungere un pezzo al tubo
3. **Immagini** → `file → client`, con `Content-Length`
4. **Video** → il browser chiede solo un pezzo (`Range: bytes=1000-1999`),
   il server risponde `206` leggendo solo quei byte: `createReadStream(file, { start, end })`.
   È così che puoi **spostarti nel video** senza scaricarlo tutto (YouTube fa lo stesso).

## Demo live (confronto.js)
```
node --expose-gc confronto.js
curl -s localhost:3001/readfile -o /dev/null
curl -s localhost:3001/pipeline -o /dev/null
curl -s --limit-rate 10M -m 1 localhost:3001/pipe -o /dev/null
curl -s --limit-rate 10M -m 1 localhost:3001/pipeline -o /dev/null
```
Su Windows: `-o NUL` al posto di `-o /dev/null`.

Risultato:
```
/readfile  | RAM picco: 500 MB | completato: si | file ancora aperti: 0
/pipeline  | RAM picco:  14 MB | completato: si | file ancora aperti: 0
/pipe      | RAM picco:  12 MB | completato: NO | file ancora aperti: 1   <- leak
/pipe      | RAM picco:  10 MB | completato: NO | file ancora aperti: 2   <- leak, sale ancora
/pipeline  | RAM picco:  12 MB | completato: NO | file ancora aperti: 2   <- resta 2: chiuso bene
```

## Domande probabili
- **Gli stream sono vecchi?** No, sono la base di Node (http, fs, zlib, socket sono tutti stream).
  È vecchio `.pipe()` da solo, sostituito da `pipeline`.
- **E il futuro?** I **Web Streams** (`ReadableStream`): lo stesso concetto, ma standard uguale per
  browser, Deno, Bun, Cloudflare Workers. Lì si scrive `return new Response(stream)`.
  Node li supporta e converte: `Readable.toWeb(stream)`.
- **Ma in produzione?** Per file statici si usa nginx o un CDN, che fanno esattamente
  queste cose (gzip, Range, streaming). Qui abbiamo visto come funzionano da dentro.
