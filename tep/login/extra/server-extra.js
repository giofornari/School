// EXTRA: OLTRE LE SLIDE. Hash delle password (crypto.scrypt) + sessione con cookie.
// Stessa struttura di ../server.js; cambiano solo i punti segnati con "EXTRA".
// Avvio: node extra/server-extra.js (porta 3001, così non litiga con server.js)
const http = require("http");
const fs = require("fs");
const path = require("path");
const qs = require("querystring");
// EXTRA: modulo nativo, ma non è nel programma (slide 1-54)
const crypto = require("crypto");

const hostname = "127.0.0.1";
const port = 3001;
const MAX_BODY = 1024;
const MAX_CAMPO = 30;

const mimeTypes = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8'
};

const allowedURLPaths = {
    '/': '../index.html',
    '/stile.css': '../stile.css'
};

// EXTRA: nel codice NON c'è la password, solo sale + hash.
// Se qualcuno legge il file, non può risalire alla password.
function creaHash(password) {
    const sale = crypto.randomBytes(16).toString("hex");
    const hash = crypto.scryptSync(password, sale, 64).toString("hex");
    return { sale: sale, hash: hash };
}

function passwordGiusta(password, utente) {
    const prova = crypto.scryptSync(password, utente.sale, 64);
    // timingSafeEqual: il confronto dura uguale anche se sbaglia al primo byte
    return crypto.timingSafeEqual(prova, Buffer.from(utente.hash, "hex"));
}

// in un progetto vero gli hash si generano una volta e si salvano su file
const utenti = [
    Object.assign({ nome: "mario" }, creaHash("Rossi2026")),
    Object.assign({ nome: "anna" }, creaHash("Verdi2026"))
];

// EXTRA: sessioni in memoria. id casuale -> nome utente. Si perdono al riavvio.
const sessioni = {};

function leggiCookie(req) {
    const cookie = {};
    const testo = req.headers.cookie || "";
    for (const pezzo of testo.split(";")) {
        const uguale = pezzo.indexOf("=");
        if (uguale > 0) {
            cookie[pezzo.slice(0, uguale).trim()] = pezzo.slice(uguale + 1).trim();
        }
    }
    return cookie;
}

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
    const fileStream = fs.createReadStream(path.join(__dirname, filePath));
    fileStream.on('open', function () {
        res.writeHead(200, { 'Content-Type': contentType });
        fileStream.pipe(res);
    });
    fileStream.on('error', function (error) {
        console.error("Errore nella lettura del file: " + error.message);
        if (!res.headersSent) {
            res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
            res.end("Errore interno del server");
        } else {
            res.destroy();
        }
    });
}

function riceviLogin(req, res) {
    let body = "";
    let troppoGrande = false;
    req.on('data', function (data) {
        if (body.length + data.length > MAX_BODY) {
            troppoGrande = true;
        } else {
            body += data;
        }
    });
    req.on('end', function () {
        if (troppoGrande) {
            res.writeHead(413, { 'Content-Type': 'text/plain; charset=utf-8' });
            res.end("Dati troppo grandi");
            return;
        }
        const post = qs.parse(body);
        const nome = String(post.nome || "").trim();
        const pass = String(post.pass || "");
        if (nome === "" || pass === "" || nome.length > MAX_CAMPO || pass.length > MAX_CAMPO) {
            res.writeHead(400, { 'Content-Type': 'text/html; charset=utf-8' });
            res.end(paginaLogin("Compila username e password (max 30 caratteri).", ""));
            return;
        }
        const utente = utenti.find(function (u) {
            return u.nome === nome;
        });
        // EXTRA: confronto con l'hash, non con la password in chiaro
        if (!utente || !passwordGiusta(pass, utente)) {
            res.writeHead(401, { 'Content-Type': 'text/html; charset=utf-8' });
            res.end(paginaLogin("Username o password errati.", nome));
            return;
        }
        // EXTRA: id lungo e casuale, così non si indovina
        const id = crypto.randomBytes(32).toString("hex");
        sessioni[id] = utente.nome;
        // HttpOnly: il JavaScript della pagina non legge il cookie (XSS non lo ruba)
        // SameSite=Strict: il browser non lo manda da altri siti (niente CSRF)
        res.writeHead(303, {
            'Set-Cookie': 'sessione=' + id + '; HttpOnly; SameSite=Strict; Path=/',
            'Location': '/area'
        });
        res.end();
    });
}

function requestHandler(req, res) {
    console.log(req.method + " " + req.url);

    if (req.url === "/login") {
        if (req.method !== "POST") {
            res.writeHead(405, { 'Content-Type': 'text/plain; charset=utf-8', 'Allow': 'POST' });
            res.end("Metodo non consentito");
            return;
        }
        riceviLogin(req, res);
        return;
    }

    if (req.method !== "GET" && req.method !== "HEAD") {
        res.writeHead(405, { 'Content-Type': 'text/plain; charset=utf-8', 'Allow': 'GET, HEAD' });
        res.end("Metodo non consentito");
        return;
    }

    // EXTRA: pagina riservata, si vede solo con un cookie di sessione valido
    if (req.url === "/area") {
        const nome = sessioni[leggiCookie(req).sessione];
        if (!nome) {
            res.writeHead(401, { 'Content-Type': 'text/html; charset=utf-8' });
            res.end(paginaLogin("Devi fare il login.", ""));
            return;
        }
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(pagina("Area riservata", `<h1>Benvenuto ${escapeHtml(nome)}!</h1>
        <p><a href="/logout">Esci</a></p>`));
        return;
    }

    // EXTRA: logout = cancello la sessione sul server e faccio scadere il cookie
    if (req.url === "/logout") {
        delete sessioni[leggiCookie(req).sessione];
        res.writeHead(303, {
            'Set-Cookie': 'sessione=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0',
            'Location': '/'
        });
        res.end();
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
