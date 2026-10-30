# Ripasso — B1 (pp. 84–94) e B3 (pp. 123–144)

Ollari, *Corso di Sistemi e Reti* vol. 2, Zanichelli.
Sintesi per la verifica della seconda settimana di scuola.

> **Nota sul programma.** Gli esercizi di pag. 101–102 assegnati (es. 13–17)
> usano **distance vector** e **link state**, che stanno alle pp. 95–100, cioè
> **oltre** il limite di pag. 94 indicato dal prof. In fondo trovi un'appendice
> con l'essenziale per risolverli. Vale la pena chiedere se rientrano o no
> nella verifica.

---

# B1 — Il livello 3: Rete

## 1. Perché esiste il livello 3

In una LAN i nodi sono direttamente connessi; in una **rete magliata** (WAN)
no. Serve un meccanismo per trovare un **cammino valido** fra due stazioni
qualsiasi: è il compito del **livello 3 Rete (Network Layer)**.

| Sigla | Nome | Cosa fa |
|---|---|---|
| **ES** | *End System* — host, stazione | estremo della comunicazione, **non** implementa in modo sostanziale il livello 3 |
| **IS** | *Intermediate System* — router (o *switch* nelle reti CONS) | nodo intermedio con **almeno due interfacce fisiche** su reti diverse; è qui che vive il livello 3 |

Nel gergo TCP/IP: gli IS si chiamano **gateway**, gli ES **host**.

**Schema a livelli di una comunicazione WAN** — i router implementano solo
L1-L2-L3, gli host tutti e sette:

```
   A                                              M
 utente                                        utente
  L7 ─┐                                          ┌─ L7
  L6  │                                          │  L6
  L5  │                                          │  L5
  L4  │                                          │  L4
  L3 ─┤   R1 ── R2 ── R3 ── R4  (solo L1-L2-L3)  ├─ L3
  L2  │                                          │  L2
  L1 ─┘                                          └─ L1
```

Conseguenza importante: **il livello 3 isola i dettagli dell'hardware di rete e
li nasconde ai livelli superiori.** Gran parte del L3 e tutto ciò che sta sopra
è esclusivamente software.

**I 4 elementi base del livello 3**

1. l'apparato **router** e le sue porte di inoltro;
2. gli **indirizzi** contenuti nei pacchetti di livello 3;
3. la **TdI** (tabella di instradamento): i dati per decidere i cammini;
4. l'**algoritmo di instradamento**: le regole per creare e aggiornare la TdI.

**Ciclo di funzionamento su un IS:** ricevo il pacchetto → apro la PDU di L3 →
estraggo gli indirizzi L3 → avvio l'algoritmo di instradamento che aggiorna la
TdI → decido la porta di inoltro.

---

## 2. Routing e tabella di instradamento

La **TdI** è un insieme di righe. Campi principali:

| Campo | Significato |
|---|---|
| **Indirizzo** | destinazione, anche **gruppi** di indirizzi (così non serve una riga per host) |
| **Porta** | interfaccia su cui inoltrare |
| **costo** | metrica economica / di efficienza o velocità della linea |
| **hops** | quanti nodi intermedi attraversare prima della destinazione |

Possono esistere **più righe con lo stesso indirizzo** ma porta diversa: sono le
**alternative di instradamento** in caso di porta o linea guasta.
Criterio di scelta convenzionale: **prima il costo minore, poi gli hops minori**.

### Requisiti di un algoritmo di routing

| Requisito | Significato |
|---|---|
| **Robustezza / versatilità** | si adatta senza oneri alle variazioni di topologia |
| **Stabilità** | *converge*: trova un cammino in tempi ragionevoli; se la rete non cambia l'instradamento è immediato |
| **Equità** | non danneggia nodi particolari, anche a costo di usare cammini non ottimali |

### Obiettivi di ottimalità (spesso in contrasto fra loro)

* minimizzare il **ritardo medio** per pacchetto → punto di vista dell'**utente**;
* massimizzare l'**utilizzo della rete** → punto di vista del **gestore**;
* garantire un certo grado di **fault tolerance**.

> **Perché la TdI ideale non esiste.** Dovrebbe avere una riga per ogni host
> della rete, essere presente su ogni IS ed essere aggiornata **istantaneamente**
> a ogni modifica di topologia. Impossibile anche su reti piccole: da qui la
> necessità di algoritmi non deterministici.

---

## 3. I due approcci: CNLS e CONS

| | **CNLS** — *connectionless* | **CONS** — *connection oriented* |
|---|---|---|
| Tecnica | **routing by network address** | **label swapping** |
| IS detto | **router** | **switch** (*label switch*) |
| Cosa c'è nel pacchetto | indirizzi mittente/destinatario L3 | solo una **label** (identificativo del circuito virtuale) |
| Decisione di instradamento | **per ogni pacchetto**, su ogni IS | **una sola volta**, all'apertura della connessione |
| Struttura consultata | TdI (una riga per ogni possibile destinazione) | **look-up table** (una riga per circuito virtuale attivo) |
| Velocità | lenta: ricerca per chiave nella TdI | velocissima: **accesso indicizzato**, fattibile in hardware |
| Cammino dei pacchetti | può cambiare fra un pacchetto e l'altro | fisso: **circuito virtuale** |
| Fault tolerance | **alta** | **assente** (presume L2 affidabile) |
| Congestione | **alta** | bassa |
| Controllo errori L3 | **no**: demandato a L4, cioè agli ES | — |
| Reti reali | **TCP/IP** | **ATM**, **MPLS** |

### 3.1 Routing CNLS by network address

Il pacchetto di L3 resta **immutato** per tutto il percorso; la trama di L2
viene **riscritta a ogni tratta** per adattarsi alla nuova linea fisica.

```
 tratta LAN di A → R1 :   r1  a  │ A  M │ dati
 tratta R1 → R2      :   r2  r1 │ A  M │ dati
 tratta R2 → R3      :   r3  r2 │ A  M │ dati
 tratta R3 → R4      :   r4  r3 │ A  M │ dati
 tratta R4 → LAN di M:   m   r4 │ A  M │ dati
                        └─ L2 ─┘└─ L3 ─┘
```

Il perché del "non fidarsi": privilegiare le alternative di cammino significa
**non fidarsi dell'affidabilità delle infrastrutture di rete**, che appartengono
agli enti gestori. Il controllo dell'errore va quindi al **livello 4**, cioè sulle
macchine finali (ES) possedute da chi è proprietario della comunicazione.

### 3.2 Routing CONS: label swapping

Mittente e destinatario aprono **preventivamente** una connessione decidendo il
cammino. La ricerca del cammino usa gli stessi principi delle reti CNLS
(indirizzi L3 univoci + TdI); poi i pacchetti successivi contengono **solo la
label**.

Su ogni IS la coppia **(porta d'ingresso, label)** è già l'**indice esatto** per
recuperare dalla look-up table la coppia **(porta d'uscita, nuova label)**.
Il pacchetto subisce la modifica del campo label a ogni passaggio: da qui
*label swapping*.

```
Switch S
┌─────────┬─────────┐
│  input  │  output │
│  P    L │  P    L │
├─────────┼─────────┤
│  4    6 │  2    5 │   pacchetto entrato da P4 con label 6
│  4    7 │  3    1 │   → esce da P2 con label 5
└─────────┴─────────┘
```

**Vantaggi:** velocità, tabella piccola (tanti circuiti attivi, non tante
destinazioni possibili), realizzabile in hardware.
**Svantaggio:** se una tratta cade durante la sessione il circuito virtuale
salta: **nessuna tolleranza ai guasti di sessione**.

---

## 4. Classificazione degli algoritmi di instradamento

```
                    ┌── non adattativi (statici) ── FDR
                    │                            └─ Flooding
Algoritmi di ───────┤
instradamento       │                            ┌─ Routing centralizzato (RCC)
                    └── adattativi (dinamici) ────┼─ Routing isolato (backward learning)
                                                 └─ Routing distribuito ┬─ distance vector
                                                                        └─ link state packet
```

| Tipo | Criteri di instradamento |
|---|---|
| **non adattativi** (statici) | costanti, stabiliti a mano dal responsabile di rete o da algoritmi generali |
| **adattativi** (dinamici) | calcolati automaticamente in funzione di topologia, stato dei collegamenti e carico; monitorano la rete in tempo reale |

### 4.1 FDR — *Fixed Directory Routing* (non adattativo)

Ogni IS ha una TdI **scritta manualmente** con regole Indirizzo/Porta. Si possono
associare più linee a un destinatario per gestire un po' di fault tolerance. Le
regole fisse si chiamano **route statiche**.
Il sysadmin ha il **controllo totale** dei flussi di carico.

### 4.2 Flooding (non adattativo)

I pacchetti vengono ritrasmessi **su tutte le linee tranne quella d'arrivo**.
Nato in ambito militare: il pacchetto arriva **sempre** a destinazione, a
prescindere dal prezzo pagato dalla rete. È **garantito convergente**.

Difetti: genera **loop** e pacchetti duplicati su reti magliate, non ottimizza le
linee. Si mitiga con campi **age counter** nei pacchetti L3, aggiornati a ogni
transito per eliminare i pacchetti recidivi.
**Nella pratica non si usa quasi mai da solo, ma come supporto ad altri algoritmi.**

### 4.3 Routing centralizzato (adattativo)

Un IS speciale, l'**RCC** (*Routing Control Center*):
1. riceve informazioni sullo stato della rete;
2. calcola le TdI per **tutti** i router;
3. le distribuisce a tutti.

Ottimizza le prestazioni ma è **poco robusto**: se cade l'RCC o una sua linea,
la rete collassa. Accumula molto carico ⟹ deve essere una stazione potente.

### 4.4 Routing isolato / backward learning (adattativo)

Ogni IS decide la propria TdI **da solo**, in base al **solo traffico che lo
attraversa**. Simile alla gestione dei Bridge 802.1D (con Spanning Tree).

> **Regola del backward learning**
> se da una porta **P** giunge un pacchetto **proveniente** dall'host **A**,
> allora attraverso **P** si può raggiungere **A** ⟹ aggiungi in TdI
> `(address = A; porta = P)`.

Si impara **dal mittente**, non dal destinatario. Gestione eminentemente locale:
i pacchetti "stranieri" sono instradati con difficoltà. Anche il backward
learning è **usato spesso come supporto** ad altri algoritmi.

---

# B3 — Indirizzamento IP

## 5. Concetti di base

* Indirizzi IPv4: **32 bit** (4 byte), **big endian**, notazione **dotted**
  (`137.168.0.1`).
* **Non sono i nodi ad avere un indirizzo IP, ma le interfacce fisiche.**
  Un router con 3 interfacce ha 3 indirizzi IP. Parlare dell'«IP di un router»
  è sbagliato per definizione.
* Un indirizzo si divide in due parti significative:
  **netId** (*network prefix*, la rete) + **hostId** (*host number*, l'host).
* Ai numeri si associano gli **hostname**, definiti localmente nel file `hosts`
  o, su reti grandi, tramite **DNS** (base di dati distribuita).

**Chi assegna gli indirizzi** (RFC 2050):

```
ICANN ──► IANA ──► RIR (continentali, es. RIPE per l'Europa)
                    └─► enti nazionali ──► LIR (locali, ~600 in Italia) + ISP
```

---

## 6. Classful (RFC 760, 791, 1166)

Schema originale, **ufficialmente decaduto nel 1993** a favore di CIDR, ma
indispensabile per capire tutto il resto.

| Classe | Leading bit | 1° byte | netId | hostId | N. reti | Host per rete |
|---|---|---|---|---|---|---|
| **A** | `0` | 0 ÷ 127 | 7 bit | 24 bit | 2⁷ = 128 | 2²⁴ |
| **B** | `10` | 128 ÷ 191 | 14 bit | 16 bit | 2¹⁴ | 2¹⁶ |
| **C** | `110` | 192 ÷ 223 | 21 bit | 8 bit | 2²¹ | 2⁸ |
| **D** | `1110` | 224 ÷ 239 | — **multicast** (RFC 1112) | | | |
| **E** | `1111` | 240 ÷ 255 | — **riservati** per usi futuri | | | |

### Riconoscere la classe con le maschere di bit

|  | maschera | leading bit |
|---|---|---|
| A | `IPMASK_A = 10000000b = 0x80 = 128` | `IPCLASS_A = 00000000b = 0x00 = 0` |
| B | `IPMASK_B = 11000000b = 0xC0 = 192` | `IPCLASS_B = 10000000b = 0x80 = 128` |
| C | `IPMASK_C = 11100000b = 0xE0 = 224` | `IPCLASS_C = 11000000b = 0xC0 = 192` |

Test: `(primo_byte AND IPMASK_x) == IPCLASS_x`.

### Netmask di classe

| Classe | Netmask dotted | Esadecimale |
|---|---|---|
| A | `255.0.0.0` | `ff000000` |
| B | `255.255.0.0` | `ffff0000` |
| C | `255.255.255.0` | `ffffff00` |

**netId = indirizzo AND netmask.**
Due indirizzi stanno sulla **stessa rete** ⟺ hanno lo **stesso netId**.

> **Esempio del libro (p.125–126).**
> `137.168.0.1` → 137 sta fra 128 e 191 ⟹ classe **B** ⟹ netmask `ffff0000`
> ⟹ netId = `89A80001 AND FFFF0000` = `89A80000` = `137.168.0.0`.
> `137.168.249.17` → stesso netId `89A80000` ⟹ **stessa rete**.
> *(Scorciatoia: la classe B ha 2 byte a 255, quindi il netId sono i primi 2 byte.)*

Vedi il programma `porting_python/b3_p126_classful_netid.py`.

---

## 7. Instradamento classful

**Le due regole implicite:**

1. netId destinazione **uguale** al netId di una propria interfaccia
   ⟹ **consegna diretta**: inoltro sulla stessa interfaccia (MAC del
   destinatario recuperato con ARP);
2. netId destinazione **diverso** da quello di ogni propria interfaccia
   ⟹ **consegna indiretta**: inoltro al **gateway di default** (*next hop*).

Quindi i **due parametri fondamentali** di un host per il routing classful sono
la **netmask** della propria rete e l'**IP del gateway di default**.

### La TdI di un host

| Indirizzo | Mask | Gateway | Interfaccia |
|---|---|---|---|
| `0.0.0.0` | `0.0.0.0` | `196.13.1.254` | `196.13.1.1` |
| `196.13.1.0` | `255.255.255.0` | `196.13.1.1` | `196.13.1.1` |

**Come si valuta una riga** — per l'indirizzo destinazione `D`:

```
(D AND Mask_riga) == Indirizzo_riga   ⟹   la regola è VERA
```

Regole d'oro:

* la riga con `Mask = 0.0.0.0` è **sempre vera** per qualunque indirizzo:
  è la **regola dei «pacchetti stranieri»** o **«dell'ultima opportunità»**
  (la *default route*);
* se **più regole sono vere**, si sceglie quella con **più bit a 1 nella Mask**
  (⟹ *longest prefix match*).

> Esempio: destinazione `196.13.1.2`.
> Riga 1: `196.13.1.2 AND 0.0.0.0 = 0.0.0.0` = Indirizzo ⟹ vera.
> Riga 2: `196.13.1.2 AND 255.255.255.0 = 196.13.1.0` = Indirizzo ⟹ vera.
> Vince la riga 2 (mask più lunga) ⟹ **consegna diretta**.
>
> Destinazione `196.13.2.5`: riga 1 vera, riga 2 falsa
> (`196.13.2.0 ≠ 196.13.1.0`) ⟹ **consegna indiretta** via gateway.

Vedi `porting_python/b3_p129_instradamento_classful.py`.

### 7.1 Perché classful è fallito

Spazio totale IPv4 = 2³² = 4.294.967.296 indirizzi. La gerarchia classful è
**troppo rigida**:

* **spreco interno**: ogni sottorete dell'organizzazione non sfrutta tutti i
  numeri di rete acquistati;
* **blocchi sovradimensionati**: caso tipico della classe B — molte
  organizzazioni hanno più di 256 macchine (classe C) ma molte meno di 65 536;
* **classi A troppo grandi**: 2²⁴ = 16 777 216 indirizzi ciascuna; a oggi ne sono
  state assegnate ~60, l'ultima nel 2010;
* **TdI degli ISP inutilmente ampie** (tante classi C contigue = tante righe).

Dal 1993 l'IETF introduce **CIDR** (*Classless Inter-Domain Routing*, RFC 1519).
Gli indirizzi IPv4 si sono **effettivamente esauriti il 3 febbraio 2011**.

| Tecnica | Problema che risolve |
|---|---|
| **Subnetting** (+ reti private) | lo spreco **all'interno** delle organizzazioni |
| **Supernetting / CIDR** | lo spreco dovuto alla **rigidità delle classi** |

---

## 8. Subnetting (RFC 950)

Suddividere una rete classful in più **sottoreti fisiche** all'interno di una
stessa organizzazione. Diventa molto efficace applicato alle **reti private**
(*Private Internets*, RFC 1918).

| Range IPv4 | Netmask | N. indirizzi | Equivalente classful |
|---|---|---|---|
| `10.0.0.0 ÷ 10.255.255.255` | `255.0.0.0` (/8) | 2²⁴ = 16 777 216 | 1 rete di classe A |
| `172.16.0.0 ÷ 172.31.255.255` | `255.255.0.0` (/16) | 2²⁰ = 1 048 576 | 16 reti di classe B contigue |
| `192.168.0.0 ÷ 192.168.255.255` | `255.255.255.0` (/24) | 2¹⁶ = 65 536 | 256 reti di classe C contigue |

> Paradosso apparente: milioni di macchine in Internet hanno lo **stesso**
> indirizzo IP (es. `192.168.0.1`). Escono verso Internet tramite router con
> un'interfaccia sulla rete privata e una sulla pubblica (NAT). Le reti private
> hanno introdotto il concetto di **intranet**.

### La subnet mask

Un valore analogo alla netmask, ma con **più «uni» consecutivi**: ricopre tutto
il netId **e parte dell'hostId**. L'indirizzo si divide così in **tre** parti:

```
                       netmask
        11111111 11111111 00000000 00000000
classful   │  netId   │        hostId       │
subnetting │  netId   │ subnetId │  hostId  │
        11111111 11111111 111111 0000000000
                              subnet mask
```

Con il subnetting **il meccanismo di routing implicito di classful resta
invariato**: l'unica differenza è che ogni host va configurato con la **subnet
mask** invece della sola netmask di classe.

### Procedura di progetto (metodo da usare alla verifica)

1. **Somma gli host** richiesti e conta le **sottoreti** necessarie.
2. **Scegli il lotto privato** più piccolo che basta.
3. **Bit di subnetId**: il più piccolo `s` con `2^s ≥ n_sottoreti`.
4. **Bit di hostId**: `h = bit_liberi − s`. Verifica che `2^h ≥ host_max`
   (anzi `2^h − 2`, vedi sotto).
5. **Subnet mask** = `netmasklen + s` bit a 1.
6. Elenca le sottoreti: la *i*-esima ha indirizzo `netId + (i << h)`.

> **Esempio guida (p.132–134).** 3 gruppi da 50, 30 e 20 host ⟹ 100 host,
> 3 sottoreti. Basta un lotto di classe C ⟹ `192.168.0.0` netmask `/24`,
> restano 8 bit. Servono 3 sottoreti: `2¹ < 3 ≤ 2²` ⟹ **s = 2 bit**
> (4 sottoreti: `00`, `01`, `10`, `11`). Restano `8 − 2 = 6` bit ⟹ 2⁶ = 64
> host teorici per sottorete ≥ 50 ✔.
> **Subnet mask = /26 = `255.255.255.192`** (`11111111.11111111.11111111.11000000`).

| Subnet | subnetId | Nome (rete) | Broadcast | Indirizzi assegnabili |
|---|---|---|---|---|
| A | `00` | `192.168.0.0` | `192.168.0.63` | `.1 ÷ .62` |
| B | `01` | `192.168.0.64` | `192.168.0.127` | `.65 ÷ .126` |
| C | `10` | `192.168.0.128` | `192.168.0.191` | `.129 ÷ .190` |
| D | `11` | `192.168.0.192` | `192.168.0.255` | `.193 ÷ .254` (inutilizzata) |

> ⚠️ **Refuso del libro (p.137).** Per la subnet A il testo scrive
> «indirizzi disponibili: 192.168.0.1 ÷ 192.168.0.**64**». È sbagliato:
> `.63` è il broadcast e `.64` appartiene già alla subnet B.
> Il range corretto è **`.1 ÷ .62`**. (Coerente col resto del libro, che mette
> il router R a `192.168.0.62`.)

Vedi `porting_python/b3_p134_subnetting.py`.

---

## 9. Instradamento con subnetting: gli indirizzi speciali (RFC 1009)

Notazione: `{netId, hostId}` in classful, `{netId, subnetId, hostId}` in
subnetting. `0` = tutti i bit a zero, `-1` = tutti i bit a uno.

| # | Forma | Nome | Uso |
|---|---|---|---|
| a | `{0, 0}` | *This host on this network* (`0.0.0.0`) | **sorgente**: host che non ha ancora un IP |
| b | `{0, hostId}` | *Specified host on this network* | **sorgente**: host preciso su rete indeterminata |
| c | `{-1, -1}` | *Limited broadcast* (`255.255.255.255`) | **destinazione**: tutti gli host della propria rete/subnet, mai altre |
| d | `{netId, -1}` | *Directed broadcast to specified network* | **destinazione**: tutti gli host della rete classful indicata |
| e | `{netId, subnetId, -1}` | *Directed broadcast to specified subnet* | **destinazione**: tutti gli host di quella subnet |
| f | `{netId, -1, -1}` | *Directed broadcast to all subnets* | **destinazione**: tutti gli host di tutte le subnet della rete |
| g | `{127, any}` | *Internal host loopback* (`127.0.0.1`, `localhost`) | sorgente o destinazione, **non passa sulla rete fisica** |
| h | `{netId, 0}` | *Specified network* | **non assegnabile**: indica la rete |
| i | `{netId, subnetId, 0}` | *Specified subnet* | **non assegnabile**: indica la subnet |

**Conseguenza pratica (chiave d'esame):** in ogni subnet **due indirizzi sono
persi** — il **nome della subnet** (tutti zero nell'hostId) e il **broadcast
diretto** (tutti uno). Perciò gli host disponibili sono **2^h − 2**.

> Nella subnet `192.168.0.0/26`: `192.168.0.0` (nome) e `192.168.0.63`
> (broadcast) **non** sono assegnabili ⟹ restano 62 host.

### TdI complete (esempio p.137–138)

**TdI dell'host A1 (`192.168.0.1`, subnet mask `/26`, gateway `192.168.0.62`)**

| Indirizzo | Mask | Gateway | Interfaccia | Metrica | Significato |
|---|---|---|---|---|---|
| `0.0.0.0` | `0.0.0.0` | `192.168.0.62` | `192.168.0.1` | 1 | pacchetti stranieri |
| `127.0.0.0` | `255.0.0.0` | `127.0.0.1` | `127.0.0.1` | 1 | loopback |
| `192.168.0.0` | `255.255.255.192` | `192.168.0.1` | `192.168.0.1` | 1 | rete di provenienza |
| `192.168.0.1` | `255.255.255.255` | `127.0.0.1` | `127.0.0.1` | 1 | sé stesso (host) |
| `192.168.0.63` | `255.255.255.255` | `192.168.0.1` | `192.168.0.1` | 1 | broadcast sulla propria rete |
| `224.0.0.0` | `224.0.0.0` | `192.168.0.1` | `192.168.0.1` | 1 | multicast |
| `255.255.255.255` | `255.255.255.255` | `192.168.0.1` | `192.168.0.1` | 1 | broadcast limitato |

**Il router R** ha le stesse categorie di righe, ma **ripetute per ognuna delle
sue tre interfacce** (`192.168.0.62`, `.126`, `.190`), e la riga di default ha
gateway e interfaccia **nulli** (non ha un default gateway proprio).

Forma compatta stile Linux (`route -n`):

| Destination | Genmask | Gateway | Flags | Iface |
|---|---|---|---|---|
| `192.168.0.0` | `255.255.255.192` | `192.168.0.62` | U | eth0 |
| `192.168.0.64` | `255.255.255.192` | `192.168.0.126` | U | eth1 |
| `192.168.0.128` | `255.255.255.192` | `192.168.0.190` | U | eth2 |

---

## 10. Internetwork e VLSM

Su una rete con più LAN **e** più link punto-punto fra router, si assegna una
subnet **anche a ogni link**. Esempio del libro: lotto `172.16.0.0/16`,
subnet mask `/20` ⟹ subnetId = 4 bit ⟹ **16 sottoreti** da
`2¹² − 2 = 4094` host ciascuna.

| Subnet | subnetId | Nome | Broadcast | Uso |
|---|---|---|---|---|
| LAN A | `0000` | `172.16.0.0` | `172.16.15.255` | LAN |
| LAN B | `0001` | `172.16.16.0` | `172.16.31.255` | LAN |
| LAN C | `0010` | `172.16.32.0` | `172.16.47.255` | LAN |
| LAN D | `0011` | `172.16.48.0` | `172.16.63.255` | LAN |
| R1-R2 | `1100` | `172.16.192.0` | `172.16.207.255` | link |
| R2-R3 | `1101` | `172.16.208.0` | `172.16.223.255` | link |
| R3-R4 | `1110` | `172.16.224.0` | `172.16.239.255` | link |
| R3-R5 | `1111` | `172.16.240.0` | `172.16.255.255` | link |

Regola per scrivere la TdI di un router: **una riga per ogni subnet della rete**;
nella colonna Mask sempre la stessa subnet mask; le subnet **direttamente
connesse** hanno consegna diretta (gateway vuoto / *On-link*).

**VLSM** (*Variable Length Subnet Masks*, RFC 1009): in origine il subnetting
imponeva **una sola subnet mask** per tutta la rete. VLSM abolisce il vincolo e
consente una distribuzione più razionale degli indirizzi.

### Il programma `route`

Presente sia su Windows che su Linux, gestisce la TdI del nodo.

| Azione | Windows | Linux |
|---|---|---|
| Visualizzare | `route print` (utile `route print > tdi.txt`) | `route -n` |
| Aggiungere | `route add 10.0.0.0 mask 255.0.0.0 192.168.0.1` | `route add -net 10.0.0.0 netmask 255.0.0.0 gw 192.168.0.1` |
| Eliminare | `route delete 10.0.0.0` | `route del -net 10.0.0.0 netmask 255.0.0.0 gw 192.168.0.1` |

L'ultimo parametro è sempre il **gateway**. Su Windows la regola si perde al
riavvio: per renderla persistente serve `-p`.

---

## 11. Supernetting / CIDR (RFC 1519)

Il problema opposto al subnetting: invece di **spezzare** una rete, si
**aggregano** più reti classful contigue in un'unica rete logica.

**Cosa dice il CIDR:**

1. la **metà superiore della classe A** (64 ÷ 127) è riservata;
2. gli indirizzi di **classe B** si assegnano solo se la rete ha ≥ 32 sottoreti
   **e** oltre 4096 host complessivi;
3. gli indirizzi della **metà inferiore della classe C** si assegnano a **blocchi
   contigui** in base alla localizzazione geografica;
4. la **metà superiore della classe C** (208.0.0 ÷ 223.255.255) **non** è
   assegnata.

Il punto 3 è quello che rende possibile il supernetting: un ISP può aggregare
*n* reti di classe C contigue e cederle come **un unico blocco** rappresentante
un'unica rete fisica.

**Notazione CIDR `a.b.c.d/n`**: i primi `n` bit sono il netId.

> `192.192.0.0/22` ⟹ `24 − 22 = 2` bit liberi ⟹ aggrega `2² = 4` reti di
> classe C: `192.192.0.x`, `192.192.1.x`, `192.192.2.x`, `192.192.3.x`.

**La stessa notazione si usa anche per il subnetting**: `192.168.0.0` con subnet
mask `255.255.255.192` si scrive `192.168.0.0/26`.

### Metodo del dimezzamento successivo (esempio p.143–144)

Blocco `210.1.8.0/21` (2¹¹ = **2048** indirizzi, cioè 8 reti di classe C:
`210.1.8.0` ÷ `210.1.15.0`). Richieste: A = 1000, B = 500, C = 200, D = 100.

Si procede **dalla richiesta più grande**, dimezzando ogni volta:

| Passo | Blocco da dividere | Assegnato | Resto |
|---|---|---|---|
| 1 | 2048 (`/21`) | **A → `210.1.8.0/22`** (1024) | 1024 (`/22`) |
| 2 | 1024 | **B → `210.1.12.0/23`** (512) | 512 (`/23`) |
| 3 | 512 | **C → `210.1.14.0/24`** (256) | 256 (`/24`) |
| 4 | — | **D → `210.1.15.0/24`** (256) | — |

**Risultato: 4 sole maschere** nelle TdI dell'ISP —
`/22` (A), `/23` (B), `/24` (C), `/24` (D).
Ogni dimezzamento = **un bit in più** nella maschera.

---

# Appendice — Distance vector e link state (pp. 95–100)

Serve per gli **esercizi 13–17**, ma è fuori dal limite di pag. 94.

## Routing distribuito

Gli IS **cooperano** scambiandosi periodicamente informazioni di servizio
(*neighbor greetings*). Unisce l'ottimizzazione del routing centralizzato con
l'efficienza locale del routing isolato. Due famiglie:

| | **Distance vector** | **Link state packet** |
|---|---|---|
| Anche detto | Bellman-Ford | — |
| Dimensione rete | medio-piccole (fino a ~1000 nodi) | ampie (migliaia di nodi) |
| Complessità | relativamente semplice | relativamente complesso |
| Cosa si scambia | **DV**: triple `indirizzo-hops-costo` (senza la porta) ai **soli router adiacenti** | **LSP**: elenco dei propri vicini + costo, in **flooding a tutta la rete** |
| Cosa conosce ogni router | solo le distanze riferite dai vicini — **nessun router ha la mappa della rete** | la **topologia completa** (LSPdbase identico ovunque) |
| Calcolo | aggiornamento incrementale | **Dijkstra** sul grafo |
| Difetti | loop di routing, *count to infinity*, non deterministico | più pesante da calcolare |

## Distance vector in pratica

* Il **DV** deriva dalla TdI togliendo la colonna della porta. La porta si
  ricava comunque: è **quella da cui il DV è stato ricevuto**.
* Un router **ricalcola** la TdI se: cade una linea attiva · scopre un nuovo IS ·
  viene eliminato un IS · **riceve un DV diverso** da quello memorizzato.
* Se due DV sulla stessa porta contengono la stessa destinazione:
  si sceglie in base al **costo** e, a parità di costo, al **minor numero di hops**.
* Quando la TdI cambia, il router invia un DV a **tutti i suoi adiacenti** ⟹
  propagazione a catena, che però si esaurisce rapidamente (**convergenza**).
* **Route poisoning**: quando un router scopre che una sua tratta è guasta
  (*link down*), lo segnala ai vicini inviando quella rotta con **metrica infinita**.

**Le tre azioni alla ricezione di un pacchetto** (modello dell'ESEMPIO di p.96,
dove a R0 arriva su P1 il pacchetto `Z;C;3;15`):

1. il router **impara** `Mitt │ porta d'ingresso │ h │ c` con `h` e `c` presi
   così come sono dal pacchetto → R0 inserisce `Z, 1, 3, 15`;
2. **inoltra** il pacchetto verso `Dest` consultando la propria TdI;
3. **invia un DV** `(Mitt, h, c)` a **tutti** i router adiacenti — non solo a
   quello sul cammino del pacchetto.

**Regola di propagazione** — il vicino `R'` che riceve il DV sulla porta `P'`
inserisce `Mitt │ P' │ h+1 │ c + costo(link)`.
Nell'esempio del libro R1 e R2 aggiungono `Z,3,4,22` e `Z,1,4,22`:
`h` da 3 a **4**, `c` da 15 a **22 = 15 + 7**.
La catena continua finché nessun router migliora più: è la **convergenza**.

> ⚠️ Non confondere con il **backward learning** (p.94): là si impara *solo*
> la porta, *solo* sui router che il pacchetto attraversa, e non si propaga
> niente ai vicini.

**Come si ricavano i costi mancanti** (es. 13 e 15): una riga con `h = 1` ha
`c` = costo della sola linea verso il vicino; una riga con `h = 2` ha `c` = somma
di due linee. Si mette a sistema.

## Link state in pratica

1. Ogni router genera il proprio **LSP**: elenco dei **vicini diretti** con il
   costo della linea. È l'unica cosa che conosce di prima mano.
2. Gli LSP vengono diffusi in **flooding** a tutta la rete.
3. Ogni router costruisce il **LSPdbase**: l'insieme di **tutti** gli LSP —
   identico su ogni router, è la mappa completa della rete.
4. Ogni router applica **Dijkstra** sul LSPdbase e ricava la propria TdI:
   per ogni destinazione, prima porta del cammino minimo + hops + costo.

**Vantaggio decisivo:** ogni router calcola da sé l'albero dei cammini minimi
sulla topologia completa ⟹ convergenza rapida e nessun *count to infinity*.

---

# Checklist rapida pre-verifica

**B1**

- [ ] Differenza ES / IS; perché gli ES non implementano il L3
- [ ] I 4 elementi base del L3
- [ ] Campi della TdI e criterio costo-prima-poi-hops
- [ ] Robustezza / stabilità / equità + i 3 obiettivi di ottimalità
- [ ] Tabella comparativa CNLS vs CONS (a memoria)
- [ ] Saper scrivere le intestazioni L2/L3 tratta per tratta
- [ ] Saper compilare una look-up table per un circuito virtuale
- [ ] I 4 algoritmi: FDR, flooding, centralizzato, isolato — pro e contro
- [ ] La regola del backward learning, testuale

**B3**

- [ ] Le 5 classi con leading bit, range del 1° byte, netId/hostId
- [ ] Maschere e leading bit per il test di classe
- [ ] Calcolo del netId con AND; «stessa rete» ⟺ stesso netId
- [ ] Le 2 regole dell'instradamento classful (diretta / indiretta)
- [ ] Valutazione di una riga di TdI + longest prefix match + regola dei pacchetti stranieri
- [ ] I 3 lotti privati RFC 1918 con netmask e numero di indirizzi
- [ ] Procedura completa di progetto di un subnetting
- [ ] I 9 indirizzi speciali RFC 1009 — soprattutto perché si perdono 2 indirizzi per subnet
- [ ] Notazione CIDR `/n` e metodo del dimezzamento successivo per il supernetting
- [ ] Comandi `route` su Windows e Linux
