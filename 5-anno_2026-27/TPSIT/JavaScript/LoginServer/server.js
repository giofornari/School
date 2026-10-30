const http = require('http');
const fs = require('fs');
const path = require('path');

const utenti = [
    { nome: 'Mario', password: '1234' },
    { nome: 'Anna', password: '5678' }
];

http.createServer((req, res) => {
    const url = new URL(req.url, 'http://localhost:3000');

    if (url.pathname === '/' && req.method === 'GET') {
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(fs.readFileSync(path.join(__dirname, 'index.html')));
    } else if (url.pathname === '/login' && (req.method === 'GET' || req.method === 'POST')) {
        let dati = '';
        req.on('data', pezzo => dati += pezzo);
        req.on('end', () => {
            const parametri = req.method === 'GET' ? url.searchParams : new URLSearchParams(dati);
            const utente = utenti.find(u => u.nome === parametri.get('nome') && u.password === parametri.get('password'));
            res.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
            res.end(utente ? 'Benvenuto ' + utente.nome : 'Utente non autorizzato');
        });
    } else {
        res.writeHead(404);
        res.end('Pagina non trovata');
    }
}).listen(3000, () => console.log('Server avviato su http://localhost:3000'));
