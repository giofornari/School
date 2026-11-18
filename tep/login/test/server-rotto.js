// VERSIONE ROTTA, apposta: è quella che scrivi di corsa e perdi punti.
// Serve al Boss di gioco.html per controllare che la griglia la bocci (sotto il 60%).
// Errori: readFileSync, niente 405, niente limite al body, niente charset,
// niente trim/validazione, 200 anche col login sbagliato, nome stampato senza escape.
const http = require("http");
const fs = require("fs");
const qs = require("querystring");

const utenti = [
    { nome: "mario", pass: "Rossi2026" }
];

function requestHandler(req, res) {
    if (req.url === "/") {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(fs.readFileSync("index.html"));
    } else if (req.url === "/login") {
        let body = "";
        req.on('data', function (data) {
            body += data;
        });
        req.on('end', function () {
            const post = qs.parse(body);
            const utente = utenti.find(function (u) {
                return u.nome === post.nome && u.pass === post.pass;
            });
            res.writeHead(200, { 'Content-Type': 'text/html' });
            if (utente) {
                res.end("<h1>Benvenuto " + post.nome + "</h1>");
            } else {
                res.end("Utente non autorizzato " + post.nome);
            }
        });
    } else {
        res.end("errore url non trovato");
    }
}

http.createServer(requestHandler).listen(3000);
