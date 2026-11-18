// Login con Node.js: solo moduli nativi (slide 18-54)
const http = require("http");
const fs = require("fs");
const path = require("path");
const qs = require("querystring");

const hostname = "127.0.0.1";
const port = 3000;

// tetto al body del POST: senza, un client può riempire la RAM del server
const MAX_BODY = 1024;
// stesso valore del maxlength nel form: il controllo del browser si aggira con curl
const MAX_CAMPO = 30;

// estensione -> Content-Type: senza charset le lettere accentate si rompono
const mimeTypes = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8'
};

// solo questi URL sono permessi: tutto il resto è 404
const allowedURLPaths = {
    '/': './index.html',
    '/stile.css': './stile.css'
};

// utenti abilitati (in verifica basta un array, come nella slide 48)
const utenti = [
    { nome: "mario", pass: "Rossi2026" },
    { nome: "anna", pass: "Verdi2026" }
];

// trasforma i caratteri speciali in entità: <script> diventa testo, non codice (niente XSS)
function escapeHtml(testo) {
    return String(testo)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
}

function pagina(titolo, contenuto) {
    return `<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${titolo}</title>
    <link rel="stylesheet" href="/stile.css">
</head>
<body>
    <main>
        ${contenuto}
    </main>
</body>
</html>`;
}

// il form torna indietro con lo username già scritto e la password vuota
function paginaLogin(messaggio, nome) {
    return pagina("Login", `<h1>Login</h1>
        <p class="errore">${messaggio}</p>
        <form action="/login" method="POST">
            <label for="nome">Username</label>
            <input type="text" id="nome" name="nome" value="${escapeHtml(nome)}" maxlength="30" required>
            <label for="pass">Password</label>
            <input type="password" id="pass" name="pass" maxlength="30" required>
            <button type="submit">Accedi</button>
        </form>`);
}

function inviaFileStatico(res, filePath) {
    const contentType = mimeTypes[path.extname(filePath)] || 'application/octet-stream';
    // __dirname: il file si trova anche se avvio node da un'altra cartella
    const fileStream = fs.createReadStream(path.join(__dirname, filePath));

    // il 200 parte solo quando il file è davvero aperto
    fileStream.on('open', function () {
        res.writeHead(200, { 'Content-Type': contentType });
        fileStream.pipe(res);
    });

    fileStream.on('error', function (error) {
        console.error("Errore nella lettura del file: " + error.message);
        if (!res.headersSent) {
            if (error.code === 'ENOENT') {
                res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
                res.end("File non trovato");
            } else {
                res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
                res.end("Errore interno del server");
            }
        } else {
            // header già partiti: chiudo la connessione per non lasciare il client in attesa
            res.destroy();
        }
    });
}

function riceviLogin(req, res) {
    let body = "";
    let troppoGrande = false;

    // il body arriva a pezzi (chunk): li accumulo finché stanno sotto il tetto
    req.on('data', function (data) {
        if (body.length + data.length > MAX_BODY) {
            troppoGrande = true;
        } else {
            body += data;
        }
    });

    // 'end' scatta una volta sola, quando il body è arrivato tutto
    req.on('end', function () {
        if (troppoGrande) {
            res.writeHead(413, { 'Content-Type': 'text/plain; charset=utf-8' });
            res.end("Dati troppo grandi");
            return;
        }

        const post = qs.parse(body);
        // || "" copre il campo mancante; la password non si trimma: lo spazio può farne parte
        const nome = String(post.nome || "").trim();
        const pass = String(post.pass || "");

        // validazione lato server: il required del browser non basta
        if (nome === "" || pass === "") {
            res.writeHead(400, { 'Content-Type': 'text/html; charset=utf-8' });
            res.end(paginaLogin("Compila username e password.", nome));
            return;
        }

        if (nome.length > MAX_CAMPO || pass.length > MAX_CAMPO) {
            res.writeHead(400, { 'Content-Type': 'text/html; charset=utf-8' });
            res.end(paginaLogin("Username o password troppo lunghi.", ""));
            return;
        }

        const utente = utenti.find(function (u) {
            return u.nome === nome && u.pass === pass;
        });

        // messaggio unico: non dico quale dei due è sbagliato
        if (!utente) {
            res.writeHead(401, { 'Content-Type': 'text/html; charset=utf-8' });
            res.end(paginaLogin("Username o password errati.", nome));
            return;
        }

        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(pagina("Benvenuto", `<h1>Benvenuto ${escapeHtml(utente.nome)}!</h1>
        <p><a href="/">Esci</a></p>`));
    });
}

function requestHandler(req, res) {
    console.log(req.method + " " + req.url);

    if (req.url === "/login") {
        // il login si accetta solo in POST: con GET la password finirebbe nell'URL
        if (req.method !== "POST") {
            res.writeHead(405, { 'Content-Type': 'text/plain; charset=utf-8', 'Allow': 'POST' });
            res.end("Metodo non consentito");
            return;
        }
        riceviLogin(req, res);
        return;
    }

    // i file statici si leggono e basta
    if (req.method !== "GET" && req.method !== "HEAD") {
        res.writeHead(405, { 'Content-Type': 'text/plain; charset=utf-8', 'Allow': 'GET, HEAD' });
        res.end("Metodo non consentito");
        return;
    }

    if (allowedURLPaths.hasOwnProperty(req.url)) {
        inviaFileStatico(res, allowedURLPaths[req.url]);
    } else {
        res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
        res.end("Pagina non trovata");
    }
}

const server = http.createServer(requestHandler);
server.listen(port, hostname, function () {
    console.log(`Server running at http://${hostname}:${port}/`);
});
