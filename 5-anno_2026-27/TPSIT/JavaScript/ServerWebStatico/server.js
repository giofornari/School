const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3000;

// tipi file
const tipi = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css',
    '.png': 'image/png',
    '.jpg': 'image/jpeg'
};

function errore404(res) {
    res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end('<h1>404 - Risorsa non trovata</h1>');
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

    fs.readFile(file, (err, dati) => {
        if (err) return errore404(res);
        res.writeHead(200, { 'Content-Type': tipi[path.extname(file)] || 'text/plain' });
        res.end(dati);
    });
});

server.listen(PORT, () => {
    console.log('server avviato su http://localhost:' + PORT);
});
