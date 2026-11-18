// Verifica che SCHELETRO.md e gli esercizi di gioco.html combacino con server.js e index.html.
// Uso: node test/verifica.js   (esce con 1 se qualcosa non combacia)
const fs = require("fs");
const path = require("path");
const cartella = path.join(__dirname, "..");
const sorgenti = {
    "server.js": fs.readFileSync(path.join(cartella, "server.js"), "utf8"),
    "index.html": fs.readFileSync(path.join(cartella, "index.html"), "utf8")
};
let errori = 0;
function ko(msg) { errori++; console.log("FAIL " + msg); }

// stessa regola del gioco: spazi ignorati, ' " ` equivalenti
function norm(s) { return s.replace(/\s+/g, "").replace(/['"`]/g, '"'); }
// righe di codice di un file: niente vuote, niente commenti su riga propria
function righe(testo) {
    return testo.split("\n").map(function (r) { return r.trim(); })
        .filter(function (r) { return r !== "" && !r.startsWith("//"); });
}
const righeSorgente = {};
for (const f in sorgenti) righeSorgente[f] = righe(sorgenti[f]).map(norm);

// le righe devono esistere, in quest'ordine, in uno dei due file; contigue = true se devono essere attaccate
function trovaInOrdine(lista, contigue, minuscole) {
    const giu = function (r) { return minuscole ? r.toLowerCase() : r; };
    const cercate = righe(lista.join("\n")).map(norm).map(giu);
    for (const f in righeSorgente) {
        const src = righeSorgente[f].map(giu);
        if (contigue) {
            for (let i = 0; i + cercate.length <= src.length; i++) {
                if (cercate.every(function (r, k) { return src[i + k] === r; })) return { file: f };
            }
            continue;
        }
        let pos = -1, ok = true;
        for (const r of cercate) {
            const j = src.indexOf(r, pos + 1);
            if (j < 0) { ok = false; break; }
            pos = j;
        }
        if (ok) return { file: f };
    }
    // diagnosi: quale riga manca?
    const mancanti = cercate.filter(function (r) {
        return !Object.values(righeSorgente).some(function (s) { return s.includes(r); });
    });
    return { mancanti: mancanti };
}

// ---------- 1. SCHELETRO.md ----------
const md = fs.readFileSync(path.join(cartella, "SCHELETRO.md"), "utf8");
const blocchi = [...md.matchAll(/```(?:js|html)\n([\s\S]*?)```/g)].map(function (m) { return m[1]; });
let righeControllate = 0;
blocchi.forEach(function (b, i) {
    const esito = trovaInOrdine(b.split("\n"), false);
    righeControllate += righe(b).length;
    if (!esito.file) ko("SCHELETRO blocco " + (i + 1) + ": righe non in server.js/index.html: " + esito.mancanti.join(" | "));
});
console.log("SCHELETRO.md: " + blocchi.length + " blocchi, " + righeControllate + " righe controllate");

// ---------- 2. gioco.html ----------
const giocoPath = path.join(cartella, "gioco.html");
if (fs.existsSync(giocoPath)) {
    const html = fs.readFileSync(giocoPath, "utf8");
    const json = html.match(/<script id="dati" type="application\/json">([\s\S]*?)<\/script>/);
    if (!json) { ko("gioco.html: blocco dati non trovato"); }
    else {
        const dati = JSON.parse(json[1]);
        let n = 0, nJs = 0;
        const richiesteHttp = [];
        for (const livello of dati.livelli) {
            for (const es of livello.esercizi) {
                n++;
                const dove = "L" + livello.n + " " + es.id + " (" + es.tipo + ")";
                let attese = [];
                if (es.tipo === "completa") {
                    for (const alt of es.risposta) {
                        const r = trovaInOrdine((es.prima || []).concat([es.testo.replace("___", alt)]), true, es.ignoraMaiuscole);
                        if (!r.file) ko(dove + ": la risposta '" + alt + "' non dà una riga del codice");
                    }
                    continue;
                }
                if (es.tipo === "riordina") attese = es.righe;
                if (es.tipo === "errore") {
                    attese = es.righe.slice();
                    attese[es.sbagliata] = es.corretta;
                    if (norm(es.righe[es.sbagliata]) === norm(es.corretta)) ko(dove + ": la riga sbagliata è uguale a quella giusta");
                }
                if (es.tipo === "blocco") attese = es.soluzione.split("\n");
                if (es.tipo === "prevedi") {
                    if (es.http) richiesteHttp.push({ dove: dove, es: es });
                    if (es.js) {
                        const valore = String(valuta(es.js));
                        if (valore !== es.risposta[0]) ko(dove + ": " + es.js + " dà '" + valore + "', non '" + es.risposta[0] + "'");
                        nJs++;
                    }
                    if (es.codice) attese = es.codice.split("\n");
                    else continue;
                }
                const r = trovaInOrdine(attese, true);
                if (!r.file) ko(dove + ": righe non presenti (contigue) nel codice: " + (r.mancanti || []).join(" | "));
            }
        }
        console.log("gioco.html: " + n + " esercizi controllati sul testo, " + nJs + " previsioni calcolate con le funzioni di server.js");

        // la griglia del Boss: 100% su server.js, sotto 60% sul server rotto
        const griglia = dati.boss.griglia;
        const rotto = fs.readFileSync(path.join(__dirname, "server-rotto.js"), "utf8");
        const punti = function (testo) {
            return griglia.filter(function (c) { return controllaVoce(c, testo); }).length;
        };
        const pBuono = punti(sorgenti["server.js"]), pRotto = punti(rotto);
        console.log("Boss: server.js " + pBuono + "/" + griglia.length + " (" + Math.round(pBuono * 100 / griglia.length) + "%), server-rotto.js " +
            pRotto + "/" + griglia.length + " (" + Math.round(pRotto * 100 / griglia.length) + "%)");
        griglia.forEach(function (c) {
            if (!controllaVoce(c, sorgenti["server.js"])) ko("Boss: server.js non passa '" + c.nome + "'");
            if (c.tipo !== "conta" && !trovaInOrdine([c.riga], true).file) ko("Boss: la riga mostrata per '" + c.nome + "' non è in server.js");
        });
        if (pRotto * 100 / griglia.length >= 60) ko("Boss: il server rotto prende il 60% o più");
        if (griglia.length < 15 || griglia.length > 20) ko("Boss: la griglia deve avere 15-20 controlli");

        // le previsioni dei codici di stato: le provo davvero sul server
        provaHttp(richiesteHttp).then(fine);
        return;
    }
}
fine();

// esegue server.js in una sandbox (http finto, niente listen) e valuta l'espressione con le sue funzioni
var sandbox = null;
function valuta(espressione) {
    const vm = require("vm");
    if (!sandbox) {
        const finto = { createServer: function () { return { listen: function () {} }; } };
        sandbox = vm.createContext({ require: function (m) { return m === "http" ? finto : require(m); }, __dirname: cartella, console: { log: function () {}, error: function () {} }, String: String });
        vm.runInContext(sorgenti["server.js"], sandbox);
    }
    return vm.runInContext(espressione, sandbox);
}

function controllaVoce(c, testo) {
    if (c.tipo === "conta") {
        const quanti = function (re) { return (testo.match(new RegExp(re, "g")) || []).length; };
        return quanti(c.piu) >= quanti(c.meno) && quanti(c.meno) > 0;
    }
    return c.re.every(function (re) { return new RegExp(re).test(testo); });
}

function provaHttp(lista) {
    const http = require("http");
    const { spawn } = require("child_process");
    const srv = spawn(process.execPath, ["server.js"], { cwd: cartella });
    return new Promise(function (ok) { setTimeout(ok, 500); }).then(async function () {
        for (const { dove, es } of lista) {
            const stato = await new Promise(function (ok) {
                const body = es.http.bodyLungo ? "nome=" + "a".repeat(es.http.bodyLungo) : (es.http.body || "");
                const r = http.request({ host: "127.0.0.1", port: 3000, method: es.http.metodo, path: es.http.url,
                    headers: body ? { "Content-Type": "application/x-www-form-urlencoded", "Content-Length": Buffer.byteLength(body) } : {} },
                    function (res) { res.resume(); ok(res.statusCode); });
                r.on("error", function () { ok("errore"); });
                r.end(body);
            });
            if (String(stato) !== String(es.risposta[0])) ko(dove + ": previsto " + es.risposta[0] + ", il server dà " + stato);
        }
        console.log("Previsioni HTTP provate sul server: " + lista.length);
        srv.kill();
    });
}

function fine() {
    console.log(errori === 0 ? "TUTTO OK" : errori + " problemi");
    process.exitCode = errori === 0 ? 0 : 1;
}
