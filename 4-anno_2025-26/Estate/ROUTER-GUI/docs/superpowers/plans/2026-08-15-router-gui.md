# ROUTER-GUI — Piano di Implementazione

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Simulatore grafico di router IP con TDI editabile, Longest Prefix Match spiegato riga per riga, e persistenza su file JSON.

**Architecture:** Tre strati con confini verificabili — logica (`js/ip.js`, `rotta.js`, `tdi.js`, `iface.js`, `pacchetto.js`, `router.js`) senza alcun riferimento al DOM; persistenza (`js/persistenza.js`) che traduce dominio ↔ JSON; vista (`js/vista-tdi.js`, `vista-sim.js`, `app.js`) senza aritmetica sugli indirizzi. `Tdi.cerca()` restituisce un `Esito` che contiene già la spiegazione della scelta, così la vista si limita a disegnare.

**Tech Stack:** HTML5, CSS3, JavaScript ES2019 vanilla. Zero dipendenze, zero build step.

## Global Constraints

- **Niente ES modules.** Nessun `import`/`export`. I file si caricano con `<script>` classici in ordine di dipendenza, perché `file://` blocca i moduli.
- **Zero dipendenze esterne.** Nessun `npm`, nessun CDN, nessun framework CSS.
- **Deve funzionare con doppio click su `index.html`.**
- **Logica: zero DOM.** In `js/ip.js`, `rotta.js`, `tdi.js`, `iface.js`, `pacchetto.js`, `router.js` non compaiono mai `document`, `window`, `alert`.
- **Vista: zero aritmetica IP.** In `js/vista-tdi.js`, `vista-sim.js`, `app.js` non compaiono mai gli operatori `&`, `|`, `>>>`, `<<` su indirizzi né conversioni dotted.
- **Ogni valore a 32 bit va normalizzato con `>>> 0`** prima di essere confrontato per ordinamento o mostrato. Gli operatori bit a bit di JS lavorano su int32 con segno.
- **Lingua:** identificatori e UI in italiano, anglicismi dove sono la parola giusta (`gw`, `iface`, `pkt`, `msk`). Abbreviazioni e minuscole dove non danneggiano la leggibilità. Classi in `PascalCase`.
- **Stile:** commenti solo dove un umano si fermerebbe davvero (la trappola del `>>> 0`, il perché della scansione lineare, il test di contiguità della mask). Densità irregolare — non un commento per metodo. Ironia ammessa **solo nei commenti**, mai negli identificatori né nelle stringhe dell'interfaccia.
- **Test:** nessun framework. `test.html` + `test/test.js` con un mini-runner di asserzioni scritto a mano.

---

### Task 1: Runner di test + `Ip`

**Files:**
- Create: `test/runner.js`
- Create: `js/ip.js`
- Create: `test/test-ip.js`
- Create: `test.html`

**Interfaces:**
- Consumes: niente (primo task)
- Produces:
  - `runner.js` → globali `ok(desc, cond)`, `eq(desc, a, b)`, `lancia(desc, fn)` (asserisce che `fn` sollevi), `riassunto()`
  - `Ip.dotted2int(s) -> uint32` — lancia `Error` su input malformato
  - `Ip.int2dotted(n) -> string`
  - `Ip.msk2pfx(m) -> int 0..32` — lancia `Error` su mask non contigua
  - `Ip.pfx2msk(p) -> uint32`
  - `Ip.mskValida(m) -> bool`
  - `Ip.parseMsk(s) -> uint32` — accetta sia `"255.255.255.0"` sia `"/24"` sia `"24"`

- [ ] **Step 1: Scrivere il runner**

`test/runner.js` — nessun framework, solo un contatore e un po' di DOM:

```js
const T = { ok: 0, ko: 0, righe: [] };

function ok(desc, cond) {
  if (cond) { T.ok++; T.righe.push(['ok', desc]); }
  else      { T.ko++; T.righe.push(['ko', desc]); }
}

function eq(desc, a, b) {
  ok(desc + '  (atteso ' + b + ', ottenuto ' + a + ')', a === b);
}

function lancia(desc, fn) {
  try { fn(); ok(desc, false); }
  catch (e) { ok(desc, true); }
}

function riassunto() { /* stampa T.righe nel div #esiti, verde/rosso */ }
```

- [ ] **Step 2: Scrivere i test di `Ip` (falliranno)**

`test/test-ip.js`:

```js
eq('dotted2int 0.0.0.0', Ip.dotted2int('0.0.0.0'), 0);
eq('dotted2int 192.168.1.1', Ip.dotted2int('192.168.1.1'), 3232235777);
eq('dotted2int broadcast resta positivo', Ip.dotted2int('255.255.255.255'), 4294967295);
eq('int2dotted round-trip', Ip.int2dotted(Ip.dotted2int('196.13.2.5')), '196.13.2.5');
eq('int2dotted su /0', Ip.int2dotted(0), '0.0.0.0');

lancia('ottetto fuori range', () => Ip.dotted2int('256.1.1.1'));
lancia('troppo pochi ottetti', () => Ip.dotted2int('1.2.3'));
lancia('roba non numerica', () => Ip.dotted2int('a.b.c.d'));
lancia('ottetto vuoto', () => Ip.dotted2int('1..3.4'));

eq('msk2pfx /0', Ip.msk2pfx(Ip.dotted2int('0.0.0.0')), 0);
eq('msk2pfx /24', Ip.msk2pfx(Ip.dotted2int('255.255.255.0')), 24);
eq('msk2pfx /32', Ip.msk2pfx(Ip.dotted2int('255.255.255.255')), 32);
eq('pfx2msk 24', Ip.pfx2msk(24), Ip.dotted2int('255.255.255.0'));
eq('pfx2msk 0', Ip.pfx2msk(0), 0);
eq('pfx2msk 32', Ip.pfx2msk(32), 4294967295);

ok('mask contigua accettata', Ip.mskValida(Ip.dotted2int('255.255.128.0')));
ok('mask a buchi rifiutata', !Ip.mskValida(Ip.dotted2int('255.0.255.0')));
lancia('msk2pfx su mask a buchi', () => Ip.msk2pfx(Ip.dotted2int('255.0.255.0')));

eq('parseMsk dotted', Ip.parseMsk('255.255.255.0'), Ip.pfx2msk(24));
eq('parseMsk /24', Ip.parseMsk('/24'), Ip.pfx2msk(24));
eq('parseMsk 24 nudo', Ip.parseMsk('24'), Ip.pfx2msk(24));
lancia('parseMsk /33', () => Ip.parseMsk('/33'));
```

- [ ] **Step 3: Aprire `test.html`, verificare che i test falliscano**

`test.html` carica in ordine: `test/runner.js`, `js/ip.js`, `test/test-ip.js`, poi chiama `riassunto()`.
Atteso: tutto rosso, `Ip is not defined`.

- [ ] **Step 4: Implementare `js/ip.js`**

Oggetto letterale con soli metodi — non serve istanziarlo. Punti chiave:
- `dotted2int`: `split('.')`, validare 4 pezzi, ognuno `/^\d{1,3}$/` e `<= 255`, poi
  `((a << 24) | (b << 16) | (c << 8) | d) >>> 0`
- `int2dotted`: `(n >>> 24) & 255`, `(n >>> 16) & 255`, `(n >>> 8) & 255`, `n & 255`
- `mskValida`: una netmask è 1 seguiti da 0. Test: `(~m >>> 0) + 1` è potenza di due o zero →
  `const c = (~m >>> 0) + 1; return c === 0 || (c & (c - 1)) === 0;`
- `msk2pfx`: se non valida lancia; altrimenti conta i bit a 1
- `pfx2msk`: `p === 0 ? 0 : (0xFFFFFFFF << (32 - p)) >>> 0` — il caso `p === 0` va separato perché in JS lo shift usa solo i 5 bit bassi, quindi `<< 32` equivale a `<< 0` e restituirebbe tutti 1

- [ ] **Step 5: Riaprire `test.html`, tutto verde**

- [ ] **Step 6: Commit**

```bash
git add js/ip.js test/ test.html
git commit -m "feat(ip): conversione e validazione indirizzi + runner di test"
```

---

### Task 2: `Rotta`

**Files:**
- Create: `js/rotta.js`
- Create: `test/test-rotta.js`
- Modify: `test.html` (aggiungere i due `<script>`)

**Interfaces:**
- Consumes: `Ip.*` da Task 1
- Produces:
  - `new Rotta(rete, msk, gw, iface, metr)` — tutti gli indirizzi come `uint32`, `iface` stringa, `metr` intero. Il costruttore lancia se `msk` non è contigua o se `rete` ha bit accesi fuori dalla mask.
  - `r.pfx` — getter, `int 0..32`
  - `r.copre(ip) -> bool`
  - `r.calcolo(ip) -> { and: uint32, rete: uint32, esito: bool }`
  - `r.stessaDest(altra) -> bool` — stessa `rete` **e** stessa `msk` (destinazione condivisa: **ammessa**, è la rotta di riserva)
  - `r.identicaA(altra) -> bool` — stessa `rete`, `msk` **e** `gw` (ridondanza pura: rifiutata da `Tdi.agg`)
  - `r.toJSON() -> { rete, msk, gw, iface, metr }` con indirizzi in dotted
  - `Rotta.daJSON(o) -> Rotta`
  - `Rotta.daDotted(rete, msk, gw, iface, metr) -> Rotta` — comodo per test e form

- [ ] **Step 1: Scrivere i test (falliranno)**

```js
const r24 = Rotta.daDotted('192.168.1.0', '255.255.255.0', '0.0.0.0', 'eth0', 1);
const def = Rotta.daDotted('0.0.0.0', '0.0.0.0', '192.168.1.254', 'eth0', 10);

eq('pfx di /24', r24.pfx, 24);
eq('pfx della default', def.pfx, 0);

ok('copre indirizzo interno', r24.copre(Ip.dotted2int('192.168.1.77')));
ok('non copre altra rete', !r24.copre(Ip.dotted2int('192.168.2.77')));
ok('default copre tutto', def.copre(Ip.dotted2int('8.8.8.8')));
ok('default copre anche 0.0.0.0', def.copre(0));

const c = r24.calcolo(Ip.dotted2int('192.168.1.77'));
eq('calcolo espone AND', Ip.int2dotted(c.and), '192.168.1.0');
ok('calcolo espone esito', c.esito === true);

ok('stessaDest vero', r24.stessaDest(Rotta.daDotted('192.168.1.0', '/24', '1.1.1.1', 'eth9', 5)));
ok('stessaDest falso su mask diversa', !r24.stessaDest(Rotta.daDotted('192.168.1.0', '/25', '0.0.0.0', 'eth0', 1)));
ok('identicaA falso se cambia il gw', !r24.identicaA(Rotta.daDotted('192.168.1.0', '/24', '1.1.1.1', 'eth9', 5)));
ok('identicaA vero a parita di rete/msk/gw', r24.identicaA(Rotta.daDotted('192.168.1.0', '/24', '0.0.0.0', 'eth1', 9)));

lancia('mask a buchi rifiutata dal costruttore',
  () => Rotta.daDotted('10.0.0.0', '255.0.255.0', '0.0.0.0', 'eth0', 1));
lancia('bit fuori dalla mask rifiutati',
  () => Rotta.daDotted('192.168.1.77', '255.255.255.0', '0.0.0.0', 'eth0', 1));

const j = r24.toJSON();
eq('toJSON in dotted', j.rete, '192.168.1.0');
eq('round-trip JSON', Rotta.daJSON(j).copre(Ip.dotted2int('192.168.1.5')), true);
```

- [ ] **Step 2: Aprire `test.html`, verificare il fallimento** (`Rotta is not defined`)

- [ ] **Step 3: Implementare `js/rotta.js`**

`copre` è una riga: `((ip & this.msk) >>> 0) === this.rete`.
Il controllo "bit fuori dalla mask" nel costruttore serve a rifiutare `192.168.1.77/24`: chi
scrive una route intende `192.168.1.0/24`, e accettarlo in silenzio nasconde un errore.

- [ ] **Step 4: Riaprire `test.html`, tutto verde**

- [ ] **Step 5: Commit**

```bash
git add js/rotta.js test/test-rotta.js test.html
git commit -m "feat(rotta): riga di TDI con validazione e calcolo del match"
```

---

### Task 3: `Tdi` e il Longest Prefix Match

**Files:**
- Create: `js/tdi.js`
- Create: `test/test-tdi.js`
- Modify: `test.html`

**Interfaces:**
- Consumes: `Ip.*`, `Rotta` dai task precedenti
- Produces:
  - `new Tdi()` — parte vuota
  - `t.agg(rotta)` — lancia `Error` solo se esiste già una rotta `identicaA` (stessa rete, mask **e** gateway). Stessa destinazione con gateway diverso è **ammessa**: è la rotta di riserva.
  - `t.rimuovi(i)` — per indice
  - `t.svuota()`
  - `t.elenco() -> Rotta[]` — copia difensiva
  - `t.cerca(ip) -> Esito`
  - `t.toJSON() -> array`, `Tdi.daJSON(arr) -> Tdi`
  - **`Esito`** = oggetto semplice:
    ```js
    {
      ip: uint32,
      righe: [ { rotta, idx, and, esito } ],   // una per OGNI rotta, in ordine di tabella
      scelta: Rotta | null,
      alternative: Rotta[],                     // ordinate per preferenza
      motivo: string
    }
    ```

- [ ] **Step 1: Scrivere i test (falliranno)**

```js
function tdiEsempio() {
  const t = new Tdi();
  t.agg(Rotta.daDotted('0.0.0.0',     '/0',  '196.13.1.1', 'eth0', 10));
  t.agg(Rotta.daDotted('196.13.0.0',  '/16', '196.13.1.1', 'eth0', 5));
  t.agg(Rotta.daDotted('196.13.2.0',  '/24', '196.13.1.2', 'eth1', 5));
  return t;
}

const e = tdiEsempio().cerca(Ip.dotted2int('196.13.2.5'));
eq('righe = una per rotta', e.righe.length, 3);
eq('LPM sceglie la /24', e.scelta.pfx, 24);
eq('due alternative', e.alternative.length, 2);
eq('prima alternativa e la /16', e.alternative[0].pfx, 16);
eq('la default e ultima', e.alternative[1].pfx, 0);
ok('motivo cita il prefisso', e.motivo.indexOf('24') >= 0);

const e2 = tdiEsempio().cerca(Ip.dotted2int('8.8.8.8'));
eq('fuori rete vince la default', e2.scelta.pfx, 0);
eq('nessuna alternativa', e2.alternative.length, 0);

const vuota = new Tdi();
vuota.agg(Rotta.daDotted('10.0.0.0', '/8', '0.0.0.0', 'eth0', 1));
const e3 = vuota.cerca(Ip.dotted2int('8.8.8.8'));
ok('senza default nessun match', e3.scelta === null);
ok('motivo dice irraggiungibile', e3.motivo.toLowerCase().indexOf('irraggiungibile') >= 0);

// il prefisso batte sempre la metrica
const pfxVsMetr = new Tdi();
pfxVsMetr.agg(Rotta.daDotted('192.168.0.0', '/16', '1.1.1.1', 'eth0', 1));
pfxVsMetr.agg(Rotta.daDotted('192.168.0.0', '/17', '2.2.2.2', 'eth1', 99));
eq('il prefisso batte la metrica',
   pfxVsMetr.cerca(Ip.dotted2int('192.168.1.1')).scelta.pfx, 17);

// floating static route: stessa destinazione, gateway diversi. Decide la metrica.
const tie = new Tdi();
tie.agg(Rotta.daDotted('10.0.0.0', '/8', '1.1.1.1', 'eth0', 20));
tie.agg(Rotta.daDotted('10.0.0.0', '/8', '2.2.2.2', 'eth1', 3));
const eTie = tie.cerca(Ip.dotted2int('10.1.2.3'));
eq('a parita di prefisso vince la metrica minore',
   Ip.int2dotted(eTie.scelta.gw), '2.2.2.2');
eq('l altra resta come fallback',
   Ip.int2dotted(eTie.alternative[0].gw), '1.1.1.1');
ok('il motivo cita la metrica', eTie.motivo.toLowerCase().indexOf('metrica') >= 0);

lancia('rotta identica (stesso gw) rifiutata', () => {
  const t = new Tdi();
  t.agg(Rotta.daDotted('10.0.0.0', '/8', '1.1.1.1', 'eth0', 1));
  t.agg(Rotta.daDotted('10.0.0.0', '/8', '1.1.1.1', 'eth0', 7));
});

const t2 = tdiEsempio();
eq('round-trip JSON conserva le rotte', Tdi.daJSON(t2.toJSON()).elenco().length, 3);
```

- [ ] **Step 2: Aprire `test.html`, verificare il fallimento**

- [ ] **Step 3: Implementare `js/tdi.js`**

`cerca` in una passata, senza saltare regole — l'elenco completo serve alla vista:

```js
cerca(ip) {
  const righe = this.rotte.map((rt, idx) => {
    const c = rt.calcolo(ip);
    return { rotta: rt, idx: idx, and: c.and, esito: c.esito };
  });
  const match = righe.filter(r => r.esito).map(r => r.rotta);
  // prefisso piu lungo, poi metrica piu bassa. A parita piena decide l'ordine
  // di inserimento: sort e stabile da ES2019, quindi non serve altro.
  match.sort((a, b) => b.pfx - a.pfx || a.metr - b.metr);
  const scelta = match.length ? match[0] : null;
  return { ip, righe, scelta, alternative: match.slice(1), motivo: this._motivo(ip, scelta, match) };
}
```

`_motivo` compone il testo: se `scelta` è `null` → «destinazione irraggiungibile: nessuna
regola compatibile»; altrimenti cita rete/prefisso vincente, dice quante alternative ci sono
e, se la prima alternativa ha lo stesso `pfx`, aggiunge che ha deciso la metrica.

- [ ] **Step 4: Riaprire `test.html`, tutto verde**

- [ ] **Step 5: Commit**

```bash
git add js/tdi.js test/test-tdi.js test.html
git commit -m "feat(tdi): tabella di instradamento con Longest Prefix Match spiegato"
```

---

### Task 4: `Iface`, `Pacchetto`, `Router`

**Files:**
- Create: `js/iface.js`
- Create: `js/pacchetto.js`
- Create: `js/router.js`
- Create: `test/test-router.js`
- Modify: `test.html`

**Interfaces:**
- Consumes: `Ip`, `Rotta`, `Tdi`
- Produces:
  - `new Iface(nome, ip, msk, su = true)` — `ip`/`msk` come `uint32`; `toJSON`/`daJSON` in dotted
  - `new Pacchetto(src, dst, ttl = 64)` — `uint32`
  - `new Router(nome)` — crea una `Tdi` vuota e `ifaces = []`
  - `rt.aggIface(iface)`, `rt.iface(nome) -> Iface | null` (risoluzione nome → oggetto, il
    punto che permetterà il multi-hop senza toccare `Rotta`)
  - `rt.inoltra(pkt) -> Esito`
  - `rt.toJSON()`, `Router.daJSON(o)`

- [ ] **Step 1: Scrivere i test (falliranno)**

```js
const r = new Router('R1');
r.aggIface(new Iface('eth0', Ip.dotted2int('196.13.1.1'), Ip.pfx2msk(24)));
r.tdi.agg(Rotta.daDotted('196.13.1.0', '/24', '0.0.0.0', 'eth0', 1));
r.tdi.agg(Rotta.daDotted('0.0.0.0', '/0', '196.13.1.254', 'eth0', 10));

const es = r.inoltra(new Pacchetto(0, Ip.dotted2int('196.13.1.9')));
eq('inoltra usa la connessa', es.scelta.pfx, 24);
eq('risoluzione nome interfaccia', r.iface('eth0').nome, 'eth0');
ok('interfaccia inesistente da null', r.iface('eth9') === null);
eq('ttl di default', new Pacchetto(0, 0).ttl, 64);

const rj = Router.daJSON(r.toJSON());
eq('round-trip router: nome', rj.nome, 'R1');
eq('round-trip router: rotte', rj.tdi.elenco().length, 2);
eq('round-trip router: ifaces', rj.ifaces.length, 1);
```

- [ ] **Step 2: Aprire `test.html`, verificare il fallimento**

- [ ] **Step 3: Implementare i tre file**

`Router.inoltra` è un delegatore: `return this.tdi.cerca(pkt.dst)`. Sottile di proposito —
è il punto in cui, nel multi-router, si innesterà il ciclo di `Rete.invia`.

- [ ] **Step 4: Riaprire `test.html`, tutto verde**

- [ ] **Step 5: Commit**

```bash
git add js/iface.js js/pacchetto.js js/router.js test/test-router.js test.html
git commit -m "feat(router): router, interfacce e pacchetto"
```

---

### Task 5: `Persistenza`

**Files:**
- Create: `js/persistenza.js`
- Create: `test/test-persistenza.js`
- Modify: `test.html`

**Interfaces:**
- Consumes: `Router`
- Produces:
  - `Persistenza.serializza(router) -> object` — `{ versione: 1, router: {...} }`
  - `Persistenza.deserializza(obj) -> Router` — lancia `Error` su versione ignota o struttura mancante
  - `Persistenza.esporta(router, nomeFile)` — Blob + `<a download>` (tocca il DOM: è lo strato
    di persistenza, non la logica, quindi è ammesso)
  - `Persistenza.importa(file) -> Promise<Router>` — `FileReader`

- [ ] **Step 1: Scrivere i test (falliranno)**

Solo `serializza`/`deserializza` sono testabili senza interazione utente:

```js
const r = new Router('R1');
r.aggIface(new Iface('eth0', Ip.dotted2int('10.0.0.1'), Ip.pfx2msk(24)));
r.tdi.agg(Rotta.daDotted('10.0.0.0', '/24', '0.0.0.0', 'eth0', 1));

const o = Persistenza.serializza(r);
eq('versione presente', o.versione, 1);
eq('indirizzi salvati in dotted', o.router.tdi[0].rete, '10.0.0.0');

const r2 = Persistenza.deserializza(o);
eq('round-trip nome', r2.nome, 'R1');
eq('round-trip rotte', r2.tdi.elenco().length, 1);
eq('round-trip lookup', r2.inoltra(new Pacchetto(0, Ip.dotted2int('10.0.0.5'))).scelta.pfx, 24);

lancia('versione ignota rifiutata', () => Persistenza.deserializza({ versione: 99, router: {} }));
lancia('struttura mancante rifiutata', () => Persistenza.deserializza({ versione: 1 }));
```

- [ ] **Step 2: Aprire `test.html`, verificare il fallimento**

- [ ] **Step 3: Implementare `js/persistenza.js`**

`esporta`: `new Blob([JSON.stringify(o, null, 2)], {type:'application/json'})` →
`URL.createObjectURL` → `<a>` temporaneo con `download` → `click()` → `revokeObjectURL`.
`importa`: `FileReader.readAsText`, `JSON.parse` dentro un `try` che rigetta la Promise con
un messaggio leggibile.

- [ ] **Step 4: Riaprire `test.html`, tutto verde**

- [ ] **Step 5: Commit**

```bash
git add js/persistenza.js test/test-persistenza.js test.html
git commit -m "feat(persistenza): salvataggio e caricamento della configurazione su file JSON"
```

---

### Task 6: Pagina, stile e vista della TDI

**Files:**
- Create: `index.html`
- Create: `css/stile.css`
- Create: `js/vista-tdi.js`

**Interfaces:**
- Consumes: `Tdi`, `Rotta`, `Ip` (solo per `int2dotted` in rendering — unica eccezione
  ammessa nella vista, ed è formattazione, non aritmetica)
- Produces:
  - `new VistaTdi(elTabella)` 
  - `v.disegna(tdi, esito)` — `esito` può essere `null` (nessuna simulazione in corso)
  - `v.onElimina(cb)` — `cb(indice)`

- [ ] **Step 1: Scrivere `index.html`**

Tre sezioni: *Tabella di Instradamento* (tabella + form d'inserimento + salva/carica),
*Simulazione* (campo IP + pulsante), *Esito*. In fondo i `<script>` **in questo ordine**:
`js/ip.js`, `js/rotta.js`, `js/tdi.js`, `js/iface.js`, `js/pacchetto.js`, `js/router.js`,
`js/persistenza.js`, `js/vista-tdi.js`, `js/vista-sim.js`, `js/app.js`.

- [ ] **Step 2: Scrivere `css/stile.css`**

Classi di evidenziazione richieste dalla traccia:
`.scelta` (verde) · `.alt` (giallo) · `.no` (grigio, testo attenuato) · `.calcolo` (monospace).

- [ ] **Step 3: Scrivere `js/vista-tdi.js`**

`disegna` ricostruisce il `<tbody>`. Se `esito` è presente, per ogni riga applica la classe:
`scelta` se `rt === esito.scelta`, `alt` se compare in `esito.alternative`, `no` altrimenti —
e aggiunge una riga espandibile col calcolo `ip & msk = risultato` confrontato con la rete.
Gli indici delle righe corrispondono a `esito.righe[i].idx`.

- [ ] **Step 4: Aprire `index.html` con doppio click**

Atteso: la pagina si disegna, la tabella è vuota, nessun errore in console che non sia
`vista-sim.js`/`app.js` non ancora scritti. Verificare che **non** compaia
`Cannot use import statement outside a module`.

- [ ] **Step 5: Commit**

```bash
git add index.html css/stile.css js/vista-tdi.js
git commit -m "feat(ui): pagina, stile e rendering della tabella di instradamento"
```

---

### Task 7: Vista simulazione + controller

**Files:**
- Create: `js/vista-sim.js`
- Create: `js/app.js`

**Interfaces:**
- Consumes: tutto quanto sopra
- Produces:
  - `new VistaSim(elIngresso, elBottone, elEsito)`
  - `v.onSimula(cb)` — `cb(stringaIp)`
  - `v.mostra(esito)` — riquadro con route scelta, elenco ordinato delle alternative e `motivo`
  - `v.errore(msg)`
  - `App.avvia()` — istanzia `Router`, viste, collega gli eventi, carica una TDI d'esempio e
    disegna. L'esempio parte dalle due righe di pag. 129 (`0.0.0.0/0` via `196.13.1.1` e
    `196.13.1.0/24` direttamente connessa) e aggiunge due righe che il programma C non poteva
    esprimere: una `196.13.2.0/24` via `196.13.1.2` metrica 5, e la sua riserva
    `196.13.2.0/24` via `196.13.1.3` metrica 20. Così al primo avvio si vedono già sia il
    Longest Prefix Match sia il fallback per metrica.

- [ ] **Step 1: Scrivere `js/vista-sim.js`**

Nessuna aritmetica: riceve `esito` e formatta. Le route si stampano con `Ip.int2dotted`.

- [ ] **Step 2: Scrivere `js/app.js`**

Collega: form → `tdi.agg` (con `try/catch` che mostra l'errore di validazione inline);
pulsante elimina → `tdi.rimuovi`; salva → 
`Persistenza.esporta`; carica → `Persistenza.importa` con `catch` che lascia lo stato
intatto; simula → `router.inoltra` → `vistaTdi.disegna(tdi, esito)` + `vistaSim.mostra(esito)`.

- [ ] **Step 3: Aprire `index.html`, provare il flusso completo**

Verifiche manuali, con la TDI d'esempio caricata:
1. Instradare `196.13.2.5` → vince la `/24` via `196.13.1.2` (metrica 5); come alternative
   compaiono in ordine la `/24` via `196.13.1.3` (metrica 20) e poi la default `/0`. Il
   motivo cita sia il prefisso sia la metrica.
2. Instradare `196.13.1.9` → vince la `/24` direttamente connessa, la default resta come
   unica alternativa
3. Instradare `8.8.8.8` → vince la default, nessuna alternativa
4. Inserire una route con mask `255.0.255.0` → errore inline, tabella invariata
5. Inserire `192.168.1.77/24` → errore: bit accesi fuori dalla mask
6. Reinserire una rotta identica a una esistente (stesso gw) → errore; cambiando solo il
   gateway → accettata
7. Eliminare una route → la tabella si aggiorna
8. Salvare → scarica `config.json`; ricaricare la pagina; caricare il file → TDI ripristinata
9. Caricare un file JSON spazzatura → messaggio d'errore, TDI precedente intatta

- [ ] **Step 4: Commit**

```bash
git add js/vista-sim.js js/app.js
git commit -m "feat(ui): pannello di simulazione e controller dell'applicazione"
```

---

### Task 8: README

**Files:**
- Create: `README.md`

- [ ] **Step 1: Scrivere il README**

Come si apre (doppio click su `index.html`, niente da installare), come si lancia il test
(doppio click su `test.html`), com'è organizzato il codice nei tre strati, rimando alla spec
per la motivazione delle strutture dati e per il diagramma UML.

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: README con istruzioni d'uso e mappa del progetto"
```
