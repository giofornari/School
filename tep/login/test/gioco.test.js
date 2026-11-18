// Test end-to-end di gioco.html a 390x844 (telefono). Uso: node test/gioco.test.js [cartella-screenshot]
// Completa ogni livello rispondendo giusto, sbaglia apposta una volta (foglio rosso), batte il Boss
// incollando server.js, controlla il server rotto sotto il 60%, fa il ripasso e verifica il salvataggio.
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");
const cartella = path.join(__dirname, "..");
const scatti = process.argv[2];

(async function () {
    const browser = await chromium.launch();
    const context = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: scatti ? 2 : 1, hasTouch: true });
    // i font di Google qui non servono: risposta vuota, così niente errori di rete
    // negli screenshot i font veri; nel test normale risposta vuota, così niente errori di rete
    if (!scatti) await context.route(/fonts\.(googleapis|gstatic)\.com/, function (r) { r.fulfill({ status: 200, contentType: "text/css", body: "" }); });
    const page = await context.newPage();
    const erroriConsole = [];
    page.on("console", function (m) { if (m.type() === "error") erroriConsole.push(m.text()); });
    page.on("pageerror", function (e) { erroriConsole.push(e.message); });
    await page.goto("file://" + path.join(cartella, "gioco.html"));
    const dati = await page.evaluate(function () { return JSON.parse(document.getElementById("dati").textContent); });
    const perId = {};
    dati.livelli.forEach(function (l) { l.esercizi.forEach(function (e) { perId[e.id] = e; }); });
    let controlli = 0;
    function ok(cond, msg) { if (!cond) throw new Error("FALLITO: " + msg); controlli++; }

    async function senzaScrollOrizzontale(dove) {
        const larghezza = await page.evaluate(function () { return document.documentElement.scrollWidth; });
        ok(larghezza <= 390, dove + ": la pagina scorre in orizzontale (" + larghezza + "px)");
    }

    async function rispondi(es, giusto) {
        if (es.tipo === "completa" || es.tipo === "prevedi") await page.fill("#risposta", giusto ? es.risposta[0] : "boh");
        if (es.tipo === "blocco") await page.fill("#risposta", giusto ? es.soluzione : "boh");
        if (es.tipo === "riordina") {
            const ordine = es.righe.map(function (_, i) { return i; });
            if (!giusto) ordine.reverse();
            for (const i of ordine) await page.click('#pool .riga[data-i="' + i + '"]');
        }
        if (es.tipo === "errore") {
            const i = giusto ? es.sbagliata : (es.sbagliata + 1) % es.righe.length;
            await page.click('#gioco .righe .riga[data-i="' + i + '"]');
            if (es.correggi) await page.fill("#risposta", es.corretta);
        }
        await page.click("#controlla");
        await page.waitForSelector("#foglio:not([hidden])");
    }

    async function giocaFinoAllaFine(sbagliaPrimo) {
        let n = 0;
        while (await page.isVisible("#esercizio")) {
            const id = await page.getAttribute("#esercizio", "data-id");
            const es = perId[id];
            await senzaScrollOrizzontale(id);
            const giusto = !(sbagliaPrimo && n === 0);
            await rispondi(es, giusto);
            const classe = await page.getAttribute("#foglio", "class");
            ok(classe === (giusto ? "verde" : "rosso"), id + ": atteso foglio " + (giusto ? "verde" : "rosso") + ", trovato " + classe);
            if (!giusto) {
                const testo = await page.textContent("#foglio");
                ok(testo.includes("PERCHÉ") && testo.includes("RIGA GIUSTA"), "il foglio rosso ha perché e riga giusta");
                ok(await page.isVisible("#foglio .insulto"), "il foglio rosso ha l'insulto animato");
                if (scatti) { await page.waitForTimeout(900); await page.screenshot({ path: path.join(scatti, "foglio-rosso.png") }); }
                console.log("  sbagliato apposta " + id + ": foglio rosso con insulto, perché e riga giusta");
            }
            await page.click("#continua");
            n++;
            if (n > 60) throw new Error("troppi esercizi: ciclo infinito?");
        }
        return n;
    }

    // livelli 1-7
    for (const l of dati.livelli) {
        await page.click('.tappa[data-livello="' + l.n + '"]');
        if (l.n === 1 && scatti) {
            await page.waitForSelector("#esercizio");
            await page.screenshot({ path: path.join(scatti, "esercizio.png") });
        }
        const fatti = await giocaFinoAllaFine(l.n === 1);
        const fine = await page.textContent("#fine");
        ok(fine.includes("FATTO!"), "livello " + l.n + " completato");
        console.log("Livello " + l.n + " (" + l.titolo + "): " + l.esercizi.length + " esercizi, " + fatti + " risposte, completato");
        await page.click("#mappa");
    }
    if (scatti) await page.screenshot({ path: path.join(scatti, "mappa.png"), fullPage: true });

    // Boss con server.js -> 100%
    async function boss(testo) {
        await page.click('.tappa[data-livello="8"]');
        await page.click("#via");
        await page.fill("#editor", testo);
        await page.click("#consegna");
        return Number(await page.getAttribute("#esito-boss", "data-perc"));
    }
    const pBuono = await boss(fs.readFileSync(path.join(cartella, "server.js"), "utf8"));
    ok(pBuono === 100, "Boss con server.js: " + pBuono + "%");
    console.log("Boss con server.js: " + pBuono + "%");
    await page.click("#ancora");
    await page.click("#via");
    await page.fill("#editor", fs.readFileSync(path.join(__dirname, "server-rotto.js"), "utf8"));
    await page.click("#consegna");
    const pRotto = Number(await page.getAttribute("#esito-boss", "data-perc"));
    ok(pRotto < 60, "Boss con server rotto sotto 60%: " + pRotto + "%");
    console.log("Boss con server-rotto.js: " + pRotto + "% (righe mancanti elencate: " + (await page.$$eval(".griglia .no", function (x) { return x.length; })) + ")");
    if (scatti) await page.screenshot({ path: path.join(scatti, "boss.png") });
    await page.click("#mappa-boss");

    // ripasso: c'è l'esercizio sbagliato al livello 1
    const etichetta = await page.textContent("#ripasso");
    ok(/1 sbagliat/.test(etichetta), "il ripasso conta 1 esercizio sbagliato (" + etichetta + ")");
    await page.click("#ripasso");
    await giocaFinoAllaFine(false);
    ok((await page.textContent("#fine")).includes("PULITO"), "ripasso finito");
    await page.click("#mappa");
    ok(await page.isDisabled("#ripasso"), "dopo il ripasso non resta niente da ripassare");
    console.log("Ripasso finale: completato, lista sbagliati vuota");

    // salvataggio
    await page.reload();
    const boss8 = await page.textContent('.tappa[data-livello="8"]');
    ok(boss8.includes("BATTUTO") && boss8.includes("100%"), "dopo il reload il Boss risulta battuto col record");
    console.log("Progressi salvati in localStorage: ok dopo il reload");

    ok(erroriConsole.length === 0, "errori in console: " + erroriConsole.join(" | "));
    console.log("Errori in console: 0 · controlli superati: " + controlli);
    await browser.close();
})().catch(function (e) { console.error(e.message); process.exit(1); });
