/*
 * Server web statico in Node.js (solo moduli nativi, niente Express)
 * Autore: Giordano Fornari
 *
 * Struttura del progetto:
 *   public/  -> pagine HTML (index.html e la home su "/")
 *   css/     -> foglio di stile, servito su /css/...
 *   img/     -> immagini, servite su /img/...
 *
 * Se viene richiesta una risorsa che non esiste il server risponde 404.
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;

// cartelle da cui il server legge i file
const CARTELLE = {
    public: path.join(__dirname, 'public'),
    css: path.join(__dirname, 'css'),
    img: path.join(__dirname, 'img'),
};

// estensione del file -> Content-Type da mandare al browser
const MIME = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.ico': 'image/x-icon',
};

// trasforma l'url richiesto nel percorso del file su disco (null se non valido)
function percorsoFile(url) {
    let pathname;
    try {
        // new URL toglie la query string (?a=1), decodeURIComponent gli %20 ecc.
        pathname = decodeURIComponent(new URL(url, 'http://localhost').pathname);
    } catch {
        return null; // url malformato
    }

    // un byte nullo farebbe lanciare un'eccezione a fs.readFile
    if (pathname.includes('\0')) return null;

    // home
    if (pathname === '/') pathname = '/index.html';

    // /css/... e /img/... hanno la loro cartella, tutto il resto sta in public
    const [, primo, ...resto] = pathname.split('/');
    let base = CARTELLE.public;
    let relativo = pathname;
    if (primo === 'css' || primo === 'img') {
        base = CARTELLE[primo];
        relativo = resto.join('/');
    }

    const file = path.join(base, relativo);

    // impedisce di uscire dalla cartella (es. /css/..%2F..%2Fserver.js)
    if (!file.startsWith(base + path.sep)) return null;

    return file;
}

// err 404: manda la pagina public/404.html (o un testo semplice se manca)
function errore404(res) {
    fs.readFile(path.join(CARTELLE.public, '404.html'), (err, dati) => {
        res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(err ? '<h1>404 - Pagina non trovata</h1>' : dati);
    });
}

const server = http.createServer((req, res) => {
    // log di ogni richiesta con il codice di risposta (200, 404, ...)
    res.on('finish', () => console.log(`${req.method} ${req.url} -> ${res.statusCode}`));

    const file = percorsoFile(req.url);
    if (!file) return errore404(res);

    fs.readFile(file, (err, dati) => {
        if (err) {
            // file inesistente o cartella -> 404, qualsiasi altro problema -> 500
            if (['ENOENT', 'EISDIR', 'ENOTDIR'].includes(err.code)) return errore404(res);
            res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
            return res.end('500 - Errore interno del server');
        }

        const tipo = MIME[path.extname(file).toLowerCase()] || 'application/octet-stream';
        res.writeHead(200, { 'Content-Type': tipo });
        res.end(dati);
    });
});

server.listen(PORT, () => {
    console.log('server avviato su http://localhost:' + PORT);
});
