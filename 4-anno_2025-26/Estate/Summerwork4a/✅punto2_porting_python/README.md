# Porting Python dei sorgenti C — capitoli B1 e B3

Ollari, *Corso di Sistemi e Reti* vol. 2, Zanichelli.
Python 3 standard, nessuna dipendenza.

```bash
python3 b1_p087_hops.py
```

| File | Libro | Cosa fa |
|---|---|---|
| `b1_p087_hops.py` | B1 p.87 | Percorso di un pacchetto fra R1..R4 usando triplette `(ra, rb, porta)` |
| `b1_p090_routing_cnls.py` | B1 p.90–91 | Routing CNLS *next hop*: consulta la TdI di ogni router e salta al successivo |
| `b3_p126_classful_netid.py` | B3 p.126–127 | Classe di appartenenza e netId di 4 indirizzi; quali stanno sulla stessa rete |
| `b3_p129_instradamento_classful.py` | B3 p.129–130 | Stampa la TdI di un host e valuta le regole di instradamento (AND con la mask) |
| `b3_p134_subnetting.py` | B3 p.134–135 | Elenco delle sottoreti ottenibili da una rete privata con una subnet mask |

`guida_al_porting.md` analizza i cinque sorgenti C riga per riga e spiega ogni
scelta di traduzione. I file `.mmd` sono i flowchart in formato Mermaid.

## Struttura del codice: lineare come il C

Il C del libro fa tutto dentro `main()`. Il porting fa lo stesso: **codice
lineare, letto dall'alto verso il basso**, con i riferimenti alle righe del
sorgente originale nei commenti (`# C righe 31-44`).

Le **uniche due funzioni** sono quelle che sono funzioni anche nel C:

| Funzione Python | Corrisponde a |
|---|---|
| `dotted_to_decimal()` in `b3_p129` | `DottedToDecimal()`, C righe 43–49 |
| `dec_to_bin()` in `b3_p134` | `DectoszBin()`, che il libro include da `dectoszbin.c` |

Questo rende il confronto fra i due sorgenti immediato: a ogni blocco di C
corrisponde un blocco di Python nello stesso ordine.

## Corrispondenze C → Python

| C | Python |
|---|---|
| `struct` + array di struct | lista di tuple |
| `char ra[3]` con `ra[1]` per il numero | `int(ra[1])` sulla stringa |
| `sizeof(v)/sizeof(T)` per contare gli elementi | `len(lista)`, o iterazione diretta |
| `malloc` + `memcpy` + `free` | niente: si legge direttamente la lista |
| `switch (r) { case 1: ... }` | `TDI[r]`, accesso al dizionario |
| `getche()` (conio.h, solo Windows/DOS) | `input()` |
| `chS - '0'` / `rm + '0'` | `int(chS)` / f-string `f"R{rm}"` |
| `sprintf(pc+n, ...)` per accodare a stringa | `lista.append(...)` + `" ".join(...)` |
| `printf("%X", v)` | f-string `f"{v:08X}"` |
| `return 0` / `return 1` da `main` | `raise SystemExit` |
| `1 << subnetlen` | identico, Python ha gli stessi operatori bit a bit |

## Bug del libro corretti (e perché)

1. **`b1_p090` — `for (i=0; i<sizeof(tdi); i++)`**
   `tdi` è un *puntatore*: `sizeof` restituisce 4 o 8, non il numero di righe.
   Serviva `sizeof(tdiR1)/sizeof(TDI)`. In Python si itera sulla lista e il
   problema non esiste.

2. **`b1_p090` — `malloc` + `memcpy` + `free` (righe 43-49)**
   Non è un errore di correttezza — `tdi` è una variabile **globale**, quindi il
   C la azzera all'avvio e `free(NULL)` è legale — ma sono **7 righe inutili**:
   copiano in memoria dinamica una tabella costante che non viene mai
   modificata. Bastava `tdi = tdiR1;`.

3. **`b3_p129` — `Else`** con la E maiuscola: non compila.
   Anche `unsigned intDottedToDecimal` e `unsignedchar` sono refusi di
   impaginazione (mancano gli spazi).

4. **`b3_p134` — `case 2:`** stampa `Ipp[idx].id2` **due volte**, quindi come
   terzo ottetto esce `168` invece di `0`. È il motivo per cui l'OUTPUT
   stampato a pag.134 dice `192.168.168.0`, `192.168.168.64`… che è sbagliato.
   Le sottoreti corrette di `192.168.0.0/24` con mask `/26` sono:
   `192.168.0.0`, `192.168.0.64`, `192.168.0.128`, `192.168.0.192`.
   Sempre a pag.134: `Subnetmask = 26;` con la S maiuscola.

5. **`b1_p087` — scelta della tripletta di ripiego.**
   Il testo dice «si prende la *prima* tripletta d'uscita dal router», ma il
   codice non fa `break` in quel ramo, quindi `ok` finisce per contenere
   l'*ultima*. Comportamento riprodotto fedelmente (non cambia i risultati
   sulla topologia a catena del libro), segnalato nei commenti.

## Verifica: confronto con i box OUTPUT del libro

Eseguito a mano, programma per programma. Le stringhe a video sono state
tradotte in inglese, quindi va confrontato il **contenuto**, non la lettera.

| Programma | Input | Libro | Ottenuto | |
|---|---|---|---|---|
| `b1_p087` | `3`, `1` | `Tratta: R3 R2` / `Tratta: R3 R2 R1  ok` | `track: R3 R2` / `track: R3 R2 R1` / `ok` | ✔ |
| `b1_p087` | `2`, `4` | caso (a): torna indietro | `track: R2 R1 R2 R3 R4` | ✔ |
| `b1_p087` | `1`, `9` | caso (c): TTL | `error TTL!` | ✔ |
| `b1_p090` | `a`, `c` | `Percorso: a R1 R2 R3 c` | `path: a R1 R2 R3 c` | ✔ |
| `b3_p126` | — | 4 righe classe/netId + «stessa rete» | `class A/C/B/B`, netId `0A000000` `C0A80000` `89A80000` `89A80000`, `same net` | ✔ |
| `b3_p129` | — | `Regola n.1 vera`, `Regola n.2 falsa` | `rule n.1 ... true.`, `rule n.2 ... false.` | ✔ |
| `b3_p134` | — | `subnetid: 11`, 4 subnet | `subnetid: 11`, `.0 .64 .128 .192` | ✔ (ottetto corretto, vedi bug 4) |

**Controlli fatti a mano sui numeri:**

* `137.168.0.1` → `0x89A80001`; classe B ⟹ netmask `0xFFFF0000`;
  `0x89A80001 AND 0xFFFF0000 = 0x89A80000`.
  `137.168.249.17` → `0x89A8F911 AND 0xFFFF0000 = 0x89A80000`. Stesso netId ✔
* `196.13.2.5 AND 0.0.0.0 = 0.0.0.0` = indirizzo riga 1 ⟹ vera (default route).
  `196.13.2.5 AND 255.255.255.0 = 196.13.2.0` ≠ `196.13.1.0` ⟹ falsa ✔
* `/26` su `/24`: `subnetlen = 2`, `hostlen = 6`, `n_subnet = 4`,
  passo `2⁶ = 64` ⟹ `.0`, `.64`, `.128`, `.192` ✔

**Verifica indipendente del ramo `idx == 1`:** cambiando le due righe hard coded
in `a = 172`, `subnetmask = 20` il programma stampa le 16 sottoreti
`172.16.0.0`, `172.16.16.0`, `172.16.32.0` … `172.16.240.0`, **identiche** alla
figura di pag. 139. Usa dati diversi e un risultato che il libro riporta
altrove, quindi è la conferma più forte che l'algoritmo è giusto.
