const http = require('http');
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');
const { pipeline } = require('stream');

const PORT = 3000;

// tipi file
const tipi = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.mp4': 'video/mp4'
};

function errore404(res) {
    res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end('<h1>404 - Risorsa non trovata</h1>');
}

// pipeline chiama questa a fine invio: se il client chiude la pagina a metà
// arriva un errore e pipeline ha già chiuso il file (con .pipe() resterebbe aperto)
function finito(err) {
    if (err) console.log('invio interrotto:', err.code);
}

// range "bytes=1000-1999": il browser vuole solo un pezzo del file (es. sposti il video)
function inviaPezzo(res, file, info, tipo, range) {
    const [a, b] = range.replace('bytes=', '').split('-');
    const inizio = a === '' ? info.size - Number(b) : Number(a);
    const fine = a === '' || b === '' ? info.size - 1 : Math.min(Number(b), info.size - 1);

    // pezzo non valido -> 416
    if (isNaN(inizio) || isNaN(fine) || inizio < 0 || inizio > fine) {
        res.writeHead(416, { 'Content-Range': 'bytes */' + info.size });
        return res.end();
    }

    res.writeHead(206, {
        'Content-Type': tipo,
        'Content-Length': fine - inizio + 1,
        'Content-Range': 'bytes ' + inizio + '-' + fine + '/' + info.size,
        'Accept-Ranges': 'bytes'
    });
    pipeline(fs.createReadStream(file, { start: inizio, end: fine }), res, finito);
}

const server = http.createServer((req, res) => {
    let url = req.url;

    // home
    if (url === '/') url = '/index.html';

    // blocca ../
    if (url.includes('..')) return errore404(res);

    // css in Css, resto in public
    let file;
    if (url.startsWith('/Css/')) file = path.join(__dirname, url);
    else file = path.join(__dirname, 'public', url);

    // stat: il file esiste? quanto pesa? (non lo legge)
    fs.stat(file, (err, info) => {
        if (err || !info.isFile()) return errore404(res);

        const tipo = tipi[path.extname(file)] || 'text/plain';

        // 1) richiesta di un pezzo (video) -> 206
        if (req.headers.range) return inviaPezzo(res, file, info, tipo, req.headers.range);

        // 2) testo e il browser accetta gzip -> file -> gzip -> client
        const accetta = req.headers['accept-encoding'] || '';
        if (tipo.startsWith('text/') && accetta.includes('gzip')) {
            res.writeHead(200, { 'Content-Type': tipo, 'Content-Encoding': 'gzip' });
            return pipeline(fs.createReadStream(file), zlib.createGzip(), res, finito);
        }

        // 3) resto (immagini...) -> file -> client, 64 KB alla volta
        res.writeHead(200, { 'Content-Type': tipo, 'Content-Length': info.size, 'Accept-Ranges': 'bytes' });
        pipeline(fs.createReadStream(file), res, finito);
    });
});

server.listen(PORT, () => {
    console.log('server avviato su http://localhost:' + PORT);
});
