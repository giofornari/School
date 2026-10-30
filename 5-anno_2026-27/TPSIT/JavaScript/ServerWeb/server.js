const http = require('http');

const PORT = 3000;
const studente = { nome: 'Mario', cognome: 'Rossi', classe: '5A' };

const server = http.createServer((req, res) => {
    switch (req.url) {
        // home
        case '/':
            res.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
            res.end('Benvenuto nel mio server!');
            break;

        // obj json
        case '/json':
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify(studente));
            break;

        // pag html
        case '/html':
            res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
            res.end('<h1>Benvenuto nella pagina Html</h1>');
            break;

        // err 404
        default:
            res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
            res.end('<h1>404 - Pagina non trovata</h1>');
    }
});

server.listen(PORT, () => {
    console.log('server avviato su http://localhost:' + PORT);
});
