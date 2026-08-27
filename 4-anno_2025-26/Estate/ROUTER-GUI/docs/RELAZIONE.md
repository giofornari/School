# Simulatore Grafico di Router — Relazione Tecnica Completa

Documento unico di progetto: scelte architetturali con vantaggi e svantaggi, prerequisiti
di sintassi, e analisi integrale del codice blocco per blocco.

---

## Indice

- **Parte 0** — [Come leggere questo documento](#parte-0--come-leggere-questo-documento)
- **Parte I** — [Il problema](#parte-i--il-problema)
  - [1.1 La traccia](#11-la-traccia)
  - [1.2 Cos'è davvero una tabella di instradamento](#12-cosè-davvero-una-tabella-di-instradamento)
  - [1.3 Il codice di partenza di pag. 129, riga per riga](#13-il-codice-di-partenza-di-pag-129-riga-per-riga)
  - [1.4 I limiti di quel codice](#14-i-limiti-di-quel-codice)
- **Parte II** — [Le scelte progettuali](#parte-ii--le-scelte-progettuali)
- **Parte III** — [Prerequisiti: tutta la sintassi che serve](#parte-iii--prerequisiti-tutta-la-sintassi-che-serve)
- **Parte IV** — [Analisi del codice, file per file](#parte-iv--analisi-del-codice-file-per-file)
- **Parte V** — [I flussi completi](#parte-v--i-flussi-completi)
- **Parte VI** — [Verifiche eseguite](#parte-vi--verifiche-eseguite)
- **Parte VII** — [Evoluzione verso il multi-router](#parte-vii--evoluzione-verso-il-multi-router)
- **Appendice** — [Glossario](#appendice--glossario)

---

# Parte 0 — Come leggere questo documento

Il documento è scritto senza dare per scontata la conoscenza di JavaScript, degli operatori
bit a bit, del DOM o dell'algoritmo di Longest Prefix Match. Ogni costrutto viene spiegato
la prima volta che compare, e la **Parte III** raccoglie in un unico posto tutta la sintassi
ricorrente, così che la Parte IV possa concentrarsi sul *ragionamento* invece che sulla
grammatica.

Tre convenzioni tipografiche:

- I blocchi di codice sono **citazioni letterali** dai file del progetto, non
  riscritture semplificate. Quello che si legge qui è quello che gira.
- Dopo ogni blocco c'è la sezione *Cosa fa*, *Come funziona*, e dove serve *Perché così* con
  vantaggi e svantaggi dell'alternativa scartata.
- Gli indirizzi IP sono mostrati sia in notazione decimale puntata (`192.168.1.0`) sia, dove
  serve capire il meccanismo, in **binario** raggruppato per ottetti.

---

# Parte I — Il problema

## 1.1 La traccia

Realizzare un'applicazione con interfaccia grafica in JavaScript che simuli un router IP e
la sua Tabella di Instradamento (TDI). L'applicazione deve consentire di:

1. visualizzare la tabella completa;
2. inserire una rotta;
3. eliminare una rotta;
4. salvare e caricare la configurazione da file;
5. simulare l'instradamento: dato un indirizzo di destinazione, individuare **tutte** le
   rotte compatibili evidenziandole, applicare il criterio del **Longest Prefix Match**,
   evidenziare la rotta selezionata e le eventuali alternative utilizzabili come fallback,
   e mostrare chiaramente il motivo della scelta.

Vincoli espliciti: strutture dati motivate, sviluppo orientato agli oggetti con separazione
fra interfaccia grafica, logica di instradamento e persistenza, e un'architettura che
permetta in futuro di introdurre `Interface`, `Link`, `Packet` e la simulazione multi-hop
**senza modifiche sostanziali**.

## 1.2 Cos'è davvero una tabella di instradamento

Un router riceve un pacchetto, legge l'indirizzo IP di destinazione scritto nell'intestazione,
e deve decidere **da quale interfaccia farlo uscire** e **a chi consegnarlo**. Non conosce
l'intera Internet: conosce solo un elenco di regole. Quell'elenco è la Tabella di
Instradamento.

Ogni riga della tabella dice, in sostanza: *«se la destinazione appartiene a questa rete,
mandala di là»*. Quattro informazioni per riga:

| Colonna | Significato |
|---|---|
| **Rete di destinazione** | L'indirizzo che identifica un gruppo di macchine, es. `196.13.2.0` |
| **Netmask** | Quanti bit iniziali dell'indirizzo definiscono la rete, es. `255.255.255.0` |
| **Gateway** (next hop) | A chi consegnare fisicamente il pacchetto perché prosegua |
| **Interfaccia d'uscita** | Da quale scheda di rete farlo uscire |

A queste il progetto aggiunge una quinta colonna, la **metrica** (§ 2.8).

### Come si verifica se una regola è applicabile

Il meccanismo è l'AND bit a bit fra l'indirizzo di destinazione e la netmask. Se il
risultato è uguale all'indirizzo di rete della regola, la regola è **compatibile**.

Esempio concreto. Destinazione `196.13.2.5`, regola `196.13.2.0 / 255.255.255.0`:

```
indirizzo   196.13.2.5    →  11000100 00001101 00000010 00000101
netmask     255.255.255.0 →  11111111 11111111 11111111 00000000
                             ────────────────────────────────────  AND
risultato   196.13.2.0    →  11000100 00001101 00000010 00000000

rete regola 196.13.2.0    →  11000100 00001101 00000010 00000000
                             uguali → REGOLA COMPATIBILE
```

L'AND bit a bit restituisce 1 solo dove **entrambi** gli operandi hanno 1. Poiché la netmask
è fatta di 1 iniziali seguiti da 0, l'AND **conserva** i bit dove la maschera vale 1 e
**azzera** quelli dove vale 0. In pratica: *«dimentica la parte finale dell'indirizzo, quella
che identifica la singola macchina, e guarda solo la parte iniziale, quella che identifica
la rete»*.

Stessa destinazione contro una regola diversa, `196.13.1.0 / 255.255.255.0`:

```
196.13.2.5 & 255.255.255.0 = 196.13.2.0
                             ≠ 196.13.1.0  → REGOLA NON COMPATIBILE
```

### La lunghezza del prefisso e il Longest Prefix Match

La **lunghezza del prefisso** è il numero di bit a 1 nella netmask. Si scrive con la barra:
`255.255.255.0` ha 24 bit a 1 e si abbrevia `/24`. Questa è la notazione CIDR.

Il prefisso misura la **specificità** della regola: più bit sono fissati, più piccolo è
l'insieme di indirizzi che la regola copre.

| Prefisso | Netmask | Quanti indirizzi copre |
|---|---|---|
| `/0` | `0.0.0.0` | tutti e 4 294 967 296 |
| `/8` | `255.0.0.0` | 16 777 216 |
| `/16` | `255.255.0.0` | 65 536 |
| `/24` | `255.255.255.0` | 256 |
| `/32` | `255.255.255.255` | 1 solo (un host preciso) |

Più regole possono essere compatibili contemporaneamente con lo stesso indirizzo. La regola
di scelta si chiama **Longest Prefix Match**: *vince la regola compatibile con il prefisso
più lungo*, cioè la più specifica, quella che sa di più su dove sta andando il pacchetto.

Esempio con tre regole compatibili con `196.13.2.5`:

| # | Regola | Prefisso | Compatibile? |
|---|---|---|---|
| 1 | `0.0.0.0/0` | 0 | sì (copre tutto) |
| 2 | `196.13.0.0/16` | 16 | sì |
| 3 | `196.13.2.0/24` | 24 | sì ← **vince** |

### La default route

`0.0.0.0/0` è la **default route**, la rotta predefinita. La sua netmask è tutta a zero,
quindi `qualsiasi_indirizzo & 0 = 0`, che è sempre uguale alla rete `0.0.0.0`: è compatibile
con **qualunque** destinazione. Ma il suo prefisso è 0, il minimo possibile, quindi sotto il
Longest Prefix Match finisce sempre ultima. È la regola *«per tutto il resto, manda al mio
router di uscita»*.

Questo è importante: la default route non ha bisogno di alcun trattamento speciale nel
codice. Emerge automaticamente come ultima scelta dall'ordinamento per prefisso. Nel
programma in C di pag. 129 la default c'è, ma poiché il programma non ordina nulla, il suo
ruolo non si vede mai.

## 1.3 Il codice di partenza di pag. 129, riga per riga

Il progetto parte dall'esempio in C visto a lezione. Lo si riporta ricostruito e commentato,
perché l'analisi dei suoi limiti è parte della consegna.

```c
typedef struct {
  unsigned char Ia, Ib, Ic, Id;   // colonna Indirizzo
  unsigned char Ma, Mb, Mc, Md;   // colonna Mask
  unsigned char Ga, Gb, Gc, Gd;   // colonna Gateway (next hop)
  unsigned char Ua, Ub, Uc, Ud;   // colonna Use (interfaccia d'uscita)
} TDI;

TDI tdiHost[] = {
  {0,0,0,0,       0,0,0,0,         196,13,1,254,  196,13,1,1},
  {196,13,1,0,    255,255,255,0,   196,13,1,1,    196,13,1,1}
};
```

Ogni riga della tabella è una `struct` con **sedici** campi `unsigned char`, quattro per
ciascuna delle quattro colonne. Un `unsigned char` in C occupa un byte e contiene un valore
da 0 a 255: giusto per un ottetto.

```c
unsigned int DottedToDecimal(unsigned char a, unsigned char b,
                             unsigned char c, unsigned char d)
{
  unsigned int ul;
  ul = a*0x1000000 + b*0x10000 + c*0x100 + d;
  return ul;
}
```

Questa funzione ricompone i quattro ottetti in un unico intero a 32 bit. `0x1000000` è
16 777 216 in esadecimale, cioè 2²⁴; `0x10000` è 2¹⁶; `0x100` è 2⁸. Moltiplicare il primo
ottetto per 2²⁴ significa spostarlo di 24 posizioni verso sinistra nella rappresentazione
binaria. È una moltiplicazione usata al posto di uno scorrimento di bit.

```c
a=196; b=13; c=2; d=5;                      // indirizzo da instradare
for (i=0; i<sizeof(tdiHost)/sizeof(TDI); i++)
{
  unsigned int u;
  printf("Regola n.%d per %d.%d.%d.%d: ", i+1, a, b, c, d);
  u = DottedToDecimal(tdiHost[i].Ma, tdiHost[i].Mb, tdiHost[i].Mc, tdiHost[i].Md);
  u = u & DottedToDecimal(a, b, c, d);
  if (u == DottedToDecimal(tdiHost[i].Ia, tdiHost[i].Ib, tdiHost[i].Ic, tdiHost[i].Id))
    printf(" vera.\n");
  else
    printf(" falsa.\n");
}
```

Il ciclo scorre le righe della tabella. Per ciascuna:

1. ricompone la netmask della regola in un intero (`DottedToDecimal` sui campi `M*`);
2. ricompone l'indirizzo da instradare e fa l'AND;
3. ricompone l'indirizzo di rete della regola e confronta.

Poi stampa `vera` o `falsa`. E si ferma lì.

`sizeof(tdiHost)/sizeof(TDI)` è l'idioma C per contare gli elementi di un array: dimensione
totale in byte diviso dimensione di un elemento.

## 1.4 I limiti di quel codice

| # | Limite | Conseguenza pratica | Come lo risolve questo progetto |
|---|---|---|---|
| 1 | **Non implementa il Longest Prefix Match.** Stampa `vera`/`falsa` per ogni regola e termina. | Non sceglie mai una rotta. Manca proprio il cuore dell'instradamento: sapere che due regole sono entrambe vere non dice quale usare. | `Tdi.cerca()` ordina i match per lunghezza di prefisso e seleziona il vincitore. |
| 2 | **Sedici `unsigned char` per riga** invece di quattro interi a 32 bit. Il dato viene smontato per essere memorizzato e ricostruito a ogni operazione. | `DottedToDecimal` viene chiamata **tre volte per ogni riga della tabella** solo per poter fare un AND e un confronto. Il codice è verboso e il nome dei campi (`Ia`, `Ib`, `Ic`, `Id`) non dice nulla. | Indirizzi come interi a 32 bit; il dotted esiste solo al confine di input/output (§ 2.3). |
| 3 | **TDI fissata a tempo di compilazione** in un array inizializzato nel sorgente. | Aggiungere una rotta richiede di riscrivere il programma e ricompilarlo. | `Tdi.agg()` / `Tdi.rimuovi()`, con form grafico. |
| 4 | **Nessuna metrica, nessun criterio di pareggio.** | Due regole ugualmente specifiche sono indistinguibili: il programma non ha modo di preferirne una. | Campo `metr`, secondo criterio d'ordinamento (§ 2.8). |
| 5 | **La colonna "Use" è una stringa di ottetti**, non un'astrazione di interfaccia: non ha comportamento, non si può collegare a nulla. | Impossibile evolvere verso il multi-hop: un collegamento fisico unisce due interfacce, non due numeri. | Classe `Iface` con nome, indirizzo, mask e stato. |
| 6 | **Zero validazione.** Accetta netmask non contigue come `255.0.255.0` e ottetti fuori range. | Il programma calcola felicemente risultati privi di senso. | Validazione su indirizzi e contiguità della mask (§ 2.9). |
| 7 | **Nessuna persistenza.** | La configurazione muore con il processo. | Esportazione e importazione JSON (§ 2.7). |
| 8 | **Si intitola «instradamento classful» ma esegue mascheratura classless.** Le classi A/B/C non compaiono da nessuna parte: c'è solo l'AND con una netmask esplicita, che è CIDR. | Discrepanza fra titolo e contenuto, didatticamente confondente. | Il progetto è dichiaratamente classless, con lunghezza di prefisso esplicita. |
| 9 | **La default route c'è ma il suo ruolo non emerge mai**, perché senza ordinamento non si vede che è l'ultima scelta possibile. | Lo studente non capisce perché quella riga è lì. | L'ordinamento la colloca naturalmente in fondo; l'interfaccia la etichetta come fallback. |
| 10 | **Nessuna separazione delle responsabilità.** Struttura dati, logica di confronto e output sono intrecciati nello stesso ciclo `for`. | Non si può testare la logica senza stampare, né cambiare l'output senza toccare la logica. | Tre strati con confini verificabili (§ 2.6). |

---

# Parte II — Le scelte progettuali

Ogni sezione ha la stessa forma: **il problema**, **le opzioni considerate**, **la scelta**,
**vantaggi**, **svantaggi**.

## 2.1 Linguaggio e runtime: JavaScript vanilla, nessun build step

**Il problema.** La traccia impone JavaScript e un'interfaccia grafica. JavaScript oggi si
scrive in molti modi diversi, con conseguenze molto diverse sulla consegna.

**Le opzioni.**

| Opzione | Cosa comporta |
|---|---|
| **HTML + CSS + JS puri, nessuna dipendenza** | Si consegna una cartella. Si apre con doppio click. |
| React / Vue con Vite | `npm install` scarica centinaia di pacchetti; serve `npm run build`; il risultato è codice generato illeggibile. |
| Node.js con interfaccia da terminale | Non soddisfa il requisito di interfaccia grafica. |
| Electron | Applicazione desktop vera, ma un pacchetto da centinaia di megabyte per una tabella. |

**La scelta: JavaScript vanilla, zero dipendenze, zero compilazione.**

**Vantaggi.**

- **Consegnabilità.** Il professore riceve una cartella, fa doppio click su `index.html` e
  il programma parte. Nessuna installazione, nessuna versione di Node da azzeccare, nessuna
  connessione a internet.
- **Leggibilità.** Il codice che si legge è il codice che gira. Non c'è transpilazione, non
  c'è bundling, non c'è minificazione. Un file `.js` corrisponde a una classe.
- **Durata.** Fra tre anni `npm install` su un progetto di oggi ha buone probabilità di
  fallire per dipendenze deprecate. Un file HTML del 2005 si apre ancora.
- **Aderenza alla valutazione.** Ciò che viene valutato è la progettazione a oggetti e
  l'algoritmo, non la capacità di configurare un bundler.

**Svantaggi, dichiarati onestamente.**

- **Niente reattività automatica.** Con React basta cambiare lo stato e l'interfaccia si
  aggiorna da sola. Qui bisogna chiamare esplicitamente `ridisegna()` dopo ogni modifica.
  Il costo è una riga in più per ogni azione, e il rischio è di dimenticarsene: è la ragione
  per cui nel controller ogni modifica alla tabella passa per la stessa coppia
  `scordaEsito(); ridisegna();`.
- **Ridisegno totale.** Ogni ridisegno ricostruisce l'intero corpo della tabella invece di
  aggiornare solo ciò che è cambiato. Su una tabella da dieci righe è irrilevante; su
  diecimila sarebbe un problema.
- **Niente controllo dei tipi.** TypeScript segnalerebbe a tempo di scrittura un
  `rt.rette` scritto per sbaglio invece di `rt.rete`. Qui il refuso si scopre solo quando
  il valore risulta `undefined`. Contromisura: i test.
- **Ambito globale condiviso.** Tutte le classi finiscono nello stesso spazio dei nomi.
  Con dieci classi si gestisce; con cento sarebbe ingestibile.

## 2.2 Niente ES modules: perché `import` è vietato in questo progetto

**Il problema.** JavaScript moderno organizza il codice in moduli, con `export` in un file e
`import` nell'altro. È il modo giusto di scrivere JS oggi. Qui non si può.

**Il motivo tecnico, in dettaglio.** Quando si apre un file HTML con doppio click, il browser
usa il protocollo `file://`. Quando lo si serve da un server web, usa `http://`. La
differenza non è cosmetica: i browser applicano la *same-origin policy*, che classifica ogni
documento con un'**origine** (protocollo + dominio + porta) e limita cosa può accedere a
cosa. Per i documenti `file://` l'origine è considerata **opaca**: due file nella stessa
cartella sono trattati come provenienti da origini diverse e reciprocamente estranee.

Gli ES modules vengono caricati con una richiesta soggetta a CORS (*Cross-Origin Resource
Sharing*). Con origine opaca quel controllo fallisce sempre. Il risultato pratico:

```
Access to script at 'file:///.../js/ip.js' from origin 'null' has been blocked
by CORS policy
```

oppure, se manca `type="module"`:

```
Uncaught SyntaxError: Cannot use import statement outside a module
```

In entrambi i casi: pagina bianca.

**La scelta: `<script>` classici, caricati in ordine esplicito di dipendenza.**

```html
<script src="js/ip.js"></script>
<script src="js/rotta.js"></script>
<script src="js/tdi.js"></script>
...
```

Uno `<script src="...">` senza `type="module"` non è soggetto a CORS: il browser lo carica
come una risorsa qualunque e ne esegue il contenuto nello **stesso ambito globale** della
pagina. Tutte le dichiarazioni di primo livello (`const Ip = {...}`, `class Rotta {...}`)
diventano visibili a tutti gli script successivi.

**Vantaggi.** Funziona con doppio click, che è il requisito.

**Svantaggi.**

- **L'ordine dei tag conta ed è manuale.** `rotta.js` usa `Ip`, quindi `ip.js` deve venire
  prima. Se si sbaglia l'ordine si ottiene `Ip is not defined`. Con i moduli l'ordine lo
  calcolerebbe il browser.
- **Nessun incapsulamento a livello di file.** Tutto ciò che è dichiarato al primo livello è
  globale. Un nome ripetuto in due file è una collisione silenziosa.
- **Nessuna dichiarazione esplicita delle dipendenze.** Guardando `tdi.js` non è scritto da
  nessuna parte che dipende da `Rotta` e da `Ip`: lo si scopre leggendo il corpo.

Mitigazione adottata: i nomi delle classi sono distinti e specifici del dominio, e l'ordine
di caricamento è documentato con un commento nell'HTML e ripetuto identico in `test.html`.

## 2.3 Rappresentazione degli indirizzi: un intero a 32 bit

**Il problema.** Un indirizzo IPv4 si scrive `192.168.1.1`, ma non è una stringa: è un
numero di 32 bit, e la notazione puntata è solo un modo comodo di leggerlo, un ottetto (8
bit) alla volta, ciascuno convertito in decimale.

```
192.168.1.1  =  11000000 10101000 00000001 00000001  =  3232235777
     192          168        1          1
```

**Le opzioni.**

| Rappresentazione | Come si fa l'AND con la mask | Come si confronta | Come si ordina per prefisso |
|---|---|---|---|
| **Stringa `"192.168.1.1"`** | Impossibile: bisogna prima convertire | Confronto di stringhe, inutile | Impossibile |
| **Quattro ottetti separati** (scelta di pag. 129) | Quattro AND, uno per ottetto, oppure ricostruzione a ogni uso | Quattro confronti | Contare i bit ottetto per ottetto |
| **Un intero a 32 bit** ✅ | `ip & msk` — **una** operazione | `===` — **una** operazione | Confronto fra due numeri |
| Array di 32 booleani | Concettualmente pulito | 32 confronti | Scansione dell'array |

**La scelta: `uint32`. La notazione puntata vive solo al confine di input/output.**

Questo è il principio che struttura tutto il programma: la conversione avviene in due soli
punti — quando l'utente digita nel form e quando si legge o si scrive il file JSON. Nel
mezzo circolano soltanto numeri.

**Vantaggi.**

- **Ogni operazione del dominio diventa una riga.** Il test di compatibilità di una regola,
  che nel codice C richiede tre chiamate di funzione e sei righe, qui è:

  ```js
  copre(ip) { return (((ip >>> 0) & this.msk) >>> 0) === this.rete; }
  ```

- **Ordinare per specificità è ordinare numeri.** Nessuna logica speciale.
- **Meno stato da sbagliare.** Un campo invece di quattro significa che non può esistere lo
  stato incoerente «tre ottetti aggiornati e uno no».
- **Corrisponde alla realtà.** È così che l'indirizzo viaggia davvero sul cavo e così che è
  scritto nell'intestazione del pacchetto IP.

**Svantaggi.**

- **Illeggibile in debug.** `3232235777` non dice nulla a un essere umano; `192.168.1.1` sì.
  Serve passare da `Ip.int2dotted()` ogni volta che si vuole guardare un valore. Nel codice
  questo si vede: tutti i messaggi d'errore chiamano `int2dotted`.
- **JavaScript ha una trappola sul segno.** È il punto seguente, ed è abbastanza serio da
  meritare una sezione propria.

### 2.3.1 La trappola del segno e l'operatore `>>> 0`

JavaScript ha un solo tipo numerico, `number`, che è un numero in virgola mobile a doppia
precisione (IEEE 754, 64 bit). Ma **gli operatori bit a bit non lavorano su quel tipo**:
prima convertono l'operando in un intero **a 32 bit con segno** (complemento a due), poi
operano, e restituiscono ancora un intero a 32 bit con segno.

Con segno significa che il bit più significativo (il 32°) indica il segno. Un indirizzo come
`255.255.255.0` ha quel bit a 1:

```
255.255.255.0  =  11111111 11111111 11111111 00000000
                  ↑
                  bit di segno = 1  →  interpretato come numero NEGATIVO
```

Quindi in JavaScript:

```js
(255 << 24) | (255 << 16) | (255 << 8) | 0     // →  -256
```

Il valore in memoria è corretto: i 32 bit sono esattamente quelli giusti. Sbagliata è
l'**interpretazione** quando quel valore viene stampato, confrontato con `<` o `>`, o
ordinato.

**La soluzione: `>>> 0`.** L'operatore `>>>` è lo scorrimento a destra *senza segno*
(*unsigned right shift*). A differenza di `>>`, non propaga il bit di segno. Scorrere di
**zero** posizioni non muove nulla, ma per definizione del linguaggio `>>>` produce sempre un
risultato **unsigned**. È quindi il modo idiomatico di dire *«prendi questi 32 bit e
interpretali come un numero senza segno»*:

```js
(-256) >>> 0     // →  4294967040
```

Stessi bit, interpretazione corretta.

**La regola applicata in tutto il progetto:** ogni valore a 32 bit viene normalizzato con
`>>> 0` prima di essere confrontato, mostrato o ordinato. Nel codice compare, per esempio,
in `Ip.dotted2int` (riga finale), in `Ip.int2dotted` (prima riga), in `Rotta.copre`, in
`Tdi.cerca`.

**Nota importante e sottile.** Il confronto `(ip & msk) === rete` funzionerebbe *anche senza*
`>>> 0`, purché **tutti e tre** i valori arrivino dalla stessa conversione: due numeri
negativi identici restano identici. Il `>>> 0` non serve alla correttezza del confronto di
uguaglianza, serve a evitare che un valore negativo trapeli in un ordinamento o in una
stampa. Applicarlo sistematicamente costa nulla ed elimina un'intera categoria di errori.

## 2.4 La struttura della TDI: array con scansione lineare completa

**Il problema.** Dove tenere le rotte e come cercarle.

**Le opzioni.**

| Struttura | Costo del lookup | Analisi |
|---|---|---|
| **Array + scansione lineare** ✅ | O(n) | Scelta. Vedi sotto. |
| Array ordinato per prefisso decrescente | O(n) con uscita anticipata al primo match | L'uscita anticipata farebbe risparmiare tempo *ma* impedirebbe di raccogliere le rotte alternative, che vanno comunque mostrate: la scansione andrebbe completata lo stesso. Guadagno nullo, complessità aggiunta sull'inserimento (mantenere l'ordine costa O(n) o O(log n) per inserimento). |
| Dizionario (`Map`) indicizzato per rete | O(1) per la ricerca esatta | Inutilizzabile: non si cerca una rete, si cerca *quale rete contiene un indirizzo*. Bisognerebbe provare tutti i 33 prefissi possibili, mascherando l'indirizzo e cercando ogni volta. Diventa O(33) con 33 accessi al dizionario, e comunque non produce l'elenco delle regole valutate. |
| Trie binario / Patricia trie | O(32) indipendente da n | È ciò che usa un router reale. Vedi sotto. |

**Perché non un trie.** Un trie binario è un albero in cui ogni livello corrisponde a un bit
dell'indirizzo: si scende partendo dal bit più significativo, e la foglia più profonda
raggiunta è la rotta con il prefisso più lungo. Il costo è al massimo 32 passi
**indipendentemente dal numero di rotte** — motivo per cui un router di dorsale, che ha
centinaia di migliaia di rotte, usa esattamente questo.

Due ragioni per non usarlo qui, la seconda molto più importante della prima:

1. **n è piccolo per costruzione.** Una TDI didattica compilata a mano ha una decina di
   righe. Con n = 10 la differenza fra 10 confronti e 32 discese in un albero è a favore
   dell'array. L'ottimizzazione asintotica riguarda una scala che questo programma non
   raggiungerà mai.
2. **Un trie salta le regole non compatibili — ed è esattamente l'informazione che serve.**
   La traccia chiede di *«individuare tutte le route compatibili, magari evidenziandole sulla
   TDI»*. Questo non è un requisito grafico: impone che l'algoritmo **visiti ogni regola e
   conservi l'esito di ogni confronto**. Una struttura il cui pregio è non guardare le regole
   inutili non può produrre quel dato. In questo programma **la scansione lineare *è* la
   visualizzazione**: ogni iterazione del ciclo corrisponde a una riga della tabella da
   colorare e a un calcolo da mostrare.

**Vantaggi della scelta.**

- Produce naturalmente l'elenco completo dei confronti richiesto dalla traccia.
- Il codice dell'algoritmo sta in dieci righe leggibili e ispezionabili.
- L'inserimento è O(1) in coda; nessuna struttura da mantenere ordinata.
- L'ordine delle righe in tabella è quello di inserimento, quindi l'interfaccia è prevedibile
  e la numerazione `#` stabile.

**Svantaggi.**

- O(n) per lookup. Su decine di migliaia di rotte sarebbe inaccettabile.
- Nessun indice: cercare una rotta specifica per rete richiede anch'esso una scansione.

Il trie viene comunque documentato nel progetto come *«ciò che farebbe un router reale»*,
perché saper spiegare **perché non** si è usata la struttura teoricamente migliore vale più
che averla usata senza sapere perché.

## 2.5 L'Esito: la spiegazione è un dato prodotto dalla logica

**Il problema.** La traccia chiede di *«mostrare chiaramente il motivo della scelta
effettuata»*. Dove nasce quel motivo?

**Le opzioni.**

| Opzione | Descrizione | Problema |
|---|---|---|
| **A — La logica restituisce solo il vincitore, la vista ricostruisce il perché** | `cerca()` restituisce una `Rotta`; il codice grafico riguarda la tabella e riscrive la spiegazione | La logica di instradamento finisce **duplicata** dentro la vista. Due implementazioni della stessa regola che possono divergere. Non testabile senza browser. |
| **B — La logica restituisce un oggetto ricco che contiene anche la spiegazione** ✅ | `cerca()` restituisce `{ ip, righe, scelta, alternative, motivo }` | Nessuno |
| C — La logica emette eventi che la vista ascolta | Pattern observer | Sovradimensionato per un solo consumatore; aggiunge indirezione senza guadagno |

**La scelta: B.** `Tdi.cerca(ip)` restituisce un oggetto `Esito` così fatto:

```js
{
  ip: 3289317381,                  // l'indirizzo cercato, come uint32
  righe: [                         // UNA VOCE PER OGNI ROTTA, in ordine di tabella
    { rotta: <Rotta>, idx: 0, and: 3289317376, esito: false },
    ...
  ],
  scelta: <Rotta> | null,          // la vincente secondo LPM
  alternative: [<Rotta>, ...],     // le altre compatibili, ordinate per preferenza
  motivo: "Per 196.13.2.5 vince 196.13.2.0/24. Fissa 24 bit di prefisso, ..."
}
```

**Vantaggi.**

- **Una sola implementazione dell'algoritmo**, nello strato che gli compete.
- **Testabile senza browser.** Tutti i test sul Longest Prefix Match verificano `motivo` e
  `alternative` senza aprire una pagina.
- **La vista diventa banale**, e quindi difficile da sbagliare: riceve un oggetto completo e
  lo disegna.
- **Riutilizzabile.** Quando arriverà il forwarding multi-hop, ogni hop produrrà il proprio
  `Esito` con la propria spiegazione, e il registro del percorso sarà un elenco di `Esito`
  senza una riga di codice nuova.
- `righe` è allineato **posizionalmente** con `tdi.elenco()`: `righe[i]` descrive la rotta
  `i`. La vista può iterare in parallelo senza cercare nulla.

**Svantaggi.**

- L'oggetto contiene **riferimenti** alle `Rotta`, non copie. Se qualcuno modificasse una
  rotta dopo aver ottenuto l'esito, l'esito ne risentirebbe. Nel programma non succede,
  perché ogni modifica alla tabella scarta l'esito precedente (`App.scordaEsito()`), ma è
  una fragilità da conoscere.
- La stringa `motivo` è in italiano e cablata nella logica. Per internazionalizzare il
  programma bisognerebbe restituire dati strutturati e comporre il testo altrove. È una
  scelta consapevole: per un progetto scolastico in italiano, il testo pronto è più
  utile della flessibilità.

## 2.6 Architettura a tre strati

**Il vincolo della traccia.** Separare interfaccia grafica, logica di instradamento e
gestione della persistenza.

**La scelta.**

| Strato | File | Regola ferrea |
|---|---|---|
| **Logica** | `ip.js` `rotta.js` `tdi.js` `iface.js` `pacchetto.js` `router.js` | Nessun riferimento a `document`, `window`, `alert`. Deve poter girare senza browser. |
| **Persistenza** | `persistenza.js` | Traduce fra oggetti del dominio e JSON. Non conosce la vista. |
| **Vista** | `vista-tdi.js` `vista-sim.js` `app.js` | Nessuna aritmetica sugli indirizzi. Riceve dati elaborati e li disegna. |

**Perché queste regole sono buone regole: sono verificabili meccanicamente.** Un principio
architetturale che non si può controllare viene violato senza che nessuno se ne accorga.
Questi due si controllano con un comando:

```bash
grep -l "document\|window" js/ip.js js/rotta.js js/tdi.js js/iface.js js/pacchetto.js js/router.js
# → nessun risultato: confine rispettato
```

```bash
grep -nE "[^&]&[^&]|>>>|<<" js/vista-tdi.js js/vista-sim.js js/app.js
# → js/vista-tdi.js:82:  Ip.int2dotted(ip) + ' & ' + Ip.int2dotted(rt.msk) + ...
```

**Il secondo comando produce esattamente una corrispondenza, ed è istruttivo esaminarla.**
Non è un operatore: è il **carattere** `&` dentro una stringa di testo, quella che compone la
riga di dettaglio `196.13.2.5 & 255.255.255.0 = 196.13.2.0`. La vista sta *scrivendo* il
simbolo dell'AND per mostrarlo all'utente, non lo sta *eseguendo*.

È il caso in cui una verifica automatica va letta e non solo eseguita: un solo risultato, in
una stringa, con il valore già calcolato da `Tdi.cerca` e passato alla vista dentro
`riga.and`. Il confine regge. Se un giorno quella riga diventasse
`Ip.int2dotted(ip & rt.msk)` — cioè la vista rifacesse il conto invece di riceverlo — lo
stesso comando lo segnalerebbe allo stesso modo, e quello sarebbe una violazione vera.

**Il valore concreto della separazione**, al di là del voto:

- I 129 test della logica girano **anche da riga di comando con Node**, senza browser,
  perché lo strato logico non ne dipende (§ 6).
- Cambiare completamente l'aspetto dell'interfaccia non tocca una riga di algoritmo.
- L'algoritmo è leggibile: `tdi.js` è lungo 110 righe e non contiene una sola istruzione
  grafica.

**Unica eccezione, dichiarata.** La vista chiama `Ip.int2dotted()`. È **formattazione**, non
calcolo: converte un numero nella sua rappresentazione leggibile, esattamente come si
chiamerebbe `toFixed(2)` su un prezzo. La regola vietata è fare *aritmetica* (AND,
scorrimenti, confronti di prefisso) nella vista, e quella non viene infranta.

**Svantaggi della separazione.**

- **Più file e più indirezione.** Aggiungere una colonna alla tabella richiede di toccare
  `Rotta` (il campo), `Tdi` (la serializzazione), `VistaTdi` (la cella), `App` (il form) e
  `index.html`. In un file unico sarebbe una modifica sola.
- **Più codice di collegamento.** `App` esiste solo per collegare le viste al dominio: non
  contiene logica di valore, è quasi tutto cablaggio.

Su un progetto di questa dimensione il costo si paga volentieri, perché la traccia valuta
proprio la separazione e perché senza di essa i test non esisterebbero.

## 2.7 Persistenza: serializzare il Router, non la sola tabella

**Il vincolo del browser, spiegato per intero.** Una pagina web **non può scrivere su disco**.
Non esiste un'API che permetta a `index.html` di sovrascrivere un file: sarebbe una falla di
sicurezza enorme (qualunque sito potrebbe riscrivere i documenti dell'utente). L'unica cosa
che una pagina può fare è **offrire un file al browser**, che lo tratterà come un download
normale, con la cartella e il nome decisi dall'utente.

Quindi:

| Operazione | Meccanismo |
|---|---|
| **Salva** | Si costruisce il testo JSON → si crea un `Blob` (un oggetto che rappresenta dati binari in memoria) → `URL.createObjectURL` genera un indirizzo temporaneo `blob:...` che punta a quei dati → si crea un elemento `<a download="config.json">` con quell'indirizzo → si simula il click. Il browser scarica. |
| **Carica** | `<input type="file">` apre il selettore di file del sistema → l'oggetto `File` scelto viene letto da una `FileReader` in modo asincrono → `JSON.parse` → ricostruzione degli oggetti. |

**Perché non `localStorage`.** `localStorage` è un archivio chiave-valore interno al browser.
Sarebbe più comodo, ma **non è un file**: non si può allegare a un'email, non si può copiare
su una chiavetta, non sopravvive a un cambio di browser. La traccia dice «salvare e caricare
la configurazione **da file**», e `localStorage` non lo soddisfa. Non viene usato.

**La scelta più significativa: si serializza il `Router` intero, non la sola `Tdi`.**

```json
{
  "versione": 1,
  "router": {
    "nome": "R1",
    "ifaces": [ { "nome": "eth0", "ip": "196.13.1.1", "msk": "255.255.255.0", "su": true } ],
    "tdi": [
      { "rete": "196.13.2.0", "msk": "255.255.255.0", "gw": "196.13.1.2", "iface": "eth0", "metr": 5 }
    ]
  }
}
```

**Il ragionamento.** Il formato multi-router del futuro sarà:

```json
{ "versione": 2, "routers": [ {...}, {...} ], "links": [ {...} ] }
```

che è un **superset** di quello attuale. Il codice di caricamento potrà accettare entrambi
con un `if` sul campo `versione`, e i file salvati oggi continueranno a caricarsi. Se invece
si fosse salvata la sola tabella (`{ "tdi": [...] }`), il formato futuro sarebbe stato
incompatibile e avrebbe richiesto una migrazione.

**Perché il campo `versione` c'è fin dall'inizio.** Aggiungere un numero di versione a un
formato che già circola è impossibile: i file vecchi non ce l'hanno e non si distinguono da
un file corrotto. Metterlo dal primo giorno costa un campo e compra la possibilità di
evolvere. Il codice lo controlla e rifiuta versioni ignote con un messaggio esplicito
invece di caricare dati che non capisce.

**Perché gli indirizzi nel JSON sono in notazione puntata e non come interi.** Dentro il
programma circolano interi (§ 2.3), ma nel file no: un file di configurazione deve poter
essere **aperto con un editor di testo, letto e corretto a mano**. `"196.13.2.0"` si legge,
`3289317376` no. Il costo è una conversione in serializzazione e una in deserializzazione,
che è esattamente il confine di I/O dove le conversioni devono stare.

**Vantaggi.** Formato leggibile, evolvibile, e con un punto di controllo esplicito.
**Svantaggi.** File più grande (irrilevante), e una conversione in più (irrilevante).

## 2.8 La metrica e le rotte di riserva — una correzione di progetto

Questa sezione documenta un **errore trovato durante l'implementazione e corretto**, perché
il ragionamento è più istruttivo del risultato.

**Il progetto iniziale prevedeva** che `Tdi.agg()` rifiutasse una rotta se ne esisteva già
una con la stessa rete e la stessa netmask. Sembra sensato: due righe uguali sono un errore
di configurazione.

**Il problema, scoperto scrivendo i test.** Si voleva verificare il caso «stesso prefisso,
metrica diversa: vince la metrica minore». Il test era impossibile da scrivere. Il motivo è
una piccola dimostrazione:

> Siano due rotte compatibili con lo stesso indirizzo `ip` e con la stessa lunghezza di
> prefisso. Stessa lunghezza di prefisso ⟹ stessa netmask `m` (una netmask contigua è
> univocamente determinata dalla sua lunghezza). Entrambe compatibili ⟹
> `ip & m = rete₁` e `ip & m = rete₂` ⟹ `rete₁ = rete₂`.
> **Due rotte con lo stesso prefisso che coprono lo stesso indirizzo hanno necessariamente
> stessa rete e stessa netmask.**

Conseguenza: se si rifiutano le rotte con stessa rete e stessa mask, il pareggio sul
prefisso **non può mai verificarsi**, e il campo `metr` non viene mai letto. La metrica era
codice morto.

**La correzione.** La configurazione rifiutata era proprio quella interessante. Nel
funzionamento reale dei router si chiama **floating static route**: la stessa destinazione
raggiungibile per due strade diverse, una principale e una di riserva, distinte dalla
metrica. È esattamente ciò che la traccia chiama *«route alternative utilizzabili come
fallback o fault tolerance»*.

Il criterio corretto:

| Confronto | Metodo | Esito |
|---|---|---|
| Stessa rete + stessa mask | `stessaDest()` | **Ammesso.** È la rotta di riserva. |
| Stessa rete + stessa mask + **stesso gateway** | `identicaA()` | **Rifiutato.** È la stessa istruzione scritta due volte: nessuna informazione aggiuntiva. |

**Il criterio di ordinamento finale**, in tre livelli:

1. **prefisso decrescente** — la regola più specifica vince sempre, qualunque sia la metrica;
2. a parità di prefisso, **metrica crescente** — costo minore vince;
3. a parità di entrambi, **ordine di inserimento** — garantito dalla stabilità di
   `Array.prototype.sort` (obbligatoria dallo standard ECMAScript 2019 in poi).

L'ordine dei livelli non è arbitrario: il prefisso viene prima della metrica perché la
specificità è una proprietà **topologica** (quella regola sa di più su dove sta andando il
pacchetto), mentre la metrica è una preferenza **amministrativa**. Una preferenza non deve
poter scavalcare un'informazione migliore sulla topologia.

**Vantaggi.** La metrica diventa funzionale e il concetto di fallback diventa dimostrabile:
la tabella d'esempio caricata all'avvio contiene proprio una coppia principale/riserva, e
simulando `196.13.2.5` si vede la scelta e il fallback.
**Svantaggi.** Il controllo sui duplicati è più permissivo, quindi è possibile riempire la
tabella di rotte ridondanti verso la stessa destinazione con gateway diversi. È però
esattamente ciò che si può fare su un router vero.

## 2.9 Validazione severa: fallire rumorosamente

**Il principio.** Quando un dato è dubbio, ci sono tre comportamenti possibili: accettarlo,
correggerlo in silenzio, rifiutarlo con un messaggio. Il progetto sceglie sistematicamente
il terzo.

**Caso 1 — bit accesi fuori dalla maschera.** L'utente scrive `192.168.1.77 / 255.255.255.0`.

- *Accettare*: la tabella conterrebbe una riga il cui campo «rete» non è una rete. Il
  confronto `(ip & msk) === rete` sarebbe **sempre falso**, perché il lato sinistro ha
  sempre gli ultimi 8 bit a zero mentre `rete` li ha a 77. Regola morta e silenziosa: il
  caso peggiore, perché non dà errore ma non funziona.
- *Correggere in silenzio* (mascherare a `192.168.1.0`): funzionerebbe, ma nasconderebbe un
  errore di ragionamento dell'utente, che non imparerebbe nulla.
- *Rifiutare con messaggio* ✅ — e suggerire la correzione:
  `la rete 192.168.1.77 ha bit accesi fuori dalla mask /24 — forse intendevi 192.168.1.0`

**Caso 2 — netmask non contigua**, per esempio `255.0.255.0`. Una netmask valida è per
definizione una sequenza di bit a 1 seguita da una sequenza di bit a 0. `255.0.255.0` è
`11111111 00000000 11111111 00000000`: ha un buco. Il concetto stesso di «lunghezza del
prefisso» non è definito, quindi il Longest Prefix Match non avrebbe senso. Rifiutata in tre
punti: nel costruttore di `Rotta`, in quello di `Iface`, e in `Ip.parseMsk`.

**Caso 3 — file JSON malformato o di versione ignota.** Il caricamento fallisce, viene
mostrato un messaggio, e **lo stato corrente resta intatto**. Mai lasciare l'applicazione in
uno stato parziale: è peggio di non aver caricato affatto, perché l'utente non sa più cosa
sta guardando. Nel codice questo si ottiene costruendo il nuovo `Router` **per intero** prima
di sostituire quello vecchio: se la costruzione lancia un errore, l'assegnamento non avviene
mai.

**Caso 4 — nessuna rotta compatibile.** Questo **non è un errore del programma**: è un esito
legittimo. Un router senza default route che riceve un pacchetto per una destinazione
sconosciuta lo scarta (ed eventualmente emette un ICMP *network unreachable*). Il programma
lo riporta come esito, non come eccezione: `scelta: null` e il motivo che lo spiega.

**Vantaggi.** Gli errori si manifestano dove nascono, con un messaggio che dice cosa fare.
**Svantaggi.** Più codice di controllo e un'interfaccia più rigida: chi volesse
deliberatamente inserire una configurazione strana non può.

## 2.10 Test senza framework

**Il problema.** I test servono, ma introdurre Jest o Vitest significa introdurre `npm`, e
con `npm` un build step — che è precisamente il vincolo che il progetto si è dato (§ 2.1).

**La scelta: un runner di asserzioni scritto a mano, una cinquantina di righe.**

`test/runner.js` definisce quattro funzioni globali — `ok`, `eq`, `lancia`, `gruppo` — e una
`riassunto()` che stampa il risultato. `test.html` carica gli **stessi identici file** di
`index.html`, più i file di test, e chiama `riassunto()`.

**Vantaggi.**

- Coerente col vincolo: zero dipendenze anche per i test.
- **Si dimostra in dieci secondi**: doppio click su `test.html` e c'è una lista verde.
- Il runner è leggibile per intero, quindi non c'è magia da spiegare.
- Funziona **anche fuori dal browser**: `riassunto()` controlla se esiste `document`, e in
  sua assenza stampa su console. Questo permette di eseguire tutti i test da riga di comando
  con Node durante lo sviluppo, che è ciò che è stato fatto (§ 6).

**Svantaggi.**

- Nessun *test runner* vero: niente esecuzione selettiva di un singolo test, niente
  isolamento fra test, niente report di copertura, niente mock.
- I test condividono l'ambito globale, quindi due variabili con lo stesso nome in file
  diversi collidono. Contromisura: nomi distinti in ogni file di test.
- Le asserzioni sono minime: `ok`, `eq` (con `===`) e `lancia`. Per confrontare oggetti
  bisogna confrontarne i campi uno a uno, che è ciò che i test fanno.

## 2.11 Nomi, lingua e stile del codice

Identificatori e interfaccia in **italiano**, con anglicismi dove l'inglese è la parola
tecnica giusta (`gw`, `iface`, `pkt`, `msk`, `pfx`), abbreviazioni dove non danneggiano la
leggibilità, classi in `PascalCase` per convenzione JavaScript.

**Perché l'italiano.** Coerenza con la traccia, con il lessico usato a lezione (TDI, rotta,
instradamento) e con il progetto ISO-OSI in C della stessa materia. Un `Tdi.cerca()` è più
immediato di un `RoutingTable.lookup()` per chi valuta.

**Perché le abbreviazioni.** `msk`, `pfx`, `gw`, `metr` compaiono decine di volte ciascuna:
in tabelle allineate e in espressioni come
`match.sort((a, b) => b.pfx - a.pfx || a.metr - b.metr)` la forma breve è più leggibile della
forma estesa, perché la struttura dell'espressione resta visibile in una riga.

**Lo stile dei commenti.** I commenti stanno **dove un lettore si fermerebbe davvero a
chiedersi perché**, non uno per metodo:

- la trappola del segno e il `>>> 0` (in testa a `ip.js`);
- il motivo della scansione lineare invece del trie (in testa a `tdi.js`);
- il test di contiguità della netmask, che è un idioma non ovvio;
- il caso limite di `pfx2msk(0)`;
- il perché `Iface` e `Pacchetto` esistono già pur essendo scheletrici.

Il resto del codice si spiega da sé e non viene annotato. Un commento per ogni metodo
(`// costruttore`, `// restituisce il prefisso`) è rumore che allontana l'occhio dai commenti
che contano davvero.

---

# Parte III — Prerequisiti: tutta la sintassi che serve

Questa parte spiega ogni costrutto JavaScript usato nel progetto. Chi conosce già il
linguaggio può saltare alla Parte IV e tornare qui alla bisogna.

## 3.1 Come il browser esegue questi file

Aprendo `index.html`, il browser legge il documento dall'alto verso il basso. Quando incontra

```html
<script src="js/ip.js"></script>
```

**interrompe** l'analisi del documento, scarica il file, lo esegue integralmente, e solo poi
riprende. Questo è il motivo per cui l'ordine dei tag è vincolante: quando `rotta.js` viene
eseguito, `ip.js` è già stato eseguito e `Ip` esiste.

Gli script sono messi **in fondo al `<body>`**, non nel `<head>`, per due ragioni: la pagina
è già disegnata quando gli script partono (nessun ritardo visibile), e gli elementi HTML
esistono già quando il codice prova a cercarli.

Alla fine dell'analisi il browser emette l'evento `DOMContentLoaded`, e l'ultima riga di
`app.js` lo usa per far partire il programma:

```js
document.addEventListener('DOMContentLoaded', () => App.avvia());
```

## 3.2 `const`, `let` — e perché mai `var`

```js
const Ip = { ... };     // legame non riassegnabile
let n = 0;              // variabile riassegnabile
n = n + 1;              // lecito
```

- `const` dichiara un **legame** che non può essere riassegnato. Attenzione alla sfumatura:
  `const p = [1,2]` impedisce `p = [3,4]` ma **non** impedisce `p.push(3)`. Vincola il nome,
  non il contenuto. Nel progetto `const Ip = {...}` impedisce di sostituire l'oggetto `Ip`,
  ma i suoi metodi restano quelli.
- `let` dichiara una variabile riassegnabile. Nel progetto compare solo dove serve davvero
  accumulare: `let n = 0` nei contatori di `dotted2int` e `msk2pfx`, `let s = '...'` nella
  costruzione del testo di `_motivo`.
- `var` non compare mai. `var` ha ambito di *funzione* invece che di *blocco*, il che produce
  comportamenti sorprendenti: una `var` dichiarata dentro un `for` è visibile anche fuori.
  `const` e `let` hanno ambito di blocco, che è ciò che ci si aspetta.

**Regola seguita nel progetto:** `const` sempre, `let` solo quando la riassegnazione è
necessaria. Un `const` comunica al lettore «questo non cambierà più», che è
un'informazione utile.

## 3.3 Oggetti letterali e metodi abbreviati

Un oggetto letterale è una raccolta di coppie chiave-valore fra graffe:

```js
const punto = { x: 10, y: 20 };
punto.x        // → 10
punto['x']     // → 10, forma equivalente
```

Se un valore è una funzione, si chiama **metodo**. La sintassi abbreviata omette `function`:

```js
const Ip = {
  dotted2int(s) { ... },        // forma abbreviata, usata nel progetto
  // equivalente a:
  // dotted2int: function (s) { ... }
};
```

**Perché `Ip` è un oggetto letterale e non una classe.** `Ip` non ha stato: non c'è nulla da
memorizzare fra una conversione e l'altra. Un oggetto con soli metodi è la forma minima
corretta. Se fosse una classe bisognerebbe scrivere `new Ip()` senza motivo, oppure marcare
tutti i metodi `static`, che è più rumoroso. Lo stesso vale per `Persistenza` e `App`.

**Attenzione a `this` negli oggetti letterali.** Dentro `Ip`, i metodi si richiamano fra loro
scrivendo `Ip.mskValida(m)` e non `this.mskValida(m)`. Il motivo è che `this` in JavaScript
dipende da **come** la funzione viene chiamata, non da dove è definita: se qualcuno estraesse
il metodo (`const f = Ip.msk2pfx; f(x)`), `this` sarebbe `undefined` e il codice si
romperebbe. Usare il nome esplicito `Ip` elimina il problema.

## 3.4 Classi, costruttori, getter, metodi statici

```js
class Rotta {
  constructor(rete, msk, gw, iface, metr) {
    this.rete = rete;                    // crea la proprietà sull'oggetto nuovo
  }

  get pfx() { return Ip.msk2pfx(this.msk); }     // getter

  copre(ip) { ... }                              // metodo d'istanza

  static daDotted(rete, msk, gw, iface, metr) {  // metodo statico
    return new Rotta(...);
  }
}
```

- **`constructor`** è il metodo chiamato da `new Rotta(...)`. `this` è l'oggetto appena
  creato; assegnare a `this.qualcosa` crea la proprietà.
- **`get pfx()`** definisce un **getter**: si legge come una proprietà (`rotta.pfx`, senza
  parentesi) ma esegue codice. Serve per i **valori derivati**: `pfx` non è memorizzato, è
  calcolato da `msk` ogni volta. Vantaggio: non può mai andare fuori sincrono con `msk`.
  Svantaggio: viene ricalcolato a ogni lettura — nel `sort` succede più volte per confronto.
  Su tabelle di questa dimensione è irrilevante; su tabelle enormi si memorizzerebbe il
  valore nel costruttore.
- **`static`** definisce un metodo che appartiene alla **classe**, non alle istanze: si
  chiama `Rotta.daDotted(...)`, non `unaRotta.daDotta(...)`. Serve per le **factory**, cioè
  funzioni che *costruiscono* un oggetto a partire da una forma diversa (`daJSON`,
  `daDotted`). Sono statiche perché quando vengono chiamate l'oggetto non esiste ancora.

**Convenzione dell'underscore.** `_motivo`, `_td`, `_span`, `_dettaglio` cominciano con `_`.
JavaScript (in questa forma) non ha metodi privati veri: l'underscore è una **convenzione**
che significa *«dettaglio interno, non chiamarlo da fuori»*. Non è imposto dal linguaggio,
ma è universalmente compreso.

## 3.5 Funzioni freccia e il problema di `this`

```js
(x) => x * 2                     // un parametro, corpo che è un'espressione: return implicito
x => x * 2                       // le parentesi sono opzionali con un solo parametro
(a, b) => a + b                  // due parametri
() => { ... }                    // nessun parametro, corpo a blocco: serve return esplicito
```

Le funzioni freccia sono più brevi, ma la differenza importante è un'altra: **non hanno un
proprio `this`**, lo ereditano dal contesto in cui sono scritte. È esattamente ciò che serve
nei gestori di eventi:

```js
this.tbody.addEventListener('click', ev => {
  if (b && this.cbElimina) this.cbElimina(...);   // `this` è ancora la VistaTdi
});
```

Con `function (ev) { ... }`, `this` sarebbe stato l'elemento HTML che ha ricevuto il click, e
`this.cbElimina` sarebbe stato `undefined`. Prima delle funzioni freccia si risolveva con
`const self = this;` all'inizio del costruttore.

## 3.6 I metodi degli array usati nel progetto

Sono il vocabolario che rende il codice breve. Tutti tranne `push`, `splice` e `sort`
**non modificano** l'array originale: ne restituiscono uno nuovo.

| Metodo | Cosa fa | Esempio nel progetto |
|---|---|---|
| `push(x)` | Aggiunge in coda. **Modifica.** | `this.rotte.push(r)` |
| `splice(i, n)` | Rimuove `n` elementi da posizione `i`. **Modifica.** | `this.rotte.splice(i, 1)` |
| `slice()` | Copia superficiale dell'array. Con argomento `slice(1)` copia da posizione 1 in poi. | `this.rotte.slice()` per la copia difensiva; `match.slice(1)` per le alternative |
| `map(f)` | Nuovo array con `f` applicata a ogni elemento. Stessa lunghezza. | `this.rotte.map(r => r.toJSON())` |
| `filter(f)` | Nuovo array con i soli elementi per cui `f` è vera. | `righe.filter(r => r.esito)` |
| `forEach(f)` | Esegue `f` su ogni elemento. Non restituisce nulla. | `rotte.forEach((rt, i) => {...})` |
| `some(f)` | `true` se **almeno un** elemento soddisfa `f`. Si ferma al primo. | `this.rotte.some(x => x.identicaA(r))` |
| `find(f)` | Il **primo** elemento che soddisfa `f`, o `undefined`. | `this.ifaces.find(x => x.nome === nome)` |
| `findIndex(f)` | La **posizione** del primo che soddisfa `f`, o `-1`. | `this.ifaces.findIndex(...)` |
| `indexOf(x)` | Posizione di `x` (confronto per identità), o `-1`. | `esito.alternative.indexOf(rt)` |
| `sort(f)` | Ordina **sul posto**. `f(a,b)` deve restituire un numero. | `match.sort((a,b) => ...)` |
| `join(s)` | Unisce gli elementi in una stringa separandoli con `s`. | `.join(', ')` |

**`map` e `forEach` ricevono anche l'indice** come secondo parametro:

```js
this.rotte.map((rt, idx) => { ... })     // rt = elemento, idx = posizione
```

**Come funziona `sort` in dettaglio.** La funzione di confronto riceve due elementi e deve
restituire:

- un numero **negativo** se `a` deve venire **prima** di `b`;
- **zero** se sono equivalenti;
- un numero **positivo** se `a` deve venire **dopo**.

L'espressione usata nel progetto:

```js
match.sort((a, b) => b.pfx - a.pfx || a.metr - b.metr);
```

`b.pfx - a.pfx` — nota l'ordine invertito — è positivo quando `b` ha prefisso maggiore,
quindi `b` viene prima: **ordine decrescente** di prefisso. Se i prefissi sono uguali la
sottrazione dà `0`, che in JavaScript è un valore *falsy*, e l'operatore `||` passa al
secondo termine: `a.metr - b.metr`, che è **crescente** di metrica. Se anche questo dà `0`,
`sort` mantiene l'ordine originale, perché la specifica ECMAScript 2019 impone che `sort`
sia **stabile**.

## 3.7 Gli operatori bit a bit, per intero

Sono il fondamento dell'intero programma. Ogni numero viene prima convertito in un intero a
32 bit con segno, poi l'operatore lavora bit per bit.

### AND — `&`

Restituisce 1 solo dove **entrambi** i bit sono 1.

| a | b | a & b |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

```
  11000100 00001101 00000010 00000101     196.13.2.5
& 11111111 11111111 11111111 00000000     255.255.255.0
= 11000100 00001101 00000010 00000000     196.13.2.0
```

**Uso nel progetto:** applicare la netmask, cioè azzerare la parte host dell'indirizzo.

### OR — `|`

Restituisce 1 dove **almeno uno** dei bit è 1.

| a | b | a \| b |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 1 |

**Uso nel progetto:** comporre l'indirizzo ottetto per ottetto in `dotted2int`. Dopo aver
spostato i bit già accumulati di 8 posizioni a sinistra, gli ultimi 8 bit sono zero, e l'OR
vi deposita il nuovo ottetto: `n = (n << 8) | v`.

### NOT — `~`

Inverte tutti i bit. `~0` è `-1`, perché in complemento a due tutti i bit a 1 rappresentano
`-1`.

```
  11111111 11111111 11111111 00000000     255.255.255.0
~ ─────────────────────────────────────
  00000000 00000000 00000000 11111111     0.0.0.255
```

**Uso nel progetto:** il test di contiguità della netmask.

### Scorrimento a sinistra — `<<`

`x << k` sposta i bit di `k` posizioni a sinistra, riempiendo con zeri a destra. Equivale a
moltiplicare per 2ᵏ.

```
  00000000 00000000 00000000 11000100     196
<< 24
  11000100 00000000 00000000 00000000     196 · 2²⁴
```

**Attenzione a un caso limite decisivo:** JavaScript usa **solo i 5 bit meno significativi**
del secondo operando, cioè lo scorrimento è calcolato **modulo 32**. Quindi `x << 32`
equivale a `x << 0`, cioè non sposta nulla. È il motivo per cui `pfx2msk(0)` è trattato
separatamente:

```js
return p === 0 ? 0 : (0xFFFFFFFF << (32 - p)) >>> 0;
```

Se `p` valesse 0, l'espressione sarebbe `0xFFFFFFFF << 32` = `0xFFFFFFFF << 0` =
`0xFFFFFFFF`, cioè `255.255.255.255` invece del `0.0.0.0` corretto. Un errore che passerebbe
inosservato fino a quando qualcuno inserisce una default route.

### Scorrimento a destra con segno — `>>`

Sposta a destra **propagando il bit di segno**: se il numero è negativo, riempie con 1. Nel
progetto **non viene usato**, proprio perché su indirizzi IP darebbe risultati sbagliati.

### Scorrimento a destra senza segno — `>>>`

Sposta a destra riempiendo **sempre con zeri**, e produce sempre un risultato senza segno.

```
   11000100 00001101 00000010 00000101     196.13.2.5
>>> 24
   00000000 00000000 00000000 11000100     196   ← il primo ottetto
```

**Due usi distinti nel progetto:**

1. **Estrarre un ottetto**, in `int2dotted`: `(n >>> 24) & 255` sposta l'ottetto voluto in
   fondo e poi l'AND con `255` (che è `00000000...11111111`) tiene solo gli ultimi 8 bit.
2. **Normalizzare il segno**, con `>>> 0`: non sposta nulla, ma forza l'interpretazione
   unsigned (§ 2.3.1).

### Precedenza degli operatori — perché tante parentesi

Gli operatori bit a bit hanno precedenza **più bassa** dei confronti in JavaScript. Questo
significa che

```js
ip & msk === rete
```

viene interpretato come `ip & (msk === rete)`, che è quasi certamente non ciò che si voleva.
Nel progetto le parentesi sono sempre esplicite:

```js
(((ip >>> 0) & this.msk) >>> 0) === this.rete
```

Sono più parentesi del minimo necessario, ma rendono l'ordine di valutazione leggibile senza
dover ricordare una tabella di precedenze.

## 3.8 Operatori logici e di confronto

| Operatore | Significato |
|---|---|
| `===` | Uguaglianza **stretta**: nessuna conversione di tipo. `1 === '1'` è `false`. |
| `!==` | Disuguaglianza stretta. |
| `==` | Uguaglianza con conversione. `1 == '1'` è `true`. **Non usato nel progetto**, perché le sue regole di conversione sono piene di casi sorprendenti. |
| `!x` | Negazione. Converte `x` in booleano e lo inverte. |
| `!!x` | Doppia negazione: converte in booleano vero e proprio. Usato in `classList.toggle('simulata', !!esito)`. |
| `a \|\| b` | Se `a` è *truthy* restituisce `a`, altrimenti `b`. Usato per i valori predefiniti: `String(nome \|\| 'R1')`. |
| `a && b` | Se `a` è *falsy* restituisce `a`, altrimenti `b`. Usato come guardia: `if (b && this.cbElimina)`. |
| `c ? x : y` | Operatore ternario: se `c` è vera vale `x`, altrimenti `y`. |

**Valori *falsy*** — quelli che si comportano come `false` in un contesto booleano:
`false`, `0`, `''` (stringa vuota), `null`, `undefined`, `NaN`. Tutto il resto è *truthy*,
compresi `[]` e `{}`.

Questo spiega alcune espressioni del progetto:

```js
const scelta = match.length ? match[0] : null;
```

`match.length` vale 0 se l'array è vuoto, e `0` è falsy: quindi `scelta` diventa `null`.
Non serve scrivere `match.length > 0`.

```js
if (esito.alternative.length) { ... }     // «se ci sono alternative»
```

## 3.9 Stringhe

Il progetto usa la **concatenazione con `+`**:

```js
'rotta già presente: ' + Ip.int2dotted(r.rete) + '/' + r.pfx
```

JavaScript offre anche i *template literal* con i backtick e `${}`. Sono spesso più
leggibili, ma qui la concatenazione è preferita per uniformità: le espressioni interpolate
sono quasi tutte chiamate di funzione, e `' + Ip.int2dotted(x) + '` non è meno chiaro di
`${Ip.int2dotted(x)}`.

**Metodi usati:**

| Metodo | Cosa fa |
|---|---|
| `String(x)` | Converte qualsiasi valore in stringa. Robusto anche su `null`/`undefined`. |
| `.trim()` | Toglie spazi bianchi iniziali e finali. |
| `.split('.')` | Divide in un array usando `.` come separatore. |
| `.indexOf(s)` | Posizione della prima occorrenza, o `-1` se assente. |
| `.slice(1)` | Sottostringa da posizione 1 in poi. Usato per togliere lo `/` da `/24`. |
| `.toLowerCase()` | Minuscolo. Usato solo nei test, per confronti insensibili alle maiuscole. |
| `t[0]` | Primo carattere. |

**L'apostrofo nelle stringhe.** Le stringhe sono delimitate da apici singoli, quindi un
apostrofo interno va protetto con la barra rovesciata:

```js
'non c\'è una default route'
```

## 3.10 Numeri e conversioni

| Espressione | Cosa fa |
|---|---|
| `parseInt(s, 10)` | Converte una stringa in intero **in base 10**. La base va sempre indicata esplicitamente: senza, alcune stringhe verrebbero lette in base 8 o 16. |
| `Number(x)` | Conversione numerica generale. Restituisce `NaN` se impossibile. |
| `Number.isInteger(x)` | `true` solo se `x` è un numero intero. `Number.isInteger('5')` è `false`. |
| `Number.isFinite(x)` | `true` se è un numero finito: esclude `NaN`, `Infinity`, `-Infinity`. |

**Perché `Number.isFinite` e non `isFinite`.** La versione globale `isFinite('5')`
restituisce `true` perché converte prima la stringa. La versione su `Number` non converte:
è più severa, ed è quella giusta per validare.

**La notazione esadecimale.** `0xFFFFFFFF` è 4 294 967 295, cioè 32 bit tutti a 1. Si usa
l'esadecimale perché ogni cifra corrisponde esattamente a 4 bit, quindi `0xFF` = `11111111`
si legge a colpo d'occhio come «un ottetto pieno».

## 3.11 Espressioni regolari

Il progetto ne usa due.

```js
/^\d{1,3}$/.test(o)
```

| Pezzo | Significato |
|---|---|
| `/` ... `/` | Delimitatori dell'espressione regolare |
| `^` | Ancora all'**inizio** della stringa |
| `\d` | Una cifra da 0 a 9 |
| `{1,3}` | Da una a tre ripetizioni di ciò che precede |
| `$` | Ancora alla **fine** della stringa |
| `.test(s)` | Restituisce `true` se `s` corrisponde |

Le ancore `^` e `$` sono essenziali: senza di esse, `/\d{1,3}/.test('abc12')` sarebbe `true`,
perché troverebbe `12` da qualche parte dentro. Con le ancore, la stringa **intera** deve
essere da una a tre cifre.

La seconda, `/^\d{1,2}$/`, è la stessa cosa per la notazione CIDR: da una a due cifre, così
`/24` viene accettato e `/241` no.

**Cosa questa espressione lascia passare deliberatamente.** `010` corrisponde a `^\d{1,3}$`,
e `parseInt('010', 10)` dà 10. Gli zeri iniziali vengono quindi accettati e interpretati in
base 10. È una scelta: rifiutarli sarebbe più severo, accettarli è più tollerante con chi
digita, e non introduce ambiguità perché la base è forzata a 10.

## 3.12 `throw`, `try`/`catch`, `Error`

```js
throw new Error('netmask non contigua: ' + Ip.int2dotted(m));
```

`throw` interrompe immediatamente l'esecuzione e propaga l'errore verso l'alto lungo la
catena delle chiamate, finché qualcuno non lo cattura. Se nessuno lo cattura, il programma
si ferma e il browser lo segnala in console.

`new Error(messaggio)` crea un oggetto errore con una proprietà `.message`.

```js
try {
  this.router.tdi.agg(Rotta.daDotted(...));
  // se si arriva qui, non è stato lanciato nulla
} catch (e) {
  err.textContent = e.message;
}
```

**Perché questo schema è quello giusto qui.** La validazione sta nel **costruttore di
`Rotta`**, cioè il più vicino possibile al dato. Un oggetto `Rotta` che esiste è, per
costruzione, valido: nessun'altra parte del programma deve ricontrollarlo. Il controller si
limita a catturare l'errore e a mostrarlo.

**Il punto cruciale nel controller:** l'ordine delle operazioni.

```js
this.router.tdi.agg(Rotta.daDotted(...));   // se lancia, si salta tutto il resto
err.hidden = true;
// ... svuotamento del form, ridisegno
```

`Rotta.daDotted(...)` viene valutata **prima** che `agg` venga chiamata, e `agg` prima di
tutto il resto. Se la costruzione fallisce, l'esecuzione salta direttamente al `catch`: la
tabella non viene toccata, il form non viene svuotato, il ridisegno non avviene. Lo stato
resta esattamente com'era. Questo non è un caso: è il motivo per cui la validazione sta nel
costruttore e non in un metodo `valida()` da chiamare a parte, che si potrebbe dimenticare.

## 3.13 Callback e Promise

### Callback

Una **callback** è una funzione passata a un'altra funzione perché la chiami quando serve.
Nel progetto è il meccanismo con cui la vista comunica al controller senza conoscerlo:

```js
// dentro VistaTdi
onElimina(cb) { this.cbElimina = cb; }        // memorizza la funzione

// più tardi, al click:
if (b && this.cbElimina) this.cbElimina(Number(b.dataset.i));
```

```js
// dentro App
this.vTdi.onElimina(i => {                     // fornisce la funzione
  this.router.tdi.rimuovi(i);
  this.scordaEsito();
  this.ridisegna();
});
```

**Perché è importante:** `VistaTdi` non sa che esiste `App`, non sa che esiste `Tdi`, non sa
cosa succederà quando qualcuno clicca «elimina». Sa solo che deve avvisare. È
l'**inversione delle dipendenze**: la vista, che sta in basso, non dipende dal controller,
che sta in alto.

### Promise

Leggere un file è **asincrono**: il risultato non è disponibile subito. Una `Promise` è un
oggetto che rappresenta un valore *che arriverà*.

```js
importa(file) {
  return new Promise((risolvi, rifiuta) => {
    const fr = new FileReader();
    fr.onerror = () => rifiuta(new Error('impossibile leggere il file'));
    fr.onload  = () => {
      try { risolvi(Persistenza.deserializza(JSON.parse(fr.result))); }
      catch (e) { rifiuta(new Error('file non valido: ' + e.message)); }
    };
    fr.readAsText(file);
  });
}
```

Il costruttore riceve una funzione con due parametri: `risolvi` da chiamare in caso di
successo, `rifiuta` in caso di errore. Chi usa la Promise si aggancia con `.then()` e
`.catch()`:

```js
Persistenza.importa(f)
  .then(r => { /* successo: r è il Router ricostruito */ })
  .catch(e => { /* errore: e è l'Error */ });
```

**Perché la Promise serve qui.** `FileReader` funziona a eventi (`onload`, `onerror`).
Avvolgerlo in una Promise trasforma un'API a eventi in una a valore, e permette al chiamante
di scrivere il percorso felice e quello d'errore uno accanto all'altro invece che sparsi in
due gestori.

**Il `try`/`catch` dentro `onload` è essenziale.** Un'eccezione lanciata dentro un gestore di
evento **non** viene catturata dal `catch` del chiamante: il gestore viene eseguito molto
dopo, in un altro giro del ciclo degli eventi, quando lo stack della chiamata originale non
esiste più. Senza quel `try`/`catch`, un file JSON malformato produrrebbe un errore in
console e la Promise resterebbe **sospesa per sempre**, senza né `then` né `catch`.

## 3.14 Il DOM: creare, riempire, ascoltare

Il **DOM** (*Document Object Model*) è la rappresentazione ad oggetti della pagina. Ogni
elemento HTML è un oggetto manipolabile da JavaScript.

### Trovare elementi

```js
document.getElementById('tab-tdi')     // l'elemento con id="tab-tdi", o null
tabella.querySelector('tbody')         // il primo <tbody> dentro `tabella`
ev.target.closest('button[data-i]')    // il primo antenato (o sé stesso) che è un
                                       // <button> con attributo data-i
```

### Creare e riempire

```js
const td = document.createElement('td');    // crea l'elemento, ancora staccato dalla pagina
td.textContent = 'eth0';                    // ne imposta il contenuto testuale
td.className = 'ind';                       // ne imposta l'attributo class
padre.appendChild(td);                      // lo inserisce nel documento
```

**`textContent` e non `innerHTML`, sempre.** `innerHTML` interpreta la stringa come **HTML**:
se contenesse `<script>` o un attributo `onerror`, verrebbe eseguito. Poiché parte del
contenuto viene da ciò che l'utente digita (il nome dell'interfaccia, per esempio), usare
`innerHTML` sarebbe una vulnerabilità XSS. `textContent` inserisce testo e basta: un `<` resta
un `<`. È anche più veloce, perché non richiede analisi sintattica.

**`this.tbody.textContent = ''`** è il modo più rapido di svuotare un elemento: rimuove tutti
i figli in una sola operazione.

### Altri accessi usati

| Espressione | Cosa fa |
|---|---|
| `el.hidden = true` | Nasconde l'elemento (attributo HTML `hidden`) |
| `el.classList.toggle('x', cond)` | Aggiunge la classe `x` se `cond` è vera, la toglie se falsa |
| `b.dataset.i = 5` | Imposta l'attributo `data-i="5"`; si rilegge con `b.dataset.i` (come **stringa**) |
| `td.colSpan = 7` | La cella occupa 7 colonne |
| `input.value` | Il testo digitato in un campo |
| `input.files[0]` | Il primo file scelto in un `<input type="file">` |

**Gli attributi `data-*`** sono il modo standard di attaccare dati applicativi a un elemento
HTML. Qui servono a ricordare **quale riga** rappresenta ogni bottone «elimina». Nota che
`dataset` restituisce sempre stringhe, per cui il codice converte: `Number(b.dataset.i)`.

### Ascoltare eventi e la delega

```js
elemento.addEventListener('click', funzione);
```

Il progetto usa la **delega degli eventi**: invece di registrare un ascoltatore su ciascuno
dei bottoni «elimina», ne registra **uno solo** sul `<tbody>` che li contiene.

```js
this.tbody.addEventListener('click', ev => {
  const b = ev.target.closest('button[data-i]');
  if (b && this.cbElimina) this.cbElimina(Number(b.dataset.i));
});
```

**Come funziona.** Quando si clicca un bottone, l'evento *risale* (bubbling) dal bottone
verso i suoi antenati, quindi arriva al `<tbody>`. Lì `ev.target` è l'elemento originale che
è stato cliccato; `closest('button[data-i]')` risale finché non trova un bottone con
l'attributo `data-i`, e restituisce `null` se il click era altrove.

**Perché è la scelta giusta qui.** Il corpo della tabella viene **ricostruito da zero a ogni
ridisegno**: tutti i bottoni vengono distrutti e ricreati. Con un ascoltatore per bottone
bisognerebbe registrarli ogni volta, e i vecchi resterebbero in memoria attaccati a elementi
che non esistono più. Il `<tbody>`, invece, non viene mai sostituito: il suo ascoltatore è
registrato una volta sola nel costruttore e continua a funzionare per sempre.

### `preventDefault`

```js
this.form.addEventListener('submit', ev => {
  ev.preventDefault();
  ...
});
```

Il comportamento predefinito dell'invio di un `<form>` è **ricaricare la pagina**, inviando i
dati a un server. Qui non c'è nessun server e ricaricare azzererebbe tutto.
`preventDefault()` annulla quel comportamento e lascia che sia il codice a gestire l'evento.

Usare comunque un `<form>` invece di un semplice bottone porta due vantaggi gratuiti:
premere **Invio** in un campo invia il form, e gli attributi `required` fanno fare al browser
un primo controllo di campo non vuoto prima ancora che il codice parta.

---

# Parte IV — Analisi del codice, file per file

Ordine di lettura: dal più basso livello al più alto, che è anche l'ordine in cui i file
vengono caricati dall'HTML.

## 4.1 `js/ip.js` — conversioni e validazione

Unico punto del programma che conosce la notazione puntata. Sei funzioni, nessuno stato.

### 4.1.1 Intestazione e dichiarazione

```js
// Un indirizzo IPv4 è un numero a 32 bit. La notazione dotted è solo il vestito
// che indossa per farsi leggere dagli umani: nasce qui, muore qui, e nel resto del
// programma circolano soltanto interi.
//
// Avvertenza valida per tutto il file: in JavaScript gli operatori bit a bit
// lavorano su interi a 32 bit CON SEGNO. Senza il ">>> 0" finale, 255.255.255.255
// verrebbe fuori come -1, il che rende i confronti d'ordine molto creativi.
const Ip = {
```

**Cosa fa.** Dichiara un oggetto letterale con soli metodi, senza stato (§ 3.3).

**Perché non una classe.** Non c'è nulla da memorizzare fra una conversione e l'altra. Una
classe imporrebbe `new Ip()` senza ragione, oppure `static` su ogni metodo. L'oggetto
letterale è la forma minima corretta.

**Perché il commento sta qui.** È l'avvertenza che vale per tutto il file e per tutto il
programma. Chi apre `ip.js` per la prima volta legge subito la cosa che gli farebbe perdere
un'ora di debug.

### 4.1.2 `dotted2int` — da `"192.168.1.1"` a `3232235777`

```js
  dotted2int(s) {
    const p = String(s).trim().split('.');
    if (p.length !== 4) throw new Error('servono esattamente 4 ottetti: "' + s + '"');
    let n = 0;
    for (const o of p) {
      if (!/^\d{1,3}$/.test(o)) throw new Error('ottetto non numerico in "' + s + '"');
      const v = parseInt(o, 10);
      if (v > 255) throw new Error('ottetto fuori range 0-255 in "' + s + '"');
      n = (n << 8) | v;
    }
    return n >>> 0;
  },
```

**Riga 1 — `String(s).trim().split('.')`.**
Tre operazioni concatenate. `String(s)` converte in stringa qualunque cosa arrivi: se
qualcuno passasse un numero o `null`, non si otterrebbe un errore incomprensibile su un
metodo mancante. `.trim()` toglie gli spazi ai lati, così `"  10.0.0.1  "` digitato per
sbaglio funziona. `.split('.')` divide sul punto e restituisce un array di stringhe.

**Riga 2 — controllo del numero di ottetti.** `"1.2.3"` produce un array di 3 elementi:
rifiutato. `"1.2.3.4.5"` ne produce 5: rifiutato. Il messaggio d'errore include la stringa
originale fra virgolette, così l'utente vede esattamente cosa ha digitato — comprese
eventuali spaziature invisibili.

**Riga 3 — `let n = 0`.** L'accumulatore. È `let` e non `const` perché viene riassegnato a
ogni giro del ciclo.

**Riga 4 — `for (const o of p)`.** Il ciclo `for...of` scorre i **valori** di un iterabile.
Da non confondere con `for...in`, che scorre le **chiavi** (per un array, gli indici come
stringhe: `"0"`, `"1"`, ...) ed è quasi sempre l'errore. `const o` è lecito dentro un
`for...of` perché a ogni iterazione viene creato un legame nuovo.

**Riga 5 — la validazione dell'ottetto.** `/^\d{1,3}$/` (§ 3.11) impone: da una a tre cifre,
niente altro. Questo rifiuta `"a"`, `"1a"`, `"-1"`, `""` (stringa vuota, che si ottiene da
`"1..3.4"`), `" 5"` (perché lo spazio interno non è stato rimosso da `trim`, che agisce solo
sui bordi della stringa intera).

**Riga 6 — `parseInt(o, 10)`.** La base 10 esplicita è obbligatoria per igiene. Storicamente
`parseInt("010")` senza base poteva essere interpretato in ottale.

**Riga 7 — il controllo di range.** Il controllo `> 255` viene **dopo** quello sintattico e
non prima: senza il controllo sintattico, `parseInt("abc")` restituirebbe `NaN`, e
`NaN > 255` è `false`, quindi il valore fasullo passerebbe. L'ordine dei due controlli non è
casuale.

Non serve un controllo `< 0`: la regex non ammette il segno meno.

**Riga 8 — `n = (n << 8) | v`.** Il cuore della funzione. Sposta l'accumulato di 8 posizioni
a sinistra, liberando gli ultimi 8 bit, e vi deposita il nuovo ottetto con l'OR. Traccia
completa per `192.168.1.1`:

| Giro | `n` prima | `n << 8` | `v` | `n` dopo (binario) | `n` dopo (decimale) |
|---|---|---|---|---|---|
| 1 | `0` | `0` | 192 | `00000000 00000000 00000000 11000000` | 192 |
| 2 | 192 | `…11000000 00000000` | 168 | `00000000 00000000 11000000 10101000` | 49 320 |
| 3 | 49 320 | `…10101000 00000000` | 1 | `00000000 11000000 10101000 00000001` | 12 626 433 |
| 4 | 12 626 433 | `…00000001 00000000` | 1 | `11000000 10101000 00000001 00000001` | −1 062 731 519 ⚠️ |

**Riga 9 — `return n >>> 0`.** Ecco perché serve. All'ultimo giro il bit più significativo
diventa 1 e il valore viene interpretato come negativo. `>>> 0` restituisce gli stessi 32 bit
letti come unsigned: `3232235777`. Senza questa riga, tutti i confronti d'ordine e tutte le
stampe successive sarebbero sbagliate.

**Alternativa scartata.** Si sarebbe potuto scrivere
`p[0]*16777216 + p[1]*65536 + p[2]*256 + p[3]`, come fa il codice C. Funziona e non ha il
problema del segno, perché usa l'aritmetica in virgola mobile a 64 bit. Ma è meno diretto —
maschera che l'operazione vera è uno spostamento di bit — e comunque il valore andrebbe poi
usato con operatori bit a bit, che lo riconvertirebbero a 32 bit con segno. Tanto vale
restare nel dominio dei bit dall'inizio e normalizzare una volta sola.

### 4.1.3 `int2dotted` — la conversione inversa

```js
  int2dotted(n) {
    n = n >>> 0;
    return ((n >>> 24) & 255) + '.' + ((n >>> 16) & 255) + '.' +
           ((n >>>  8) & 255) + '.' + ( n         & 255);
  },
```

**Riga 1 — normalizzazione in ingresso.** La funzione viene chiamata anche con valori
potenzialmente negativi (per esempio dentro un messaggio d'errore, su un dato non ancora
validato). Normalizzare subito la rende robusta: `Ip.int2dotted(-1)` restituisce
`"255.255.255.255"` invece di qualcosa di assurdo. C'è un test apposta per questo.

**Righe 2-3 — estrazione degli ottetti.** Ogni ottetto si estrae in due mosse:

1. `n >>> k` porta l'ottetto voluto nelle 8 posizioni meno significative;
2. `& 255` (cioè `& 0b11111111`) azzera tutto il resto.

Su `192.168.1.1` = `11000000 10101000 00000001 00000001`:

| Espressione | Dopo lo scorrimento | Dopo `& 255` | Valore |
|---|---|---|---|
| `n >>> 24` | `00000000 00000000 00000000 11000000` | idem | 192 |
| `n >>> 16` | `00000000 00000000 11000000 10101000` | `…10101000` | 168 |
| `n >>> 8` | `00000000 11000000 10101000 00000001` | `…00000001` | 1 |
| `n` | invariato | `…00000001` | 1 |

Per il primo ottetto l'AND con 255 sarebbe superfluo (lo scorrimento di 24 posizioni ha già
azzerato tutto il resto), ma è mantenuto per **simmetria**: quattro espressioni della stessa
forma si leggono meglio di tre uguali e una diversa.

**Perché `>>>` e non `>>`.** Con `>>` e un indirizzo il cui primo bit è 1, lo scorrimento
propagherebbe il bit di segno riempiendo di 1: `(-1) >> 24` dà `-1`, e `-1 & 255` dà 255 —
in questo caso specifico il risultato sarebbe corretto per caso, ma per i valori intermedi
no. `>>>` non lascia margine.

**L'allineamento a colonna.** Gli spazi in `(n >>>  8)` e `( n         & 255)` sono
deliberati: incolonnano le quattro espressioni così che la struttura ripetuta si veda a
colpo d'occhio.

### 4.1.4 `mskValida` — il test di contiguità

```js
  // Una netmask valida è una fila di 1 seguita da una fila di 0, senza buchi.
  // Complementandola si ottiene 0...01...1; sommando 1 resta una sola potenza di
  // due (o si va in overflow a 0, che è il caso /0). E "x & (x-1) === 0" è il
  // classico test per le potenze di due.
  mskValida(m) {
    const c = (((~m) >>> 0) + 1) >>> 0;
    return c === 0 || (c & (c - 1)) === 0;
  },
```

**Il problema.** Una netmask valida ha la forma `1…1 0…0`. `255.0.255.0` no. Come
riconoscerlo senza scorrere i 32 bit?

**Il ragionamento, in tre passi.**

*Passo 1 — complemento.* Se `m` è `1…1 0…0`, allora `~m` è `0…0 1…1`.

```
m  = 255.255.255.0  =  11111111 11111111 11111111 00000000
~m                  =  00000000 00000000 00000000 11111111   = 255
```

*Passo 2 — somma di 1.* Un numero della forma `0…0 1…1` (k bit a 1 in fondo) sommato a 1
diventa `0…0 1 0…0`, cioè esattamente 2ᵏ: **una potenza di due**.

```
~m + 1  =  00000000 00000000 00000001 00000000   = 256 = 2⁸
```

*Passo 3 — test di potenza di due.* `x & (x - 1) === 0` è l'idioma classico. Il motivo:
sottrarre 1 a una potenza di due spegne l'unico bit acceso e accende tutti quelli sotto.

```
x     = 256  =  ...00000001 00000000
x - 1 = 255  =  ...00000000 11111111
x & (x-1)    =  ...00000000 00000000  = 0   → è una potenza di due ✓
```

Se invece un numero ha più di un bit acceso, sottrarre 1 tocca solo il bit acceso più basso e
quelli sotto, lasciando intatti quelli più alti — che quindi sopravvivono all'AND:

```
x     = 12  =  1100
x - 1 = 11  =  1011
x & (x-1)   =  1000  ≠ 0   → NON è una potenza di due ✗
```

**Verifica su una maschera non valida.**

```
m     = 255.0.255.0  =  11111111 00000000 11111111 00000000
~m                   =  00000000 11111111 00000000 11111111   = 16 711 935
~m + 1               =  00000000 11111111 00000001 00000000   = 16 711 936
(~m+1) & (~m+1 - 1)  =  00000000 11111111 00000000 00000000   ≠ 0  → rifiutata ✓
```

**Il caso `/0`.** Se `m` è 0, `~m` è `0xFFFFFFFF` = 4 294 967 295, e sommando 1 si ottiene
4 294 967 296, che in JavaScript **non trabocca** (è un `number` a 64 bit, quindi il valore è
rappresentabile esattamente). Ma `>>> 0` lo tronca a 32 bit, e i 32 bit bassi di 2³² sono
tutti zero: il risultato è `0`. Da qui il ramo `c === 0 ||` all'inizio del `return`.

**Il caso `/32`.** `m` = `0xFFFFFFFF`, `~m >>> 0` = 0, `+1` = 1, e `1 & 0` = 0: accettata ✓.

**Perché due `>>> 0`.** Il primo, su `~m`, normalizza il complemento che sarebbe negativo. Il
secondo, sul totale, tronca il possibile 2³² del caso `/0` riportandolo nei 32 bit.
Entrambi sono necessari.

**Alternativa scartata.** Un ciclo che scorre i 32 bit da sinistra e verifica che dopo il
primo 0 non ci siano più 1. È più lungo, più facile da sbagliare sui bordi, e non insegna
nulla. L'idioma bit a bit è compatto e, con il commento accanto, comprensibile.

### 4.1.5 `msk2pfx` — contare i bit a 1

```js
  msk2pfx(m) {
    m = m >>> 0;
    if (!Ip.mskValida(m)) throw new Error('netmask non contigua: ' + Ip.int2dotted(m));
    let n = 0;
    for (let i = 0; i < 32; i++) {
      if (m & (1 << (31 - i))) n++;
    }
    return n;
  },
```

**Riga 2 — la validazione prima del conteggio.** Fondamentale: su una maschera con buchi il
numero di bit a 1 esisterebbe comunque (`255.0.255.0` ne ha 16), ma sarebbe **privo di
significato**, perché non corrisponderebbe a nessun prefisso. Contare senza validare
produrrebbe un numero plausibile e sbagliato — il tipo di errore peggiore. La funzione
preferisce lanciare.

**Righe 4-6 — il conteggio.** `1 << (31 - i)` costruisce una maschera con **un solo bit
acceso**, che scorre da sinistra a destra:

| `i` | `31 - i` | `1 << (31-i)` |
|---|---|---|
| 0 | 31 | `10000000 00000000 00000000 00000000` |
| 1 | 30 | `01000000 00000000 00000000 00000000` |
| … | … | … |
| 31 | 0 | `00000000 00000000 00000000 00000001` |

`m & maschera` vale zero se quel bit di `m` è 0, e un valore diverso da zero se è 1. Poiché
zero è *falsy* e ogni altro numero è *truthy* (§ 3.8), l'`if` funziona senza confronto
esplicito.

**Nota sul segno, che qui non dà fastidio.** Al primo giro `1 << 31` produce
`-2147483648` (il bit di segno acceso). L'AND con `m` restituisce o `0` o `-2147483648`,
entrambi valutati correttamente come falsy/truthy. Il segno è irrilevante perché il valore
serve solo come booleano, non viene confrontato né stampato.

**Perché scorrere da sinistra.** Il risultato sarebbe identico partendo da destra, dato che
si conta e basta. L'ordine da sinistra rispecchia però il modo in cui si legge una netmask e
rende il codice coerente con l'idea di «prefisso», che è la parte iniziale.

**Alternativa scartata.** Poiché la maschera è già stata validata come contigua, il prefisso
si potrebbe ricavare senza ciclo: `32 - Math.log2((~m >>> 0) + 1)`. È più corto ma passa per
i logaritmi in virgola mobile per calcolare un numero intero, il che è concettualmente
sbagliato e potenzialmente impreciso ai bordi. Il ciclo a 32 passi è esatto e trasparente.

### 4.1.6 `pfx2msk` — da `/24` a `255.255.255.0`

```js
  pfx2msk(p) {
    if (!Number.isInteger(p) || p < 0 || p > 32) throw new Error('prefisso fuori range: /' + p);
    // Il /0 va trattato a parte: lo shift usa solo i 5 bit bassi del secondo
    // operando, quindi "<< 32" equivale a "<< 0" e restituirebbe tutti 1.
    return p === 0 ? 0 : (0xFFFFFFFF << (32 - p)) >>> 0;
  },
```

**Riga 1 — la validazione.** Tre controlli in uno. `Number.isInteger` esclude i decimali e
i valori non numerici (`"24"` come stringa viene rifiutato: la conversione è compito del
chiamante). Poi il range 0–32.

**Riga 4 — il caso limite, che è la ragione d'essere di questa funzione.**
`0xFFFFFFFF << (32 - p)` prende 32 bit tutti a 1 e li spinge a sinistra, facendo entrare zeri
da destra: `<< 8` lascia 24 bit a 1, cioè `/24`.

Ma per `p = 0` lo scorrimento sarebbe di 32 posizioni, e come spiegato in § 3.7 JavaScript
calcola lo scorrimento **modulo 32**: `<< 32` equivale a `<< 0`, e il risultato sarebbe
`0xFFFFFFFF` — cioè `255.255.255.255` invece di `0.0.0.0`.

**Perché questo bug sarebbe stato particolarmente insidioso.** Non provoca nessun errore. La
default route verrebbe semplicemente creata con maschera `/32` invece che `/0`, quindi
smetterebbe di funzionare come default: non coprirebbe più tutti gli indirizzi ma uno solo.
Un pacchetto per `8.8.8.8` risulterebbe irraggiungibile senza spiegazione apparente. Il
programma continuerebbe a funzionare, dando risposte sbagliate. C'è un test dedicato:
`eq('pfx2msk 0', Ip.pfx2msk(0), 0)`.

**Verifica per `p = 24`:**

```
0xFFFFFFFF        =  11111111 11111111 11111111 11111111
<< (32 - 24) = 8  =  11111111 11111111 11111111 00000000   →  255.255.255.0 ✓
```

### 4.1.7 `parseMsk` — accettare tre notazioni

```js
  // Accetta sia "255.255.255.0" sia "/24" sia "24", perché nessuno ha voglia di
  // ricordarsi quale delle tre voleva il form.
  parseMsk(s) {
    const t = String(s).trim();
    if (t === '') throw new Error('netmask vuota');
    if (t.indexOf('.') >= 0) {
      const m = Ip.dotted2int(t);
      if (!Ip.mskValida(m)) throw new Error('netmask non contigua: ' + t);
      return m;
    }
    const cidr = t[0] === '/' ? t.slice(1) : t;
    if (!/^\d{1,2}$/.test(cidr)) throw new Error('netmask non riconosciuta: "' + s + '"');
    return Ip.pfx2msk(parseInt(cidr, 10));
  }
```

**Il criterio di discriminazione: la presenza del punto.** Se la stringa contiene un punto è
notazione decimale puntata, altrimenti è CIDR. È un criterio semplice e sufficiente: nessuna
notazione CIDR contiene punti, nessuna notazione puntata ne è priva.

**Ramo puntato.** Riusa `dotted2int` (che valida ottetti e formato) e poi aggiunge il
controllo di contiguità, che per un indirizzo generico non ha senso ma per una maschera sì.
Il messaggio d'errore riporta la stringa originale `t`, non il valore convertito: è più
utile vedere ciò che si è digitato.

**Ramo CIDR.** `t[0] === '/' ? t.slice(1) : t` toglie la barra se c'è, così `"/24"` e `"24"`
diventano entrambi `"24"`. Poi la regex `^\d{1,2}$` limita a due cifre — `/33` viene
respinto già qui, e comunque `pfx2msk` lo respingerebbe di nuovo. Doppio controllo
volutamente ridondante: `parseMsk` dà un messaggio orientato all'input dell'utente,
`pfx2msk` protegge sé stessa anche se chiamata da altrove.

**Perché questa funzione esiste.** È la sola concessione alla comodità dell'utente in tutto
lo strato logico, ed è motivata: la netmask è il campo che si sbaglia più spesso, e obbligare
a una sola notazione fra tre ugualmente diffuse è una frizione inutile. Il costo è dieci
righe, il beneficio è che `255.255.255.0`, `/24` e `24` funzionano tutti.

## 4.2 `js/rotta.js` — una riga della tabella

### 4.2.1 Il costruttore: dove vive tutta la validazione

```js
class Rotta {

  constructor(rete, msk, gw, iface, metr) {
    msk = msk >>> 0;
    if (!Ip.mskValida(msk)) {
      throw new Error('netmask non contigua: ' + Ip.int2dotted(msk));
    }
    rete = rete >>> 0;

    // Chi scrive 192.168.1.77/24 intende 192.168.1.0/24. Mascherare in silenzio
    // funzionerebbe, ma nasconderebbe un errore di ragionamento: meglio dirlo.
    if (((rete & msk) >>> 0) !== rete) {
      throw new Error('la rete ' + Ip.int2dotted(rete) + ' ha bit accesi fuori dalla mask /' +
                      Ip.msk2pfx(msk) + ' — forse intendevi ' + Ip.int2dotted((rete & msk) >>> 0));
    }

    const m = Number(metr);
    if (!Number.isFinite(m) || m < 0) throw new Error('metrica non valida: ' + metr);

    this.rete  = rete;
    this.msk   = msk;
    this.gw    = gw >>> 0;
    this.iface = String(iface).trim();
    this.metr  = m;

    if (this.iface === '') throw new Error('interfaccia d\'uscita mancante');
  }
```

**Il principio che governa questo blocco: se un oggetto `Rotta` esiste, è valido.** Tutta la
validazione avviene qui, prima che l'oggetto sia utilizzabile. Nessun altro punto del
programma deve ricontrollare, e nessuno può creare una rotta incoerente senza passare da
qui — perché non esiste un altro modo di crearne una.

**La netmask prima di tutto.** `msk` viene validata per prima perché i controlli successivi
la usano: il messaggio d'errore sui bit fuori maschera chiama `Ip.msk2pfx(msk)`, che a sua
volta lancerebbe se la maschera non fosse contigua. Validare in quest'ordine garantisce che
quando si costruisce quel messaggio, `msk` è già sicuramente valida.

**Il controllo dei bit fuori maschera, in dettaglio.** `(rete & msk) >>> 0` è la rete
"pulita". Se differisce da `rete`, significa che `rete` ha bit accesi nella parte host.

```
rete = 192.168.1.77  =  11000000 10101000 00000001 01001101
msk  = /24           =  11111111 11111111 11111111 00000000
AND                  =  11000000 10101000 00000001 00000000  = 192.168.1.0
                                                      ↑
                                     ≠ rete: i bit 01001101 (=77) sono di troppo
```

**Perché non mascherare in silenzio.** Sono state considerate tre opzioni (§ 2.9). Correggere
in silenzio produrrebbe un programma che funziona ma che nasconde un errore di ragionamento
dell'utente. Accettare produrrebbe una regola morta: `(ip & msk)` ha sempre gli ultimi 8 bit
a zero, mentre `rete` li ha a 77, quindi il confronto sarebbe **sempre falso** e la riga non
verrebbe mai usata — senza che nulla lo segnali. Rifiutare con un suggerimento
(`forse intendevi 192.168.1.0`) insegna qualcosa e costa una riga.

**La metrica.** `Number(metr)` converte, perché il valore arriva da un campo di testo HTML ed
è quindi una stringa. `Number.isFinite` esclude `NaN` (conversione fallita), `Infinity` e
`-Infinity`. Il controllo `< 0` esclude i costi negativi, che nel modello non hanno senso.
Il messaggio riporta `metr`, cioè il valore **originale** prima della conversione: se
l'utente ha scritto `"abc"`, il messaggio dice `abc` e non `NaN`.

**L'interfaccia.** `String(iface).trim()` normalizza, e il controllo di stringa vuota viene
**dopo** l'assegnamento perché opera sul valore già ripulito: `"   "` diventa `""` e viene
rifiutato. È l'unico controllo posto dopo gli assegnamenti, e lo è per questa ragione
specifica.

**Perché tanti `>>> 0` in ingresso.** `msk`, `rete` e `gw` vengono normalizzati appena
arrivano. Il costruttore accetta interi da chiamanti diversi (`daDotted`, i test, il
controller) e non può assumere che siano già normalizzati. Normalizzare al confine
garantisce che da lì in poi, **dentro l'oggetto**, i valori siano sempre unsigned.

### 4.2.2 I due getter

```js
  get pfx() { return Ip.msk2pfx(this.msk); }

  // Gateway 0.0.0.0 vuol dire "la rete è attaccata qui": nessun next hop.
  get connessa() { return this.gw === 0; }
```

**`pfx`** è un valore **derivato**: non viene memorizzato, viene ricalcolato a ogni lettura da
`msk`. Vantaggio: non può mai andare fuori sincrono con la maschera. Svantaggio: dentro
`sort` viene ricalcolato più volte per ogni confronto, e ogni calcolo è un ciclo di 32
iterazioni. Su una tabella di dieci righe si parla di qualche migliaio di operazioni
elementari, cioè nulla. Su una tabella enorme si memorizzerebbe il valore nel costruttore,
accettando il rischio di doverlo aggiornare se `msk` cambiasse — ma `msk` non cambia mai,
perché una `Rotta` è trattata come immutabile dopo la costruzione.

**`connessa`** codifica una convenzione del dominio: gateway `0.0.0.0` significa che la rete
di destinazione è **direttamente raggiungibile** dall'interfaccia, senza passare per un altro
router. Il getter dà un nome a quella convenzione, così il resto del codice scrive
`rt.connessa` invece di `rt.gw === 0`, che richiederebbe di ricordarsi cosa significa lo
zero. Viene usato in tre punti: nella spiegazione testuale, nel rendering della colonna
Gateway, e nel verdetto della simulazione.

### 4.2.3 `copre` e `calcolo` — lo stesso test, due usi

```js
  copre(ip) { return (((ip >>> 0) & this.msk) >>> 0) === this.rete; }

  // Come copre(), ma restituisce anche i passaggi intermedi: è ciò che la GUI
  // mostra per spiegare il match, l'equivalente del printf del programma in C.
  calcolo(ip) {
    const and = (((ip >>> 0) & this.msk) >>> 0);
    return { and: and, rete: this.rete, esito: and === this.rete };
  }
```

**`copre`** è la regola di instradamento ridotta all'osso, la traduzione diretta di ciò che
nel programma in C occupava sei righe e tre chiamate di funzione.

Le parentesi, dall'interno verso l'esterno: `ip >>> 0` normalizza l'ingresso; `& this.msk`
applica la maschera; `>>> 0` normalizza il risultato dell'AND; `===` confronta.

**`calcolo`** fa lo stesso lavoro ma restituisce anche il valore intermedio. Esiste perché
l'interfaccia deve **mostrare il conto**, non solo l'esito: nella riga di dettaglio sotto ogni
regola si legge `196.13.2.5 & 255.255.255.0 = 196.13.2.0 = 196.13.2.0 ✓`, e quel
`196.13.2.0` centrale è il campo `and`.

**Perché due metodi e non uno.** Si potrebbe tenere solo `calcolo` e scrivere
`rt.calcolo(ip).esito` ovunque. Sarebbe più corto ma meno espressivo: `copre` dichiara
un'intenzione (*«questa rotta copre questo indirizzo?»*), `calcolo` un'altra (*«mostrami il
conto»*). Il costo della duplicazione è una riga, e la riga duplicata è talmente breve che il
rischio di divergenza è nullo. `Tdi.cerca` usa `calcolo`, perché ha bisogno del valore
intermedio; `copre` è la porta d'ingresso semplice, usata dai test e disponibile per chi
scriverà `Rete.invia`.

### 4.2.4 `stessaDest` e `identicaA` — la distinzione che rende viva la metrica

```js
  // Stessa destinazione ma gateway diverso è legittimo: è la rotta di riserva.
  stessaDest(a) { return this.rete === a.rete && this.msk === a.msk; }

  // Stessa destinazione E stesso gateway invece è solo la stessa istruzione
  // scritta due volte.
  identicaA(a) { return this.stessaDest(a) && this.gw === a.gw; }
```

Questa coppia è il risultato della correzione documentata in § 2.8.

**`stessaDest`** riconosce due rotte che puntano alla stessa destinazione. **Non** è un
criterio di rifiuto: è la configurazione principale/riserva, il fallback che la traccia
chiede.

**`identicaA`** aggiunge il gateway. Due rotte con stessa destinazione **e** stesso gateway
sono la stessa istruzione ripetuta: la seconda non aggiunge informazione, e viene rifiutata
da `Tdi.agg`.

**Nota su cosa non entra nel confronto.** Né `iface` né `metr` fanno parte di `identicaA`.
Due rotte identiche in rete, maschera e gateway ma con metriche diverse restano rifiutate,
ed è corretto: se il next hop è lo stesso, il pacchetto seguirà comunque la stessa strada, e
avere due costi diversi per la stessa strada è una contraddizione, non un'alternativa. Il
messaggio d'errore lo spiega esplicitamente: *«Per una rotta di riserva serve un gateway
diverso»*.

### 4.2.5 Serializzazione: `toJSON`, `daJSON`, `daDotted`

```js
  toJSON() {
    return {
      rete:  Ip.int2dotted(this.rete),
      msk:   Ip.int2dotted(this.msk),
      gw:    Ip.int2dotted(this.gw),
      iface: this.iface,
      metr:  this.metr
    };
  }

  static daJSON(o) {
    if (!o || typeof o !== 'object') throw new Error('rotta non valida nel file');
    return Rotta.daDotted(o.rete, o.msk, o.gw, o.iface, o.metr);
  }

  static daDotted(rete, msk, gw, iface, metr) {
    return new Rotta(Ip.dotted2int(rete), Ip.parseMsk(msk), Ip.dotted2int(gw), iface, metr);
  }
```

**`toJSON` ha un nome speciale.** `JSON.stringify` cerca automaticamente un metodo chiamato
esattamente `toJSON` sugli oggetti che incontra, e se lo trova serializza il suo valore di
ritorno invece dell'oggetto. Questo significa che `JSON.stringify(unaRotta)` produce già la
forma giusta, senza che il chiamante debba saperlo. È una convenzione del linguaggio
sfruttata deliberatamente.

**Gli indirizzi vengono riconvertiti in puntato** (§ 2.7): il file deve restare leggibile.

**`daJSON` è il percorso inverso, con controllo.** Il controllo `!o || typeof o !== 'object'`
serve perché il dato viene da un file che potrebbe contenere qualsiasi cosa. `typeof null` in
JavaScript restituisce `'object'` — una nota stranezza storica del linguaggio — quindi il
`!o` iniziale è necessario per escludere `null`, che altrimenti passerebbe il secondo
controllo.

**`daJSON` delega a `daDotted`, che delega al costruttore.** La catena è deliberata: tutta la
validazione resta in un unico posto. Un file JSON che contenga `"999.1.1.1"` fallisce dentro
`Ip.dotted2int`, con lo stesso messaggio che riceverebbe l'utente digitandolo nel form. Non
esistono due percorsi di validazione da tenere allineati. C'è un test dedicato a questo:
`lancia('tabella corrotta nel file', ...)`.

**`daDotted` è una factory di comodità.** È il costruttore per chi ha in mano delle stringhe,
cioè il form, i test e la tabella d'esempio. Senza di essa ogni chiamante dovrebbe scrivere
`new Rotta(Ip.dotted2int('...'), Ip.parseMsk('...'), Ip.dotted2int('...'), ...)`, che è
rumoroso e ripetuto. È statica perché quando viene chiamata l'oggetto non esiste ancora
(§ 3.4).

## 4.3 `js/tdi.js` — la tabella e l'algoritmo

Il file centrale del progetto.

### 4.3.1 Intestazione e struttura

```js
// La Tabella di Instradamento: un array di Rotta, più l'algoritmo che sceglie.
//
// Array e scansione lineare, non un trie. Un router vero usa un Patricia trie
// perché ha centinaia di migliaia di rotte; qui ne ha dieci, e soprattutto la
// scansione completa È la visualizzazione. Un trie salta le regole non
// compatibili, che è esattamente l'informazione che questa GUI deve mostrare.
class Tdi {

  constructor() { this.rotte = []; }
```

Il commento risponde in anticipo alla domanda che un lettore competente porrebbe subito
(§ 2.4). Il costruttore non prende argomenti: una tabella nasce vuota e si riempie con
`agg`. Ricostruirla da un file è compito della factory statica `daJSON`.

### 4.3.2 `agg` — inserimento con controllo di ridondanza

```js
  agg(r) {
    if (this.rotte.some(x => x.identicaA(r))) {
      throw new Error('rotta già presente: ' + Ip.int2dotted(r.rete) + '/' + r.pfx +
                      ' via ' + Ip.int2dotted(r.gw) +
                      '. Per una rotta di riserva serve un gateway diverso.');
    }
    this.rotte.push(r);
  }
```

`some` restituisce `true` al primo elemento che soddisfa la condizione e si ferma lì
(§ 3.6). Il criterio è `identicaA`, non `stessaDest`: la ragione è tutta in § 2.8.

**Il messaggio d'errore fa due cose.** Dice cosa è successo *e* come ottenere ciò che
probabilmente si voleva. Un messaggio che dicesse solo «rotta già presente» lascerebbe
l'utente convinto che le rotte di riserva non siano supportate.

**Il metodo riceve una `Rotta` già costruita**, non i suoi campi. Conseguenza: quando `agg`
viene invocata, la rotta è già stata validata dal costruttore. `Tdi` non deve sapere nulla di
netmask contigue o di ottetti fuori range: si occupa solo di ciò che riguarda la
**collezione**, cioè la ridondanza. Ogni classe convalida ciò che le compete.

### 4.3.3 `rimuovi`, `svuota`, `elenco`, `vuota`

```js
  rimuovi(i) {
    if (!Number.isInteger(i) || i < 0 || i >= this.rotte.length) {
      throw new Error('indice fuori dalla tabella: ' + i);
    }
    this.rotte.splice(i, 1);
  }

  svuota() { this.rotte = []; }

  elenco() { return this.rotte.slice(); }

  get vuota() { return this.rotte.length === 0; }
```

**`rimuovi` valida l'indice.** Senza il controllo, `splice(99, 1)` su un array di 5 elementi
non farebbe nulla e non segnalerebbe nulla: un click su un bottone rimasto appeso a una riga
non più esistente sembrerebbe funzionare senza effetto. Meglio un errore esplicito.
`Number.isInteger` esclude anche indici frazionari o valori non numerici.

**`elenco` restituisce una copia difensiva.** `slice()` senza argomenti copia l'array. Questo
significa che chi riceve l'elenco può ordinarlo, filtrarlo o modificarlo senza toccare la
tabella vera:

```js
const copia = tdi.elenco();
copia.push('spazzatura');      // la Tdi non ne risente
```

Il costo è la creazione di un array di riferimenti a ogni chiamata, che su dieci elementi è
irrilevante. Il beneficio è che l'incapsulamento è reale e non solo dichiarato: `this.rotte`
non esce mai dalla classe. C'è un test apposta.

**Attenzione alla sfumatura.** `slice()` è una copia **superficiale**: l'array è nuovo, ma gli
oggetti `Rotta` dentro sono gli stessi. Modificare `copia[0].metr` modificherebbe la rotta
vera. Nel programma non succede perché le `Rotta` sono trattate come immutabili dopo la
costruzione, ma è la stessa fragilità già notata a proposito dell'`Esito` (§ 2.5).

**`vuota` è un getter** perché è una domanda sullo stato, non un'azione: `tdi.vuota` si legge
meglio di `tdi.vuota()`. Serve alla vista per decidere se mostrare il messaggio «la tabella
è vuota».

### 4.3.4 `cerca` — il Longest Prefix Match

Il metodo più importante del programma.

```js
  // Longest Prefix Match, in una passata sola. Nessuna regola viene saltata:
  // l'esito di ogni confronto finisce in righe[], che è quello che la vista
  // colora.
  cerca(ip) {
    ip = ip >>> 0;

    const righe = this.rotte.map((rt, idx) => {
      const c = rt.calcolo(ip);
      return { rotta: rt, idx: idx, and: c.and, esito: c.esito };
    });

    const match = righe.filter(r => r.esito).map(r => r.rotta);

    // Prefisso più lungo, poi metrica più bassa. A parità di entrambi decide
    // l'ordine in tabella: sort è stabile da ES2019, quindi non serve altro.
    match.sort((a, b) => b.pfx - a.pfx || a.metr - b.metr);

    const scelta = match.length ? match[0] : null;

    return {
      ip: ip,
      righe: righe,
      scelta: scelta,
      alternative: match.slice(1),
      motivo: this._motivo(ip, scelta, match)
    };
  }
```

**Passo 0 — normalizzazione.** `ip >>> 0` all'ingresso. Da qui in poi l'indirizzo è unsigned
e resta tale anche nell'oggetto restituito, dove la vista lo rileggerà per stamparlo.

**Passo 1 — la scansione completa.**

```js
const righe = this.rotte.map((rt, idx) => {
  const c = rt.calcolo(ip);
  return { rotta: rt, idx: idx, and: c.and, esito: c.esito };
});
```

`map` produce un array della **stessa lunghezza** dell'originale: una voce per ogni rotta, in
ordine di tabella, indipendentemente dall'esito. Questa è la decisione centrale: **nessuna
regola viene saltata**. È ciò che permette alla vista di colorare ogni riga e di mostrare
ogni calcolo, cioè il requisito *«individuare tutte le route compatibili, magari
evidenziandole sulla TDI»*.

Ogni voce contiene:

| Campo | Cosa contiene | A cosa serve |
|---|---|---|
| `rotta` | riferimento all'oggetto `Rotta` | permette il confronto per identità nella vista |
| `idx` | posizione in tabella | numerazione stabile e riferimento incrociato |
| `and` | il risultato di `ip & msk` | è il numero mostrato nella riga di dettaglio |
| `esito` | `true`/`false` | decide il colore della riga |

**Il parametro `idx` di `map`.** `map` passa alla funzione l'elemento **e** il suo indice
(§ 3.6). Conservarlo rende `righe[i]` autodescrittivo: chi lo legge non deve dedurre la
posizione dalla propria variabile di ciclo.

**Passo 2 — il filtro.**

```js
const match = righe.filter(r => r.esito).map(r => r.rotta);
```

Due operazioni concatenate: `filter` tiene solo le voci compatibili, `map` estrae da ciascuna
l'oggetto `Rotta`. Il risultato è un array di sole rotte compatibili.

**Perché due passaggi e non uno.** Si potrebbe fare tutto in un `reduce`, ma sarebbe meno
leggibile. Il costo è un array intermedio su dieci elementi: irrilevante. La leggibilità di
`filter().map()` — «tieni quelle vere, poi prendine la rotta» — vale molto di più.

**Passo 3 — l'ordinamento, il cuore dell'algoritmo.**

```js
match.sort((a, b) => b.pfx - a.pfx || a.metr - b.metr);
```

Tre criteri in un'espressione (§ 3.6):

1. **`b.pfx - a.pfx`** — ordine invertito, quindi **prefisso decrescente**. Il più specifico
   per primo. Questo *è* il Longest Prefix Match.
2. **`|| a.metr - b.metr`** — se i prefissi pareggiano, la sottrazione dà `0`, che è falsy, e
   `||` valuta il secondo termine: ordine **crescente** di metrica, costo minore per primo.
3. **La stabilità di `sort`** — se anche le metriche pareggiano il confronto restituisce `0`
   e `sort` mantiene l'ordine originale, che è quello di inserimento in tabella. Lo standard
   ECMAScript **impone** la stabilità dal 2019, quindi non è un dettaglio implementativo su
   cui si sta scommettendo: è garantito.

**Perché il prefisso viene prima della metrica.** Non è arbitrario. La lunghezza del prefisso
è un'informazione **topologica**: dice quanto quella regola sa della destinazione. La metrica
è una preferenza **amministrativa**: dice quanto quella strada costa. Una preferenza di costo
non deve poter scavalcare un'informazione migliore su dove si trova la destinazione — se una
regola sa che il pacchetto va in una sottorete precisa, quella conoscenza vale più di uno
sconto sul costo. È anche il comportamento dei router reali.

**Nota.** `sort` ordina **sul posto** e restituisce l'array stesso. Qui il valore di ritorno è
ignorato perché `match` è già la variabile giusta. `match` è un array creato da `filter`, non
la tabella: ordinarlo **non** riordina `this.rotte`, che conserva l'ordine di inserimento.
Questo è essenziale, perché la vista disegna le righe nell'ordine della tabella e le allinea
con `righe[i]`.

**Passo 4 — la selezione.**

```js
const scelta = match.length ? match[0] : null;
```

Dopo l'ordinamento il primo elemento è il vincitore. Se non ci sono match, `match.length` è
`0` (falsy) e `scelta` diventa `null`. `null` è deliberato: significa *«non c'è»* in modo
esplicito e distinguibile da `undefined`, che significherebbe *«non l'ho impostato»*.

**Passo 5 — la costruzione dell'esito.**

```js
return {
  ip: ip,
  righe: righe,
  scelta: scelta,
  alternative: match.slice(1),
  motivo: this._motivo(ip, scelta, match)
};
```

`match.slice(1)` copia da posizione 1 in poi: tutte le compatibili tranne la vincente, già
ordinate per preferenza. È l'elenco dei fallback.

**La default route non richiede nessun caso speciale.** Ha `pfx = 0`, il minimo possibile,
quindi l'ordinamento la mette sempre in fondo. Se ci sono regole più specifiche, finisce fra
le alternative; se è l'unica compatibile, vince. Entrambi i comportamenti sono corretti e
nessuno dei due è stato programmato esplicitamente: **emergono dall'ordinamento**. È il segno
che l'algoritmo è quello giusto.

### 4.3.5 `_motivo` — la spiegazione come dato

```js
  _motivo(ip, scelta, match) {
    const d = Ip.int2dotted(ip);

    if (!scelta) {
      return 'Destinazione ' + d + ' irraggiungibile: nessuna regola della tabella la copre, ' +
             'e non c\'è una default route a fare da rete di sicurezza. Il pacchetto viene scartato.';
    }
```

**Il caso senza match.** `!scelta` è vero quando `scelta` è `null`. Il messaggio dice tre
cose: che non c'è nessuna regola compatibile, **perché** (manca la default route, che è
sempre la causa), e cosa succede al pacchetto. Un router reale in questa situazione scarta il
pacchetto ed eventualmente emette un ICMP *network unreachable*.

```js
    const dest = Ip.int2dotted(scelta.rete) + '/' + scelta.pfx;
    let s = 'Per ' + d + ' vince ' + dest + '. ';

    s += scelta.pfx === 0
      ? 'È la default route: compatibile con qualunque indirizzo, ma con prefisso di lunghezza 0 ' +
        'resta sempre l\'ultima scelta possibile. Viene usata perché nessuna regola più specifica corrisponde. '
      : 'Fissa ' + scelta.pfx + ' bit di prefisso, più di ogni altra regola compatibile. ';
```

**`let s` e `+=`.** Qui la riassegnazione serve davvero: il testo si costruisce a pezzi, e
quali pezzi dipende dal caso. È l'unico `let` nello strato logico insieme ai due contatori di
`ip.js`.

**Il ramo sulla default route.** Quando `pfx` è 0, dire «fissa 0 bit di prefisso» sarebbe
tecnicamente corretto e didatticamente inutile. Il ramo dedicato spiega invece il concetto:
compatibile con tutto, ma sempre ultima. È esattamente la cosa che il programma in C non
riusciva a comunicare (§ 1.4, limite 9).

```js
    s += scelta.connessa
      ? 'La rete è direttamente connessa su ' + scelta.iface + ': nessun next hop. '
      : 'Next hop ' + Ip.int2dotted(scelta.gw) + ' su ' + scelta.iface + '. ';
```

Usa il getter `connessa` per distinguere i due casi. Per una rete direttamente connessa non
esiste un next hop e stampare `0.0.0.0` sarebbe fuorviante: si dice cosa significa.

```js
    const alt = match.slice(1);

    if (alt.length === 0) {
      return s + 'Nessuna alternativa: se questa via cade, il pacchetto non ha dove andare.';
    }

    if (alt[0].pfx === scelta.pfx) {
      s += 'Stesso prefisso anche via ' + Ip.int2dotted(alt[0].gw) +
           ', quindi ha deciso la metrica: ' + scelta.metr + ' contro ' + alt[0].metr + '. ';
    }
```

**Il controllo `alt[0].pfx === scelta.pfx`.** L'array è ordinato, quindi se esiste un
pareggio sul prefisso il pareggiante è necessariamente il **primo** delle alternative. Basta
controllare quello. Quando il pareggio c'è, il messaggio dice esplicitamente che a decidere è
stata la metrica e mostra i due valori a confronto: è il caso della floating static route
(§ 2.8), e senza questa frase l'utente vedrebbe due righe apparentemente identiche di cui una
vince, senza capire perché.

```js
    s += alt.length === 1 ? '1 alternativa disponibile come fallback: '
                          : alt.length + ' alternative disponibili come fallback, nell\'ordine: ';

    return s + alt.map(r =>
      Ip.int2dotted(r.rete) + '/' + r.pfx +
      (r.connessa ? ' connessa su ' + r.iface : ' via ' + Ip.int2dotted(r.gw)) +
      ' (metrica ' + r.metr + ')'
    ).join(', ') + '.';
  }
```

**Singolare e plurale.** Un dettaglio piccolo ma visibile: «1 alternativa disponibile» invece
di «1 alternative disponibili». Costa un ternario.

**`map(...).join(', ')`** è l'idioma per costruire un elenco leggibile: `map` trasforma ogni
rotta in una stringa, `join` le unisce con virgola e spazio. Il `+ '.'` finale chiude la
frase.

### 4.3.6 Serializzazione della tabella

```js
  toJSON() { return this.rotte.map(r => r.toJSON()); }

  static daJSON(arr) {
    if (!Array.isArray(arr)) throw new Error('la tabella nel file non è un elenco');
    const t = new Tdi();
    arr.forEach(o => t.agg(Rotta.daJSON(o)));
    return t;
  }
```

**`toJSON` delega.** Ogni `Rotta` sa serializzarsi; `Tdi` si limita a mappare. La
responsabilità resta dove sta il dato.

**`daJSON` ricostruisce passando da `agg`, non da `push`.** È una scelta precisa: significa
che un file contenente due rotte identiche viene **rifiutato al caricamento**, con lo stesso
controllo che si applica all'inserimento manuale. Se avesse usato `push` direttamente, un
file scritto a mano potrebbe introdurre nella tabella uno stato che l'interfaccia non
permette di creare. La regola: **ogni via d'ingresso dei dati passa per gli stessi
controlli**.

**`Array.isArray`** è il modo corretto di verificare che un valore sia un array: `typeof []`
restituisce `'object'`, quindi `typeof` non basta.

## 4.4 `js/iface.js` — l'interfaccia di rete

```js
// Interfaccia di rete. Nel simulatore mono-router fa poco: dà un tipo alla
// colonna "Use" della TDI, che nel programma in C era una stringa di ottetti
// senza comportamento.
//
// Esiste già adesso perché è l'aggancio del multi-hop: un Link collegherà due
// Iface, non due stringhe.
class Iface {

  constructor(nome, ip, msk, su) {
    this.nome = String(nome).trim();
    if (this.nome === '') throw new Error('interfaccia senza nome');
    this.ip  = ip >>> 0;
    this.msk = msk >>> 0;
    if (!Ip.mskValida(this.msk)) {
      throw new Error('netmask non contigua su ' + this.nome + ': ' + Ip.int2dotted(this.msk));
    }
    this.su = su !== false;
  }
```

**Perché questa classe esiste già ora, pur facendo quasi nulla.** È la risposta concreta al
vincolo della traccia: *«una corretta progettazione dovrebbe consentire, senza modifiche
sostanziali all'architettura, l'introduzione futura di entità quali Interface, Link,
Packet»*. Non basta dire che si potrebbe fare: bisogna che il posto dove agganciarle esista.
Nel programma in C la colonna «Use» era `Ua, Ub, Uc, Ud`, quattro numeri senza comportamento:
a un oggetto simile non si può collegare nulla. Un `Link` unisce due `Iface`; se `Iface` non
esistesse, il multi-hop richiederebbe di inventarla e di riscrivere ciò che la usa.

**`this.nome` viene assegnato prima di essere validato.** L'ordine è voluto: il messaggio
d'errore della netmask cita `this.nome`, quindi il nome deve già esserci. Il controllo di
stringa vuota sta subito dopo l'assegnamento, così opera sul valore già ripulito da `trim`.

**`this.su = su !== false`.** Un idioma per «vero salvo esplicita smentita». La tabella di
verità:

| `su` in ingresso | `su !== false` | Interpretazione |
|---|---|---|
| `true` | `true` | esplicitamente attiva |
| `false` | `false` | esplicitamente disattiva |
| `undefined` (parametro omesso) | `true` | predefinito: attiva |
| `null` | `true` | dato assente nel file: attiva |

**Perché non `su || true`.** Non funzionerebbe: `false || true` dà `true`, quindi sarebbe
impossibile creare un'interfaccia disattiva. **Perché non un parametro predefinito
`su = true`.** Coprirebbe `undefined` ma non `null`, e `JSON.parse` di un campo mancante può
produrre `undefined` mentre un campo scritto `null` produce `null`. Il confronto esplicito
con `false` copre entrambi i casi.

**A cosa servirà `su`.** Oggi a nulla: il campo è memorizzato e salvato ma non ha effetto.
Nel multi-router sarà il modo di simulare un guasto — si abbassa un'interfaccia, le rotte che
la usano diventano inutilizzabili, e il traffico passa alle alternative. È il motivo per cui
la metrica e le rotte di riserva esistono già (§ 2.8): quando arriverà la simulazione dei
guasti, tutto il necessario sarà già al suo posto.

```js
  get pfx() { return Ip.msk2pfx(this.msk); }

  // Vero se l'indirizzo appartiene alla rete di questa interfaccia.
  locale(ip) { return (((ip >>> 0) & this.msk) >>> 0) === ((this.ip & this.msk) >>> 0); }
```

**`locale` risponde a «questo indirizzo è sulla mia stessa rete?»**. Il meccanismo è lo
stesso di `Rotta.copre`, ma con una differenza importante: qui il termine di confronto non è
memorizzato, va **calcolato**. `Rotta` ha già il campo `rete` pulito (il costruttore lo
esige); `Iface` invece ha l'indirizzo **dell'interfaccia stessa**, per esempio
`196.13.1.1/24`, che non è un indirizzo di rete. Va mascherato:

```
this.ip  = 196.13.1.1    →  11000100 00001101 00000001 00000001
this.msk = /24           →  11111111 11111111 11111111 00000000
AND                      →  11000100 00001101 00000001 00000000  = 196.13.1.0  ← la rete
```

Da cui il doppio AND nella riga: uno sull'argomento, uno sull'indirizzo dell'interfaccia.

**A cosa servirà.** Nel forwarding multi-hop, per decidere se il pacchetto è **arrivato**:
se la destinazione è locale a una delle interfacce del router corrente, il viaggio è finito.
Oggi non è chiamato dal programma, solo dai test.

```js
  toJSON() {
    return {
      nome: this.nome,
      ip:   Ip.int2dotted(this.ip),
      msk:  Ip.int2dotted(this.msk),
      su:   this.su
    };
  }

  static daJSON(o) {
    if (!o || typeof o !== 'object') throw new Error('interfaccia non valida nel file');
    return new Iface(o.nome, Ip.dotted2int(o.ip), Ip.parseMsk(o.msk), o.su);
  }
```

Stesso schema di `Rotta`: puntato nel file, controllo sul tipo, delega al costruttore per la
validazione.

## 4.5 `js/pacchetto.js` — il pacchetto IP

```js
// Al momento di questo pacchetto interessa solo dst. src e ttl ci sono perché
// quando arriverà l'inoltro multi-hop non si dovrà cambiare la firma di
// Router.inoltra(): il ttl serve lì, a non far girare i pacchetti in tondo per
// sempre quando due router si rimbalzano la stessa destinazione.
class Pacchetto {

  constructor(src, dst, ttl) {
    this.src = src >>> 0;
    this.dst = dst >>> 0;
    this.ttl = ttl === undefined ? 64 : ttl;
  }

  static daDotted(src, dst, ttl) {
    return new Pacchetto(Ip.dotted2int(src), Ip.dotted2int(dst), ttl);
  }
}
```

La classe più piccola del progetto, e forse la più interessante da giustificare.

**Perché esiste, visto che serve solo `dst`.** Si potrebbe scrivere `router.inoltra(ip)` e
risparmiare un file. Ma quando arriverà il multi-hop servirà anche il TTL, e cambiare la
firma di `inoltra` significherebbe toccare ogni chiamante. Introdurre `Pacchetto` ora costa
quindici righe e congela una firma che non dovrà più cambiare: `inoltra(pkt)` funziona sia
oggi che domani. È il principio applicato anche a `Iface` — creare adesso i punti di
aggancio, così l'evoluzione è **aggiunta** e non riscrittura.

**Cos'è il TTL.** *Time To Live*: un contatore nell'intestazione di ogni pacchetto IP. Ogni
router che lo inoltra lo decrementa di uno; quando arriva a zero il pacchetto viene scartato.
Serve contro i **loop di instradamento**: se per un errore di configurazione due router si
rimbalzano lo stesso pacchetto, senza TTL girerebbe per sempre saturando il collegamento.
Con il TTL muore dopo un numero limitato di salti. Il valore predefinito 64 è quello usato da
Linux.

**`ttl === undefined ? 64 : ttl`.** Confronto esplicito con `undefined` invece di `ttl || 64`:
con `||`, passare `ttl = 0` — che significa «pacchetto già scaduto», un valore legittimo in
un test — verrebbe silenziosamente sostituito con 64, perché `0` è falsy.

**Nessuna validazione qui.** `src` e `dst` sono normalizzati ma non controllati, perché un
pacchetto può in linea di principio contenere qualunque valore a 32 bit: non c'è un concetto
di «indirizzo di destinazione non valido» analogo a quello di netmask non contigua. La
validazione dell'input avviene prima, in `Ip.dotted2int`, quando l'utente digita.

## 4.6 `js/router.js` — il nodo

```js
// Il router: un nome, una TDI, un po' di interfacce.
class Router {

  constructor(nome) {
    this.nome   = String(nome || 'R1').trim();
    this.tdi    = new Tdi();
    this.ifaces = [];
  }
```

**`String(nome || 'R1')`.** Se `nome` è `undefined`, `null` o stringa vuota — tutti falsy —
si usa `'R1'`. Utile perché `Router.daJSON` passa `o.nome`, che potrebbe mancare in un file
scritto a mano.

**Composizione, non aggregazione.** Il router **crea** la propria `Tdi` nel costruttore: non
la riceve da fuori. È una relazione di composizione — la tabella non esiste
indipendentemente dal router che la possiede, e muore con lui. Nel diagramma UML è il rombo
pieno.

```js
  aggIface(i) {
    if (this.iface(i.nome)) throw new Error('interfaccia già presente: ' + i.nome);
    this.ifaces.push(i);
  }

  rimuoviIface(nome) {
    const k = this.ifaces.findIndex(x => x.nome === nome);
    if (k < 0) throw new Error('interfaccia inesistente: ' + nome);
    this.ifaces.splice(k, 1);
  }
```

**`aggIface` riusa `iface()` come test di esistenza.** `iface()` restituisce l'oggetto o
`null`; `null` è falsy, quindi l'`if` funziona senza confronti espliciti. Il nome è la chiave
univoca: due interfacce chiamate `eth0` sullo stesso router non hanno senso, perché le rotte
le citano per nome e non si potrebbe distinguerle.

**`findIndex` invece di `find`** in `rimuoviIface`, perché `splice` ha bisogno della
posizione, non dell'oggetto. Il controllo `k < 0` intercetta il caso «non trovato».

```js
  // La TDI cita l'interfaccia d'uscita per nome, come fa un router vero. È qui
  // che il nome torna a essere un oggetto. Quando arriverà Rete, questo è il
  // punto in cui si aggancerà il Link — e Rotta non dovrà cambiare di una virgola.
  iface(nome) {
    return this.ifaces.find(x => x.nome === nome) || null;
  }
```

**Il metodo architetturalmente più significativo del file.** `Rotta.iface` è una **stringa**,
non un riferimento a un oggetto `Iface`. È una scelta deliberata, con tre conseguenze
positive:

1. **`Rotta` resta serializzabile senza dipendenze.** `toJSON` scrive `"eth0"` e basta. Con
   un riferimento a oggetto bisognerebbe gestire l'identità: come si salva un puntatore in un
   file JSON? Con un identificatore, cioè... di nuovo una stringa.
2. **`Rotta` resta indipendente da `Router`.** Una rotta si può costruire e testare senza che
   esista un router. Tutti i test su `Rotta` e su `Tdi` ne approfittano.
3. **È ciò che fa un router reale.** Su un router Cisco si scrive
   `ip route 10.0.0.0 255.0.0.0 GigabitEthernet0/1`: un **nome**. La risoluzione nome →
   interfaccia avviene al momento dell'inoltro.

**Perché questo rende vera l'affermazione sul multi-router.** Quando arriverà `Rete`, sarà
`Rete.invia()` a chiedere `router.iface(esito.scelta.iface)` per trovare l'oggetto, e da lì
il `Link` collegato. **Nessuna classe esistente cambia**: `Rotta` continua a contenere una
stringa, `Tdi` continua a non sapere cosa sia un'interfaccia, e il metodo di risoluzione è
già scritto. Se invece `Rotta.iface` fosse un riferimento, oggi bisognerebbe già gestire cosa
succede quando si elimina un'interfaccia citata da una rotta.

```js
  // Sottile di proposito: qui, un giorno, Rete.invia() chiamerà in ciclo.
  inoltra(pkt) { return this.tdi.cerca(pkt.dst); }
```

Una riga: estrae la destinazione dal pacchetto e la passa alla tabella. Sembra superfluo, ma
è il **punto di estensione**. Nel multi-hop diventerà il corpo del ciclo di `Rete.invia`, e
potrà arricchirsi (controllo del TTL, verifica che l'interfaccia d'uscita sia attiva) senza
che i chiamanti cambino. Un metodo sottile oggi è un punto di aggancio domani.

```js
  toJSON() {
    return {
      nome:   this.nome,
      ifaces: this.ifaces.map(i => i.toJSON()),
      tdi:    this.tdi.toJSON()
    };
  }

  static daJSON(o) {
    if (!o || typeof o !== 'object') throw new Error('il file non contiene un router');
    const r = new Router(o.nome);
    (o.ifaces || []).forEach(x => r.aggIface(Iface.daJSON(x)));
    r.tdi = Tdi.daJSON(o.tdi || []);
    return r;
  }
```

**`(o.ifaces || [])`** protegge dal campo mancante: se `o.ifaces` è `undefined`, si itera su
un array vuoto invece di sollevare `Cannot read property 'forEach' of undefined`. Stessa cosa
per `o.tdi || []`. Un file di configurazione minimale — solo `{"nome": "R1"}` — viene
accettato e produce un router vuoto, che è ragionevole.

**`r.tdi = Tdi.daJSON(...)` sostituisce la tabella creata dal costruttore.** L'alternativa
sarebbe iterare le rotte chiamando `r.tdi.agg()` una a una; sostituire l'oggetto intero è più
diretto e riusa la factory già scritta.

**L'ordine delle due righe conta.** Le interfacce vengono caricate prima delle rotte. Oggi
non è indispensabile, perché `Tdi.daJSON` non verifica che le interfacce citate esistano. Ma
se un giorno si volesse aggiungere quel controllo — ragionevole — l'ordine giusto è già
questo, e non bisognerà accorgersene a posteriori.

## 4.7 `js/persistenza.js` — salvare e caricare

```js
const Persistenza = {

  VERSIONE: 1,

  serializza(router) {
    return { versione: Persistenza.VERSIONE, router: router.toJSON() };
  },

  deserializza(o) {
    if (!o || typeof o !== 'object') throw new Error('il file non contiene un oggetto JSON');
    if (o.versione !== Persistenza.VERSIONE) {
      throw new Error('versione del file non supportata: ' + o.versione +
                      ' (questa applicazione legge la ' + Persistenza.VERSIONE + ')');
    }
    if (!o.router) throw new Error('il file non contiene un router');
    return Router.daJSON(o.router);
  },
```

**La divisione in due coppie di metodi è la chiave del file.**

| Coppia | Cosa fa | Testabile? |
|---|---|---|
| `serializza` / `deserializza` | Oggetti ↔ struttura JSON. **Logica pura.** | Sì, completamente |
| `esporta` / `importa` | Struttura JSON ↔ file su disco. **Solo plumbing del browser.** | No: richiedono un utente che clicchi |

Separarle significa che **tutta la logica** di persistenza è coperta dai test, e ciò che resta
non testato è codice che non contiene decisioni. È il motivo per cui i test di
`test-persistenza.js` verificano il round-trip completo senza toccare un file.

**`VERSIONE` come costante nominata** invece del letterale `1` sparso: c'è un solo posto da
cambiare, e il messaggio d'errore la cita automaticamente.

**I tre controlli di `deserializza`, in ordine.** Prima che sia un oggetto (con il `!o` che
esclude `null`, vedi § 4.2.5), poi la versione, poi la presenza del router. L'ordine va dal
più generale al più specifico: non ha senso controllare la versione di qualcosa che non è un
oggetto.

**Il messaggio sulla versione dice entrambi i numeri**: quella trovata e quella attesa. Chi
lo legge capisce subito se ha un file troppo vecchio o troppo nuovo.

```js
  esporta(router, nomeFile) {
    const testo = JSON.stringify(Persistenza.serializza(router), null, 2);
    const url = URL.createObjectURL(new Blob([testo], { type: 'application/json' }));
    const a = document.createElement('a');
    a.href = url;
    a.download = nomeFile || 'config.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  },
```

Sette righe che meritano una spiegazione ciascuna, perché sono l'unico modo che una pagina
web ha di produrre un file.

**Riga 1 — `JSON.stringify(oggetto, null, 2)`.** Il secondo parametro è il *replacer*, una
funzione per filtrare i campi: non serve, quindi `null`. Il terzo è l'indentazione: `2`
produce JSON formattato su più righe con due spazi di rientro invece di una riga unica.
Costa qualche byte e rende il file **leggibile e modificabile a mano**, che è il requisito di
§ 2.7.

**Riga 2 — `Blob` e `createObjectURL`.** Un `Blob` (*Binary Large OBject*) è un oggetto che
rappresenta dati grezzi in memoria; il costruttore riceve un array di pezzi e un tipo MIME.
`URL.createObjectURL` registra quel blob nel browser e restituisce un indirizzo temporaneo
della forma `blob:http://.../a1b2c3...`, valido solo dentro questa pagina e per la sua durata.
È il trucco: si crea qualcosa che *sembra* un file remoto ma vive in memoria.

**Righe 3-5 — l'ancora.** Si crea un `<a>` con quell'indirizzo e l'attributo `download`, che
dice al browser «non aprire questa risorsa, scaricala», e ne fornisce il nome predefinito.

**Riga 6 — `document.body.appendChild(a)`.** L'ancora deve essere **nel documento** perché il
click programmatico funzioni: alcuni browser ignorano il click su elementi staccati dal DOM.

**Riga 7 — `a.click()`.** Simula il click. Da qui in poi è il browser a gestire il download,
con le sue impostazioni e la sua cartella predefinita.

**Righe 8-9 — la pulizia.** `removeChild` toglie l'ancora, che ha esaurito il suo scopo:
lasciarla accumulerebbe un elemento invisibile a ogni salvataggio. `revokeObjectURL` libera
la memoria occupata dal blob — senza, il browser terrebbe in vita i dati fino alla chiusura
della pagina. Su un file da qualche kilobyte non si nota, ma è la cosa corretta da fare e
costa una riga.

**Nota architetturale.** Questo metodo tocca il DOM, e la regola dello strato logico lo
vieta. Ma `persistenza.js` **non è nello strato logico**: è lo strato di persistenza (§ 2.6),
il cui compito è proprio mediare fra il dominio e il mondo esterno. La regola rispettata è
un'altra: non conosce la vista, non sa che esistono `VistaTdi` o `App`.

```js
  importa(file) {
    return new Promise((risolvi, rifiuta) => {
      const fr = new FileReader();
      fr.onerror = () => rifiuta(new Error('impossibile leggere il file'));
      fr.onload = () => {
        try {
          risolvi(Persistenza.deserializza(JSON.parse(fr.result)));
        } catch (e) {
          rifiuta(new Error('file non valido: ' + e.message));
        }
      };
      fr.readAsText(file);
    });
  }
};
```

**`FileReader` è asincrono.** Leggere un file dal disco richiede tempo, e JavaScript nel
browser ha un solo thread: bloccarlo congelerebbe la pagina. `readAsText` avvia la lettura e
ritorna subito; quando i dati sono pronti il browser chiama `onload`.

**L'avvolgimento in una Promise** (§ 3.13) trasforma questa API a eventi in una a valore, così
il chiamante può scrivere `.then().catch()` invece di gestire due callback separate.

**Il `try`/`catch` dentro `onload` è la parte critica.** Vale la pena insistere: un'eccezione
lanciata dentro un gestore di evento **non** viene catturata da nessun `try` esterno, perché
il gestore viene eseguito in un altro giro del ciclo degli eventi, quando lo stack della
chiamata originale non esiste più. Senza questo `try`/`catch`, un file JSON malformato
produrrebbe un errore rosso in console e la Promise resterebbe **sospesa per sempre**: né
`then` né `catch` verrebbero mai chiamati, il messaggio d'errore non comparirebbe, e
l'utente resterebbe a fissare un'interfaccia che non reagisce.

**Due sorgenti d'errore, una gestione.** `JSON.parse` fallisce sul testo malformato,
`deserializza` fallisce sulla struttura sbagliata. Entrambe finiscono nello stesso `catch`,
che aggiunge un prefisso e rilancia. Il messaggio finale che l'utente vede è per esempio:

```
Caricamento fallito: file non valido: Expected property name or '}' in JSON at position 2
 — la tabella attuale resta com'era.
```

Tre livelli di contesto — il controller, la persistenza, il parser — concatenati in una frase
sola.

## 4.8 `js/vista-tdi.js` — disegnare la tabella

### 4.8.1 Costruttore e delega degli eventi

```js
class VistaTdi {

  constructor(tabella, elVuota) {
    this.tab    = tabella;
    this.tbody  = tabella.querySelector('tbody');
    this.elVuota = elVuota;
    this.cbElimina = null;

    // Delega: i bottoni nascono e muoiono a ogni ridisegno, l'ascoltatore no.
    this.tbody.addEventListener('click', ev => {
      const b = ev.target.closest('button[data-i]');
      if (b && this.cbElimina) this.cbElimina(Number(b.dataset.i));
    });
  }

  onElimina(cb) { this.cbElimina = cb; }
```

**Il costruttore riceve gli elementi, non li cerca.** `new VistaTdi(document.getElementById(...))`
invece di `document.getElementById` dentro la classe. È **iniezione delle dipendenze**: la
vista non è legata a identificatori specifici dell'HTML, quindi si potrebbero avere due
tabelle nella stessa pagina — cosa che servirà con più router. Chi decide quali elementi sono
è `App`, che è il posto giusto per quella decisione.

**La delega degli eventi** (§ 3.14) è qui una necessità, non un'ottimizzazione. `disegna`
svuota il `<tbody>` e ricrea tutte le righe: ogni bottone «elimina» viene distrutto e
ricostruito a ogni ridisegno. Con un ascoltatore per bottone bisognerebbe registrarli tutti
ogni volta. Il `<tbody>` invece non viene mai sostituito, quindi il suo unico ascoltatore,
registrato una volta nel costruttore, continua a funzionare per sempre.

**`ev.target.closest('button[data-i]')`** risale dall'elemento cliccato fino a trovare un
bottone con l'attributo `data-i`. Serve perché il click potrebbe colpire un nodo interno al
bottone, o una parte della tabella che non è un bottone: in quel caso `closest` restituisce
`null` e la guardia `if (b && ...)` fa cadere l'evento nel vuoto.

**`Number(b.dataset.i)`.** Gli attributi `data-*` sono sempre stringhe. `dataset.i`
restituirebbe `"3"`, e `rimuovi("3")` fallirebbe il controllo `Number.isInteger`. La
conversione è obbligatoria e sta qui, al confine.

**`cbElimina` inizializzato a `null` e la guardia `if (b && this.cbElimina)`.** Se nessuno ha
ancora registrato una callback, il click non deve rompere nulla. È difensivo ma costa un
`&&`.

### 4.8.2 `disegna` — il ridisegno completo

```js
  disegna(tdi, esito) {
    const rotte = tdi.elenco();

    this.tab.classList.toggle('simulata', !!esito);
    this.elVuota.hidden = rotte.length > 0;
    this.tbody.textContent = '';
```

**`tdi.elenco()`** restituisce la copia difensiva (§ 4.3.3): la vista non può modificare la
tabella nemmeno per sbaglio.

**`classList.toggle('simulata', !!esito)`** aggiunge o toglie la classe CSS in base a una
condizione. `!!esito` converte in booleano vero e proprio (§ 3.8): `toggle` con un secondo
argomento non booleano avrebbe comportamento meno prevedibile. La classe `simulata` serve al
CSS per togliere il bordo inferiore alle righe-regola, così ogni regola e il suo calcolo
appaiono visivamente appaiati (§ 4.12).

**`this.elVuota.hidden = rotte.length > 0`.** L'attributo `hidden` nasconde l'elemento. La
condizione è invertita rispetto a come si leggerebbe: il messaggio «la tabella è vuota» viene
nascosto **quando ci sono righe**.

**`this.tbody.textContent = ''`** svuota il corpo della tabella in un colpo solo.

```js
    rotte.forEach((rt, i) => {
      const riga = esito ? esito.righe[i] : null;
      const tr = document.createElement('tr');

      if (esito) {
        if (rt === esito.scelta) tr.className = 'scelta';
        else if (esito.alternative.indexOf(rt) >= 0) tr.className = 'alt';
        else tr.className = 'no';
      }
```

**`esito.righe[i]`** — l'allineamento posizionale. `righe` è stato costruito da `map` sullo
stesso array `this.rotte`, e `elenco()` è una copia dello stesso array nello stesso ordine:
quindi `righe[i]` descrive esattamente `rotte[i]`. Nessuna ricerca, nessun identificatore da
confrontare: un accesso diretto. È il motivo per cui `cerca` produce una voce **per ogni**
rotta e non solo per quelle compatibili — se saltasse le non compatibili, l'indice `i` non
corrisponderebbe più e la vista dovrebbe cercare.

**`rt === esito.scelta` — confronto per identità.** `===` su oggetti confronta i
**riferimenti**, non i contenuti: è vero solo se le due variabili puntano allo stesso oggetto
in memoria. Qui è esattamente ciò che serve, e funziona perché `esito.scelta` è un
riferimento a una delle `Rotta` che stanno nella tabella, non una copia. Se `cerca` avesse
restituito copie, il confronto fallirebbe e nessuna riga verrebbe colorata.

Questo spiega anche perché due rotte identiche in tutti i campi verrebbero comunque
distinte: sono oggetti diversi. È un vantaggio del confronto per identità rispetto a un
confronto per valore.

**`esito.alternative.indexOf(rt) >= 0`** cerca la rotta fra le alternative; `indexOf` usa
anch'esso l'identità. Restituisce `-1` se assente, da cui il `>= 0`.

**Le tre classi CSS** — `scelta` (verde), `alt` (giallo), `no` (grigio) — coprono i tre casi
richiesti dalla traccia. Quando `esito` è `null` non viene assegnata nessuna classe: la
tabella è neutra, com'è giusto prima di una simulazione.

```js
      tr.appendChild(this._td(String(i + 1), 'num'));

      const tdRete = this._td(Ip.int2dotted(rt.rete), 'ind');
      if (esito && rt === esito.scelta) tdRete.appendChild(this._etichetta('scelta'));
      else if (esito) {
        const k = esito.alternative.indexOf(rt);
        if (k >= 0) tdRete.appendChild(this._etichetta('fallback ' + (k + 1)));
      }
      tr.appendChild(tdRete);
```

**`String(i + 1)`** — numerazione da 1 per l'utente, mentre gli indici interni partono da 0.
La conversione esplicita a stringa non è necessaria (`textContent` convertirebbe da solo) ma
rende l'intenzione chiara e uniforma la chiamata a `_td`, che riceve sempre stringhe.

**Le etichette.** Oltre al colore, la riga scelta porta un badge `scelta` e le alternative
`fallback 1`, `fallback 2`, ... **numerate secondo l'ordine di preferenza**. È
un'informazione che il colore da solo non può dare: fra due righe gialle, quale sarebbe usata
per prima? `k + 1` traduce l'indice dell'array nel numero d'ordine mostrato all'utente.

```js
      tr.appendChild(this._td(Ip.int2dotted(rt.msk) + '  /' + rt.pfx, 'ind'));
      tr.appendChild(this._td(rt.connessa ? '— connessa' : Ip.int2dotted(rt.gw), 'ind'));
      tr.appendChild(this._td(rt.iface));
      tr.appendChild(this._td(String(rt.metr), 'num'));
```

**La netmask mostrata in entrambe le notazioni**, `255.255.255.0  /24`. La forma puntata è
quella che si digita, la forma CIDR è quella che rende immediato il confronto fra prefissi —
e il confronto fra prefissi è ciò che la simulazione deve far capire. Mostrarle entrambe
costa nulla e serve la comprensione.

**`rt.connessa ? '— connessa' : ...`** — per una rete direttamente connessa si scrive
`— connessa` invece di `0.0.0.0`, che sarebbe tecnicamente il valore ma comunicherebbe la
cosa sbagliata (sembra un indirizzo, e non lo è).

**La classe `ind`** applica il carattere monospaziato agli indirizzi, così le cifre si
incolonnano fra righe diverse e il confronto visivo dei prefissi funziona. `num` allinea a
destra i numeri.

```js
      const tdAz = document.createElement('td');
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'mini';
      b.dataset.i = i;
      b.textContent = 'elimina';
      b.title = 'Elimina questa rotta';
      tdAz.appendChild(b);
      tr.appendChild(tdAz);

      this.tbody.appendChild(tr);

      // Il calcolo va su una riga tutta sua: in colonna starebbe stretto e
      // manderebbe la tabella in scroll orizzontale proprio sulla cosa che
      // interessa di più vedere.
      if (riga) this.tbody.appendChild(this._dettaglio(esito.ip, rt, riga, tr.className));
    });
  }
```

**`b.type = 'button'` è obbligatorio.** Il tipo predefinito di un `<button>` dentro un
`<form>` è `submit`. Questo bottone non è dentro il form, ma dichiararlo esplicitamente è una
buona abitudine e protegge da ristrutturazioni future dell'HTML.

**`b.dataset.i = i`** memorizza l'indice sull'elemento, dove l'ascoltatore delegato lo
ritroverà (§ 4.8.1). È l'unico collegamento fra il bottone disegnato e la riga logica.

**La riga di dettaglio: una correzione fatta guardando il risultato.** La prima versione
metteva il calcolo in una **colonna** della tabella. Provandola nel browser, con sette colonne
già occupate da indirizzi in carattere monospaziato, la colonna «Verifica» finiva oltre il
bordo e richiedeva uno scorrimento orizzontale — proprio sulla cosa più importante da vedere.
La soluzione è una riga aggiuntiva a tutta larghezza sotto ogni regola. Non c'è più nessun
problema di spazio e la lettura è più naturale: prima la regola, poi il suo conto.

Il quarto argomento, `tr.className`, propaga la classe di colore alla riga di dettaglio, così
regola e calcolo condividono lo sfondo e si leggono come un blocco unico.

### 4.8.3 `_dettaglio` — il calcolo mostrato

```js
  // Il conto che il programma in C stampava con printf, qui scritto per esteso:
  // indirizzo AND netmask, e il confronto col valore della colonna Rete.
  _dettaglio(ip, rt, riga, cls) {
    const tr = document.createElement('tr');
    tr.className = 'dettaglio ' + cls;
    const td = document.createElement('td');
    td.colSpan = 7;
    td.className = 'verifica';

    td.appendChild(this._span('calc',
      Ip.int2dotted(ip) + ' & ' + Ip.int2dotted(rt.msk) + ' = ' + Ip.int2dotted(riga.and)));
    td.appendChild(this._span('segno', riga.esito ? ' = ' : ' ≠ '));
    td.appendChild(this._span('calc', Ip.int2dotted(rt.rete)));
    td.appendChild(this._span('esito ' + (riga.esito ? 'si' : 'no'),
      riga.esito ? '  ✓ regola compatibile' : '  ✗ regola non compatibile'));

    tr.appendChild(td);
    return tr;
  }
```

**Questo è il punto in cui il progetto risponde alla richiesta «mostrare chiaramente il motivo
della scelta».** Il risultato visibile per la destinazione `196.13.2.5`:

```
196.13.2.5 & 255.255.255.0 = 196.13.2.0  =  196.13.2.0   ✓ regola compatibile
196.13.2.5 & 255.255.255.0 = 196.13.2.0  ≠  196.13.1.0   ✗ regola non compatibile
```

È esattamente l'informazione che il programma in C produceva con `printf` — ma lì era una
riga di testo su terminale, qui è allineata sotto la regola a cui si riferisce, colorata
secondo l'esito, e affiancata alle altre.

**`colSpan = 7`** fa occupare alla cella tutte e sette le colonne della tabella (`#`, rete,
netmask, gateway, interfaccia, metrica, azioni).

**Quattro `<span>` invece di una stringa unica.** Servono per applicare stili diversi ai
pezzi: il segno `=`/`≠` in grassetto, l'esito in verde o grigio. Con una stringa sola non si
potrebbe.

**`'esito ' + (riga.esito ? 'si' : 'no')`** produce `"esito si"` o `"esito no"`: due classi
CSS sullo stesso elemento, una generica per la forma e una specifica per il colore. È il
modo standard di combinare stili in CSS.

**I simboli `≠`, `✓`, `✗`** sono caratteri Unicode inseriti direttamente nel sorgente. Non
servono immagini né font speciali: il file è salvato in UTF-8 e l'HTML lo dichiara con
`<meta charset="utf-8">`.

### 4.8.4 I metodi di supporto

```js
  _span(cls, testo) {
    const s = document.createElement('span');
    s.className = cls;
    s.textContent = testo;
    return s;
  }

  _td(testo, cls) {
    const td = document.createElement('td');
    td.textContent = testo;
    if (cls) td.className = cls;
    return td;
  }

  _etichetta(testo) {
    const s = document.createElement('span');
    s.className = 'etichetta';
    s.textContent = testo;
    return s;
  }
```

Tre funzioni di comodità che riducono la creazione di un elemento da tre righe a una.
Sostituiscono, complessivamente, una trentina di righe ripetute in `disegna`.

**`if (cls)` in `_td`** perché la classe è opzionale: alcune celle non ne hanno.

**Tutte usano `textContent`, mai `innerHTML`** (§ 3.14). Il nome dell'interfaccia arriva da
ciò che l'utente ha digitato: se fosse inserito con `innerHTML`, un valore come
`<img src=x onerror=alert(1)>` verrebbe eseguito. Con `textContent` viene mostrato come
testo. È una protezione XSS che non costa nulla, ottenuta scegliendo la proprietà giusta.

## 4.9 `js/vista-sim.js` — il pannello della simulazione

```js
// Pannello della simulazione: raccoglie l'indirizzo e mostra l'esito.
// La spiegazione arriva già scritta dentro esito.motivo — qui non si ragiona,
// si impagina.
class VistaSim {

  constructor(form, ingresso, elEsito, elErrore) {
    this.form  = form;
    this.in    = ingresso;
    this.box   = elEsito;
    this.err   = elErrore;
    this.cb    = null;

    this.form.addEventListener('submit', ev => {
      ev.preventDefault();
      if (this.cb) this.cb(this.in.value);
    });
  }

  onSimula(cb) { this.cb = cb; }
```

**`ev.preventDefault()`** impedisce il ricaricamento della pagina (§ 3.14). Senza, cliccare
«Instrada» azzererebbe tutto.

**La vista passa una stringa grezza**, `this.in.value`, e non un indirizzo convertito. È
coerente con la regola dello strato: la conversione e la validazione sono compito del
controller e di `Ip`. La vista raccoglie caratteri.

```js
  errore(msg) {
    this.err.textContent = msg;
    this.err.hidden = false;
    this.box.hidden = true;
  }

  pulisci() {
    this.err.hidden = true;
    this.box.hidden = true;
    this.box.textContent = '';
  }
```

**`errore` nasconde l'esito mentre mostra il messaggio.** Se restasse visibile l'esito di una
simulazione precedente accanto a un errore nuovo, si leggerebbe come se il risultato fosse
quello — un'informazione falsa.

**`pulisci` nasconde tutto e svuota.** Serve dopo ogni modifica alla tabella: un esito
calcolato su una tabella che non esiste più non vuol dire niente (§ 4.10).

```js
  mostra(esito) {
    this.err.hidden = true;
    this.box.textContent = '';
    this.box.hidden = false;

    const v = document.createElement('div');
    v.className = 'verdetto' + (esito.scelta ? '' : ' ko');

    if (esito.scelta) {
      v.appendChild(document.createTextNode('Il pacchetto per ' + Ip.int2dotted(esito.ip) + ' esce da '));
      v.appendChild(this._forte(esito.scelta.iface));
      v.appendChild(document.createTextNode(esito.scelta.connessa
        ? ' verso la rete direttamente connessa '
        : ' con next hop '));
      v.appendChild(this._forte(esito.scelta.connessa
        ? Ip.int2dotted(esito.scelta.rete) + '/' + esito.scelta.pfx
        : Ip.int2dotted(esito.scelta.gw)));
      v.appendChild(document.createTextNode('.'));
    } else {
      v.textContent = 'Destinazione ' + Ip.int2dotted(esito.ip) +
                      ' irraggiungibile: il pacchetto viene scartato.';
    }
    this.box.appendChild(v);
```

**Il verdetto è una frase, non una tabella di campi.** La differenza è deliberata: *«Il
pacchetto per 196.13.2.5 esce da **eth0** con next hop **196.13.1.2**»* si legge e si capisce;
un elenco `Interfaccia: eth0 / Gateway: 196.13.1.2` va interpretato.

**`document.createTextNode`** crea un nodo di testo puro, da alternare agli elementi. È la
tecnica per costruire una frase in cui alcune parti sono evidenziate senza usare `innerHTML`:
si alternano nodi di testo e `<span>`.

**La classe `ko`** viene aggiunta solo se non c'è una scelta, e cambia il colore del riquadro
da verde a rosso.

```js
    const p = document.createElement('p');
    p.className = 'motivo';
    p.textContent = esito.motivo;
    this.box.appendChild(p);
```

**Tre righe per la spiegazione completa.** È la ricompensa della decisione di § 2.5: la vista
non ragiona, prende una stringa già pronta e la mette in un paragrafo. Tutta la logica che
produce quel testo sta in `Tdi._motivo`, dove è testabile.

```js
    if (esito.alternative.length) {
      const h = document.createElement('h3');
      h.textContent = 'Alternative utilizzabili come fallback';
      this.box.appendChild(h);

      const ol = document.createElement('ol');
      ol.className = 'fallback';
      esito.alternative.forEach(rt => {
        const li = document.createElement('li');
        li.appendChild(document.createTextNode(
          Ip.int2dotted(rt.rete) + '/' + rt.pfx +
          (rt.connessa ? ' — connessa su ' + rt.iface
                       : ' via ' + Ip.int2dotted(rt.gw) + ' su ' + rt.iface) + ' '));
        const m = document.createElement('span');
        m.className = 'metr';
        m.textContent = '(prefisso /' + rt.pfx + ', metrica ' + rt.metr + ')';
        li.appendChild(m);
        ol.appendChild(li);
      });
      this.box.appendChild(ol);
    }
  }

  _forte(testo) {
    const s = document.createElement('span');
    s.className = 'rotta';
    s.textContent = testo;
    return s;
  }
}
```

**`<ol>` e non `<ul>`.** Un elenco **numerato**, perché l'ordine è informazione: la prima
alternativa è quella che verrebbe usata per prima se la principale cadesse. Un elenco puntato
suggerirebbe che siano intercambiabili.

**Il blocco viene omesso quando non ci sono alternative** — `if (esito.alternative.length)` —
invece di mostrare un titolo seguito da un elenco vuoto. In quel caso l'informazione è già
nel `motivo`: *«Nessuna alternativa: se questa via cade, il pacchetto non ha dove andare»*.

**I criteri fra parentesi.** Ogni voce ripete prefisso e metrica anche se il prefisso è già
visibile nell'indirizzo: è ciò che permette di verificare l'ordinamento con l'occhio.
Leggendo `(prefisso /24, metrica 20)` seguito da `(prefisso /0, metrica 10)` si capisce
perché il primo viene prima nonostante la metrica peggiore — prefisso più lungo vince
(§ 2.8).

## 4.10 `js/app.js` — il controller

L'unico file che conosce sia il dominio sia le viste. Il suo compito è collegarli.

### 4.10.1 Struttura e stato

```js
// Controller: tiene il router, collega le viste al dominio, ridisegna.
// Nessuna aritmetica sugli indirizzi nemmeno qui — al massimo si chiede a Ip di
// convertire ciò che l'utente ha digitato, che è lettura di input.
const App = {

  router: null,
  vTdi: null,
  vSim: null,
  ultimoEsito: null,
```

**Un oggetto letterale e non una classe** perché di `App` esiste una sola istanza per
definizione: è l'applicazione. Istanziare un singoletto con `new` è cerimonia inutile.

**Quattro campi di stato.** `router` è il modello; `vTdi` e `vSim` sono le viste;
`ultimoEsito` è lo stato dell'interfaccia — quale simulazione è attualmente visualizzata.

**Perché `ultimoEsito` è stato del controller e non della vista.** Serve a **due** viste
contemporaneamente: `VistaTdi` lo usa per colorare, `VistaSim` per il verdetto. Se lo tenesse
una delle due, l'altra dovrebbe chiederglielo, creando un accoppiamento fra viste che oggi
non esiste.

### 4.10.2 `avvia` — il cablaggio

```js
  avvia() {
    this.router = App.esempio();

    this.vTdi = new VistaTdi(document.getElementById('tab-tdi'),
                             document.getElementById('tdi-vuota'));
    this.vSim = new VistaSim(document.getElementById('form-sim'),
                             document.getElementById('in-dest'),
                             document.getElementById('esito'),
                             document.getElementById('err-sim'));
```

**Tutti i `getElementById` sono concentrati qui.** È l'unico punto del programma che conosce
gli identificatori dell'HTML. Le viste li ricevono già risolti (§ 4.8.1): se un giorno un
identificatore cambia, si modifica una riga sola.

```js
    this.vTdi.onElimina(i => {
      this.router.tdi.rimuovi(i);
      this.scordaEsito();
      this.ridisegna();
    });
```

**Lo schema che si ripete in tutto il file:** *modifica il modello → scarta l'esito →
ridisegna*. Tre righe, sempre nello stesso ordine.

```js
    this.vSim.onSimula(testo => {
      try {
        const pkt = new Pacchetto(0, Ip.dotted2int(testo));
        this.ultimoEsito = this.router.inoltra(pkt);
        this.vSim.mostra(this.ultimoEsito);
        this.ridisegna();
      } catch (e) {
        this.vSim.errore('Indirizzo non valido: ' + e.message);
      }
    });
```

**Il percorso completo della simulazione in cinque righe.** `Ip.dotted2int(testo)` valida e
converte — se la stringa è malformata lancia, e il `catch` mostra l'errore senza toccare
nulla. `new Pacchetto(0, ...)` costruisce il pacchetto con sorgente `0.0.0.0`, che non è
usata. `router.inoltra` produce l'esito. Poi si aggiornano entrambe le viste: `vSim.mostra`
per il verdetto, `ridisegna` per l'evidenziazione della tabella.

**Perché la conversione sta qui e non nella vista.** La vista raccoglie caratteri; il
controller decide cosa significano. Se `VistaSim` chiamasse `Ip.dotted2int`, lo strato di
presentazione comincerebbe a conoscere il dominio.

```js
    document.getElementById('form-rotta').addEventListener('submit', ev => {
      ev.preventDefault();
      this.aggiungiRotta();
    });

    document.getElementById('b-salva').addEventListener('click', () => {
      Persistenza.esporta(this.router, 'router-' + this.router.nome + '.json');
      this.nota('Configurazione scaricata.');
    });

    document.getElementById('b-carica').addEventListener('click', () => {
      document.getElementById('in-file').click();
    });
```

**Il form delle rotte è gestito direttamente da `App`**, senza una classe vista dedicata. È
una scelta di proporzione: cinque campi e un `submit` non giustificano una classe. Se il form
crescesse — con validazione in tempo reale, suggerimenti, modifica di righe esistenti —
meriterebbe un `VistaForm`.

**Il trucco del bottone «Carica».** Un `<input type="file">` ha un aspetto grafico imposto dal
sistema operativo, diverso su ogni piattaforma e non modificabile. La soluzione universale:
si nasconde l'input (`hidden` nell'HTML) e si mette un `<button>` normale che ne simula il
click. L'utente vede un bottone coerente col resto dell'interfaccia; il browser apre il suo
selettore di file.

```js
    document.getElementById('in-file').addEventListener('change', ev => {
      const f = ev.target.files[0];
      if (!f) return;
      Persistenza.importa(f)
        .then(r => {
          this.router = r;
          this.scordaEsito();
          this.ridisegna();
          this.nota('Caricata la configurazione di ' + r.nome + '.');
        })
        .catch(e => this.nota('Caricamento fallito: ' + e.message + ' — la tabella attuale resta com\'era.'));
      // Cosi' ricaricare due volte lo stesso file rilancia l'evento change.
      ev.target.value = '';
    });
```

**`if (!f) return;`** — l'utente può aprire il selettore e annullare: in quel caso `files` è
vuoto e non c'è nulla da fare.

**La garanzia di atomicità è nell'ordine delle righe.** `this.router = r` avviene **dentro il
`.then()`**, cioè solo se `importa` ha avuto successo. Se il file è malformato, la Promise
viene rifiutata, si esegue il `.catch()`, e `this.router` non viene mai toccato: la tabella
precedente resta intatta. Questo non è un caso fortunato, è la ragione per cui
`Persistenza.importa` costruisce un `Router` **completo** prima di risolvere, invece di
modificare quello esistente pezzo per pezzo.

**`ev.target.value = ''` — un dettaglio non ovvio.** L'evento `change` di un `<input
type="file">` scatta solo quando il valore **cambia**. Selezionando due volte di fila lo
stesso file, la seconda volta il valore è identico e l'evento non viene emesso: l'utente
clicca, sceglie il file, e non succede nulla. Azzerare il valore dopo ogni caricamento fa sì
che qualunque selezione successiva sia un cambiamento.

```js
    document.getElementById('b-esempio').addEventListener('click', () => {
      this.router = App.esempio();
      this.scordaEsito();
      this.ridisegna();
      this.nota('Caricata la tabella d\'esempio.');
    });

    document.getElementById('b-svuota').addEventListener('click', () => {
      this.router.tdi.svuota();
      this.scordaEsito();
      this.ridisegna();
    });

    this.ridisegna();
  },
```

**L'ultima riga.** Dopo aver collegato tutto, un primo ridisegno mostra la tabella d'esempio.
Senza, la pagina resterebbe vuota fino alla prima interazione.

### 4.10.3 `aggiungiRotta` — la validazione all'opera

```js
  aggiungiRotta() {
    const err = document.getElementById('err-rotta');
    try {
      this.router.tdi.agg(Rotta.daDotted(
        document.getElementById('in-rete').value,
        document.getElementById('in-msk').value,
        document.getElementById('in-gw').value,
        document.getElementById('in-iface').value,
        document.getElementById('in-metr').value
      ));
      err.hidden = true;
      document.getElementById('in-rete').value = '';
      document.getElementById('in-msk').value = '';
      document.getElementById('in-gw').value = '0.0.0.0';
      document.getElementById('in-rete').focus();
      this.scordaEsito();
      this.ridisegna();
    } catch (e) {
      err.textContent = e.message;
      err.hidden = false;
    }
  },
```

**L'ordine delle istruzioni dentro il `try` è la garanzia di atomicità** (§ 3.12). Le due
operazioni che possono fallire — `Rotta.daDotted` e `agg` — sono le **prime**. Tutto ciò che
segue (nascondere l'errore, svuotare i campi, ridisegnare) avviene solo se non è stato
lanciato nulla. Se la rotta è invalida, il flusso salta al `catch` e:

- la tabella non è stata modificata;
- il form **conserva ciò che l'utente aveva digitato**, così può correggere invece di
  riscrivere tutto;
- il messaggio d'errore compare sotto il form.

**Quali campi vengono svuotati e quali no.** `rete` e `msk` sì, perché la prossima rotta avrà
valori diversi. `gw` torna a `0.0.0.0`, il predefinito. `iface` e `metr` **restano**: quando
si inseriscono più rotte di seguito, tipicamente escono dalla stessa interfaccia con lo
stesso costo, e ridigitarlo ogni volta sarebbe una frizione inutile.

**`focus()`** rimette il cursore nel primo campo: si può inserire la rotta successiva senza
toccare il mouse.

**Nessuna conversione qui.** I cinque `.value` sono stringhe grezze passate a
`Rotta.daDotted`, che le converte e le valida (§ 4.2.5). Il controller non fa aritmetica: è
la regola dello strato vista, rispettata anche nel controller.

### 4.10.4 `scordaEsito`, `ridisegna`, `nota`

```js
  // Dopo ogni modifica alla tabella l'evidenziazione precedente non vuol più
  // dire niente: meglio toglierla che lasciare colori che mentono.
  scordaEsito() {
    this.ultimoEsito = null;
    this.vSim.pulisci();
  },

  ridisegna() { this.vTdi.disegna(this.router.tdi, this.ultimoEsito); },

  nota(msg) {
    const el = document.getElementById('msg-file');
    el.textContent = msg;
    el.hidden = false;
  },
```

**`scordaEsito` risolve un problema di correttezza, non di estetica.** Si supponga di
simulare `196.13.2.5`, veder colorata la riga 3, e poi **eliminare la riga 1**. Tutte le righe
scalano di una posizione. Senza `scordaEsito`, l'esito vecchio conterrebbe ancora
`righe[]` di lunghezza 5 mentre la tabella ne ha 4: `esito.righe[i]` sarebbe disallineato e la
vista mostrerebbe calcoli attribuiti alle righe sbagliate. Colori che mentono, appunto.

L'unica scelta corretta è invalidare l'esito a ogni modifica. Viene chiamata da **tutte** le
azioni che toccano la tabella: elimina, aggiungi, svuota, carica, esempio. L'unico percorso
che **non** la chiama è il ramo `catch` di `aggiungiRotta`, ed è giusto: lì la tabella non è
stata modificata, quindi l'evidenziazione è ancora valida.

**`ridisegna` è l'unico punto che chiama `disegna`.** Concentrare il ridisegno in un solo
metodo significa che nessun chiamante deve ricordarsi di passare `ultimoEsito`: lo prende da
sé. È il rimedio al principale svantaggio del non usare un framework reattivo (§ 2.1).

### 4.10.5 `esempio` — la tabella dimostrativa

```js
  // La TDI di pag. 129 (default route + rete connessa) più le righe che quel
  // programma non poteva esprimere: una destinazione raggiungibile per due strade
  // diverse, dove a decidere è la metrica.
  esempio() {
    const r = new Router('R1');
    r.aggIface(new Iface('eth0', Ip.dotted2int('196.13.1.1'), Ip.pfx2msk(24)));
    r.aggIface(new Iface('eth1', Ip.dotted2int('196.13.5.1'), Ip.pfx2msk(24)));

    r.tdi.agg(Rotta.daDotted('196.13.1.0', '/24', '0.0.0.0',      'eth0',  1));
    r.tdi.agg(Rotta.daDotted('196.13.5.0', '/24', '0.0.0.0',      'eth1',  1));
    r.tdi.agg(Rotta.daDotted('196.13.2.0', '/24', '196.13.1.2',   'eth0',  5));
    r.tdi.agg(Rotta.daDotted('196.13.2.0', '/24', '196.13.5.2',   'eth1', 20));
    r.tdi.agg(Rotta.daDotted('0.0.0.0',    '/0',  '196.13.1.254', 'eth0', 10));
    return r;
  }
};

document.addEventListener('DOMContentLoaded', () => App.avvia());
```

**La tabella non è casuale: ogni riga dimostra un concetto**, e insieme coprono tutti i casi
che il programma deve saper gestire.

| # | Rotta | Cosa dimostra |
|---|---|---|
| 1 | `196.13.1.0/24` connessa su eth0 | Rete direttamente connessa, gateway `0.0.0.0` |
| 2 | `196.13.5.0/24` connessa su eth1 | Un router ha più interfacce |
| 3 | `196.13.2.0/24` via `196.13.1.2` metrica **5** | Rotta con next hop — **percorso principale** |
| 4 | `196.13.2.0/24` via `196.13.5.2` metrica **20** | **Stessa destinazione, gateway diverso**: la floating static route (§ 2.8) |
| 5 | `0.0.0.0/0` via `196.13.1.254` | La default route |

**Le tre simulazioni che questa tabella rende possibili senza digitare altro:**

| Destinazione | Vince | Alternative | Concetto mostrato |
|---|---|---|---|
| `196.13.2.5` | riga 3 (metrica 5) | riga 4, poi riga 5 | **Pareggio sul prefisso risolto dalla metrica** + fallback ordinato |
| `196.13.1.9` | riga 1 (connessa) | riga 5 | Rete connessa, default come unica riserva |
| `8.8.8.8` | riga 5 (default) | nessuna | La default route come ultima risorsa |

E cancellando la riga 5 e ripetendo `8.8.8.8` si ottiene il caso «destinazione
irraggiungibile». Cinque righe coprono l'intero spazio dei comportamenti.

**Gli indirizzi vengono da pag. 129** (`196.13.x.x`, `196.13.1.1`), così il confronto con il
programma in C è immediato: si riconoscono le stesse reti.

**L'ultima riga del file.** `DOMContentLoaded` scatta quando l'HTML è stato completamente
analizzato e gli elementi esistono nel DOM. Registrare l'avvio su quell'evento è la garanzia
che i `getElementById` di `avvia()` trovino qualcosa. Gli script sono già in fondo al
`<body>`, quindi in pratica il documento è quasi sempre pronto — ma la garanzia esplicita
costa una riga e rende il codice indipendente dalla posizione dei tag.

## 4.11 `index.html` — la struttura del documento

```html
<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Simulatore di Router — Tabella di Instradamento</title>
<link rel="stylesheet" href="css/stile.css">
</head>
```

**`<!DOCTYPE html>`** attiva la modalità standard di rendering. Senza, i browser entrano in
*quirks mode*, una modalità di compatibilità con l'HTML degli anni Novanta in cui il modello
di scatola CSS si comporta diversamente e i fogli di stile moderni si rompono.

**`lang="it"`** dichiara la lingua del documento: serve ai lettori di schermo per la
pronuncia e ai correttori ortografici.

**`<meta charset="utf-8">`** dev'essere fra i primi elementi del `<head>`. Senza,
`È`, `più`, `≠`, `✓` verrebbero interpretati con la codifica predefinita del browser e
apparirebbero come sequenze di caratteri incomprensibili.

**`<meta name="viewport">`** dice ai browser mobili di usare la larghezza reale dello
schermo invece di simulare una finestra da desktop e rimpicciolire tutto.

```html
    <div class="scorri">
      <table id="tab-tdi">
        <thead>
          <tr>
            <th class="num">#</th>
            <th>Rete di destinazione</th>
            <th>Netmask</th>
            <th>Gateway</th>
            <th>Interfaccia</th>
            <th class="num">Metrica</th>
            <th></th>
          </tr>
        </thead>
        <tbody></tbody>
      </table>
    </div>
```

**`<thead>` e `<tbody>` separati.** L'intestazione è statica e scritta nell'HTML; il corpo è
vuoto e viene riempito da JavaScript. La separazione permette a `VistaTdi` di svuotare il
solo `<tbody>` senza distruggere le intestazioni, ed è ciò che rende possibile la delega
degli eventi (§ 4.8.1): il `<tbody>` è un elemento stabile a cui agganciare l'ascoltatore.

**Il `<div class="scorri">` che avvolge la tabella** ha `overflow-x: auto` nel CSS: se la
tabella dovesse risultare più larga della finestra, scorre da sola invece di far scorrere
tutta la pagina.

**L'ultima `<th>` è vuota**: è la colonna dei bottoni «elimina», che non ha titolo perché non
contiene dati.

```html
    <form id="form-rotta" autocomplete="off">
      <div class="campo">
        <label for="in-rete">Rete</label>
        <input id="in-rete" placeholder="196.13.2.0" required>
      </div>
      ...
      <div class="campo stretto">
        <label for="in-metr">Metrica</label>
        <input id="in-metr" type="number" min="0" value="1" required>
      </div>
      <button type="submit">Aggiungi rotta</button>
    </form>
```

**`<label for="in-rete">` associata all'`id` del campo.** Cliccando l'etichetta il cursore va
nel campo, e i lettori di schermo annunciano il nome corretto. È il modo giusto di etichettare
un campo, e costa un attributo.

**`required`** fa fare al browser un primo controllo — campo non vuoto — prima ancora che il
codice parta. **Non sostituisce la validazione applicativa**: `required` sa solo che il campo
non è vuoto, non che contiene un indirizzo IP valido. È un filtro grossolano gratuito.

**`type="number" min="0"`** sul campo metrica fa comparire i pulsanti su/giù e la tastiera
numerica sui dispositivi mobili. Anche qui, il controllo vero resta nel costruttore di
`Rotta`: `min="0"` è aggirabile digitando direttamente.

**`autocomplete="off"`** impedisce al browser di proporre completamenti da altri moduli: un
indirizzo IP non è un dato che ha senso ricordare fra siti.

**`placeholder`** mostra un esempio grigio nel campo vuoto. Nota che il campo netmask ha
`placeholder="255.255.255.0 oppure /24"`, che documenta la doppia notazione accettata da
`Ip.parseMsk` (§ 4.1.7) direttamente dove serve.

```html
      <button type="button" id="b-salva">Salva su file</button>
      <button type="button" id="b-carica" class="secondario">Carica da file</button>
      <input type="file" id="in-file" accept="application/json,.json" hidden>
```

**`type="button"` esplicito.** Dentro un `<form>` il tipo predefinito è `submit`: questi
bottoni sono fuori dal form, ma dichiararlo protegge da riorganizzazioni future dell'HTML.

**`accept="application/json,.json"`** filtra il selettore di file mostrando per primi i file
JSON. È un aiuto, non una garanzia: l'utente può sempre scegliere «tutti i file», ed è per
questo che `Persistenza.importa` valida comunque.

**`hidden`** sull'input file: nascosto e pilotato dal bottone (§ 4.10.2).

```html
<!-- Niente ES modules: aprendo il file con doppio click il protocollo è file://,
     che li blocca. Quindi script classici, in ordine di dipendenza. -->
<script src="js/ip.js"></script>
<script src="js/rotta.js"></script>
<script src="js/tdi.js"></script>
<script src="js/iface.js"></script>
<script src="js/pacchetto.js"></script>
<script src="js/router.js"></script>
<script src="js/persistenza.js"></script>
<script src="js/vista-tdi.js"></script>
<script src="js/vista-sim.js"></script>
<script src="js/app.js"></script>
```

**L'ordine è un vincolo di correttezza, non una preferenza** (§ 2.2). Il grafo delle
dipendenze, letto dal basso:

```
app.js        → tutto
vista-sim.js  → Ip
vista-tdi.js  → Ip
persistenza.js→ Router
router.js     → Tdi, Iface
pacchetto.js  → Ip
iface.js      → Ip
tdi.js        → Rotta, Ip
rotta.js      → Ip
ip.js         → (niente)
```

L'ordine dei tag è una **ordinazione topologica** di questo grafo: ogni file compare dopo
tutti quelli da cui dipende. Il commento spiega perché non si usano i moduli, così chi
riordinasse i tag per estetica sa cosa sta rischiando.

**Lo stesso ordine è ripetuto identico in `test.html`**, seguito dai file di test. È la
ragione per cui i test verificano davvero il codice di produzione: caricano gli stessi file
nella stessa sequenza.

## 4.12 `css/stile.css` — l'aspetto

Non è la parte valutata, ma alcune scelte hanno conseguenze funzionali.

### Le variabili CSS

```css
:root {
  --testo:    #1c1f23;
  --tenue:    #6b7280;
  --bordo:    #d8dce2;
  --sfondo:   #f6f7f9;
  --carta:    #ffffff;

  --scelta-bg:  #e3f5e6;
  --scelta-br:  #3f9d52;
  --alt-bg:     #fdf3d8;
  --alt-br:     #d19c1d;
  --no-tx:      #9aa1ab;
  --errore:     #b3261e;

  --mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
}
```

`:root` è lo pseudo-selettore che corrisponde all'elemento `<html>`; le proprietà che
cominciano con `--` sono **variabili CSS**, richiamabili con `var(--nome)`. Definire la
tavolozza in un punto solo significa che cambiare il verde della rotta scelta è una modifica
di un carattere invece di una ricerca in tutto il file.

I nomi dicono la funzione (`--scelta-bg`, `--alt-br`), non il colore (`--verde-chiaro`): se
un giorno il verde diventasse blu, il nome resterebbe corretto.

**La pila di caratteri monospaziati** elenca in ordine i font disponibili sui vari sistemi:
`ui-monospace` (il monospaziato di sistema), poi le varianti Apple, poi Linux/Windows, e
infine `monospace` come rete di sicurezza. Nessun font scaricato da internet, coerentemente
con il vincolo di funzionare offline.

### L'appaiamento fra regola e calcolo

```css
/* la regola e il suo calcolo sono due <tr> ma una cosa sola: il bordo lo tiene
   solo il secondo, così restano visivamente appaiati */
table.simulata tbody tr:not(.dettaglio) td { border-bottom: none; }
tbody tr.dettaglio td { padding-top: 0; padding-bottom: 0.55rem; }
```

Il problema: dopo una simulazione ogni regola occupa **due** righe della tabella, la regola e
il suo calcolo. Con il bordo predefinito su ogni riga, il calcolo apparirebbe separato dalla
regola a cui appartiene, e i due sembrerebbero elementi indipendenti.

La soluzione: quando la tabella ha la classe `simulata`, le righe che **non** sono di
dettaglio perdono il bordo inferiore. Il bordo resta solo sulle righe di dettaglio, quindi
separa un blocco regola+calcolo dal successivo.

**`:not(.dettaglio)`** è la pseudo-classe di negazione: seleziona ciò che *non* ha quella
classe. **`table.simulata ...`** limita la regola al caso in cui la classe sia presente:
senza simulazione le righe di dettaglio non esistono e ogni regola torna ad avere il proprio
bordo. È la controparte CSS di `classList.toggle('simulata', !!esito)` in § 4.8.2.

### L'evidenziazione

```css
tbody tr.scelta { background: var(--scelta-bg); box-shadow: inset 3px 0 0 var(--scelta-br); }
tbody tr.alt    { background: var(--alt-bg);    box-shadow: inset 3px 0 0 var(--alt-br); }
tbody tr.no     { color: var(--no-tx); }
```

**`box-shadow: inset 3px 0 0 colore`** disegna una barra colorata a sinistra della riga. Si
usa questo invece di `border-left` perché su un `<tr>` il bordo non viene reso in modo
uniforme fra browser quando le celle hanno `border-collapse: collapse`, mentre l'ombra
interna funziona sempre.

**Doppia codifica dell'informazione.** Le righe compatibili hanno uno sfondo colorato **e**
una barra laterale **e** un'etichetta testuale (`scelta`, `fallback 1`); le non compatibili
hanno il testo attenuato. Chi non distingue verde e giallo legge comunque l'etichetta. È il
principio di non affidare mai un'informazione al solo colore.

### Il resto

- **`overflow-x: auto`** sul contenitore `.scorri`: la tabella scorre da sola se troppo larga,
  la pagina no.
- **`display: flex; flex-wrap: wrap`** sui form: i campi si dispongono in riga e vanno a capo
  automaticamente su schermi stretti, senza *media query*.
- **`white-space: nowrap`** sulle celle: un indirizzo IP non deve mai andare a capo a metà.
- **`font: 15px/1.55 system-ui, ...`**: il carattere di sistema, quindi nessun font da
  scaricare e aspetto nativo su ogni piattaforma.

## 4.13 `test/runner.js` e i file di test

### Il runner

```js
// Mini-runner di asserzioni. Non è Jest, e va benissimo così: introdurre Jest
// vorrebbe dire introdurre npm, e con npm un build step — che è esattamente il
// vincolo che questo progetto si è dato.
const T = { ok: 0, ko: 0, righe: [] };

function ok(desc, cond) {
  if (cond) { T.ok++; T.righe.push(['ok', desc]); }
  else      { T.ko++; T.righe.push(['ko', desc]); }
}

function eq(desc, a, b) {
  ok(a === b ? desc : desc + '  → atteso ' + b + ', ottenuto ' + a, a === b);
}

// Asserisce che fn sollevi un errore. Se non lo fa, il test fallisce.
function lancia(desc, fn) {
  try { fn(); ok(desc + '  → non ha sollevato nulla', false); }
  catch (e) { ok(desc, true); }
}

function gruppo(nome) { T.righe.push(['gruppo', nome]); }
```

**`ok` è l'unica asserzione vera**; le altre due sono comodità costruite su di essa.

**`eq` arricchisce il messaggio solo in caso di fallimento.** Il ternario dentro la chiamata
fa sì che un test passato mostri la sua descrizione pulita, mentre uno fallito mostri
`descrizione → atteso X, ottenuto Y`. La differenza è pratica: quando tutto è verde non
serve rumore, quando qualcosa è rosso servono i numeri.

**`lancia` verifica che qualcosa fallisca.** La struttura è controintuitiva e va letta con
attenzione: si esegue `fn()`; se **non** lancia si arriva alla riga successiva, che registra
un **fallimento**; se lancia, il controllo salta al `catch`, che registra un **successo**.

**Perché testare i fallimenti è importante quanto testare i successi.** Metà del valore della
validazione (§ 2.9) sta nel rifiutare gli input sbagliati. Un test che verifica solo il
percorso felice non si accorgerebbe se un giorno qualcuno rimuovesse un controllo. Nel
progetto ci sono **28 asserzioni `lancia`** su 129 totali: più di una su cinque verifica che
il programma sappia dire di no.

**`catch (e)` senza usare `e`.** Il test verifica *che* venga sollevato un errore, non
*quale*. Legare i test al testo esatto dei messaggi li renderebbe fragili: cambiare una parola
in un messaggio d'errore romperebbe un test senza che nulla sia effettivamente rotto.

```js
function riassunto() {
  const testa = T.ko === 0
    ? 'Tutto verde: ' + T.ok + ' asserzioni passate.'
    : T.ko + ' fallite su ' + (T.ok + T.ko) + '.';

  if (typeof document === 'undefined') {
    // eseguito da riga di comando, durante lo sviluppo
    T.righe.forEach(([t, d]) => {
      if (t === 'gruppo') console.log('\n== ' + d);
      else console.log((t === 'ok' ? '  ok  ' : '  KO  ') + d);
    });
    console.log('\n' + testa);
    if (typeof process !== 'undefined' && T.ko > 0) process.exitCode = 1;
    return;
  }

  const box = document.getElementById('esiti');
  const h = document.getElementById('testa');
  h.textContent = testa;
  h.className = T.ko === 0 ? 'verde' : 'rosso';
  ...
}
```

**Il doppio ambiente è la parte più interessante del runner.** `typeof document === 'undefined'`
distingue Node dal browser. `typeof` su una variabile non dichiarata restituisce `'undefined'`
senza sollevare eccezioni — è l'unico operatore che lo fa, ed è il motivo per cui si usa
questa forma invece di `document === undefined`, che lancerebbe `ReferenceError`.

**Cosa compra questa riga.** Gli stessi test girano in due modi:

- **Nel browser**, doppio click su `test.html`: risultato visivo, verde o rosso, dimostrabile
  in dieci secondi.
- **Da riga di comando con Node**, concatenando gli stessi file: ciclo di verifica rapidissimo
  durante lo sviluppo, senza aprire un browser.

È possibile solo perché lo strato logico non dipende dal DOM (§ 2.6). La regola architetturale
si trasforma in un beneficio concreto.

**`process.exitCode = 1`** in caso di fallimento: da riga di comando il processo termina con
codice di errore, quindi il risultato è utilizzabile in una pipeline automatica.

**`T.righe.forEach(([t, d]) => ...)`** usa la **destrutturazione** dell'array: ogni elemento è
una coppia `['ok', 'descrizione']`, e `[t, d]` ne estrae direttamente i due valori invece di
scrivere `riga[0]` e `riga[1]`.

### La copertura dei test

129 asserzioni distribuite su cinque file.

| File | Asserzioni | Cosa copre |
|---|---|---|
| `test-ip.js` | 37 | Conversioni in entrambi i versi, round-trip, il caso `255.255.255.255` che non deve diventare negativo, input malformati (6 casi), tutti i prefissi limite (`/0`, `/8`, `/17`, `/24`, `/32`), contiguità della netmask, le tre notazioni di `parseMsk` |
| `test-rotta.js` | 28 | Prefisso, `connessa`, `copre` compresi i bordi (indirizzo di rete, default che copre tutto e anche il broadcast), il contenuto di `calcolo`, `stessaDest` contro `identicaA`, i quattro rifiuti del costruttore, round-trip JSON |
| `test-tdi.js` | 30 | Longest Prefix Match nei tre scenari, il numero di righe valutate, il prefisso che batte la metrica, la floating static route, la parità piena risolta dall'ordine di inserimento, il caso senza match, la copia difensiva di `elenco`, il rifiuto della rotta identica, round-trip |
| `test-router.js` | 20 | Inoltro, risoluzione nome → interfaccia, TTL predefinito ed esplicito, `locale`, rifiuti, round-trip completo |
| `test-persistenza.js` | 14 | Presenza della versione, indirizzi in puntato nel file, round-trip che preserva il comportamento, cinque casi di file invalido |
| **Totale** | **129** | |

**Tre asserzioni che meritano una nota.**

```js
eq('int2dotted non si fa ingannare dal segno', Ip.int2dotted(-1), '255.255.255.255');
```

Verifica la robustezza al problema del segno (§ 2.3.1) con l'input peggiore possibile.

```js
eq('pfx2msk 0', Ip.pfx2msk(0), 0);
```

Copre il caso limite dello scorrimento modulo 32 (§ 4.1.6). Senza questo test, il bug della
default route trasformata in `/32` passerebbe inosservato.

```js
const copia = tdiEsempio().elenco();
copia.push('spazzatura');
eq('elenco restituisce una copia difensiva', tdiEsempio().elenco().length, 3);
```

Verifica l'incapsulamento: modificare l'array restituito non deve toccare la tabella.

---

# Parte V — I flussi completi

Le sezioni precedenti hanno esaminato i pezzi. Questa li segue in movimento.

## 5.1 Avvio dell'applicazione

```
1.  Doppio click su index.html
2.  Il browser legge il documento, applica css/stile.css
3.  Incontra <script src="js/ip.js">, lo scarica ed esegue → const Ip esiste
4.  Idem per rotta, tdi, iface, pacchetto, router, persistenza, vista-tdi,
    vista-sim → tutte le classi esistono nell'ambito globale
5.  Esegue app.js → const App esiste; l'ultima riga registra DOMContentLoaded
6.  Terminata l'analisi del documento, il browser emette DOMContentLoaded
7.  App.avvia() parte:
       a. App.esempio() costruisce Router R1 con 2 interfacce e 5 rotte
          → ogni Rotta passa dal proprio costruttore: 5 validazioni
          → ogni agg() controlla la ridondanza: nessuna rotta identica
       b. new VistaTdi(...) → trova il <tbody>, registra l'ascoltatore delegato
       c. new VistaSim(...) → registra l'ascoltatore sul submit del form
       d. Si registrano i 6 ascoltatori restanti (form rotta, salva, carica,
          change su input file, esempio, svuota)
       e. this.ridisegna() → vTdi.disegna(tdi, null)
             → esito è null: nessuna classe di colore, nessuna riga di dettaglio
             → 5 righe disegnate, ognuna con 7 celle
8.  La pagina è pronta e interattiva
```

## 5.2 Aggiunta di una rotta

**Percorso felice**, l'utente digita `10.0.0.0`, `/8`, `192.168.1.1`, `eth0`, `3`:

```
1.  Click su «Aggiungi rotta» (o Invio in un campo)
2.  Il browser controlla required su tutti i campi: nessuno è vuoto → prosegue
3.  L'ascoltatore submit chiama ev.preventDefault() → nessun ricaricamento
4.  App.aggiungiRotta()
5.    Rotta.daDotted('10.0.0.0', '/8', '192.168.1.1', 'eth0', '3')
6.      Ip.dotted2int('10.0.0.0')     → 167772160
7.      Ip.parseMsk('/8')             → nessun punto → ramo CIDR → pfx2msk(8)
                                      → 4278190080
8.      Ip.dotted2int('192.168.1.1')  → 3232235777
9.      new Rotta(167772160, 4278190080, 3232235777, 'eth0', '3')
10.       mskValida(4278190080) → true
11.       (167772160 & 4278190080) === 167772160 → true, nessun bit fuori mask
12.       Number('3') = 3, finito e ≥ 0 → ok
13.       'eth0' non è vuoto → ok
14.       oggetto Rotta creato e valido
15.   tdi.agg(rotta) → some(identicaA) è false → push
16.   err.hidden = true
17.   Si svuotano rete e msk, gw torna a 0.0.0.0, focus sul primo campo
18.   scordaEsito() → ultimoEsito = null, vSim.pulisci()
19.   ridisegna() → la tabella ha 6 righe, nessuna colorata
```

**Percorso d'errore**, l'utente digita `192.168.1.77` con `/24`:

```
5.    Rotta.daDotted(...)
9.      new Rotta(3232235853, 4294967040, ...)
11.       (3232235853 & 4294967040) = 3232235776 ≠ 3232235853
            → throw new Error('la rete 192.168.1.77 ha bit accesi fuori dalla
                               mask /24 — forse intendevi 192.168.1.0')
      ↓ l'esecuzione salta direttamente al catch
20.   err.textContent = e.message; err.hidden = false
```

**Cosa NON è successo, ed è il punto:** `agg` non è stata chiamata, la tabella non è cambiata,
i campi non sono stati svuotati (l'utente può correggere il solo campo sbagliato),
`ridisegna` non è avvenuto. La garanzia viene dall'ordine delle istruzioni nel `try`
(§ 4.10.3).

## 5.3 Simulazione — il flusso principale

Tabella d'esempio, destinazione `196.13.2.5`:

```
1.  L'utente digita 196.13.2.5 e preme Invio
2.  VistaSim intercetta il submit, preventDefault, chiama la callback col testo
3.  App: Ip.dotted2int('196.13.2.5') → 3289317381
4.      new Pacchetto(0, 3289317381) → ttl 64
5.      router.inoltra(pkt) → tdi.cerca(3289317381)

6.        SCANSIONE — map su tutte e 5 le rotte, nessuna saltata:
            #1 196.13.1.0/24  → 3289317381 & /24 = 196.13.2.0 ≠ 196.13.1.0  falso
            #2 196.13.5.0/24  → 196.13.2.0 ≠ 196.13.5.0                    falso
            #3 196.13.2.0/24  → 196.13.2.0 = 196.13.2.0                    VERO
            #4 196.13.2.0/24  → 196.13.2.0 = 196.13.2.0                    VERO
            #5 0.0.0.0/0      → 3289317381 & 0 = 0 = 0.0.0.0               VERO
          righe = 5 voci

7.        FILTRO — match = [ #3 (/24 m5), #4 (/24 m20), #5 (/0 m10) ]

8.        ORDINAMENTO — sort((a,b) => b.pfx - a.pfx || a.metr - b.metr)
            #3 vs #4:  24-24 = 0 → falsy → 5-20 = -15  → #3 prima
            #3 vs #5:  0-24 = -24                       → #3 prima
            #4 vs #5:  0-24 = -24                       → #4 prima
          match ordinato = [ #3, #4, #5 ]

9.        SELEZIONE — scelta = #3, alternative = [#4, #5]

10.       MOTIVO —
          "Per 196.13.2.5 vince 196.13.2.0/24. Fissa 24 bit di prefisso, più di
           ogni altra regola compatibile. Next hop 196.13.1.2 su eth0. Stesso
           prefisso anche via 196.13.5.2, quindi ha deciso la metrica: 5 contro
           20. 2 alternative disponibili come fallback, nell'ordine:
           196.13.2.0/24 via 196.13.5.2 (metrica 20), 0.0.0.0/0 via
           196.13.1.254 (metrica 10)."

11. App: ultimoEsito = esito
12.      vSim.mostra(esito) → verdetto verde, paragrafo del motivo, elenco
                              numerato delle 2 alternative
13.      ridisegna() → vTdi.disegna(tdi, esito)
           tabella.classList aggiunge 'simulata'
           riga 1: classe 'no'      + dettaglio col calcolo e ✗
           riga 2: classe 'no'      + dettaglio col calcolo e ✗
           riga 3: classe 'scelta'  + badge «scelta»     + dettaglio ✓
           riga 4: classe 'alt'     + badge «fallback 1» + dettaglio ✓
           riga 5: classe 'alt'     + badge «fallback 2» + dettaglio ✓
```

**Il punto 8 è il cuore del progetto.** Le righe #3 e #4 hanno lo **stesso prefisso** — sono
la stessa destinazione via gateway diversi — e a decidere è la metrica. Le righe #3 e #5
hanno prefissi diversi, e il prefisso più lungo vince a prescindere dalla metrica: infatti #3
ha metrica 5 e #5 metrica 10, ma anche se fosse stato il contrario #3 avrebbe vinto lo
stesso.

## 5.4 Salvataggio su file

```
1.  Click su «Salva su file»
2.  Persistenza.esporta(router, 'router-R1.json')
3.    serializza(router) → { versione: 1, router: {...} }
4.      router.toJSON()
5.        ifaces.map(i => i.toJSON())  → indirizzi riconvertiti in puntato
6.        tdi.toJSON() → rotte.map(r => r.toJSON()) → idem
7.    JSON.stringify(o, null, 2) → testo formattato e indentato
8.    new Blob([testo], {type:'application/json'})
9.    URL.createObjectURL(blob) → 'blob:http://.../a1b2...'
10.   <a href=blob download='router-R1.json'> creato e inserito nel body
11.   a.click() → il browser avvia il download
12.   rimozione dell'ancora, revokeObjectURL → memoria liberata
13. App.nota('Configurazione scaricata.')
```

## 5.5 Caricamento da file

**Percorso felice:**

```
1.  Click su «Carica da file» → in-file.click() → si apre il selettore
2.  L'utente sceglie un file → evento 'change'
3.  f = ev.target.files[0]
4.  Persistenza.importa(f) → restituisce una Promise
5.    new FileReader(), readAsText(f)  → parte la lettura asincrona
      ... la funzione RITORNA subito, la pagina resta reattiva ...
6.    (più tardi) fr.onload:
7.      JSON.parse(fr.result) → oggetto
8.      deserializza: controlla oggetto, versione === 1, presenza di router
9.      Router.daJSON → ricostruisce Iface e Tdi, rivalidando ogni rotta
10.     risolvi(router)
11. .then(r => ...):
12.     this.router = r          ← SOLO ORA il router vecchio viene sostituito
13.     scordaEsito(); ridisegna()
14.     nota('Caricata la configurazione di R1.')
15. ev.target.value = ''         ← così ricaricare lo stesso file rifunziona
```

**Percorso d'errore, file JSON malformato:**

```
7.      JSON.parse(fr.result) → SyntaxError
        ↓ catturato dal try/catch DENTRO onload
8.      rifiuta(new Error('file non valido: Expected property name...'))
11. .catch(e => ...):
12.     nota('Caricamento fallito: file non valido: Expected property name
              or "}" in JSON at position 2 — la tabella attuale resta com\'era.')
```

**`this.router` non è mai stato toccato.** La riga 12 del percorso felice si trova dentro il
`.then()`, che non viene eseguito. Lo stato precedente sopravvive intatto.

Lo stesso vale per un file **sintatticamente valido ma semanticamente sbagliato**: versione
99, router mancante, o una rotta con `"999.1.1.1"`. In tutti i casi l'errore nasce dentro
`deserializza` o dentro un costruttore, viene catturato dallo stesso `try`, e la Promise
viene rifiutata prima che qualcosa venga sostituito.

---

# Parte VI — Verifiche eseguite

Non affermazioni ma risultati.

## 6.1 Test automatici

**129 asserzioni, tutte passate**, verificate in due ambienti distinti:

- **Nel browser**, aprendo `test.html`: intestazione verde, `Tutto verde: 129 asserzioni
  passate.`
- **Da riga di comando con Node**, concatenando gli stessi file di `test.html` ed eseguendoli
  in un contesto isolato: stesso risultato, `129 asserzioni passate`.

Il doppio ambiente non è un vezzo: è la **dimostrazione empirica** che lo strato logico non
dipende dal DOM (§ 2.6). Se una sola riga di `ip.js`, `rotta.js`, `tdi.js`, `iface.js`,
`pacchetto.js` o `router.js` toccasse `document`, l'esecuzione con Node fallirebbe.

## 6.2 Verifiche funzionali sull'interfaccia

Eseguite pilotando il browser, con la tabella d'esempio caricata.

| Verifica | Risultato osservato |
|---|---|
| Instradare `196.13.2.5` | Vince `196.13.2.0/24` via `196.13.1.2` (metrica 5). Alternative: 2, nell'ordine `196.13.5.2` (metrica 20) e la default. Tutte e 5 le righe valutate e mostrate col calcolo. |
| Instradare `196.13.1.9` | Vince la rete connessa `196.13.1.0/24` su eth0. 1 alternativa: la default. |
| Instradare `8.8.8.8` | Vince la default `0.0.0.0/0` via `196.13.1.254`. Nessuna alternativa. |
| Eliminare la default, poi instradare `8.8.8.8` | `scelta === null`, riquadro rosso, «Destinazione 8.8.8.8 irraggiungibile: il pacchetto viene scartato», con la spiegazione che manca una default route. |
| Inserire `192.168.1.77` con `/24` | Errore inline: *«la rete 192.168.1.77 ha bit accesi fuori dalla mask /24 — forse intendevi 192.168.1.0»*. Tabella invariata, campi conservati. |
| Inserire netmask `255.0.255.0` | Errore inline: *«netmask non contigua: 255.0.255.0»*. Tabella invariata. |
| Inserire una rotta identica a una esistente | Errore inline: *«rotta già presente: 196.13.2.0/24 via 196.13.1.2. Per una rotta di riserva serve un gateway diverso.»* |
| Inserire la stessa destinazione con gateway diverso | **Accettata**: è la rotta di riserva (§ 2.8). |
| Instradare `300.1.2.3` | Errore: *«Indirizzo non valido: ottetto fuori range 0-255 in "300.1.2.3"»*. Nessun esito mostrato. |
| Eliminare una riga | La tabella si aggiorna, la numerazione si ricompatta, l'evidenziazione precedente viene rimossa. |

## 6.3 Verifiche sulla persistenza

Eseguite invocando i **gestori reali** dell'applicazione — non funzioni scritte apposta per
il test — con un oggetto `File` costruito in memoria e passato all'`<input type="file">` vero.

| Verifica | Risultato osservato |
|---|---|
| Serializzazione | JSON con `"versione": 1`, indirizzi in notazione puntata, indentazione a 2 spazi |
| Caricamento di un file valido | 5 rotte ripristinate, messaggio *«Caricata la configurazione di R1.»* |
| Caricamento di un file JSON malformato | Messaggio *«Caricamento fallito: file non valido: Expected property name or '}' in JSON at position 2 — la tabella attuale resta com'era.»* e **5 rotte ancora presenti**: lo stato precedente è sopravvissuto |
| Esportazione | Ancora costruita con `href` di schema `blob:` e `download="router-R1.json"`; dopo il click **nessuna ancora residua nel documento** (la pulizia funziona) |

## 6.4 Verifiche sui vincoli

| Vincolo | Come è stato verificato | Esito |
|---|---|---|
| Nessun ES module | `grep -rE "^\s*(import\|export)\s" js/ test/` | Nessuna corrispondenza |
| Nessuna dipendenza esterna | Nessun `package.json`, nessun `node_modules`, nessun riferimento a CDN nell'HTML | Confermato |
| Console pulita | Ispezione dei messaggi di console dopo il flusso completo | Solo un 404 su `favicon.ico`, che è la richiesta automatica del browser per l'icona della scheda e non riguarda l'applicazione |
| Logica senza DOM | `grep -l "document\|window"` sui sei file di logica, **e** esecuzione dei test con Node, dove `document` non esiste | Nessuna corrispondenza; 129 asserzioni passate |
| Vista senza aritmetica IP | `grep -nE "[^&]&[^&]\|>>>\|<<"` sui tre file di vista | Una sola corrispondenza, esaminata: è il carattere `&` dentro una stringa di testo, non un operatore (§ 2.6) |

## 6.5 Un limite dichiarato

Le verifiche sull'interfaccia sono state eseguite servendo i file da `http://localhost`,
perché lo strumento di automazione del browser rifiuta il protocollo `file://`.

**Cosa questo copre e cosa no.** La differenza fra i due protocolli riguarda la *same-origin
policy* (§ 2.2), e l'unica funzionalità del programma che ne dipende è il caricamento degli
ES module — verificato assente con il `grep` di § 6.4, il che rimuove il rischio principale.
Resta un secondo punto teoricamente sensibile: il download tramite `URL.createObjectURL` con
origine opaca. Il meccanismo è stato verificato nella sua costruzione (l'ancora viene creata
con l'`href` giusto, il nome giusto, e viene rimossa dopo il click), ma non è stato osservato
un file effettivamente atterrare su disco con protocollo `file://`.

**Verifica consigliata prima della consegna:** aprire `index.html` con doppio click e premere
«Salva su file». Se il download non partisse, la soluzione è sostituire il `Blob` con un
URI `data:`, una modifica di due righe confinata dentro `Persistenza.esporta` e senza alcun
impatto architetturale.

---

# Parte VII — Evoluzione verso il multi-router

Risposta alla domanda della traccia: *«quali classi sarebbero necessarie? quali relazioni
esisterebbero tra esse?»*

## 7.1 Le classi da aggiungere

**`Rete`** — il grafo. Contiene `Router[]` e `Link[]`. Espone `invia(pkt)` che restituisce
l'elenco degli hop attraversati.

**`Link`** — un arco del grafo: collega **due `Iface`**. Eventualmente con banda, ritardo e
stato attivo/disattivo, per simulare i guasti.

**`Pacchetto`** — già presente, guadagna un uso reale del `ttl`.

## 7.2 Le relazioni

```
Rete   1 ──── *  Router      composizione
Rete   1 ──── *  Link        composizione
Link   2 ──── 2  Iface       associazione: un link unisce due interfacce
Router 1 ──── *  Iface       composizione — già presente
Router 1 ──── 1  Tdi         composizione — già presente
Tdi    1 ──── *  Rotta       composizione — già presente
Rotta  * ──── 1  Iface       interfaccia d'uscita, per nome — risolta dal Router
```

## 7.3 L'algoritmo di forwarding multi-hop

```
Rete.invia(pkt):
    corrente = il router che genera o riceve il pacchetto
    percorso = []

    finché pkt.ttl > 0:
        se una Iface di `corrente` è locale(pkt.dst):
            → consegnato, esci

        esito = corrente.inoltra(pkt)              ← IL CODICE DI OGGI
        se esito.scelta è null:
            → scartato, "destinazione irraggiungibile"

        ifaceUscita = corrente.iface(esito.scelta.iface)   ← IL METODO DI OGGI
        link = il Link che tocca ifaceUscita
        se link è giù oppure ifaceUscita.su è false:
            → prova esito.alternative in ordine        ← LE ALTERNATIVE DI OGGI
            → se nessuna è utilizzabile, scartato

        ifaceRemota = l'altro capo del link
        corrente = il Router che possiede ifaceRemota
        pkt.ttl--
        percorso.push(esito)                       ← LA SPIEGAZIONE DI OGGI

    → TTL esaurito: loop di instradamento, pacchetto scartato
```

## 7.4 Cosa cambia nelle classi esistenti: nulla

`Ip`, `Rotta`, `Tdi`, `Iface`, `Router` restano esattamente come sono. `Rete` e `Link` si
aggiungono **sopra**, e `Rete.invia` chiama in un ciclo lo stesso `Router.inoltra` già
scritto oggi.

Le quattro decisioni che rendono vera questa affermazione, e che sono state prese **prima**
di sapere se sarebbero servite:

| Decisione presa oggi | Cosa rende possibile domani |
|---|---|
| `Iface` esiste come classe, anche se scheletrica | `Link` collega due `Iface`, non due stringhe. Se non esistesse, andrebbe inventata e tutto ciò che la usa riscritto. |
| `Rotta.iface` è una **stringa** risolta da `Router.iface(nome)` | Il punto di risoluzione nome → oggetto è già scritto e collaudato. `Rotta` resta serializzabile e indipendente. |
| `Pacchetto` esiste con `ttl`, anche se inutilizzato | La firma `inoltra(pkt)` non cambia. Il TTL è già trasportato. |
| `cerca` restituisce **anche le alternative ordinate** | Il fallback su guasto del collegamento è già calcolato. Basta scorrere `esito.alternative`. |

E la persistenza: il formato attuale `{versione: 1, router: {...}}` diventerà
`{versione: 2, routers: [...], links: [...]}`, un superset. Un `if` sulla versione basta a
caricare entrambi (§ 2.7).

**È questa la verifica che la progettazione è corretta:** l'introduzione di `Rete`, `Link` e
del forwarding multi-hop non richiede di riscrivere la logica di instradamento, solo di
chiamarla dentro un ciclo. L'algoritmo LPM, la spiegazione, la conversione degli indirizzi —
tutto viene riutilizzato tale e quale a ogni salto.

---

# Appendice — Glossario

**AND bit a bit (`&`)** — Operatore che confronta due numeri bit per bit e restituisce 1 solo
dove entrambi hanno 1. Applicare una netmask a un indirizzo con l'AND azzera la parte host e
conserva la parte rete.

**CIDR** (*Classless Inter-Domain Routing*) — Notazione che scrive la netmask come numero di
bit del prefisso dopo una barra: `192.168.1.0/24` invece di `192.168.1.0` con
`255.255.255.0`. «Classless» perché supera la vecchia divisione in classi A, B, C.

**Complemento a due** — Il modo standard di rappresentare i numeri negativi in binario. Il bit
più significativo indica il segno. È la causa del problema descritto in § 2.3.1.

**DOM** (*Document Object Model*) — La rappresentazione ad oggetti di una pagina HTML,
manipolabile da JavaScript.

**Default route** — La rotta `0.0.0.0/0`, compatibile con qualunque indirizzo ma con prefisso
di lunghezza 0, quindi sempre ultima nel Longest Prefix Match. È la regola «per tutto il
resto».

**Delega degli eventi** — Registrare un solo ascoltatore su un elemento contenitore invece di
uno per ciascun figlio, sfruttando la propagazione degli eventi verso l'alto. Necessaria
quando i figli vengono ricreati di frequente.

**Floating static route** — Una rotta verso una destinazione già raggiungibile, con metrica
peggiore, che entra in funzione solo se la principale cade. È il meccanismo di fallback della
§ 2.8.

**Gateway** (*next hop*) — L'indirizzo del prossimo router a cui consegnare il pacchetto.
`0.0.0.0` significa che la rete è direttamente connessa e non serve alcun intermediario.

**Longest Prefix Match** — Il criterio di scelta fra più regole compatibili: vince quella con
il prefisso più lungo, cioè la più specifica.

**Metrica** — Il costo associato a una rotta. Serve come criterio di scelta a parità di
prefisso.

**Netmask** — Un valore a 32 bit fatto di 1 iniziali seguiti da 0, che separa la parte rete
dalla parte host di un indirizzo.

**Netmask contigua** — Una netmask ben formata, senza «buchi». `255.255.128.0` è contigua,
`255.0.255.0` no. Su una netmask non contigua il concetto di lunghezza del prefisso non è
definito.

**Prefisso (lunghezza del)** — Il numero di bit a 1 nella netmask. Misura la specificità di
una regola: più lungo, meno indirizzi copre.

**Promise** — Un oggetto JavaScript che rappresenta un valore che arriverà in futuro. Si usa
con `.then()` per il successo e `.catch()` per l'errore.

**Round-trip** — In un test, verificare che serializzare e poi deserializzare restituisca un
oggetto equivalente all'originale.

**Same-origin policy** — La regola di sicurezza dei browser che limita l'interazione fra
documenti di origini diverse. Con protocollo `file://` ogni documento ha origine opaca, il
che blocca gli ES module (§ 2.2).

**Sort stabile** — Un ordinamento che, in caso di parità, conserva l'ordine originale degli
elementi. `Array.prototype.sort` è stabile per specifica dal 2019.

**TDI** — Tabella di Instradamento, l'elenco delle regole con cui un router decide dove
mandare i pacchetti.

**Trie / Patricia trie** — Struttura ad albero in cui ogni livello corrisponde a un bit
dell'indirizzo. È ciò che usano i router reali per il Longest Prefix Match su centinaia di
migliaia di rotte. Scartata qui per le ragioni di § 2.4.

**TTL** (*Time To Live*) — Contatore nell'intestazione di un pacchetto IP, decrementato a ogni
salto. Quando arriva a zero il pacchetto viene scartato: è la protezione contro i loop di
instradamento.

**`uint32`** — Intero senza segno a 32 bit. La rappresentazione scelta per gli indirizzi IP
(§ 2.3).

**XSS** (*Cross-Site Scripting*) — Vulnerabilità che permette di iniettare codice eseguibile
in una pagina attraverso dati non filtrati. Nel progetto è prevenuta usando sempre
`textContent` e mai `innerHTML` (§ 3.14).


