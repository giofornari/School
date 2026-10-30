// demo: perché gli stream (e perché pipeline e non .pipe())
// avvio:  node --expose-gc confronto.js
// prova:  curl -s localhost:3001/readfile -o /dev/null      (Windows: -o NUL)
//         curl -s localhost:3001/pipeline -o /dev/null
//         curl -s --limit-rate 10M -m 1 localhost:3001/pipe -o /dev/null       <- chiudo a metà
//         curl -s --limit-rate 10M -m 1 localhost:3001/pipeline -o /dev/null   <- chiudo a metà
const http = require('http');
const fs = require('fs');
const path = require('path');
const { pipeline } = require('stream');

const PORT = 3001;
const MB = 1024 * 1024;
const FILE = path.join(__dirname, 'grande.bin');

// crea un file da 500 MB la prima volta
if (!fs.existsSync(FILE)) {
    console.log('creo grande.bin (500 MB)...');
    const blocco = Buffer.alloc(MB, 'x');
    const fd = fs.openSync(FILE, 'w');
    for (let i = 0; i < 500; i++) fs.writeSync(fd, blocco);
    fs.closeSync(fd);
}

// quanti file sono aperti in questo momento
let aperti = 0;
function apri() {
    const stream = fs.createReadStream(FILE);
    stream.on('open', () => aperti++);
    stream.on('close', () => aperti--);
    return stream;
}

// picco di RAM usata dai dati (buffer) durante la richiesta
let picco = 0;
setInterval(() => {
    picco = Math.max(picco, process.memoryUsage().arrayBuffers);
}, 5).unref();

http.createServer((req, res) => {
    if (global.gc) global.gc();
    picco = 0;

    res.on('close', () => {
        // aspetto un attimo che gli stream si chiudano (se si chiudono...)
        setTimeout(() => {
            console.log(req.url.padEnd(10), '| RAM picco:', String(Math.round(picco / MB)).padStart(3), 'MB',
                '| completato:', res.writableFinished ? 'si' : 'NO',
                '| file ancora aperti:', aperti);
        }, 100);
    });

    switch (req.url) {
        // tutto il file in RAM, poi lo manda
        case '/readfile':
            fs.readFile(FILE, (err, dati) => res.end(dati));
            break;

        // stream, vecchio modo: se il client chiude, il file resta aperto
        case '/pipe':
            apri().pipe(res);
            break;

        // stream, modo giusto: se qualcosa si rompe chiude tutto
        case '/pipeline':
            pipeline(apri(), res, () => {});
            break;

        default:
            res.writeHead(404);
            res.end();
    }
}).listen(PORT, () => {
    console.log('demo su http://localhost:' + PORT);
});
