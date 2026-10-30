# Guida al porting C → Python

Analisi riga per riga dei 5 programmi dei capitoli B1 e B3, con la motivazione
di ogni scelta di traduzione. L'obiettivo è che tu sappia **rispondere a voce**
a domande del tipo *«perché qui hai usato una lista invece di un array?»* o
*«cosa faceva `sizeof` e perché in Python non serve?»*.

Ordine di lettura consigliato: prima la **Parte 0** (i concetti che tornano in
tutti e cinque i programmi), poi i programmi uno per uno.

---

# PARTE 0 — Le 10 differenze che tornano sempre

Queste sono le idee di fondo. Se hai chiare queste, il porting di qualsiasi
programma del libro diventa meccanico.

## 0.1 Tipizzazione: dichiarata vs dedotta

```c
int i, rm, rd, r, ok, n = 0;
unsigned char p;
char chS, chD;
```

In C ogni variabile va **dichiarata** con il suo tipo prima di usarla, perché il
compilatore deve sapere **quanti byte** riservarle e come interpretarli.
`unsigned char` = 1 byte senza segno (0÷255), `int` = tipicamente 4 byte con
segno, `char` = 1 byte che il compilatore tratta come carattere.

In Python non dichiari niente: il tipo sta **nel valore**, non nel nome.

```python
n = 0          # ora n è un intero
n = "ciao"     # ...e ora è una stringa: legale, il nome non ha tipo
```

**Come lo spieghi:** «in C il tipo è una proprietà della variabile e serve al
compilatore per allocare la memoria; in Python è una proprietà dell'oggetto e
viene gestito a runtime, quindi le dichiarazioni spariscono».

**Conseguenza pratica sul nostro codice:** tutte le righe di dichiarazione
(righe 13-14 del programma 1, 25-27 del programma 2, ecc.) **non si traducono
affatto**: semplicemente non esistono nel porting.

## 0.2 `struct` → tupla, dizionario o classe

```c
typedef struct {
  char ra[3];
  char rb[3];
  unsigned char p;
} LINK;
```

Una `struct` è un **record**: un blocco di memoria con più campi di tipo diverso,
raggiungibili per nome. `typedef` gli dà un nome di tipo (`LINK`) così puoi
scrivere `LINK x;` invece di `struct {...} x;`.

In Python hai tre alternative:

| Scelta | Quando usarla | Costo |
|---|---|---|
| **tupla** `("R1","R2",2)` | record piccolo, immutabile, sempre letto per intero | leggerissima, ma i campi si accedono per indice |
| **dizionario** `{"ra":"R1", ...}` | record letto per nome, campi che cambiano | più verboso, accesso per chiave |
| **classe / `dataclass`** | record complesso con metodi | il più leggibile, il più lungo da scrivere |

**Nei nostri porting ho scelto la tupla** per `LINK`, `TDI`, `CLASSFUL`,
`PRIVATEIP`, perché sono tutti record di 3-4 campi che vengono **solo letti** e
sempre tutti insieme. Il vantaggio è che Python permette lo **spacchettamento**:

```c
/* C: accesso per nome, un campo alla volta */
if (linkrouter[i].ra[1] == rm + '0') { ... linkrouter[i].rb[1] ... }
```
```python
# Python: spacchetto i tre campi in un colpo solo dentro il for
for i, (ra, rb, p) in enumerate(LINKROUTER):
    if int(ra[1]) == rm: ...
```

**Come lo spieghi:** «la struct del C è un record a campi fissi; in Python la
rendo una tupla perché i dati sono costanti e li leggo sempre tutti insieme,
e lo spacchettamento mi dà nomi leggibili senza dover scrivere `linkrouter[i].ra`
ogni volta».

## 0.3 Array di struct → lista di tuple

```c
LINK linkrouter[] = {{"R1","R2",2},{"R2","R1",4}, ...};
```

Un array C è un **blocco contiguo di memoria** di dimensione fissa, decisa a
compile time. Una lista Python è un contenitore **dinamico** (puoi fare
`append`), eterogeneo, e sotto sotto è un array di puntatori a oggetti.

La sintassi è quasi identica — cambiano solo le parentesi:

```python
LINKROUTER = [("R1","R2",2), ("R2","R1",4), ...]
```

Ho scritto il nome **tutto in maiuscolo** perché in Python è la convenzione
(PEP 8) per le **costanti a livello di modulo**: segnala che è la descrizione
fissa della topologia, non una variabile di lavoro.

## 0.4 `sizeof(v)/sizeof(T)` → `len(lista)`

Questo è il punto in cui il libro sbaglia due volte, quindi va capito bene.

In C **l'array non conosce la propria lunghezza**. Il trucco standard per
contare gli elementi è:

```c
sizeof(linkrouter) / sizeof(LINK)
```

cioè *byte totali dell'array ÷ byte di un elemento*. Con 6 elementi da 8 byte
l'uno: `48 / 8 = 6`. ✔

Ma funziona **solo se `sizeof` vede l'array vero**. Se la variabile è un
**puntatore**, `sizeof` restituisce la dimensione del puntatore (4 o 8 byte),
non dell'array — ed è esattamente il bug del programma 2:

```c
TDI* tdi;                      /* puntatore! */
for (i=0; i<sizeof(tdi); i++)  /* = 4 o 8, non 3 */
```

In Python la lista **sa quanto è lunga**, quindi `len(LINKROUTER)` è sempre
corretto e l'intera classe di bug sparisce. Meglio ancora: quasi sempre non
serve nemmeno l'indice, basta iterare direttamente sugli elementi.

```python
for ra, rb, p in LINKROUTER:   # niente indici, niente lunghezze
```

**Come lo spieghi:** «in C l'array è memoria nuda e la lunghezza va ricalcolata
con `sizeof`; se per strada l'array degrada a puntatore il conto salta.
In Python la lista è un oggetto che si porta dietro la propria lunghezza,
quindi `len()` non può sbagliare».

## 0.5 Puntatori, `malloc` e `free` → niente

```c
TDI* tdi;
tdi = malloc(sizeof(tdiR1));
memcpy(tdi, tdiR1, sizeof(tdiR1));
...
if (tdi) free(tdi);
```

In C la memoria dinamica la gestisci a mano: `malloc` la chiede al sistema,
`free` la restituisce. Se dimentichi `free` hai un *memory leak*; se usi la
memoria dopo `free` hai un *dangling pointer*.

In Python **non esiste `malloc`**: ogni oggetto è allocato automaticamente e il
**garbage collector** lo libera quando nessuno lo riferisce più. Tutte le
variabili sono già riferimenti a oggetti.

Nel programma 2 le tre righe `malloc`+`memcpy`+`free` **non traducono niente**,
perché copiavano una tabella costante in memoria dinamica per poi leggerla e
buttarla. In Python la tabella si legge e basta.

**Come lo spieghi:** «erano tre righe per fare una copia di lavoro di una
tabella che non viene mai modificata: in C serviva perché il codice usa un
puntatore unico `tdi` che punta a tabelle diverse a ogni giro; in Python quel
puntatore diventa semplicemente il risultato di una ricerca in un dizionario».

## 0.6 Aritmetica sui caratteri (`- '0'` e `+ '0'`)

Questa è la conversione che compare in **tutti e due** i programmi di B1 e va
saputa a memoria.

In C un `char` **è un numero**: il suo codice ASCII. Il carattere `'0'` vale 48,
`'1'` vale 49, e così via fino a `'9'` = 57. Quindi:

```c
rm = chS - '0';        /* da carattere a numero:  '3' (51) - '0' (48) = 3   */
sprintf(pc, "R%c", rm + '0');   /* da numero a carattere: 3 + 48 = 51 = '3' */
```

In Python `str` e `int` sono **tipi diversi** e non si sommano. Le conversioni
sono esplicite e si leggono:

```python
rm = int(chS)          # '3'  ->  3
f"R{rm}"               #  3   -> "R3"
```

Attenzione al caso più subdolo, che compare in `linkrouter[i].ra[1]`:

```c
char ra[3];   /* "R1" occupa 3 byte: 'R', '1', '\0' */
ra[1]         /* è il CARATTERE '1', cioè il numero 49 */
ra[1] == rm + '0'   /* confronta due caratteri */
```
```python
ra = "R1"
ra[1]          # è la stringa "1"
int(ra[1]) == rm    # confronto fra due interi
```

**Come lo spieghi:** «`- '0'` e `+ '0'` sono il modo del C di convertire fra
cifra-carattere e cifra-numero sfruttando il fatto che i codici ASCII delle
cifre sono consecutivi; in Python diventano `int()` e f-string».

Nota anche `char ra[3]` per contenere `"R1"`: in C **ogni stringa ha un byte in
più** per il terminatore `'\0'`, che segna la fine. In Python la `str` conosce la
propria lunghezza, quindi `"R1"` occupa esattamente due caratteri.

## 0.7 `printf` → f-string

`printf` usa **segnaposto** (`%d`, `%c`, `%s`, `%x`) e prende i valori come
argomenti successivi. La f-string mette il valore **dentro** la stringa.

| C | Python | Significato |
|---|---|---|
| `printf("%d", n)` | `f"{n}"` | intero decimale |
| `printf("%3d", n)` | `f"{n:3d}"` | intero allineato a destra su 3 colonne |
| `printf("%c", ch)` | `f"{ch}"` | carattere |
| `printf("%s", s)` | `f"{s}"` | stringa |
| `printf("%x", v)` | `f"{v:x}"` | esadecimale minuscolo |
| `printf("%X", v)` | `f"{v:X}"` | esadecimale maiuscolo |
| `printf("%08X", v)` | `f"{v:08X}"` | esadecimale su 8 cifre con zeri davanti |
| `printf("\n...")` | `print()` va già a capo | il `\n` iniziale del C serve perché `printf` **non** va a capo da solo |

Questa è la differenza da citare: **`printf` non manda a capo, `print` sì.**
Ecco perché il codice del libro è pieno di `"\n..."` all'inizio delle stringhe.
Nel porting quei `\n` spariscono, perché `print()` aggiunge già il ritorno a capo.

## 0.8 Stringhe costruite a mano → lista + `join`

```c
char szHops[100], *pc;
int n = 0;
szHops[0] = 0;              /* stringa vuota: primo byte = terminatore */
pc = szHops;
n = n + sprintf(pc+n, "R%c ", rm + '0');   /* accoda e aggiorna l'offset */
```

Questo è il modo C di **accodare** a una stringa. `sprintf` scrive in memoria e
**restituisce quanti caratteri ha scritto**, così `n` tiene la posizione in cui
scrivere la volta dopo. `pc+n` è aritmetica dei puntatori: «l'indirizzo di
`szHops` spostato di `n` byte».

Serve tutta questa fatica perché in C **le stringhe sono array di byte di
dimensione fissa** (qui 100) e concatenare significa copiare byte a mano.

In Python le stringhe sono **immutabili**: concatenare in un ciclo con `+=`
creerebbe una nuova stringa ogni volta. Il modo idiomatico è accumulare i pezzi
in una **lista** e unirli alla fine:

```python
hops = [rm]              # accumulo i pezzi
hops.append(rm)          # ...
" ".join(f"R{x}" for x in hops)   # ...e li unisco solo quando servono
```

**Bonus:** nel programma 1 il buffer da 100 byte non è solo una scelta tecnica,
è anche **il TTL**! La condizione `n < 70` del `while` limita la lunghezza della
stringa e quindi, indirettamente, il numero di salti. Nel porting ho reso la
cosa esplicita con `len(hops) > MAX_HOP`, perché *contare i salti* è quello che
il vincolo **significa**, mentre *contare i caratteri* è un dettaglio
implementativo del C.

## 0.9 `getche()` → `input()`

```c
#include <conio.h>
chS = getche();
```

`getche()` sta in `<conio.h>`, una libreria **non standard** che esisteva su
MS-DOS/Windows (Borland, Turbo C). Legge **un singolo carattere** senza aspettare
l'Invio e lo ristampa a video (*get char and echo*). Su Linux/macOS non compila
nemmeno.

In Python si usa `input()`, che legge **un'intera riga** e la restituisce come
stringa (senza il carattere di a capo). Differenze da citare:

* `getche()` prende 1 carattere e va avanti subito; `input()` aspetta l'Invio;
* `getche()` restituisce un `char`, che `- '0'` converte in numero;
  `input()` restituisce una **stringa**, quindi la conversione va scritta a mano
  con `int()`.

> **Nota sullo stile.** Il porting segue il libro e basta: non aggiunge controlli
> sull'input, messaggi d'errore o casi limite che il sorgente C non prevede.
> Se digiti una lettera dove serve una cifra, il C produce un numero senza senso
> e Python solleva `ValueError`: in entrambi i casi il programma non è pensato
> per quell'uso, e inventare una validazione che il libro non chiede
> renderebbe il confronto fra i due sorgenti meno diretto. Gli unici messaggi
> d'errore presenti — «Impossibile instradare» e «Errore TTL!» — sono quelli
> **scritti nel sorgente del libro**.

## 0.10 Interi: 32 bit fissi vs precisione illimitata

```c
unsigned int ul;
ul = a*0x1000000 + b*0x10000 + c*0x100 + d;
```

`unsigned int` in C è (quasi sempre) **32 bit**: da 0 a 4 294 967 295. Un
indirizzo IPv4 ci sta esatto — non per caso, è proprio il motivo per cui il
libro usa questo tipo. Se sfori, il valore **va in overflow** e riparte da zero.

In Python gli interi hanno **precisione illimitata**: crescono finché c'è
memoria. Per il nostro codice va bene lo stesso, perché tutte le operazioni sono
AND con maschere a 32 bit e non possono mai superare quel limite. Se però
traducessi codice che *conta* sull'overflow, in Python dovresti aggiungere a
mano `& 0xFFFFFFFF`.

**Come lo spieghi:** «in C `unsigned int` è un contenitore a 32 bit, esattamente
la dimensione di un indirizzo IPv4; in Python l'intero non ha limite, quindi il
porting è sicuro perché noi facciamo solo AND con maschere a 32 bit, che non
possono farci sforare».

---

# PROGRAMMA 1 — «Hops» (B1, pag. 87-88)

**File:** `punto2_porting_python/b1_p087_hops.py`

## 1.1 Cosa deve fare

> Dato lo schema di rete del paragrafo *Routing CNLS: by network address*,
> digitati due numeri indicanti il router di partenza e il router di arrivo,
> stampare il percorso dell'ipotetico pacchetto.

La topologia è una **catena**: `R1 — R2 — R3 — R4`.

## 1.2 Il sorgente C originale

```c
00 #include <stdio.h>
01 #include <conio.h>
02 #include <string.h>
03
04 typedef struct {
05   char ra[3];       // Il router ra è connesso...
06   char rb[3];       // ...al router rb...
07   unsigned char p;  // ...sulla porta p (di ra)
08 } LINK;
09 LINK linkrouter[] =
     {{"R1","R2",2},{"R2","R1",4},{"R2","R3",2},{"R3","R2",5},{"R3","R4",3},{"R4","R3",1}};
10
11 int main (void)
12 {
13   char chS,chD, szHops[100], *pc;
14   int i,rm, rd, r, ok, n = 0;
15
16   printf("Digitare router sorgente (1..4): ");
17   chS = getche();
18   printf("\nDigitare router destinazione (1..4): ");
19   chD = getche();
20
21   rm = chS - '0';
22   rd = chD - '0';
23   r = -1;
24   szHops[0] = 0;
25   pc = szHops;
26   n = n + sprintf(pc+n,"R%c ",rm + '0');
27
28   while ((rm!=rd) && (n<70))
29   {
30       ok = -1;
31       for (i=0; i<sizeof(linkrouter)/sizeof(LINK); i++)
32       {
33         if (linkrouter[i].ra[1] == rm + '0')
34         {
35           ok = i;
36           if (linkrouter[i].rb[1] != r + '0')
37           {
38             ok = -2;
39             r = rm;
40             rm = linkrouter[i].rb[1] - '0';
41             break;
42           }
43         }
44       }
45       if (ok>=0)
46       {
47         r = rm;
48         rm = linkrouter[ok].rb[1] - '0';
49       }
50       if (ok==-1)
51       {
52         printf("\nImpossibile instradare");
53         return 0;
54       }
55
56       n = n + sprintf(pc+n,"R%c ",rm + '0');
57       printf("\nTratta: %s",szHops);
58   }
59
60   (rm==rd) ? printf(" ok") : printf("\nErrore TTL!");
61   return 0;
62 }
```

## 1.3 Analisi blocco per blocco

### Righe 00-02 — gli `#include`

```c
#include <stdio.h>    // printf, sprintf
#include <conio.h>    // getche  (NON standard, solo DOS/Windows)
#include <string.h>   // in realtà non serve: non si usa nessuna funzione di string.h
```

Un `#include` è una direttiva del **preprocessore**: prima ancora di compilare,
il testo del file indicato viene incollato al posto della riga. Serve a
dichiarare le funzioni di libreria che userai.

**Traduzione:** nessuna. Python ha `print` e `input` come *built-in*, sempre
disponibili senza importare niente. Se avessi avuto bisogno di qualcosa
(es. `math`) avrei scritto `import math`, che però è un'altra cosa: `import`
carica un **modulo a runtime**, non incolla testo.

> `string.h` è incluso ma mai usato: è codice morto, tipico del copia-incolla.
> Vale la pena notarlo, mostra che leggi il codice invece di subirlo.

### Righe 04-09 — la struttura dati della topologia

```c
typedef struct {
  char ra[3];       // router di partenza,  es. "R1"
  char rb[3];       // router di arrivo,    es. "R2"
  unsigned char p;  // porta di ra su cui è attaccato rb
} LINK;
```

Il commento del libro si legge così: **«sulla porta `p` del router `ra` è
connesso il router `rb`»**. È una *tripletta orientata*: descrive il link visto
**da un lato solo**. Per questo la lista ha 6 elementi e non 3: ogni linea fisica
compare **due volte**, una per verso.

```
R1 --P2--------P4-- R2 --P2--------P5-- R3 --P3--------P1-- R4
```

| tripletta | si legge |
|---|---|
| `{"R1","R2",2}` | sulla porta P2 di R1 è connesso R2 |
| `{"R2","R1",4}` | sulla porta P4 di R2 è connesso R1 |
| `{"R2","R3",2}` | sulla porta P2 di R2 è connesso R3 |
| `{"R3","R2",5}` | sulla porta P5 di R3 è connesso R2 |
| `{"R3","R4",3}` | sulla porta P3 di R3 è connesso R4 |
| `{"R4","R3",1}` | sulla porta P1 di R4 è connesso R3 |

**Traduzione:**

```python
LINKROUTER = [
    ("R1", "R2", 2),
    ("R2", "R1", 4),
    ("R2", "R3", 2),
    ("R3", "R2", 5),
    ("R3", "R4", 3),
    ("R4", "R3", 1),
]
```

**Perché una lista di tuple:** i tre campi sono eterogenei (due stringhe e un
numero), il record è piccolo, ed è **costante**. La tupla è immutabile, il che è
proprio quello che voglio: la topologia non deve poter cambiare per sbaglio.

**Perché maiuscolo:** convenzione PEP 8 per le costanti di modulo.

### Righe 13-14 — le dichiarazioni

```c
char chS, chD, szHops[100], *pc;
int i, rm, rd, r, ok, n = 0;
```

| variabile | ruolo |
|---|---|
| `chS`, `chD` | i due caratteri digitati (sorgente e destinazione) |
| `szHops[100]` | il buffer dove si accumula il percorso da stampare (`sz` = *string zero-terminated*, notazione ungherese) |
| `*pc` | puntatore di scrittura dentro `szHops` |
| `rm` | router **m**ittente = il router su cui si trova adesso il pacchetto |
| `rd` | router **d**estinazione |
| `r` | il router da cui il pacchetto è **appena arrivato** (per non tornare indietro) |
| `ok` | flag a tre stati, vedi sotto |
| `n` | quanti caratteri sono stati scritti finora in `szHops` |
| `i` | indice del ciclo |

**Traduzione:** spariscono tutte. `szHops`, `pc` e `n` vengono sostituiti dalla
lista `hops`; `i` non serve perché itero direttamente sugli elementi.

### Righe 16-22 — input e conversione

```c
printf("Digitare router sorgente (1..4): ");
chS = getche();
printf("\nDigitare router destinazione (1..4): ");
chD = getche();
rm = chS - '0';
rd = chD - '0';
```

```python
rm = int(input("put here source router  (1..4): "))
rd = int(input("put here destination router (1..4): "))
```

Cinque righe di C diventano due. **Perché:**

1. **`printf` + `getche()` → un solo `input(prompt)`.** `input()` accetta il
   messaggio come argomento e lo stampa senza andare a capo: fa in una riga
   quello che in C richiede due chiamate.
2. **`\n` iniziale del secondo `printf` eliminato.** Serviva perché `getche()`
   non manda a capo dopo l'eco del carattere; `input()` lo fa da solo.
3. **`chS - '0'` → `int(...)`, applicato subito.** In C servono due variabili
   (`chS` il carattere, `rm` il numero) perché la conversione è un'operazione
   aritmetica separata; in Python `int()` fa il lavoro nella stessa espressione,
   quindi le variabili-carattere spariscono.

Nessuna validazione dell'input: **il libro non ne fa**, e aggiungerla renderebbe
il confronto fra i due sorgenti meno diretto (vedi la nota in §0.9).

### Righe 23-26 — inizializzazione

```c
r = -1;              /* nessun router di provenienza: siamo alla partenza */
szHops[0] = 0;       /* stringa vuota */
pc = szHops;         /* il puntatore parte dall'inizio del buffer */
n = n + sprintf(pc+n, "R%c ", rm + '0');   /* scrive "R3 " e n diventa 3 */
```

```python
r = -1
hops = [rm]
```

`r = -1` si traduce **letteralmente**: è una **sentinella**, cioè un valore fuori
dal dominio valido (i router sono 1..4) usato per dire «non c'è». La logica
regge, quindi la tengo. In Python avrei potuto usare `None`, che è più
idiomatico; ho preferito `-1` perché il confronto `int(rb[1]) != r` funziona
comunque e resta uno-a-uno col libro. *(Se vuoi essere più pythonico, `None` va
benissimo: nessun router si chiamerà mai `None`.)*

Le tre righe di gestione del buffer collassano in `hops = [rm]`: la lista parte
già con il router di partenza dentro.

### Righe 28-58 — il cuore: il ciclo di instradamento

Questo è il pezzo da capire davvero.

```c
while ((rm != rd) && (n < 70))
```

Due condizioni in AND:
* `rm != rd` → **continua finché non sei arrivato**;
* `n < 70` → **il TTL**: se la stringa supera 70 caratteri smetti. Siccome ogni
  salto scrive 3 caratteri (`"R3 "`), 70 caratteri ≈ 23 salti.

```python
while rm != rd and len(hops) <= MAX_HOP:
```

**Perché conto i salti e non i caratteri:** `n < 70` limita la lunghezza della
stringa, ma quello che il programma *vuole* limitare è il numero di salti. Le due
condizioni restano nello stesso `while` come nel C, e per questo alla riga 60
serve il ternario
`(rm==rd) ? ... : ...` per capire *quale* delle due ha fatto uscire dal ciclo.
Separandole, il caso di errore esce subito con il suo messaggio e la fine del
ciclo può solo significare successo. Il codice diventa più corto e più chiaro.

**Perché conto i salti e non i caratteri:** `n < 70` limita la lunghezza della
stringa, ma quello che il programma *vuole* limitare è il numero di salti. Il
vincolo sui caratteri è un effetto collaterale del fatto che in C la stringa è
un buffer fisso. In Python il buffer non c'è, quindi traduco il **significato**,
non la lettera.

#### Il flag `ok`: tre stati in una sola variabile

Qui sta la parte più intricata del C, e va spiegata bene.

```c
ok = -1;
for (i=0; i<6; i++)
{
  if (linkrouter[i].ra[1] == rm + '0')   /* esiste un'uscita da rm? */
  {
    ok = i;                              /* SÌ: ricordo l'indice        (A) */
    if (linkrouter[i].rb[1] != r + '0')  /* ...e non torna indietro?    (B) */
    {
      ok = -2;                           /* PERFETTO: mi muovo subito       */
      r = rm;
      rm = linkrouter[i].rb[1] - '0';
      break;
    }
  }
}
```

`ok` porta **tre significati diversi**:

| valore | significato | cosa fa il codice dopo |
|---|---|---|
| `-1` | nessuna tripletta esce da `rm`: router isolato | riga 50: stampa «Impossibile instradare» e termina |
| `-2` | trovata un'uscita che **non** torna indietro: mi sono **già mosso** dentro il `for` | righe 45 e 50 non scattano, si prosegue |
| `≥ 0` | l'unica uscita disponibile è quella da cui sono venuto | riga 45: mi muovo lì, obtorto collo |

È un idioma C classico: riusare una variabile intera come flag per **risparmiare
una variabile**. Compatto, ma illeggibile — e infatti ti costringe a rileggerlo
tre volte per capirlo.

**Traduzione:**

```python
ok = None       # indice dell'ultima uscita trovata (ripiego)
mosso = False   # mi sono già spostato dentro il for?

for i, (ra, rb, _p) in enumerate(LINKROUTER):
    if int(ra[1]) != rm:
        continue
    ok = i
    if int(rb[1]) != r:          # non è la porta da cui sono entrato
        r, rm = rm, int(rb[1])
        mosso = True
        break

if not mosso:
    if ok is None:               # no exit: router isolated
        print(f"no exit from R{rm} to R{rd}")
        return None
    # the only exit disponibile: torno indietro
    r, rm = rm, int(LINKROUTER[ok][1][1])
```

**Le scelte, una per una:**

1. **Ho spezzato `ok` in due variabili con nomi parlanti.** `ok` resta l'indice
   di ripiego (o `None`), `mosso` è il booleano «mi sono già spostato». Motivo:
   in Python non c'è nessun vantaggio a comprimere tre stati in un intero, e un
   `bool` esplicito si legge da solo. Il comportamento è identico, la logica no:
   è la stessa, solo scritta in modo esplicito.

2. **`ok = None` invece di `ok = -1`.** In Python `None` è *il* modo di dire
   «valore assente», e il test `if ok is None` non si può confondere con un
   indice valido. Con `-1` rischi di usarlo per sbaglio come indice — e in Python
   `lista[-1]` è **l'ultimo elemento**, non un errore! Questo è un vero trabocchetto
   del porting: se avessi lasciato `-1`, `LINKROUTER[ok]` avrebbe silenziosamente
   restituito l'ultima tripletta invece di segnalare l'errore.

3. **`continue` invece di annidare l'`if`.** Il C mette tutto il corpo dentro
   `if (...ra[1] == rm + '0') { ... }`. Io ho invertito il test e uso `continue`
   per saltare subito i casi che non interessano: si chiama *guard clause* e
   toglie un livello di indentazione.

4. **`enumerate(LINKROUTER)` invece di `for (i=0; i<len; i++)` + `lista[i]`.**
   `enumerate` dà indice ed elemento insieme: ottengo `i` (che mi serve per
   `ok`) senza dover indicizzare a mano. È il modo idiomatico in Python di
   dire «voglio anche la posizione».

5. **`_p`.** Il campo *porta* non viene mai usato in questo programma
   (l'algoritmo salta di router in router, la porta è solo documentazione).
   L'underscore davanti è la convenzione Python per dire **«lo spacchetto ma non
   lo uso»**, così chi legge non lo cerca.

6. **`r, rm = rm, int(rb[1])`.** Assegnamento simultaneo: la parte destra viene
   valutata **tutta prima** di assegnare. In C servono due righe nell'ordine
   giusto (`r = rm;` **poi** `rm = ...;`), perché se le invertissi perderesti il
   vecchio `rm`. In Python l'ordine non conta e non serve una variabile
   temporanea.

7. **`int(LINKROUTER[ok][1][1])` — il triplo indice.** Si legge da sinistra:
   `LINKROUTER[ok]` = la tripletta; `[1]` = il campo `rb`, cioè la stringa
   `"R2"`; `[1]` = il secondo carattere, `"2"`; `int(...)` = il numero 2.
   È esattamente `linkrouter[ok].rb[1] - '0'` del C.
   *(Meno leggibile del resto: se volessi migliorarlo, potrei spacchettare con
   `_, rb_ok, _ = LINKROUTER[ok]` e poi `int(rb_ok[1])`.)*

#### Righe 56-57 — accodare e stampare

```c
n = n + sprintf(pc+n, "R%c ", rm + '0');
printf("\nTratta: %s", szHops);
```
```python
hops.append(rm)
print("track: " + " ".join(f"R{x}" for x in hops))
```

`hops` contiene **numeri** (1, 2, 3, 4), non stringhe: la formattazione in `"R3"`
avviene solo al momento della stampa. È una scelta precisa — **tengo separati i
dati dalla loro rappresentazione**. Nel C i due aspetti sono mescolati, perché
`szHops` è contemporaneamente la struttura dati e il testo da stampare, e infatti
è per questo che il TTL finisce per essere un vincolo sui caratteri.

Come nel C, la stampa avviene **dentro** il ciclo: si vede il percorso crescere
tratta dopo tratta.

### Riga 60 — l'operatore ternario

```c
(rm == rd) ? printf(" ok") : printf("\nErrore TTL!");
```

`condizione ? valoreSeVero : valoreSeFalso` è l'`if` in forma di **espressione**.
Qui è usato solo per l'effetto collaterale delle due `printf` — stile compatto ma
discutibile, perché il ternario nasce per **produrre un valore**, non per
scegliere quale funzione chiamare.

Python ha l'equivalente esatto, l'**espressione condizionale**
`a if cond else b`, e l'ho usata proprio come si dovrebbe: per scegliere la
**stringa** da stampare, non la funzione da chiamare.

```python
print("ok" if rm == rd else "error TTL!")
```

È lo stesso identico test del C. L'uscita anticipata del ramo «router isolato»
diventa `raise SystemExit`, che a livello di modulo fa quello che `return 0` fa
dentro `main()`: termina il programma.

### 1.4 Verifica

Input `3`, `1` (da R3 a R1). Il libro stampa:

```
track: R3 R2
track: R3 R2 R1
ok
```

Il porting produce le stesse tratte. **Traccia a mano** (impara a farla, è tipica
da verifica):

| giro | `rm` | `r` | tripletta scelta | perché |
|---|---|---|---|---|
| inizio | 3 | -1 | — | partenza da R3 |
| 1 | 3 | -1 | `{"R3","R2",5}` | prima con `ra="R3"`; `rb="R2"` ≠ provenienza (-1) ⟹ mi muovo |
| 2 | 2 | 3 | `{"R2","R1",4}` | prima con `ra="R2"`; `rb="R1"` ≠ 3 ⟹ mi muovo |
| fine | 1 | 2 | — | `rm == rd` ⟹ «ok» |

### 1.5 I limiti dell'algoritmo (li dichiara il libro stesso)

* da **R2 verso R4** il pacchetto prima **torna indietro** a R1 e poi risale,
  perché la prima tripletta con `ra="R2"` è `{"R2","R1",4}`. Prova:
  input `2`, `4` → `R2 R1 R2 R3 R4`.
* da **R3 verso R1** si comporta razionalmente (è il caso dell'esempio).
* con una destinazione inesistente (es. `R9`) gira finché non scatta il TTL.

Questo perché **non è un vero algoritmo di routing**: non consulta nessuna TdI e
non conosce le distanze. Sceglie la prima uscita che non torna indietro — è di
fatto un *flooding* degenere su una topologia a catena. Il programma 2 è quello
che introduce la TdI vera.

### 1.6 Una discrepanza fra testo e codice, da citare

Il libro scrive: *«se nessuna tripletta soddisfa la condizione, si prende la
**prima** tripletta d'uscita dal router»*. Ma nel codice il `for` **non fa
`break`** in quel ramo, quindi `ok` viene sovrascritto a ogni giro e alla fine
contiene l'indice dell'**ultima** tripletta con `ra == rm`. Sulla topologia a
catena del libro non cambia il risultato (ogni router ha al massimo due uscite),
ma testo e codice **non dicono la stessa cosa**. Nel porting ho riprodotto il
comportamento del codice, non del testo.

---

# PROGRAMMA 2 — «Routing CNLS e next hop» (B1, pag. 90-91)

**File:** `punto2_porting_python/b1_p090_routing_cnls.py`

## 2.1 Cosa deve fare

> Date le TdI per tre router R1, R2 e R3, acquisire in input gli indirizzi
> mittente e destinatario di un pacchetto trasmesso dall'host A (direttamente
> connesso al router R1), quindi mostrare in output il percorso del pacchetto.

Differenza sostanziale rispetto al programma 1: qui c'è una **vera tabella di
instradamento**. Il router non tira a indovinare, **consulta la TdI**.

## 2.2 Il sorgente C originale

```c
00 #include <stdio.h>
01 #include <conio.h>
02 #include <string.h>
03 #include <stdlib.h>
04
05 typedef struct {
06   char add;         // indirizzo
07   unsigned char p;  // porta
08   unsigned char h;  // hop
09   unsigned char c;  // costo
10 } TDI;
11 TDI tdiR1[] = {{'a',1,0,0},{'b',2,1,5},{'c',2,2,2}};
12 TDI tdiR2[] = {{'a',3,1,0},{'b',7,0,5},{'c',2,1,2}};
13 TDI tdiR3[] = {{'a',9,2,0},{'b',8,1,5},{'c',9,0,0}};
14 TDI* tdi;
15
16 typedef struct {
17   char ra[3];       // Il router ra è connesso...
18   char rb[3];       // ...al router rb...
19   unsigned char p;  // ...sulla porta p (di ra)
20 } LINK;
21 LINK linkrouter[] = {{"R1","R2",2},{"R2","R1",4},{"R2","R3",2},{"R3","R2",5}};
22
23 int main (void)
24 {
25   char chS,chD;
26   char szHops[100], *pc;
27   int i,j,h,r,p,n = 0;
28
29   printf("Digitare indirizzo sorgente (a,b,c): ");
30   chS = getche();
31   printf("\nDigitare indirizzo destinazione (a,b,c): ");
32   chD = getche();
33
34   h = -1;  r = 1;
35   szHops[0] = 0;
36   pc = szHops;
37   n = n + sprintf(pc+n,"%c ",chS);
38   while (h)
39   {
40     p = -1; h = -1;
41     n = n + sprintf(pc+n,"R%c ",r + '0');
42
43     if (tdi) free(tdi);
44     switch (r)
45     {
46     case 1: tdi = malloc(sizeof(tdiR1)); memcpy(tdi,tdiR1,sizeof(tdiR1)); break;
47     case 2: tdi = malloc(sizeof(tdiR2)); memcpy(tdi,tdiR2,sizeof(tdiR2)); break;
48     case 3: tdi = malloc(sizeof(tdiR3)); memcpy(tdi,tdiR3,sizeof(tdiR3)); break;
49     }
50
51     for (i=0; i<sizeof(tdi); i++)
52     {
53       if (chD==tdi[i].add)
54       {
55         h = tdi[i].h; p = tdi[i].p;
56         break;
57       }
58     }
59
60     if (h>0)
61     {
62       for (j=0; j<sizeof(linkrouter)/sizeof(LINK); j++)
63       {
64         if ((linkrouter[j].ra[1]==r+'0') && (linkrouter[j].p==p))
65         {
66           r = linkrouter[j].rb[1]-'0';
67           break;
68         }
69       }
70     }
71     else
72     {
73       if (h==0) n = n + sprintf(pc+n,"%c",chD);
74       else
75       {
76         printf("\nImpossibile instradare");
77         return 0;
78       }
79     }
80   }
81
82   printf("\nPercorso: %s",szHops);
83   return 0;
84 }
```

## 2.3 Analisi blocco per blocco

### Righe 05-13 — la TdI

```c
typedef struct {
  char add;         // indirizzo (UN SOLO carattere: 'a', 'b', 'c')
  unsigned char p;  // porta
  unsigned char h;  // hop
  unsigned char c;  // costo
} TDI;
```

Sono **esattamente le quattro colonne** di una tabella di instradamento come le
hai studiate: `Add | P | h | c`. Nota che `add` è un `char` singolo, non una
stringa: gli host si chiamano `a`, `b`, `c`, quindi basta un carattere e si
risparmiano i problemi delle stringhe C.

```c
TDI tdiR1[] = {{'a',1,0,0},{'b',2,1,5},{'c',2,2,2}};
```

si legge: *«da R1, per raggiungere `a` esci da P1 con 0 hop e costo 0; per `b`
esci da P2 con 1 hop e costo 5; per `c` esci da P2 con 2 hop e costo 2»*.
`h = 0` su `a` significa che **`a` è direttamente connesso a R1**, coerente con
la traccia.

**Traduzione:**

```python
TDI = {
    1: [("a", 1, 0, 0), ("b", 2, 1, 5), ("c", 2, 2, 2)],
    2: [("a", 3, 1, 0), ("b", 7, 0, 5), ("c", 2, 1, 2)],
    3: [("a", 9, 2, 0), ("b", 8, 1, 5), ("c", 9, 0, 0)],
}
```

**Perché un dizionario `numero_router → lista di righe`, e non tre liste separate.**
Nel C le tre tabelle sono tre variabili distinte (`tdiR1`, `tdiR2`, `tdiR3`) e
per scegliere quella giusta serve uno `switch` a tre casi (righe 44-49). Con un
dizionario la scelta diventa **un accesso per chiave**:

```python
TDI[r]          # invece di switch(r) { case 1: ...; case 2: ...; case 3: ... }
```

Questo cancella di colpo **sei righe di C** (lo switch, le malloc e le memcpy) e,
soprattutto, rende il programma **estensibile**: per aggiungere R4 aggiungi una
riga al dizionario, mentre in C dovresti aggiungere anche un `case`.

**Come lo spieghi:** «lo `switch` del C mappa un numero a una tabella; è
esattamente quello che fa un dizionario, quindi la struttura dati assorbe il
controllo di flusso».

> **Anomalia nei dati del libro, da notare:** `tdiR2` dice che per `a` si esce
> dalla porta 3, ma nella lista `linkrouter` R2 **non ha** nessuna porta 3.
> Idem per `tdiR3`, con le porte 8 e 9. Sono valori inventati che non vengono mai
> esercitati, perché l'esempio del libro instrada solo verso `c`. In C, se ci
> capitassi, il secondo `for` non troverebbe nulla, `r` resterebbe invariato e il
> `while` girerebbe all'infinito. Nel porting ho aggiunto il controllo
> `if nxt is None` che stampa un messaggio invece di bloccarsi.

### Riga 14 — il puntatore globale

```c
TDI* tdi;
```

`tdi` è un **puntatore a TDI**: contiene un *indirizzo di memoria*, non i dati.
Essendo una variabile globale, il C la inizializza a `NULL` (0) — quindi il
`if (tdi) free(tdi)` alla riga 43 al primo giro è **innocuo**, perché `free(NULL)`
è legale e `if (NULL)` è falso.

*(Nella mia analisi iniziale l'avevo segnalato come comportamento indefinito:
lo sarebbe se `tdi` fosse una variabile **locale**, che il C non azzera. Essendo
globale, è zero-inizializzata dallo standard. Il codice qui è salvo — resta il
fatto che `malloc`/`free` sono comunque inutili.)*

**Traduzione:** nessuna. Non esistono puntatori in Python.

### Righe 34-37 — inizializzazione

```c
h = -1;  r = 1;      /* h = sentinella "non arrivato"; r = 1 perché si parte da R1 */
n = n + sprintf(pc+n, "%c ", chS);   /* la stringa inizia con l'host mittente */
```

`r = 1` è l'assunzione della traccia: **il router di partenza è sempre R1**,
perché l'host A è connesso lì. Il libro lo dice esplicitamente («il programma dà
per scontato che il router di partenza sia R1, riga 34»).

Nel porting resta **scritto nel codice esattamente come nel C**:

```python
r = 1                       # il libro parte always da R1
percorso = [chS]
```

Renderlo un parametro sarebbe stato facile, ma il libro non lo chiede e la
traccia dice esplicitamente che l'host A è connesso a R1: tenerlo fisso
mantiene il porting sovrapponibile all'originale.

### Righe 38-40 — il ciclo e la sentinella `h`

```c
while (h)          /* continua finché h != 0 */
{
  p = -1; h = -1;  /* azzera i risultati della ricerca a ogni giro */
```

`while (h)` sfrutta la regola del C per cui **0 è falso e tutto il resto è vero**.
Quindi il ciclo prosegue finché `h != 0`, cioè **finché non sei arrivato**
(ricorda: `h == 0` in TdI significa «destinazione direttamente connessa»).

`h` è una sentinella a tre stati, come `ok` nel programma 1:

| `h` | significato |
|---|---|
| `> 0` | mancano `h` router: cerca il next hop e salta |
| `= 0` | **arrivato**: la destinazione è sulla LAN locale, consegna |
| `< 0` | **nessuna regola trovata** in TdI: impossibile instradare |

Il libro lo dice: *«per prevenire loop ed errori si usa la sentinella h = -1»*.

**Traduzione:**

```python
h = -1                      # sentinel
while h != 0:
    percorso.append(f"R{r}")
    p, h = -1, -1           # reset ad ogni giro, come il C riga 40

    for add, porta, hop, _c in TDI[r]:      # passo 2: cerco la riga
        if add == chD:
            p, h = porta, hop
            break

    if h > 0:    ...   # passo 3: salto al next hop
    elif h == 0: ...   # arrivato
    else:        ...   # impossibile instradare
```

**Le scelte:**

1. **`while (h)` → `while h != 0`.** In C `0` è falso e tutto il resto è vero,
   quindi `while (h)` significa letteralmente «finché `h` è diverso da zero».
   In Python la condizione va **scritta per esteso**: gli interi hanno sì un
   valore di verità (`0` falso, resto vero), quindi `while h:` funzionerebbe,
   ma `while h != 0` dice quello che intendi. È l'unica traduzione, non serve
   aggiungere un limite di iterazioni: con le tre destinazioni previste dal
   libro (`a`, `b`, `c`) il ciclo termina sempre, e una destinazione diversa
   fa scattare subito la sentinella `-1`.

2. **La ricerca resta inline, come nel C.** Il `for` della riga 51 sta dentro
   `main` nell'originale e sta dentro il `while` nel porting: stesso posto,
   stesso ordine. Isolarlo in una funzione a parte renderebbe il codice più
   modulare, ma spezzerebbe la corrispondenza riga-per-riga che è lo scopo di
   un esercizio di porting.

3. **La sentinella `-1` la tengo** perché è documentata nel testo del libro ed è
   parte di quello che devi saper spiegare. In Python "puro" restituirei `None`;
   qui la fedeltà al libro vince.

4. **`_c`** — il costo è nella TdI ma il programma non lo usa mai (lo dice il
   libro: «il costo non sarà tuttavia analizzato»). Underscore.

### Righe 43-49 — il blocco che sparisce

```c
if (tdi) free(tdi);
switch (r)
{
case 1: tdi = malloc(sizeof(tdiR1)); memcpy(tdi,tdiR1,sizeof(tdiR1)); break;
case 2: tdi = malloc(sizeof(tdiR2)); memcpy(tdi,tdiR2,sizeof(tdiR2)); break;
case 3: tdi = malloc(sizeof(tdiR3)); memcpy(tdi,tdiR3,sizeof(tdiR3)); break;
}
```

Sette righe che fanno questo: *libera la copia della TdI del giro precedente,
alloca memoria per la TdI del router corrente, copiaci dentro la tabella*.

**È tutto inutile.** La TdI non viene mai modificata, quindi copiarla non serve a
niente: basterebbe `tdi = tdiR1;` (far puntare il puntatore alla tabella
originale). L'unico effetto delle `malloc`/`memcpy` è consumare tempo e rischiare
un memory leak se il `free` non venisse eseguito.

**Traduzione:** un accesso al dizionario, dentro il ciclo di ricerca:

```python
TDI[router]
```

Un accesso al dizionario. Il `free`, la `malloc`, la `memcpy` e i tre `case`
dello `switch` collassano tutti qui: la scelta della tabella *è* la ricerca per
chiave.

Nota che lo `switch` del C **non ha il ramo `default:`**. Se `r` non fosse 1, 2
o 3, lo switch non farebbe niente e `tdi` resterebbe quello del giro precedente:
il programma proseguirebbe con la tabella sbagliata **senza accorgersene**.
`TDI[router]` invece solleverebbe `KeyError` e si fermerebbe subito. Non è un
controllo che ho aggiunto — è il comportamento naturale del dizionario, ed è
un caso in cui il costrutto Python è semplicemente più sicuro di quello C.

### Righe 51-58 — la ricerca della regola

```c
for (i=0; i<sizeof(tdi); i++)      /* BUG: sizeof di un puntatore */
{
  if (chD == tdi[i].add)
  {
    h = tdi[i].h; p = tdi[i].p;
    break;
  }
}
```

**Il bug.** `sizeof(tdi)` misura il **puntatore** (4 byte su sistemi a 32 bit, 8
su 64 bit), non l'array. Il ciclo scorre 4 o 8 posizioni su una tabella che ne
ha 3: legge fuori dai limiti. Il codice corretto sarebbe
`sizeof(tdiR1)/sizeof(TDI)`, ma non si può scrivere perché a quel punto il
programma non sa più *quale* delle tre tabelle sta usando — e questa è
esattamente la conseguenza dell'aver usato un puntatore unico invece di
scegliere la tabella al momento della ricerca.

Nella pratica il programma **funziona lo stesso** per fortuna: la regola cercata
si trova entro le prime 3 posizioni e il `break` esce prima di leggere memoria
non valida. Ma è fortuna, non correttezza.

**Traduzione:** il problema non esiste, perché itero direttamente sulla lista.

```python
for add, p, h, _c in TDI.get(router, []):
    if add == dest:
        return p, h
```

**`return` invece di `break` + variabili.** Nel C devi salvare `h` e `p` in
variabili esterne al ciclo e poi uscire con `break`. Avendo estratto una
funzione, posso restituire direttamente la coppia: niente variabili condivise,
niente rischio di leggerle prima che siano state assegnate.

### Righe 60-70 — trovare il next hop

```c
if (h > 0)
{
  for (j=0; j<sizeof(linkrouter)/sizeof(LINK); j++)
  {
    if ((linkrouter[j].ra[1] == r+'0') && (linkrouter[j].p == p))
    {
      r = linkrouter[j].rb[1] - '0';
      break;
    }
  }
}
```

Qui il `sizeof` è **corretto**, perché `linkrouter` è un array vero.

La condizione è un AND di due test: *la tripletta parte dal router in cui sono*
**e** *usa proprio la porta che la TdI mi ha detto*. Trovata, il router corrente
diventa `rb`.

**Questo è il collegamento fra le due strutture dati** ed è il concetto centrale
del programma: la **TdI dice la porta**, la **topologia dice cosa c'è attaccato a
quella porta**. Sono due informazioni distinte, ed è così anche nella realtà: un
router conosce la propria tabella, e conosce i propri vicini, ma sono due cose
separate.

**Traduzione:**

```python
if h > 0:
    # passo 3: chi è attached alla porta p di questo router?
    for ra, rb, porta in LINKROUTER:
        if int(ra[1]) == r and porta == p:
            r = int(rb[1])
            break
```

* anche questo resta **inline**, esattamente dove sta nel C;
* `and` al posto di `&&`, `int(ra[1])` al posto di `ra[1] == r+'0'` (vedi 0.6);
* se nessuna tripletta corrisponde, il `for` finisce e `r` **resta invariato**,
  identico al C. Il libro non gestisce questo caso. Con i suoi dati non capita
  mai — le tre destinazioni `a`, `b`, `c` arrivano tutte a una riga con
  `h == 0` prima di chiedere una porta inesistente — ma se capitasse il `while`
  rifarebbe lo stesso identico giro all'infinito. È lo stesso genere di
  fragilità del programma 1, che infatti si difende con il TTL.

### Righe 71-79 — arrivo o errore

```c
else
{
  if (h == 0) n = n + sprintf(pc+n, "%c", chD);   /* arrivato: accoda l'host */
  else
  {
    printf("\nImpossibile instradare");
    return 0;
  }
}
```

L'`else` copre `h <= 0`, e dentro si distingue `h == 0` (arrivato) da `h < 0`
(regola non trovata).

**Traduzione:** ho **invertito l'ordine** e usato uscite anticipate:

```python
if h == 0:                       # destinazione direttamente connessa
    percorso.append(destinazione)
    return " ".join(percorso)

if h < 0:                        # nessuna regola in TdI
    print(f"no route to {destinazione}")
    return None
```

**Perché:** nel C i tre casi (`h>0`, `h==0`, `h<0`) sono annidati su due livelli
(`if/else` e dentro un altro `if/else`), quindi per capire quando succede cosa
devi tenere a mente il ramo in cui ti trovi. Mettendoli in fila come tre `if` con
`return`, ogni caso si legge da solo e non c'è annidamento. È lo stesso schema
del programma 1.

Nota anche che nel C, quando `h == 0`, il pacchetto viene accodato ma **il ciclo
non termina con un `break`**: termina perché `h` vale 0 e la condizione
`while (h)` diventa falsa al giro dopo. Funziona, ma è indiretto. Con il `return`
l'uscita è immediata ed esplicita.

## 2.4 Verifica

Input `a`, `c`. Il porting stampa `path: a R1 R2 R3 c`, che e' il
`Percorso: a R1 R2 R3 c` del libro. Traccia a mano:

| giro | `r` | riga di TdI usata | `p` | `h` | next hop |
|---|---|---|---|---|---|
| 1 | R1 | `{'c',2,2,2}` | 2 | 2 | tripletta `{"R1","R2",2}` ⟹ R2 |
| 2 | R2 | `{'c',2,1,2}` | 2 | 1 | tripletta `{"R2","R3",2}` ⟹ R3 |
| 3 | R3 | `{'c',9,0,0}` | 9 | **0** | arrivato: accoda `c` |

Risultato: `a R1 R2 R3 c` ✔

Osserva il giro 3: `p` vale 9, una porta che non esiste — ma **non importa**,
perché con `h == 0` la porta non viene mai usata. È il motivo per cui il libro
si è potuto permettere di scrivere valori a caso in quelle celle.

---

# PROGRAMMA 3 — «Classful e reti di appartenenza» (B3, pag. 126-127)

**File:** `punto2_porting_python/b3_p126_classful_netid.py`

## 3.1 Cosa deve fare

> Determinare la classe dei seguenti indirizzi IP e verificare l'appartenenza
> reciproca alla stessa rete: `10.1.0.3`, `192.168.0.1`, `137.168.0.1`,
> `137.168.249.17`.

Qui non c'è input: i dati sono *hard coded*. Il programma è un esercizio di
**manipolazione di bit**.

## 3.2 Il sorgente C originale

```c
00 #include <stdio.h>
01
02 typedef struct {
03   unsigned char mask;
04   unsigned char leading;
05   unsigned int netmask;
06 } CLASSFUL;
07 CLASSFUL classiIp[] =
     {{0x80,0x00,0xff000000},{0xc0,0x80,0xffff0000},{0xe0,0xc0,0xffffff00}};
08
09 typedef struct {
10   unsigned char a,b,c,d;  // IP dotted
11   unsigned int ip;        // IP decimale
12   unsigned int netid;     // netId corrispondente alla classe di appartenenza
13 } IPINFO;
14 IPINFO Ip[4];
15
16 int main (void)
17 {
18   int i,j;
19   // I quattro indirizzi dati
20   Ip[0].a= 10; Ip[0].b=  1; Ip[0].c=  0; Ip[0].d=3;
21   Ip[1].a=192; Ip[1].b=168; Ip[1].c=  0; Ip[1].d=1;
22   Ip[2].a=137; Ip[2].b=168; Ip[2].c=  0; Ip[2].d=1;
23   Ip[3].a=137; Ip[3].b=168; Ip[3].c=249; Ip[3].d=17;
24
25   i = 0;
26   for (i=0; i<4; i++)
27   {
28     for (j=0;j<3;j++)
29     {
30       Ip[i].ip = Ip[i].a*0x1000000 + Ip[i].b*0x10000 + Ip[i].c*0x100 + Ip[i].d;
31       if ((Ip[i].a & classiIp[j].mask) == classiIp[j].leading)
32       {
33         Ip[i].netid = Ip[i].ip & classiIp[j].netmask;
34         printf("\n%3d.%3d.%3d.%3d",Ip[i].a,Ip[i].b,Ip[i].c,Ip[i].d);
35         printf("classe %c (mask: %x)e netId %X",'A'+j, classiIp[j].netmask, Ip[i].netid);
36       }
37     }
38   }
39
40   for (i=0; i<4-1; i++)
41   {
42     for (j=i+1;j<4;j++)
43     {
44       if (Ip[i].netid==Ip[j].netid)
45       {
46         printf("\n%d.%d.%d.%d",Ip[i].a,Ip[i].b,Ip[i].c,Ip[i].d);
47         printf(" e %d.%d.%d.%d stessa rete",Ip[j].a,Ip[j].b,Ip[j].c,Ip[j].d);
48       }
49     }
50   }
51
52   return 0;
53 }
```

## 3.3 Analisi blocco per blocco

### Righe 02-07 — la tabella delle classi

```c
typedef struct {
  unsigned char mask;      // maschera da applicare al PRIMO byte
  unsigned char leading;   // valore atteso dopo la maschera
  unsigned int netmask;    // netmask a 32 bit della classe
} CLASSFUL;
CLASSFUL classiIp[] = {{0x80,0x00,0xff000000},   // A
                       {0xc0,0x80,0xffff0000},   // B
                       {0xe0,0xc0,0xffffff00}};  // C
```

Questa struttura **è la teoria di pag. 125 messa in tabella**. Ricorda:

| Classe | leading bit | maschera | valore atteso | netmask |
|---|---|---|---|---|
| A | `0xxxxxxx` | `10000000` = `0x80` | `00000000` = `0x00` | `255.0.0.0` = `0xff000000` |
| B | `10xxxxxx` | `11000000` = `0xc0` | `10000000` = `0x80` | `255.255.0.0` = `0xffff0000` |
| C | `110xxxxx` | `11100000` = `0xe0` | `11000000` = `0xc0` | `255.255.255.0` = `0xffffff00` |

Il test è sempre lo stesso: **`(primo_byte AND mask) == leading`**. La maschera
isola i bit che contano (i primi 1, 2 o 3), il `leading` è il valore che quei bit
devono avere.

Il fatto che `mask` e `leading` siano `unsigned char` (1 byte) e `netmask` sia
`unsigned int` (4 byte) **non è casuale**: i primi due si confrontano con il
**primo ottetto** dell'indirizzo, la terza con l'**indirizzo intero**.

**Traduzione:**

```python
CLASSI_IP = [
    (0x80, 0x00, 0xFF000000),   # A
    (0xC0, 0x80, 0xFFFF0000),   # B
    (0xE0, 0xC0, 0xFFFFFF00),   # C
]
```

Stessa scelta del programma 1: tupla, perché è un record costante di tre campi
letti insieme. I letterali esadecimali si scrivono identici (`0x...`); ho messo
le lettere maiuscole solo per uniformità, in Python `0xff` e `0xFF` sono la
stessa cosa.

### Righe 09-14 — `IPINFO` e l'array globale

```c
typedef struct {
  unsigned char a,b,c,d;  // i 4 ottetti
  unsigned int ip;        // l'indirizzo come unico numero a 32 bit
  unsigned int netid;     // il netId calcolato
} IPINFO;
IPINFO Ip[4];
```

`unsigned char` per gli ottetti è la scelta giusta: un ottetto va da 0 a 255,
esattamente il range di `unsigned char`. È **autodocumentante**: il tipo stesso
dice «qui ci sta un byte di indirizzo».

**Punto importante che riguarda un bug:** `Ip[4]` è una variabile **globale**,
quindi il C la **azzera tutta** all'avvio. Significa che `netid` vale 0 per tutti
e quattro gli indirizzi finché non viene calcolato. Se un indirizzo fosse di
classe D o E, il test della riga 31 non scatterebbe mai, `netid` resterebbe 0, e
il **secondo ciclo lo confronterebbe con gli altri**: due indirizzi di classe D
risulterebbero «stessa rete» pur non avendo nessun netId. È un bug latente che
sui quattro indirizzi dati non si manifesta.

**Traduzione:** la struct `IPINFO` **non la traduco affatto**.

```python
INDIRIZZI = [
    (10, 1, 0, 3),
    (192, 168, 0, 1),
    (137, 168, 0, 1),
    (137, 168, 249, 17),
]
```

**Perché.** `IPINFO` mescola due cose diverse: i **dati di partenza** (i quattro
ottetti) e i **risultati intermedi** (`ip` e `netid`). In C conviene tenerli
insieme perché servono nel secondo ciclo e non c'è modo comodo di restituire più
valori da una funzione. In Python posso:

* tenere in `INDIRIZZI` solo i dati veri;
* calcolare `ip` e `netid` **dentro una funzione** che li restituisce;
* raccogliere i netId in una lista separata `info`.

È il principio di **separare i dati dai risultati**. Se qualcuno legge
`INDIRIZZI` sa subito che quello è l'input; in C devi dedurlo.

Le righe 20-23 (l'assegnamento ottetto per ottetto, 16 assegnamenti!) si
riducono così alla lista di quattro tuple.

### Riga 25 — codice morto

```c
i = 0;
for (i=0; i<4; i++)
```

`i = 0` prima di un `for` che riassegna `i = 0`: non fa niente. Non si traduce.
Segnalarlo è utile: dimostra che hai letto ogni riga.

### Righe 26-38 — il doppio ciclo di classificazione

```c
for (i=0; i<4; i++)          /* per ogni indirizzo */
{
  for (j=0; j<3; j++)        /* per ogni classe */
  {
    Ip[i].ip = Ip[i].a*0x1000000 + ... ;              /* riga 30 */
    if ((Ip[i].a & classiIp[j].mask) == classiIp[j].leading)
    { ... }
  }
}
```

Tre osservazioni:

1. **La riga 30 è dentro il ciclo `j`.** L'indirizzo decimale viene ricalcolato
   **tre volte** per ogni IP, sempre identico. Inefficienza pura: il calcolo non
   dipende da `j`. Nel porting l'ho spostato fuori.

2. **Non c'è `break` dopo il match.** Trovata la classe, il ciclo continua a
   provare le altre. Funziona lo stesso perché i tre test sono **mutuamente
   esclusivi** per costruzione, ma sono due iterazioni sprecate.
   *Verifica del perché sono esclusivi:* per `137` (= `10001001`),
   `137 & 0x80 = 0x80 ≠ 0x00` (non A), `137 & 0xC0 = 0x80 = 0x80` (**B** ✔),
   `137 & 0xE0 = 0x80 ≠ 0xC0` (non C). Una sola classe può passare.

3. **`4` e `3` scritti a mano.** Sono *numeri magici*: se aggiungi un indirizzo
   devi ricordarti di cambiare tutti i `4`. Riga 40 usa perfino `i<4-1`, che il
   compilatore riduce a `i<3`: è scritto così per far capire che il `-1` viene
   dal numero di elementi.

**Traduzione — la conversione dotted → intero:**

```c
Ip[i].a*0x1000000 + Ip[i].b*0x10000 + Ip[i].c*0x100 + Ip[i].d
```
```python
ip = a * 0x1000000 + b * 0x10000 + c * 0x100 + d
```

**Tradotta alla lettera**, e ti spiego perché ha senso così com'è. I quattro
fattori sono le potenze di 256: `0x1000000` = 256³, `0x10000` = 256², `0x100` =
256, `1`. È la stessa cosa di scrivere un numero in base 256, con gli ottetti
come cifre. Equivalente con gli shift:

```python
(a << 24) | (b << 16) | (c << 8) | d
```

Ho tenuto la forma con le moltiplicazioni **per restare aderente al libro**, ma
se il prof chiede sappi dire che sono identiche: moltiplicare per 2⁸ è come
spostare di 8 bit a sinistra, e sommare numeri che non hanno bit in comune è
come farne l'OR.

Nota il `-> int` nella firma: è una **type hint**, un'annotazione facoltativa che
Python **non controlla** a runtime. Serve a chi legge (e agli strumenti di
analisi). L'ho messa proprio perché è il punto in cui il porting perde
l'informazione di tipo che in C era obbligatoria — è un modo di recuperarla
senza rinunciare alla flessibilità.

**Traduzione — il test di classe:**

```c
if ((Ip[i].a & classiIp[j].mask) == classiIp[j].leading)
{
  Ip[i].netid = Ip[i].ip & classiIp[j].netmask;
  ...
}
```
```python
nid = 0                     # nel C i globali partono già a 0
for j, (mask, leading, netmask) in enumerate(CLASSI_IP):
    if (a & mask) == leading:
        nid = ip & netmask
        print(...)
netid.append(nid)
```

* **`&` è identico** in C e Python: AND bit a bit. Anche `|`, `^`, `~`, `<<`,
  `>>` sono uguali. Questa è la parte che **non cambia per niente**, ed è bene
  saperlo dire: la manipolazione dei bit è la stessa in tutti e due i linguaggi.
* **Le parentesi in `(a & mask) == leading` servono davvero.** In C `&` ha
  precedenza **più bassa** di `==`, quindi senza parentesi si leggerebbe
  `a & (mask == leading)`, che è tutt'altro. In Python la precedenza è più
  sensata (`&` lega più forte di `==`), ma **le ho tenute lo stesso**: sono
  gratis e tolgono ogni dubbio a chi legge.
* **`return` al primo match** = il `break` mancante del C.
* **`return None`** copre il caso classe D/E, che il C non gestisce.
* **`chr(ord('A') + j)`** traduce `'A' + j` del C. È di nuovo l'aritmetica sui
  caratteri (§0.6): in C `'A'` è il numero 65 e `'A'+2` è 67 = `'C'`. In Python
  `ord('A')` dà 65, ci sommo `j`, e `chr()` torna al carattere. Più verboso, ma
  esplicito: si vede che stai passando da carattere a numero e ritorno.

**Traduzione — la stampa:**

```c
printf("\n%3d.%3d.%3d.%3d", Ip[i].a, Ip[i].b, Ip[i].c, Ip[i].d);
printf("classe %c (mask: %x)e netId %X", 'A'+j, classiIp[j].netmask, Ip[i].netid);
```
```python
print(f"{a:3d}.{b:3d}.{c:3d}.{d:3d} class {classe} "
      f"(netmask: {netmask:08x}) and netId {nid:08X}")
```

* `%3d` → `{a:3d}`: intero allineato a destra su 3 colonne. Serve a incolonnare
  l'output (nel libro si vede `10.  1.  0.  3`).
* `%x` → `{netmask:08x}` e `%X` → `{netid:08X}`: minuscolo e maiuscolo.
  **Ho aggiunto `08`** (8 cifre con zeri davanti) perché senza, un netId come
  `0x0A000000` verrebbe stampato `a000000` (7 cifre), mentre il libro nel suo
  output mostra `0A000000`. Il `printf` del libro dice `%X` senza padding: è una
  piccola incoerenza fra il codice stampato e l'output stampato, e ho seguito
  l'output.
* Nel C il testo del formato ha due refusi evidenti — manca lo spazio prima di
  `classe` e dopo `)`, e dice `mask:` mentre l'output del libro dice `netmask:`.
  Li ho **corretti**, allineandomi all'output.
* Le due `printf` diventano **un solo `print`**: `printf` non va a capo, quindi
  in C due chiamate consecutive scrivono sulla stessa riga; con `print` andrei a
  capo due volte. Le stringhe adiacenti su righe diverse in Python si concatenano
  automaticamente (`f"..." f"..."`), che è il modo pulito di spezzare una riga
  lunga.
* Il `\n` **iniziale** sparisce, per il motivo di §0.7.

### Righe 40-50 — il confronto a coppie

```c
for (i=0; i<4-1; i++)
  for (j=i+1; j<4; j++)
    if (Ip[i].netid == Ip[j].netid) { ... }
```

Questo è uno **schema classico** da saper riconoscere: *confrontare tutte le
coppie senza ripetizioni e senza confrontare un elemento con sé stesso*.

* `i` va da 0 a `n-2`;
* `j` parte da **`i+1`**, non da 0.

Così ottieni le coppie (0,1), (0,2), (0,3), (1,2), (1,3), (2,3) — sei coppie,
cioè "4 elementi presi 2 a 2". Se `j` partisse da 0 avresti anche (1,0) che è la
stessa di (0,1), e (0,0) che è un elemento con sé stesso.

**Traduzione — l'ho tenuta identica:**

```python
for i in range(len(INDIRIZZI) - 1):
    for j in range(i + 1, len(INDIRIZZI)):
        if info[i] is not None and info[i] == info[j]:
            x, y = INDIRIZZI[i], INDIRIZZI[j]
            ia, ib, ic, idd = INDIRIZZI[i]
            ja, jb, jc, jd = INDIRIZZI[j]
            print(f"{ia}.{ib}.{ic}.{idd} and {ja}.{jb}.{jc}.{jd} same net")
```

**Le scelte:**

1. **Schema del doppio ciclo invariato.** È l'algoritmo, non un dettaglio del C.
   *(Il modo più pythonico sarebbe `for x, y in itertools.combinations(...)`, che
   fa esattamente la stessa cosa in una riga. Ho preferito il doppio `for`
   perché così il confronto col libro è immediato — ma sapere che esiste
   `combinations` è un punto in più.)*
2. **`4` → `len(INDIRIZZI)`.** Elimina il numero magico: aggiungi un indirizzo e
   il codice si adatta da solo.
3. **`info[i] is not None`** — la guardia che chiude il bug della classe D/E
   descritto sopra. In C questo controllo non c'è e due indirizzi non
   classificabili risulterebbero sulla stessa rete.
4. **Spacchetto la tupla prima di stampare.** `ia, ib, ic, idd = INDIRIZZI[i]`
   assegna i quattro ottetti a quattro nomi in una riga sola, così la f-string
   resta leggibile: `f"{ia}.{ib}.{ic}.{idd}"`. È la corrispondenza esatta del
   `printf("%d.%d.%d.%d", Ip[i].a, Ip[i].b, Ip[i].c, Ip[i].d)` del C, che infatti
   passa anche lui i quattro campi uno per uno.
   *(Nota: `idd` e non `id`, perché `id` è una funzione predefinita di Python e
   riusarne il nome la nasconderebbe.)*

## 3.4 Verifica

```
 10.  1.  0.  3 class A (netmask: ff000000) and netId 0A000000
192.168.  0.  1 class C (netmask: ffffff00) and netId C0A80000
137.168.  0.  1 class B (netmask: ffff0000) and netId 89A80000
137.168.249. 17 class B (netmask: ffff0000) and netId 89A80000

137.168.0.1 and 137.168.249.17 same net
```

Identico al libro. **Controllo a mano** del terzo:
`137.168.0.1` → `0x89A80001`; classe B → netmask `0xFFFF0000`;
`0x89A80001 AND 0xFFFF0000 = 0x89A80000`.
Il quarto: `137.168.249.17` → `0x89A8F911`; stessa netmask →
`0x89A8F911 AND 0xFFFF0000 = 0x89A80000`. **Stesso netId ⟹ stessa rete.** ✔

---

# PROGRAMMA 4 — «Instradamento classful» (B3, pag. 129-130)

**File:** `punto2_porting_python/b3_p129_instradamento_classful.py`

## 4.1 Cosa deve fare

> Data la TdI dell'host A del caso descritto, realizzare l'instradamento di un
> pacchetto diretto a B5 (`196.13.2.5`).

## 4.2 Il sorgente C originale

```c
00 #include <stdio.h>
01
02 typedef struct {
03   unsigned char Ia,Ib,Ic,Id;  // colonna Indirizzo
04   unsigned char Ma,Mb,Mc,Md;  // colonna Mask
05   unsigned char Ga,Gb,Gc,Gd;  // colonna Gateway (next hop)
06   unsigned char Ua,Ub,Uc,Ud;  // colonna Use (interfaccia d'uscita)
07 } TDI;
08 TDI tdiHost[] = {
09   {   0,0,0,0,        0,0,0,0,  196,13,1,254,  196,13,1,1},
10   {196,13,1,0,  255,255,255,0,    196,13,1,1,  196,13,1,1}
11 };
12
13 unsigned int DottedToDecimal(unsigned char a, unsigned char b,
                                unsigned char c, unsigned char d);
14
15 int main (void)
16 {
17   int i;
18   unsigned char a,b,c,d;
19
20   printf("Indirizzo\tMask\t\tGateway\t\tUse\n");  // stampa della TdI
21   for (i=0; i<sizeof(tdiHost)/sizeof(TDI); i++)
22     printf("%d.%d.%d.%d\t%d.%d.%d.%d\t%d.%d.%d.%d\t%d.%d.%d.%d\n",
              tdiHost[i].Ia,tdiHost[i].Ib,tdiHost[i].Ic,tdiHost[i].Id,
              tdiHost[i].Ma,tdiHost[i].Mb,tdiHost[i].Mc,tdiHost[i].Md,
              tdiHost[i].Ga,tdiHost[i].Gb,tdiHost[i].Gc,tdiHost[i].Gd,
              tdiHost[i].Ua,tdiHost[i].Ub,tdiHost[i].Uc,tdiHost[i].Ud);
23
24   a=196;  b=13;  c=2;  d=5;  // Indirizzo da instradare
25   for (i=0; i<sizeof(tdiHost)/sizeof(TDI); i++)
26   {
27     unsigned int u;
28
29     printf("Regola n.%d per %d.%d.%d.%d: ",i+1,a,b,c,d);
30     u = DottedToDecimal(tdiHost[i].Ma,tdiHost[i].Mb,tdiHost[i].Mc,tdiHost[i].Md);
31     u = u & DottedToDecimal(a,b,c,d);
32
33     if (u == DottedToDecimal(tdiHost[i].Ia,tdiHost[i].Ib,tdiHost[i].Ic,tdiHost[i].Id))
34       printf(" vera.\n");
35     Else
36       printf(" falsa.\n");
37   }
38
39   return 0;
40 }
41
42
43 unsigned int DottedToDecimal(unsigned char a, unsigned char b,
                                unsigned char c, unsigned char d)
44 {
45   unsigned int ul;
46
47   ul = a*0x1000000 + b*0x10000 + c*0x100 + d;
48   return ul;
49 }
```

## 4.3 Analisi blocco per blocco

### Righe 02-11 — la TdI dell'host: 16 campi

```c
typedef struct {
  unsigned char Ia,Ib,Ic,Id;  // Indirizzo
  unsigned char Ma,Mb,Mc,Md;  // Mask
  unsigned char Ga,Gb,Gc,Gd;  // Gateway
  unsigned char Ua,Ub,Uc,Ud;  // Use
} TDI;
```

**Sedici campi separati** perché il C non ha un tipo «gruppo di quattro byte» da
usare comodamente: ogni ottetto è una variabile a sé. Il prezzo si vede subito
alla riga 22, dove la `printf` ha **sedici argomenti**.

**Traduzione:**

```python
TDI_HOST = [
    ((0, 0, 0, 0),    (0, 0, 0, 0),        (196, 13, 1, 254), (196, 13, 1, 1)),
    ((196, 13, 1, 0), (255, 255, 255, 0),  (196, 13, 1, 1),   (196, 13, 1, 1)),
]
```

**Una tupla di quattro tuple da quattro.** È la differenza più visibile di tutto
il porting, e la motivazione è forte: in Python posso **raggruppare** e poi
spacchettare per nome,

```python
for indirizzo, mask, gw, use in TDI_HOST:
```

mentre in C dovrei scrivere sedici accessi `tdiHost[i].Xy`. Il raggruppamento
riflette anche la **struttura logica**: una riga di TdI ha quattro *colonne*, non
sedici numeri. E rende banale scrivere una funzione che stampa un indirizzo
dotted, perché posso passarle la tupla intera.

Nota anche l'incolonnamento che ho lasciato nel sorgente: allineare le tuple in
verticale rende la tabella leggibile come una tabella. È la stessa cosa che fa il
libro alle righe 09-10, ed è una buona abitudine.

### Riga 13 — il prototipo

```c
unsigned int DottedToDecimal(unsigned char a, ...);
```

Un **prototipo** dichiara la firma di una funzione **prima** che venga usata,
perché il compilatore C legge il file dall'alto verso il basso e alla riga 30
deve già sapere quanti argomenti prende `DottedToDecimal` e cosa restituisce.
La definizione vera è alla riga 43, **dopo** `main`.

**Traduzione:** nessuna. In Python i nomi sono risolti **al momento della
chiamata**, non della definizione: basta che `dotted_to_decimal` esista quando
`main()` viene eseguita. Nel mio file la definisco comunque prima di `main`,
perché si legge meglio dall'alto al basso.

### Righe 20-22 — la stampa della TdI

```c
printf("Indirizzo\tMask\t\tGateway\t\tUse\n");
```

`\t` è il carattere di **tabulazione**: sposta il cursore al prossimo multiplo di
8 colonne. Il doppio `\t\t` serve perché «Mask» è corta e con un solo tab la
colonna successiva finirebbe troppo a sinistra. È un allineamento **fragile**:
basta che un valore sia più lungo del previsto e le colonne saltano.

**Traduzione:**

```python
print(f"{'Indirizzo':<17}{'Mask':<17}{'Gateway':<17}{'Use'}")
for indirizzo, mask, gw, use in TDI_HOST:
    print(f"{dotted(indirizzo):<17}{dotted(mask):<17}"
          f"{dotted(gw):<17}{dotted(use)}")
```

**Ho sostituito i tab con campi a larghezza fissa.** `{x:<17}` significa
«stringa allineata a **sinistra** (`<`) su 17 colonne, riempita di spazi».
Motivo: la larghezza è **esplicita e garantita**, non dipende dai multipli di 8
né dalla lunghezza del contenuto. È l'equivalente del `%-17s` di `printf`.

Per stampare gli indirizzi spacchetto le quattro tuple direttamente
nell'intestazione del `for`, usando **i nomi dei 16 campi della struct del
libro**:

```python
for (Ia, Ib, Ic, Id), (Ma, Mb, Mc, Md), (Ga, Gb, Gc, Gd), (Ua, Ub, Uc, Ud) in TDI_HOST:
    print(f"{Ia}.{Ib}.{Ic}.{Id}".ljust(17)
          + f"{Ma}.{Mb}.{Mc}.{Md}".ljust(17)
          + f"{Ga}.{Gb}.{Gc}.{Gd}".ljust(17)
          + f"{Ua}.{Ub}.{Uc}.{Ud}")
```

Così la corrispondenza con la `printf` a sedici argomenti del C è letterale:
gli stessi sedici nomi, nello stesso ordine. La differenza è che in Python li
ottieni con **una riga di spacchettamento** invece che con sedici accessi
`tdiHost[i].Xy`.

### Righe 25-37 — la valutazione delle regole

```c
u = DottedToDecimal(Ma,Mb,Mc,Md);      /* la mask della riga, come intero  */
u = u & DottedToDecimal(a,b,c,d);      /* AND con l'indirizzo destinazione */
if (u == DottedToDecimal(Ia,Ib,Ic,Id)) /* uguale all'indirizzo della riga? */
```

**Questa è la regola di instradamento e devi saperla a memoria:**

> `(IP_destinazione AND Mask_della_riga) == Indirizzo_della_riga` ⟹ regola vera

**Traduzione:**

```python
for i, (indirizzo, mask, gw, use) in enumerate(TDI_HOST, start=1):
    u = dotted_to_decimal(*mask)
    u = u & dotted_to_decimal(*DESTINAZIONE)
    esito = "true" if u == dotted_to_decimal(*indirizzo) else "false"
    print(f"rule n.{i} for {dest}: {esito}.")
```

* **I due passaggi su `u` restano identici al C**, righe 30-31: prima la mask
  in decimale, poi l'AND con l'indirizzo destinazione.
* **`*mask`** è lo spacchettamento: la tupla `(255,255,255,0)` diventa i quattro
  argomenti che `dotted_to_decimal` si aspetta. È qui che si vede il guadagno
  di aver raggruppato gli ottetti in tuple: nel C ogni chiamata costa quattro
  argomenti scritti a mano.
* **`enumerate(..., start=1)`** fa partire il contatore da 1: traduce l'`i+1`
  che il C scrive dentro la `printf`.
* **`"true" if ... else "false"`** è l'espressione condizionale, l'equivalente
  del ternario `cond ? a : b`. Sostituisce l'`if`/`Else` delle righe 33-36.

### Riga 35 — il bug che non compila

```c
Else
  printf(" falsa.\n");
```

**`Else` con la E maiuscola.** Il C è *case sensitive*: la parola chiave è
`else`. Così com'è, il sorgente **non compila**. Insieme a `unsigned intDottedToDecimal`
e `unsignedchar` (spazi mancanti, sempre nella stessa pagina), è chiaramente un
problema di impaginazione del libro, non un errore di progetto — ma è il tipo di
cosa che va segnalata.

### Righe 43-49 — `DottedToDecimal`

```c
unsigned int ul;
ul = a*0x1000000 + b*0x10000 + c*0x100 + d;
return ul;
```

Stessa espressione che nel programma 3 sta inline (vedi §3.3), qui con una
variabile temporanea `ul` che non serve a niente: si poteva scrivere
direttamente `return a*0x1000000 + ...`.

**Questa e' una delle due sole funzioni del porting**, e c'e' per un motivo
semplice: e' una funzione anche nel C. Nel programma 3 la stessa espressione e'
scritta inline dentro il ciclo (riga 30), e inline resta anche nel porting.

Ho tenuto **due funzioni con nomi diversi in due file diversi** invece di
scriverne una sola condivisa. Motivo: ogni file resta **autonomo**, come lo è
ogni programma del libro; puoi aprire un singolo file e capirlo senza cercare le
dipendenze. In un progetto vero le metterei in un modulo comune e le importerei.

## 4.4 L'unica aggiunta rispetto al C

Il codice C **si limita a stampare** «vera» o «falsa» per ogni riga. Non decide
niente. Ma il testo di pag. 129 spiega la regola che manca:

> «Anche in questo caso la regola è vera, ma siccome nel valore Mask i bit a uno
> sono più numerosi, tra le due si sceglie questa.»

È il **longest prefix match**. Nel porting l'ho implementato:

```python
for i, riga in enumerate(TDI_HOST, start=1):
# fra le regole true vince quella con la mask più lunga (pag.129):
# una mask più lunga, letta come intero, è anche più grande
best = -1
for indirizzo, mask, gw, use in TDI_HOST:
    m = dotted_to_decimal(*mask)
    if (dotted_to_decimal(*DESTINAZIONE) & m) == dotted_to_decimal(*indirizzo):
        if m > best:
            best, scelta_gw, scelta_use = m, gw, use
print("\n-> next hop {}.{}.{}.{} on interface {}.{}.{}.{}"
Ga, Gb, Gc, Gd = scelta_gw
Ua, Ub, Uc, Ud = scelta_use
print(f"\n-> next hop {Ga}.{Gb}.{Gc}.{Gd} on interface {Ua}.{Ub}.{Uc}.{Ud}")
```

**Sii onesto su questo:** è un'**estensione**, non una traduzione. Se il prof
chiede «il porting è fedele?», la risposta è *«sì tranne le ultime tre righe,
che implementano la regola descritta nel testo di pag.129 ma assente dal
codice»*.

**Il trucco da saper spiegare:** non serve contare i bit a 1 della mask.
Una mask più lunga, letta come **intero a 32 bit**, è anche **numericamente più
grande** — `255.255.255.0` = 4294967040 contro `0.0.0.0` = 0 — perché i bit a 1
stanno tutti a sinistra. Quindi «mask più lunga» e «mask più grande» sono la
stessa cosa, e `max(..., key=...)` basta e avanza.

`max(sequenza, key=funzione)` restituisce l'elemento per cui `funzione` dà il
valore più alto. La `lambda` è una funzione anonima scritta al volo:
`lambda r: dotted_to_decimal(*r[1])` significa «di ogni riga `r` prendi il campo
1 (la mask), spacchettalo e convertilo in intero».

`enumerate(..., start=1)` fa partire il contatore da 1 invece che da 0: traduce
il `i+1` che il C scrive dentro la `printf`.

Il confronto `m > best` sostituisce il conteggio dei bit: **non serve contare
gli `1` della mask**, perché una mask più lunga letta come intero a 32 bit è
anche numericamente più grande — i suoi bit a 1 stanno tutti a sinistra.
`255.255.255.0` vale 4294967040, `0.0.0.0` vale 0.

## 4.5 Verifica

```
Address          Mask             Gateway          Use
0.0.0.0          0.0.0.0          196.13.1.254     196.13.1.1
196.13.1.0       255.255.255.0    196.13.1.1       196.13.1.1

rule n.1 for 196.13.2.5: true.
rule n.2 for 196.13.2.5: false.

-> next hop 196.13.1.254 on interface 196.13.1.1
```

Le prime cinque righe coincidono col libro; l'ultima è l'aggiunta.
**Controllo a mano:**

* Regola 1: `196.13.2.5 AND 0.0.0.0 = 0.0.0.0`, uguale all'indirizzo della riga
  (`0.0.0.0`) ⟹ **vera**. È la *regola dei pacchetti stranieri*, sempre vera.
* Regola 2: `196.13.2.5 AND 255.255.255.0 = 196.13.2.0`, diverso da `196.13.1.0`
  ⟹ **falsa**. Giusto: `196.13.2.5` sta su un'altra rete di classe C.

Essendo vera solo la prima, il pacchetto va al **gateway di default**: consegna
indiretta. Coerente con la teoria di pag. 127-128.

---

# PROGRAMMA 5 — «Calcolo delle subnet» (B3, pag. 134-135)

**File:** `punto2_porting_python/b3_p134_subnetting.py`

## 5.1 Cosa deve fare

> Dato un indirizzo IP privato e una subnet mask in formato CIDR (direttamente
> il numero dei bit a 1), calcolare e stampare tutte le subnet disponibili.

È il programma più ricco di **manipolazione di bit** e quello con il bug più
vistoso del libro.

## 5.2 Il sorgente C originale

```c
00 #include <stdio.h>
01 #include "dectoszbin.c"
02
03 typedef struct {
04   unsigned char id1,id2;   // identificativi classi private
05   unsigned int netmasklen; // lunghezza netmask
06 } PRIVATEIP;
07 PRIVATEIP Ipp[] = {{10,0,8},{172,16,16},{192,168,24}};
08
09
10 int main (void)
11 {
12   int i,idx;
13   unsigned char a,b,c,d,subnetlen,hostlen;
14   unsigned int subnetmask, subnetid, u;
15   char szBin[32];
16
17   a=192;  b=168;  c=0;  d=0;  // indirizzo IP privato da usare
18   Subnetmask = 26;            // subnet mask da applicare
19
20   idx = -1;
21   for (i=0;i<3;i++)
22     if (a==Ipp[i].id1) idx = i;  // gruppo privato individuato
23   if (idx==-1) return 1;
24
25   subnetlen = subnetmask - Ipp[idx].netmasklen;
26   if (subnetmask<Ipp[idx].netmasklen) return 2;
27
28   hostlen = 32 - subnetmask;
29   subnetid = 1<<subnetlen;
30   DectoszBin(subnetid-1,subnetlen,szBin);
31
32   printf("Rete privata del gruppo %d.%d.%d.%d (netmask /%d)\n",
              Ipp[idx].id1,Ipp[idx].id2,0,0,Ipp[idx].netmasklen);
33   printf("Subnet Mask /%d; subnetid: %s\n",subnetmask,szBin);
34   printf("Subnet disponibili:\n");
35   for (i=0;i<subnetid;i++)
36   {
37     u = i << hostlen;
38     switch (idx)
39     {
40       case 0:
41         printf("%d.%d.%d.%d\n",
                  Ipp[idx].id1,(u & 0x00ff0000)>>16,(u & 0x0000ff00)>>8,(u & 0x000000ff));
42         break;
43       case 1:
44         printf("%d.%d.%d.%d\n",
                  Ipp[idx].id1,Ipp[idx].id2,(u & 0x0000ff00)>>8,(u & 0x000000ff));
45         break;
46       case 2:
47         printf("%d.%d.%d.%d\n",
                  Ipp[idx].id1,Ipp[idx].id2,Ipp[idx].id2,(u & 0x000000ff));
48         break;
49     }
50   }
51
52   return 0;
53 }
```

## 5.3 Analisi blocco per blocco

### Riga 01 — includere un file `.c`

```c
#include "dectoszbin.c"
```

Due cose da notare:

1. **Virgolette invece di parentesi angolari.** `<stdio.h>` cerca nelle directory
   di sistema; `"dectoszbin.c"` cerca **prima nella directory del sorgente**.
   Le virgolette si usano per i propri file, le angolari per le librerie.
2. **Include di un `.c`, non di un `.h`.** È una pratica sconsigliata: normalmente
   si include l'*header* (le dichiarazioni) e si compila il `.c` a parte. Qui il
   libro incolla direttamente il codice della funzione. Funziona finché lo fai in
   un solo punto; se lo includessi in due file avresti la funzione definita due
   volte e l'errore in fase di *link*.

Il file `dectoszbin.c` **non è nel nostro capitolo** (il libro dice che sta nel
PROGRAMMA «Autonegoziazione»), quindi l'ho **reimplementato**:

```python
def dec_to_bin(valore: int, nbit: int) -> str:
    return f"{valore:0{nbit}b}"
```

Dal nome (`Dec to sz Bin` = *decimal to zero-terminated binary string*) e dalla
chiamata `DectoszBin(subnetid-1, subnetlen, szBin)` si capisce la firma:
*(valore da convertire, numero di bit, buffer di destinazione)*. In C il
risultato si restituisce **riempiendo un buffer passato dal chiamante**, perché
una funzione C non può restituire un array. In Python la funzione **restituisce
la stringa**, che è la cosa naturale.

`f"{valore:0{nbit}b}"` si legge così: dopo i due punti c'è la **format spec**,
cioè `0{nbit}b` = «in **b**inario, su `nbit` cifre, riempiendo con **0**».
Il pezzo `{nbit}` **dentro la spec** è a sua volta un campo sostituito: le
f-string permettono di annidare, quindi la larghezza può essere una variabile
invece di un numero fisso. Esempio: `dec_to_bin(3, 2)` → `"11"`.

È l'equivalente dell'`*` di `printf("%0*d", larghezza, valore)` in C.

### Righe 03-07 — i gruppi privati

```c
typedef struct {
  unsigned char id1,id2;   // es. 192 e 168
  unsigned int netmasklen; // es. 24
} PRIVATEIP;
PRIVATEIP Ipp[] = {{10,0,8},{172,16,16},{192,168,24}};
```

Sono i tre lotti della **RFC 1918** che hai studiato a pag. 132:

| `id1.id2` | `netmasklen` | rete privata |
|---|---|---|
| `10.0` | 8 | `10.0.0.0/8` |
| `172.16` | 16 | `172.16.0.0/16` |
| `192.168` | 24 | `192.168.0.0/24` ← **il libro usa /24, non /16** |

> Segnala questa cosa: il lotto privato di classe C è in realtà
> `192.168.0.0/16` (256 reti di classe C contigue), ma il libro qui lo modella
> come **una singola** rete `/24`. Non è sbagliato come esercizio — sta
> "subnettando una rete di classe C" — ma non coincide con la tabella di pag. 132.

**Traduzione:** lista di tuple, per i soliti motivi.

```python
GRUPPI_PRIVATI = [
    (10, 0, 8),
    (172, 16, 16),
    (192, 168, 24),
]
```

### Righe 17-18 — l'input hard coded (e il secondo refuso)

```c
a=192;  b=168;  c=0;  d=0;
Subnetmask = 26;
```

Il libro lo dichiara: *«per ridurre il numero di righe del programma, si
forniscono i due dati direttamente nel codice (hard coded), righe 17-18»*.

`Subnetmask` con la **S maiuscola** è un refuso come l'`Else` del programma 4:
la variabile dichiarata alla riga 14 è `subnetmask`. Non compila.

Nota anche che `b`, `c`, `d` sono assegnate ma **mai usate**: al programma serve
solo `a` (il primo ottetto) per identificare il gruppo privato. Codice morto.

**Traduzione:** i due dati diventano **parametri di funzione**.

```python
a = 192                     # C righe 17-18: i due dati sono hard coded
subnetmask = 26
```

**Restano hard coded come nel libro.** Trasformarli in parametri di funzione
renderebbe il programma riusabile senza modificarlo, ma il libro dichiara
esplicitamente la scelta opposta («per ridurre il numero di righe del programma,
si forniscono i due dati direttamente nel codice»), e il porting la rispetta.

Per provare un altro caso si cambiano le due righe, esattamente come faresti col
C. Cambiando in `a = 172` e `subnetmask = 20` il programma stampa le 16 sottoreti
della figura di pag. 139: è una verifica indipendente molto utile, perché usa il
ramo `idx == 1` e un risultato che il libro riporta altrove.

### Righe 20-23 — trovare il gruppo privato

```c
idx = -1;
for (i=0;i<3;i++)
  if (a==Ipp[i].id1) idx = i;
if (idx==-1) return 1;
```

Ricerca lineare con sentinella `-1`. **Non c'è `break`**: il ciclo prosegue anche
dopo aver trovato, quindi `idx` finisce per contenere l'**ultima** corrispondenza.
Qui non conta perché i tre `id1` (10, 172, 192) sono distinti, ma è la stessa
sciatteria del programma 1.

`return 1` da `main` è il **codice di uscita** del processo: per convenzione 0 =
tutto bene, diverso da 0 = errore. È l'unico canale di errore che ha `main`.

**Traduzione:**

```python
idx = next((i for i, g in enumerate(GRUPPI_PRIVATI) if g[0] == a), -1)
if idx == -1:
    raise ValueError(f"{a}.x.x.x non e' un gruppo di indirizzi privati")
```

**Due scelte da spiegare:**

1. **`next(generatore, default)`** è il modo idiomatico Python di dire «dammi il
   **primo** elemento che soddisfa la condizione, altrimenti il default». Il
   pezzo fra parentesi è una *generator expression*: produce gli indici `i` che
   soddisfano il test, ma **pigramente**, uno alla volta. `next` ne prende uno e
   si ferma — quindi il `break` mancante nel C qui c'è di fatto, gratis.

2. **`raise ValueError` invece di `return 1`.** Un `return 1` **si può ignorare**:
   se nessuno controlla il valore di ritorno, l'errore passa inosservato.
   Un'eccezione **non si può ignorare**: o la catturi con `try/except` o il
   programma si ferma dicendo cosa è andato storto. In più il messaggio spiega il
   problema, mentre `1` non dice niente. Stesso discorso per il `return 2` della
   riga 26.

### Righe 25-29 — i calcoli e l'ordine sbagliato

```c
subnetlen = subnetmask - Ipp[idx].netmasklen;   /* riga 25: CALCOLA */
if (subnetmask < Ipp[idx].netmasklen) return 2; /* riga 26: CONTROLLA */
hostlen = 32 - subnetmask;
subnetid = 1<<subnetlen;
```

**Il controllo arriva dopo il calcolo.** Se `subnetmask` fosse minore di
`netmasklen` (es. `/8` su `192.168.0.0/24`), la riga 25 farebbe `8 - 24 = -16`,
ma `subnetlen` è `unsigned char`: non può essere negativo, quindi il valore
"gira" e diventa un numero enorme. Solo *dopo* il programma se ne accorge e
ritorna. In questo caso specifico non fa danni perché ritorna subito, ma
l'ordine giusto è **sempre controllare prima di calcolare**.

Nel porting ho invertito, e ho aggiunto un controllo che nel C non c'è:

```python
if subnetmask < netmasklen:
    raise ValueError(...)
if subnetmask > 30:
    raise ValueError("subnet mask troppo lunga: non restano host")

subnetlen = subnetmask - netmasklen
hostlen = 32 - subnetmask
n_subnet = 1 << subnetlen
```

Il controllo `> 30` viene dalla teoria: servono almeno 2 bit di hostId perché,
tolti *nome della subnet* e *broadcast*, resti almeno un indirizzo assegnabile
(§ indirizzi speciali RFC 1009).

**Il nome `subnetid` è fuorviante** e l'ho cambiato. Guarda cosa contiene:

```c
subnetid = 1<<subnetlen;   /* con subnetlen=2: 1<<2 = 4 */
```

Non è un *subnet id*, è il **numero di sottoreti**. Un subnetId sarebbe `00`,
`01`, `10`, `11`. L'ho rinominato `n_subnet`. Rinominare bene è parte del
porting: un nome sbagliato è un commento sbagliato che non puoi ignorare.

**Lo shift `1 << subnetlen`** è la cosa da saper spiegare: spostare `1` a
sinistra di `n` posizioni dà **2ⁿ**. Con 2 bit di subnetId ottieni 4 sottoreti.
È l'operazione preferita perché è **una singola istruzione della CPU**, mentre
elevare a potenza no. In Python `<<` esiste identico, quindi l'ho tenuto:
avrei potuto scrivere `2 ** subnetlen`, ma lo shift è più aderente e mostra che
hai capito il ragionamento sui bit.

### Riga 30 — la subnetId massima in binario

```c
DectoszBin(subnetid-1, subnetlen, szBin);
```

`subnetid - 1` = `4 - 1` = 3 = `11` in binario su 2 bit. Stampa quindi la
**subnetId più alta** possibile, che serve a far vedere quanti bit occupa il
campo. Output del libro: `subnetid: 11`.

```python
dec_to_bin(n_subnet - 1, subnetlen)
```

### Righe 32-34 — le intestazioni

```c
printf("Rete privata del gruppo %d.%d.%d.%d (netmask /%d)\n",
       Ipp[idx].id1, Ipp[idx].id2, 0, 0, Ipp[idx].netmasklen);
```

Nota i due `0` passati come argomenti costanti: sono il terzo e quarto ottetto,
sempre zero perché stiamo stampando l'**indirizzo di rete** del gruppo.

```python
print(f"private net del gruppo {id1}.{id2}.0.0 (netmask /{netmasklen})")
```

In Python li scrivo direttamente **dentro** la stringa: non ha senso passare due
costanti come argomenti quando puoi scriverle nel testo.

Una formula che il programma **non** stampa ma che devi sapere a memoria è
`(1 << hostlen) - 2`, cioè 2^hostlen meno 2: sono gli host **assegnabili** di
ogni sottorete. Il `-2` toglie il nome della subnet e l'indirizzo di broadcast
(§ indirizzi speciali RFC 1009). Con `/26`: `64 - 2 = 62`.

### Righe 35-37 — il cuore: enumerare le sottoreti

```c
for (i=0; i<subnetid; i++)
{
  u = i << hostlen;
```

**Due righe, ed è tutto il subnetting.**

`i` scorre da 0 a `n_subnet-1`: sono i valori possibili del **subnetId** (0, 1,
2, 3 → `00`, `01`, `10`, `11`). Lo shift `<< hostlen` li **sposta nella posizione
giusta**, cioè immediatamente a sinistra dell'hostId.

Esempio con `192.168.0.0/24` e mask `/26` (`subnetlen=2`, `hostlen=6`):

| `i` | binario di `i` | `i << 6` | valore | ultimo ottetto |
|---|---|---|---|---|
| 0 | `00` | `00000000` | 0 | `.0` |
| 1 | `01` | `01000000` | 64 | `.64` |
| 2 | `10` | `10000000` | 128 | `.128` |
| 3 | `11` | `11000000` | 192 | `.192` |

Ecco perché le sottoreti «saltano di 64»: il passo è **2^hostlen**.

**Traduzione: identica.**

```python
for i in range(n_subnet):
    u = i << hostlen
```

Qui non c'è niente da migliorare: lo shift è l'operazione giusta e Python ce l'ha
uguale. `for (i=0; i<n; i++)` → `for i in range(n)` è la corrispondenza più
diretta di tutto il porting.

### Righe 38-49 — lo `switch` e IL BUG

```c
switch (idx)
{
  case 0:   /* gruppo 10.x.x.x : 24 bit liberi, servono 3 ottetti */
    printf("%d.%d.%d.%d\n", Ipp[idx].id1,
           (u & 0x00ff0000)>>16, (u & 0x0000ff00)>>8, (u & 0x000000ff));
    break;
  case 1:   /* gruppo 172.16.x.x : 16 bit liberi, servono 2 ottetti */
    printf("%d.%d.%d.%d\n", Ipp[idx].id1, Ipp[idx].id2,
           (u & 0x0000ff00)>>8, (u & 0x000000ff));
    break;
  case 2:   /* gruppo 192.168.x.x : 8 bit liberi, serve 1 ottetto */
    printf("%d.%d.%d.%d\n", Ipp[idx].id1, Ipp[idx].id2,
           Ipp[idx].id2,                    /* <<<<<< QUI */
           (u & 0x000000ff));
    break;
}
```

**Prima: la tecnica di estrazione degli ottetti.**

```c
(u & 0x00ff0000) >> 16
```

Si legge in due passi: `& 0x00ff0000` **azzera tutto tranne** il terzo byte
(`ff` = otto bit a 1 nella posizione che interessa); `>> 16` lo **sposta in
fondo**, così il valore va da 0 a 255 ed è stampabile come ottetto.
È l'operazione inversa della conversione dotted -> intero.

| espressione | maschera | shift | ottetto estratto |
|---|---|---|---|
| `(u & 0xff000000) >> 24` | primo byte | 24 | 1° |
| `(u & 0x00ff0000) >> 16` | secondo byte | 16 | 2° |
| `(u & 0x0000ff00) >> 8` | terzo byte | 8 | 3° |
| `(u & 0x000000ff)` | quarto byte | 0 | 4° |

Il primo byte non serve mai qui, perché è sempre `id1`.

**Adesso il bug.** Nel `case 2` il terzo argomento è `Ipp[idx].id2`, cioè **168
di nuovo**. Doveva essere il terzo ottetto calcolato, che per un gruppo `/24`
vale sempre `0`. Risultato: l'output stampato a pag. 134 dice

```
192.168.168.0
192.168.168.64
192.168.168.128
192.168.168.192
```

**che è sbagliato**. Le sottoreti corrette di `192.168.0.0/24` con mask `/26`
sono `192.168.0.0`, `.64`, `.128`, `.192`. Il fatto che l'output *stampato nel
libro* contenga l'errore dimostra che il programma è stato davvero eseguito così
com'è, e che nessuno ha ricontrollato il risultato.

**Traduzione:**

```python
if idx == 0:            # 10.0.0.0/8  -> 24 bit liberi
    b = (u & 0x00FF0000) >> 16
    c = (u & 0x0000FF00) >> 8
    d = u & 0x000000FF
    print(f"{id1}.{b}.{c}.{d}/{subnetmask}")
elif idx == 1:          # 172.16.0.0/16 -> 16 bit liberi
    c = (u & 0x0000FF00) >> 8
    d = u & 0x000000FF
    print(f"{id1}.{id2}.{c}.{d}/{subnetmask}")
else:                   # 192.168.0.0/24 -> 8 bit liberi
    d = u & 0x000000FF
    print(f"{id1}.{id2}.0.{d}/{subnetmask}")
```

**Le scelte:**

1. **`switch` → `if/elif/else`.** Python **non ha** lo `switch` classico (dalla
   3.10 esiste `match`, ma è pensato per il *pattern matching*, non per confronti
   di uguaglianza su interi). Con soli tre casi, `if/elif/else` è la traduzione
   diretta e leggibile.

   Vale la pena ricordare **perché in C lo `switch` ha bisogno dei `break`**:
   senza, l'esecuzione «cade» nel caso successivo (*fall-through*). È una fonte
   classica di bug. In Python il problema non esiste: i rami di `if/elif` sono
   mutuamente esclusivi per costruzione.

2. **Ho corretto il bug**: `.0.` al posto di `id2`. Il terzo ottetto **si
   calcola**, non si copia.

3. **Ho estratto gli ottetti in variabili con nome** (`b`, `c`, `d`) invece di
   infilare le espressioni dentro la `printf`. Nel C i quattro argomenti della
   `printf` sono tre espressioni di mascheratura più una costante, ed è
   esattamente per questo che il bug è passato inosservato: in mezzo a
   `(u & 0x0000ff00)>>8` un `Ipp[idx].id2` non salta all'occhio. Con una
   variabile per ottetto, l'errore sarebbe stato evidente.
   **Questa è la lezione di porting più importante del programma 5:** rendere
   esplicito ciò che è implicito fa emergere gli errori.

4. **Ho aggiunto `/{subnetmask}`** in fondo a ogni riga. Non è nel libro, ma la
   notazione CIDR è quella corretta per indicare una sottorete e la impari a
   pag. 144. È una piccola aggiunta didattica, dichiarala come tale.

## 5.4 Verifica

```
private net del gruppo 192.168.0.0 (netmask /24)
Subnet Mask /26; subnetid: 11
subnet available:
192.168.0.0
192.168.0.64
192.168.0.128
192.168.0.192
```

Le prime due righe coincidono col libro; le quattro sottoreti sono **corrette**
(il libro stampa `192.168.168.x` per il bug).

Il secondo caso, `172.16.0.0` con `/20`, produce le 16 sottoreti
`172.16.0.0`, `172.16.16.0`, `172.16.32.0` … `172.16.240.0`: **identiche** a
quelle della figura di pag. 139. È una verifica indipendente forte, perché usa il
ramo `idx == 1`, dati diversi e un risultato che il libro riporta altrove.

---

# PARTE 6 — Riepilogo

## 6.1 Tabella di conversione C → Python

| C | Python | Nota |
|---|---|---|
| `int i;` `unsigned char p;` | *(niente)* | il tipo sta nel valore |
| `typedef struct {...} T;` | tupla / dizionario / classe | tupla se piccola e costante |
| `T v[] = {...};` | `V = [(...), (...)]` | MAIUSCOLO se costante |
| `sizeof(v)/sizeof(T)` | `len(v)` | l'array C non conosce la sua lunghezza |
| `for (i=0;i<n;i++)` | `for i in range(n)` | |
| `for` + `v[i]` | `for x in v` | o `enumerate(v)` se serve l'indice |
| `T* p; malloc; memcpy; free` | *(niente)* | garbage collector |
| `switch(x){case 1:...}` | `if/elif/else` o `dict[x]` | il dizionario è meglio se mappi dati |
| `break` nello switch | *(niente)* | in Python non c'è fall-through |
| `ch - '0'` | `int(ch)` | da cifra-carattere a numero |
| `n + '0'` in `%c` | `f"{n}"` | da numero a cifra-carattere |
| `'A' + j` | `chr(ord('A') + j)` | |
| `char s[3]` per `"R1"` | `"R1"` | in C c'è il terminatore `'\0'` |
| `printf("%d\n", n)` | `print(f"{n}")` | `printf` non va a capo, `print` sì |
| `%3d` `%x` `%X` `%s` `%c` | `{n:3d}` `{n:x}` `{n:X}` `{s}` `{c}` | |
| `\t` per allineare | `{s:<17}` | larghezza esplicita, più robusta |
| `sprintf(pc+n, ...)` in ciclo | `lista.append(...)` + `" ".join(...)` | le `str` sono immutabili |
| `getche()` (`conio.h`) | `input()` | `conio.h` è solo DOS/Windows |
| `&` `\|` `^` `~` `<<` `>>` | identici | **la parte che non cambia** |
| `cond ? a : b` | `a if cond else b` | |
| `return 1` / `return 2` per errore | `return []` | in Python la funzione ritorna il risultato, la lista vuota dice «niente» |
| `-1` come sentinella | `None` | `lista[-1]` è l'ultimo elemento: attenzione! |
| prototipo prima di `main` | *(niente)* | i nomi si risolvono alla chiamata |
| `#include <stdio.h>` | *(niente)* | `print`/`input` sono built-in |

## 6.2 Le cinque scelte che ho fatto sistematicamente

1. **Struct → tupla, array di struct → lista di tuple**, sfruttando lo
   spacchettamento per avere nomi leggibili senza sintassi pesante.
2. **Eliminare la gestione manuale della memoria e delle lunghezze** (`malloc`,
   `free`, `sizeof`, buffer fissi): in Python non servono e portavano con sé
   almeno un bug reale (§0.4).
3. **Tenere il codice lineare come il C.** I cicli che nel libro stanno dentro
   `main()` stanno dentro il flusso principale anche in Python, nello stesso
   ordine e con il riferimento alle righe originali nei commenti. Le uniche due
   funzioni sono quelle che sono funzioni anche nel C: `dotted_to_decimal()`
   (= `DottedToDecimal`) e `dec_to_bin()` (= `DectoszBin`).
4. **Sostituire i flag multi-stato con variabili esplicite** (`ok` + `mosso` al
   posto del solo `ok` a tre valori), che è l'unico punto in cui mi allontano
   dalla lettera del C — e lo faccio perché in Python `-1` è un indice valido.
5. **Lasciare hard coded ciò che il libro lascia hard coded**: i dati del
   programma 5 e il router di partenza del programma 2.

## 6.3 I bug del libro, in ordine di gravità

| # | Dove | Bug | Effetto |
|---|---|---|---|
| 1 | prog. 5, riga 47 | `id2` stampato come terzo ottetto | **output sbagliato**: `192.168.168.x` invece di `192.168.0.x` |
| 2 | prog. 2, riga 51 | `sizeof(tdi)` su un **puntatore** | scansione della TdI fuori dai limiti (salvata solo dal `break`) |
| 3 | prog. 4, riga 35 | `Else` maiuscolo | **non compila** |
| 4 | prog. 5, riga 18 | `Subnetmask` maiuscolo | **non compila** |
| 5 | prog. 5, righe 25-26 | controllo dopo il calcolo | underflow di `unsigned char` prima del controllo |
| 6 | prog. 1, riga 45 | testo dice «prima tripletta», codice prende l'**ultima** | testo e codice non coincidono |
| 7 | prog. 3, riga 30 | calcolo dentro il ciclo sbagliato | ricalcolato 3 volte, inefficienza |
| 8 | prog. 3, righe 40-50 | `netid` a 0 per classi D/E | due indirizzi non classificabili risulterebbero «stessa rete» |
| 9 | prog. 2, righe 43-49 | `malloc`+`memcpy`+`free` su tabella costante | 7 righe inutili |

## 6.4 Domande probabili e risposte da tenere pronte

**«Perché in Python non hai dichiarato i tipi?»**
Perché in Python il tipo è una proprietà dell'oggetto, non del nome: viene
determinato a runtime. In C serve al compilatore per sapere quanti byte allocare.
Python permette le *type hint* (`def f(x: int) -> str:`), ma sono annotazioni
per chi legge, non vincoli: non le ho usate perché il libro non ne ha bisogno.

**«Perché una tupla e non una classe?»**
Perché questi record sono piccoli (3-4 campi), **costanti** e letti sempre per
intero. La tupla è immutabile — quindi la topologia non può essere modificata per
sbaglio — e lo spacchettamento mi dà nomi leggibili gratis. Con record più grandi
o con metodi userei una classe o una `dataclass`.

**«Cos'era `sizeof` e perché è sparito?»**
`sizeof` restituisce la dimensione in byte. Serviva perché in C l'array non
conosce la propria lunghezza: la si calcola come byte totali diviso byte di un
elemento. In Python la lista è un oggetto che sa quanto è lunga, quindi `len()`.
Ed è la ragione per cui il bug del programma 2 in Python non può esistere.

**«Cosa fa `ch - '0'`?»**
Converte una cifra-carattere nel numero corrispondente, sfruttando il fatto che i
codici ASCII delle cifre sono consecutivi (`'0'` = 48). `'3' - '0'` = 51 - 48 = 3.
In Python è `int(ch)`, perché `str` e `int` sono tipi distinti che non si sommano.

**«Perché hai messo un limite ai cicli che nel C non c'era?»**
Perché il `while` del programma 2 non ha nessuna condizione di terminazione
garantita: con dati incoerenti — e i dati del libro lo sono, ci sono porte che non
esistono — girerebbe per sempre. Un ciclo limitato è la stessa idea del TTL nel
programma 1 e del campo TTL nel pacchetto IP.

**«Il porting è fedele al C?»**
Sì per la logica, con **tre eccezioni dichiarate**: ho corretto il bug del terzo
ottetto nel programma 5, ho aggiunto la scelta *longest prefix match* nel
programma 4 (descritta nel testo di pag. 129 ma assente dal codice), e ho aggiunto
controlli di errore dove il C andava in loop o in overflow silenzioso.

**«Qual è la differenza più importante fra i due linguaggi, in questo codice?»**
La gestione della memoria e delle strutture dati. In C metà del codice serve a
dire alla macchina *dove* stanno i dati e *quanti* sono (puntatori, `sizeof`,
buffer, terminatori). In Python quella metà sparisce e resta solo l'algoritmo —
che è esattamente quello che il capitolo vuole insegnare.

