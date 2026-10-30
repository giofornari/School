# WAN con 5 router, PT Cloud e modem DSL — routing statico completo

Guida operativa + motivazioni. Ogni scelta è spiegata in modo che tu possa difenderla all'orale.

---

## 0. Cosa chiede davvero l'esercizio

Tre cose, in ordine:

1. **Riprodurre la topologia** del video: 5 router (R_1…R_5), 6 sottoreti "nuvola" (A–F), accesso agli host tramite modem DSL.
2. **Popolare le nuvole**: almeno un host per sottorete. Il senso della nota del prof è che una nuvola non è un oggetto misterioso — è *una sottorete IP come tutte le altre*. Il video lo dice esplicitamente: «anche la rete E è una rete che collega fra loro due router... dal punto di vista degli indirizzamenti non c'è nessuna differenza».
3. **Routing statico su tutti i router**, in modo che *ogni* sottorete raggiunga *ogni* altra. Con 10 reti e 5 router significa che ogni router deve avere in tabella tutte e 10 le reti (direttamente connesse + statiche).

---

## 1. Il problema che troverai (e che devi saper spiegare)

**Il Cloud-PT non è uno switch né un hub.** Non fa apprendimento MAC e non inoltra a broadcast. Inoltra il traffico **solo sulle coppie di porte che gli mappi esplicitamente** nella tab `Config → CONNECTIONS`:

| Tab | Cosa mappa |
|---|---|
| `DSL` | una porta **Modem (RJ-11)** ↔ una porta **Ethernet** |
| `Cable` | una porta **Coax** ↔ una porta **Ethernet** |
| `Frame Relay` | una porta **Serial** ↔ un'altra **Serial** (via DLCI) |

Non esiste una mappatura Modem↔Modem né Ethernet↔Ethernet. Il video [2] lo mostra: due PC dietro due modem DSL sulla stessa nuvola **non si pingano fra loro**, pur pingando entrambi il server a monte. La spiegazione ufficiale sul forum Cisco è la stessa: *"Cloud has from port / to port links that you must link... notice that Cloud is not same as hub or switch."*

**Conseguenza sul tuo schema:** le nuvole **A, B, C, D** sono terminali (1 router + host) → nessun problema, basta la mappatura `Modem0 ↔ Ethernet0`.
Le nuvole **E** ed **F** invece stanno *in mezzo a due router*: E collega R_4 e R_5, F collega R_2 e R_5. Servirebbe un inoltro Ethernet↔Ethernet, che la nuvola non sa fare. **La rete non funzionerebbe.**

### Soluzione adottata: uno switch dentro le sottoreti E ed F

Una sottorete IP è un **dominio di broadcast** di livello 2. Il Cloud-PT, nel nostro schema, non è "la sottorete": è solo il **DSLAM**, cioè l'apparato di accesso che porta il doppino dell'utente dentro la rete dell'operatore. Il dominio di broadcast va realizzato con un dispositivo di livello 2 vero: uno **switch**.

Quindi in E e in F:

```
R_4 ──┐                                 ┌── R_2
      ├─ Switch E ── Cloud E ══ DSL Mod E ── PC E     (stesso schema per F,
R_5 ──┘   (L2)      (DSLAM)   (doppino)               con R_2 e R_5)
```

Tutti — R_4, R_5, PC E — restano nella **stessa /24** (160.80.4.0/24). L'indirizzamento e le tabelle di routing non cambiano di una virgola rispetto al video. Cambia solo la realizzazione fisica.

> **Frase da usare all'orale:** «Il Cloud-PT modella il DSLAM, cioè l'accesso; non è un dispositivo di livello 2 general purpose, inoltra solo sulle coppie porta-porta configurate. Per realizzare il dominio di broadcast della sottorete ho usato uno switch, esattamente come nella rete di un ISP reale dove il DSLAM si attesta su uno switch di aggregazione.»

Nota: è lo stesso pattern del video [2], dove la porta Gigabit della nuvola va su uno switch 2960 e da lì al resto della rete dell'operatore.

---

## 2. Inventario apparati e moduli

### Router (Router-PT)
Spegni il router (interruttore in **Physical**), inserisci i moduli, riaccendi. Modulo da usare: **PT-ROUTER-NM-1CFE** (una porta FastEthernet rame).

| Router | Interfacce necessarie | Verso |
|---|---|---|
| R_1 | 4 | rete A, R_2, R_3, R_4 |
| R_2 | 4 | rete B, R_1, R_3, rete F |
| R_3 | 3 | rete C, R_1, R_2 |
| R_4 | 2 | rete E, R_1 |
| R_5 | 3 | rete D, rete E, rete F |

> Il nome dell'interfaccia dipende dallo **slot** in cui infili la scheda (slot *N* → `FastEthernet N/0`). Dopo l'inserimento controlla sempre con `show ip interface brief` e adatta i comandi.

### Nuvole (Cloud-PT) — 6 pezzi
Parti dalla **cloud vuota**, spegnila, e inserisci:

| Nuvola | Moduli | Motivo |
|---|---|---|
| A, B, C, D | 1× **PT-CLOUD-NM-1CFE** (Ethernet) + 1× **PT-CLOUD-NM-1AM** (RJ-11) | 1 porta verso il router + 1 doppino verso il modem |
| E, F | 1× **PT-CLOUD-NM-1CFE** + 1× **PT-CLOUD-NM-1AM** | la porta Ethernet va allo **switch** della sottorete, non direttamente a un router |

### Altri
- 6× **DSL-Modem-PT** (uno per nuvola). Nessuna configurazione: è un bridge trasparente. `Port 0` = doppino RJ-11, `Port 1` = Ethernet verso l'utente.
- **Switch C** (già nel tuo schema) dietro il modem DSL C, per i due PC C1/C2.
- **Switch E** e **Switch F**: i due switch aggiunti al punto 1.
- 7 PC.

---

## 3. Piano di indirizzamento

Schema del video: `160.80.X.0/24`, maschera `255.255.255.0` ovunque. Le reti punto-punto fra router **hanno bisogno di un indirizzo di rete proprio** esattamente come quelle popolate: il fatto che non ci siano PC è irrilevante ai fini del routing.

### Sottoreti popolate (le "nuvole")

| Rete | Indirizzo | Router attestati | Host |
|---|---|---|---|
| **A** | 160.80.1.0/24 | R_1 = .1 | PC A = .10 |
| **D** | 160.80.2.0/24 | R_5 = .1 | PC D = .10 |
| **B** | 160.80.3.0/24 | R_2 = .1 | PC B = .10 |
| **E** | 160.80.4.0/24 | R_4 = .1, R_5 = .2 | PC E = .10 |
| **C** | 160.80.5.0/24 | R_3 = .1 | PC C1 = .10, PC C2 = .11 |
| **F** | 160.80.6.0/24 | R_2 = .1, R_5 = .2 | PC F = .10 |

### Reti di transito (link router-router, senza host)

| Rete | Indirizzo | Estremi |
|---|---|---|
| R_1–R_2 | 160.80.7.0/24 | R_1 = .1, R_2 = .2 |
| R_1–R_4 | 160.80.8.0/24 | R_1 = .1, R_4 = .2 |
| R_2–R_3 | 160.80.9.0/24 | R_2 = .1, R_3 = .2 |
| R_1–R_3 | 160.80.10.0/24 | R_1 = .1, R_3 = .2 |

**Criterio usato:** il router "di numero più basso" prende `.1`, l'altro `.2`; nelle reti popolate il default gateway degli host è sempre `.1`. Un criterio qualsiasi va bene, ma dev'essere **coerente** — all'orale ti verrà chiesto perché hai scelto quel numero, e la risposta giusta è: *«qualunque indirizzo host valido della sottorete, purché unico; ho adottato una convenzione per rendere la tabella leggibile»*.

### Configurazione degli host

| PC | IP | Maschera | Default gateway |
|---|---|---|---|
| PC A | 160.80.1.10 | 255.255.255.0 | 160.80.1.1 (R_1) |
| PC D | 160.80.2.10 | 255.255.255.0 | 160.80.2.1 (R_5) |
| PC B | 160.80.3.10 | 255.255.255.0 | 160.80.3.1 (R_2) |
| PC E | 160.80.4.10 | 255.255.255.0 | 160.80.4.1 (R_4) |
| PC C1 | 160.80.5.10 | 255.255.255.0 | 160.80.5.1 (R_3) |
| PC C2 | 160.80.5.11 | 255.255.255.0 | 160.80.5.1 (R_3) |
| PC F | 160.80.6.10 | 255.255.255.0 | 160.80.6.1 (R_2) |

> **Punto fine da citare all'orale.** In E e in F ci sono **due** router sulla stessa sottorete. PC E ha un solo default gateway (R_4): quando manda un pacchetto verso la rete D, R_4 lo rimanda indietro *sulla stessa interfaccia* verso R_5 (percorso "a forcina", *hairpin*). Funziona, ma è subottimale: in una rete reale R_4 emetterebbe un **ICMP Redirect** per dire a PC E «per quella destinazione usa direttamente R_5». Il caso mostra perché un host con un solo default gateway non sempre imbocca il percorso ottimo.

---

## 4. Cablaggio: quale cavo, dove

| Collegamento | Cavo |
|---|---|
| PC ↔ DSL Modem (`Port 1`) | Copper Straight-Through |
| PC ↔ Switch | Copper Straight-Through |
| DSL Modem (`Port 0`) ↔ Cloud (`Modem0`) | **Phone** (RJ-11, tratteggiato) |
| Cloud (`Ethernet0`) ↔ Router | Copper **Cross-Over** |
| Cloud (`Ethernet0`) ↔ Switch (E, F) | Copper Straight-Through |
| Router ↔ Router | Copper **Cross-Over** |
| Router ↔ Switch | Copper Straight-Through |

Regola mnemonica: **dispositivi dello stesso "livello" → cross-over** (router-router, PC-PC, switch-switch); **livelli diversi → straight-through** (PC-switch, router-switch). Il Cloud-PT si comporta da apparato "terminale" come un PC, quindi verso un router serve il cross-over. In Packet Tracer puoi usare il cavo **Automatico** (fulmine) se hai fretta, ma all'esame è meglio saper motivare la scelta.

---

## 5. Configurazione delle nuvole (il passo che quasi tutti sbagliano)

Per **ogni** nuvola, dopo aver cablato:

1. Click sulla nuvola → tab **Config**.
2. Nella colonna di sinistra, sotto **CONNECTIONS**, scegli **DSL**.
3. Nei due menu a tendina: a sinistra **`Modem0`**, a destra **`Ethernet0`** (o il nome effettivo delle tue porte).
4. Premi **Add**. La coppia deve comparire nella lista a destra.

**Perché serve.** La nuvola rappresenta un DSLAM: raccoglie N doppini e li riversa su una o poche porte Ethernet verso la rete dell'operatore. Il DSLAM non "indovina" l'associazione: va programmata. Senza questa riga, il pacchetto entra dal modem e viene scartato — è esattamente l'errore che il video [2] mostra e poi corregge («*that's the part that I was missing*»).

**Se una nuvola dovesse servire più utenze** (es. più modem DSL sulla stessa nuvola) aggiungi una riga per ogni modem, tutte verso la stessa porta Ethernet: `Modem0↔Ethernet0`, `Modem1↔Ethernet0`, … Resta vero che i due modem **non si parlano fra loro**: il traffico fra due utenti dello stesso DSLAM deve risalire fino al router e ridiscendere. È il comportamento corretto di un DSLAM in *split horizon*.

Il **modem DSL** non richiede nessuna configurazione.

---

## 6. Configurazione dei router — interfacce

Assegnazione usata (adatta i nomi ai tuoi slot):

| Router | Interfaccia | IP | Verso |
|---|---|---|---|
| **R_1** | Fa0/0 | 160.80.1.1 | rete A |
| | Fa1/0 | 160.80.7.1 | R_2 |
| | Fa2/0 | 160.80.10.1 | R_3 |
| | Fa3/0 | 160.80.8.1 | R_4 |
| **R_2** | Fa0/0 | 160.80.3.1 | rete B |
| | Fa1/0 | 160.80.7.2 | R_1 |
| | Fa2/0 | 160.80.9.1 | R_3 |
| | Fa3/0 | 160.80.6.1 | rete F |
| **R_3** | Fa0/0 | 160.80.5.1 | rete C |
| | Fa1/0 | 160.80.10.2 | R_1 |
| | Fa2/0 | 160.80.9.2 | R_2 |
| **R_4** | Fa0/0 | 160.80.4.1 | rete E |
| | Fa1/0 | 160.80.8.2 | R_1 |
| **R_5** | Fa0/0 | 160.80.2.1 | rete D |
| | Fa1/0 | 160.80.4.2 | rete E |
| | Fa2/0 | 160.80.6.2 | rete F |

Su ogni interfaccia serve **`no shutdown`**: in Packet Tracer le porte dei router nascono amministrativamente spente. Se dalla GUI usi la spunta **On**, è la stessa cosa.

---

## 7. Come si costruisce una tabella di routing (il metodo del video)

Per ogni router, scorri **tutte e 10 le reti** e per ognuna rispondi a 4 domande:

1. **La rete è direttamente connessa a questo router?**
   - **Sì** → tipo `diretto`, **next hop assente**, interfaccia di uscita = l'IP dell'interfaccia del router su quella rete, **metrica 0**.
   - **No** → tipo `indiretto`, si prosegue.
2. **Qual è il percorso con il minor numero di hop?** Hop = numero di router da attraversare *oltre* a quello di partenza.
3. **Qual è il next hop?** L'indirizzo IP dell'**interfaccia del router vicino** sulla rete che condividi con lui. *Non* è l'indirizzo della rete di destinazione e *non* è un tuo indirizzo.
4. **Qual è l'interfaccia di uscita?** L'IP della **tua** interfaccia sulla stessa rete del next hop.

Errore classico: mettere come next hop un indirizzo che non appartiene a una rete direttamente connessa. Il router lo rifiuta (o installa una rotta inutilizzabile): il next hop deve essere **raggiungibile a livello 2**, cioè sul filo.

**Rotte equivalenti.** Quando due percorsi hanno lo stesso numero di hop, puoi metterli entrambi (ridondanza) oppure sceglierne uno. Nelle tabelle sotto la riga senza etichetta è quella che ho messo in configurazione; le righe marcate *(alt)* sono alternative equivalenti che puoi citare all'orale o aggiungere.

---

## 8. Le 5 tabelle di routing

Maschera `255.255.255.0` per tutte le righe.

### R_1 — direttamente connesso a A, 7, 8, 10

| Destinazione | Tipo | Next hop | Interfaccia uscita | Metrica | Percorso |
|---|---|---|---|---|---|
| 160.80.1.0 (A) | diretto | — | 160.80.1.1 | 0 | — |
| 160.80.2.0 (D) | indiretto | 160.80.8.2 | 160.80.8.1 | 2 | R_4 → R_5 |
| 160.80.2.0 (D) *(alt)* | indiretto | 160.80.7.2 | 160.80.7.1 | 2 | R_2 → R_5 |
| 160.80.3.0 (B) | indiretto | 160.80.7.2 | 160.80.7.1 | 1 | R_2 |
| 160.80.4.0 (E) | indiretto | 160.80.8.2 | 160.80.8.1 | 1 | R_4 |
| 160.80.5.0 (C) | indiretto | 160.80.10.2 | 160.80.10.1 | 1 | R_3 |
| 160.80.6.0 (F) | indiretto | 160.80.7.2 | 160.80.7.1 | 1 | R_2 |
| 160.80.7.0 | diretto | — | 160.80.7.1 | 0 | — |
| 160.80.8.0 | diretto | — | 160.80.8.1 | 0 | — |
| 160.80.9.0 | indiretto | 160.80.7.2 | 160.80.7.1 | 1 | R_2 |
| 160.80.9.0 *(alt)* | indiretto | 160.80.10.2 | 160.80.10.1 | 1 | R_3 |
| 160.80.10.0 | diretto | — | 160.80.10.1 | 0 | — |

### R_2 — direttamente connesso a B, F, 7, 9

| Destinazione | Tipo | Next hop | Interfaccia uscita | Metrica | Percorso |
|---|---|---|---|---|---|
| 160.80.1.0 (A) | indiretto | 160.80.7.1 | 160.80.7.2 | 1 | R_1 |
| 160.80.2.0 (D) | indiretto | 160.80.6.2 | 160.80.6.1 | 1 | R_5 |
| 160.80.3.0 (B) | diretto | — | 160.80.3.1 | 0 | — |
| 160.80.4.0 (E) | indiretto | 160.80.6.2 | 160.80.6.1 | 1 | R_5 |
| 160.80.5.0 (C) | indiretto | 160.80.9.2 | 160.80.9.1 | 1 | R_3 |
| 160.80.6.0 (F) | diretto | — | 160.80.6.1 | 0 | — |
| 160.80.7.0 | diretto | — | 160.80.7.2 | 0 | — |
| 160.80.8.0 | indiretto | 160.80.7.1 | 160.80.7.2 | 1 | R_1 |
| 160.80.9.0 | diretto | — | 160.80.9.1 | 0 | — |
| 160.80.10.0 | indiretto | 160.80.7.1 | 160.80.7.2 | 1 | R_1 |
| 160.80.10.0 *(alt)* | indiretto | 160.80.9.2 | 160.80.9.1 | 1 | R_3 |

### R_3 — direttamente connesso a C, 9, 10

| Destinazione | Tipo | Next hop | Interfaccia uscita | Metrica | Percorso |
|---|---|---|---|---|---|
| 160.80.1.0 (A) | indiretto | 160.80.10.1 | 160.80.10.2 | 1 | R_1 |
| 160.80.2.0 (D) | indiretto | 160.80.9.1 | 160.80.9.2 | 2 | R_2 → R_5 |
| 160.80.3.0 (B) | indiretto | 160.80.9.1 | 160.80.9.2 | 1 | R_2 |
| 160.80.4.0 (E) | indiretto | 160.80.9.1 | 160.80.9.2 | 2 | R_2 → R_5 |
| 160.80.4.0 (E) *(alt)* | indiretto | 160.80.10.1 | 160.80.10.2 | 2 | R_1 → R_4 |
| 160.80.5.0 (C) | diretto | — | 160.80.5.1 | 0 | — |
| 160.80.6.0 (F) | indiretto | 160.80.9.1 | 160.80.9.2 | 1 | R_2 |
| 160.80.7.0 | indiretto | 160.80.10.1 | 160.80.10.2 | 1 | R_1 |
| 160.80.7.0 *(alt)* | indiretto | 160.80.9.1 | 160.80.9.2 | 1 | R_2 |
| 160.80.8.0 | indiretto | 160.80.10.1 | 160.80.10.2 | 1 | R_1 |
| 160.80.9.0 | diretto | — | 160.80.9.2 | 0 | — |
| 160.80.10.0 | diretto | — | 160.80.10.2 | 0 | — |

### R_4 — direttamente connesso a E, 8

| Destinazione | Tipo | Next hop | Interfaccia uscita | Metrica | Percorso |
|---|---|---|---|---|---|
| 160.80.1.0 (A) | indiretto | 160.80.8.1 | 160.80.8.2 | 1 | R_1 |
| 160.80.2.0 (D) | indiretto | 160.80.4.2 | 160.80.4.1 | 1 | R_5 |
| 160.80.3.0 (B) | indiretto | 160.80.8.1 | 160.80.8.2 | 2 | R_1 → R_2 |
| 160.80.3.0 (B) *(alt)* | indiretto | 160.80.4.2 | 160.80.4.1 | 2 | R_5 → R_2 |
| 160.80.4.0 (E) | diretto | — | 160.80.4.1 | 0 | — |
| 160.80.5.0 (C) | indiretto | 160.80.8.1 | 160.80.8.2 | 2 | R_1 → R_3 |
| 160.80.6.0 (F) | indiretto | 160.80.4.2 | 160.80.4.1 | 1 | R_5 |
| 160.80.7.0 | indiretto | 160.80.8.1 | 160.80.8.2 | 1 | R_1 |
| 160.80.8.0 | diretto | — | 160.80.8.2 | 0 | — |
| 160.80.9.0 | indiretto | 160.80.8.1 | 160.80.8.2 | 2 | R_1 → R_2/R_3 |
| 160.80.10.0 | indiretto | 160.80.8.1 | 160.80.8.2 | 1 | R_1 |

### R_5 — direttamente connesso a D, E, F

| Destinazione | Tipo | Next hop | Interfaccia uscita | Metrica | Percorso |
|---|---|---|---|---|---|
| 160.80.1.0 (A) | indiretto | 160.80.6.1 | 160.80.6.2 | 2 | R_2 → R_1 |
| 160.80.1.0 (A) *(alt)* | indiretto | 160.80.4.1 | 160.80.4.2 | 2 | R_4 → R_1 |
| 160.80.2.0 (D) | diretto | — | 160.80.2.1 | 0 | — |
| 160.80.3.0 (B) | indiretto | 160.80.6.1 | 160.80.6.2 | 1 | R_2 |
| 160.80.4.0 (E) | diretto | — | 160.80.4.2 | 0 | — |
| 160.80.5.0 (C) | indiretto | 160.80.6.1 | 160.80.6.2 | 2 | R_2 → R_3 |
| 160.80.6.0 (F) | diretto | — | 160.80.6.2 | 0 | — |
| 160.80.7.0 | indiretto | 160.80.6.1 | 160.80.6.2 | 1 | R_2 |
| 160.80.8.0 | indiretto | 160.80.4.1 | 160.80.4.2 | 1 | R_4 |
| 160.80.9.0 | indiretto | 160.80.6.1 | 160.80.6.2 | 1 | R_2 |
| 160.80.10.0 | indiretto | 160.80.6.1 | 160.80.6.2 | 2 | R_2 → R_1 |
| 160.80.10.0 *(alt)* | indiretto | 160.80.4.1 | 160.80.4.2 | 2 | R_4 → R_1 |

---

## 9. Comandi CLI pronti

Apri il router → tab **CLI** → invio → incolla. Verifica prima i nomi delle interfacce con `show ip interface brief`.

### R_1
```
enable
configure terminal
hostname R1
interface FastEthernet0/0
 description --> Rete A
 ip address 160.80.1.1 255.255.255.0
 no shutdown
exit
interface FastEthernet1/0
 description --> R2
 ip address 160.80.7.1 255.255.255.0
 no shutdown
exit
interface FastEthernet2/0
 description --> R3
 ip address 160.80.10.1 255.255.255.0
 no shutdown
exit
interface FastEthernet3/0
 description --> R4
 ip address 160.80.8.1 255.255.255.0
 no shutdown
exit
ip route 160.80.2.0 255.255.255.0 160.80.8.2
ip route 160.80.3.0 255.255.255.0 160.80.7.2
ip route 160.80.4.0 255.255.255.0 160.80.8.2
ip route 160.80.5.0 255.255.255.0 160.80.10.2
ip route 160.80.6.0 255.255.255.0 160.80.7.2
ip route 160.80.9.0 255.255.255.0 160.80.7.2
end
write memory
```

### R_2
```
enable
configure terminal
hostname R2
interface FastEthernet0/0
 description --> Rete B
 ip address 160.80.3.1 255.255.255.0
 no shutdown
exit
interface FastEthernet1/0
 description --> R1
 ip address 160.80.7.2 255.255.255.0
 no shutdown
exit
interface FastEthernet2/0
 description --> R3
 ip address 160.80.9.1 255.255.255.0
 no shutdown
exit
interface FastEthernet3/0
 description --> Rete F
 ip address 160.80.6.1 255.255.255.0
 no shutdown
exit
ip route 160.80.1.0 255.255.255.0 160.80.7.1
ip route 160.80.2.0 255.255.255.0 160.80.6.2
ip route 160.80.4.0 255.255.255.0 160.80.6.2
ip route 160.80.5.0 255.255.255.0 160.80.9.2
ip route 160.80.8.0 255.255.255.0 160.80.7.1
ip route 160.80.10.0 255.255.255.0 160.80.7.1
end
write memory
```

### R_3
```
enable
configure terminal
hostname R3
interface FastEthernet0/0
 description --> Rete C
 ip address 160.80.5.1 255.255.255.0
 no shutdown
exit
interface FastEthernet1/0
 description --> R1
 ip address 160.80.10.2 255.255.255.0
 no shutdown
exit
interface FastEthernet2/0
 description --> R2
 ip address 160.80.9.2 255.255.255.0
 no shutdown
exit
ip route 160.80.1.0 255.255.255.0 160.80.10.1
ip route 160.80.2.0 255.255.255.0 160.80.9.1
ip route 160.80.3.0 255.255.255.0 160.80.9.1
ip route 160.80.4.0 255.255.255.0 160.80.9.1
ip route 160.80.6.0 255.255.255.0 160.80.9.1
ip route 160.80.7.0 255.255.255.0 160.80.10.1
ip route 160.80.8.0 255.255.255.0 160.80.10.1
end
write memory
```

### R_4
```
enable
configure terminal
hostname R4
interface FastEthernet0/0
 description --> Rete E
 ip address 160.80.4.1 255.255.255.0
 no shutdown
exit
interface FastEthernet1/0
 description --> R1
 ip address 160.80.8.2 255.255.255.0
 no shutdown
exit
ip route 160.80.1.0 255.255.255.0 160.80.8.1
ip route 160.80.2.0 255.255.255.0 160.80.4.2
ip route 160.80.3.0 255.255.255.0 160.80.8.1
ip route 160.80.5.0 255.255.255.0 160.80.8.1
ip route 160.80.6.0 255.255.255.0 160.80.4.2
ip route 160.80.7.0 255.255.255.0 160.80.8.1
ip route 160.80.9.0 255.255.255.0 160.80.8.1
ip route 160.80.10.0 255.255.255.0 160.80.8.1
end
write memory
```

### R_5
```
enable
configure terminal
hostname R5
interface FastEthernet0/0
 description --> Rete D
 ip address 160.80.2.1 255.255.255.0
 no shutdown
exit
interface FastEthernet1/0
 description --> Rete E
 ip address 160.80.4.2 255.255.255.0
 no shutdown
exit
interface FastEthernet2/0
 description --> Rete F
 ip address 160.80.6.2 255.255.255.0
 no shutdown
exit
ip route 160.80.1.0 255.255.255.0 160.80.6.1
ip route 160.80.3.0 255.255.255.0 160.80.6.1
ip route 160.80.5.0 255.255.255.0 160.80.6.1
ip route 160.80.7.0 255.255.255.0 160.80.6.1
ip route 160.80.8.0 255.255.255.0 160.80.4.1
ip route 160.80.9.0 255.255.255.0 160.80.6.1
ip route 160.80.10.0 255.255.255.0 160.80.6.1
end
write memory
```

**Totale rotte statiche: 34.** Ogni router "vede" tutte e 10 le reti: quelle direttamente connesse arrivano gratis, le altre le hai scritte a mano.

---

## 10. Metrica sulla carta vs. IOS: la distinzione da conoscere

Nella tabella cartacea la colonna **metrica** contiene il **numero di hop**. È una grandezza didattica, quella che userebbe un protocollo distance-vector come RIP.

In IOS il numero che segue il next hop **non** è la metrica, è la **distanza amministrativa** (AD):

```
ip route 160.80.2.0 255.255.255.0 160.80.7.2 5
                                              ^ AD = 5, non "5 hop"
```

L'AD di default di una rotta statica è **1** (una connessa vale 0). Serve a scegliere fra rotte per la *stessa* destinazione apprese da sorgenti diverse: vince la AD più bassa.

Conseguenze pratiche sulle **rotte alternative** marcate *(alt)*:

- Se le inserisci **con la stessa AD**, IOS le installa entrambe e fa **load balancing a costo uguale** (ECMP): il traffico si divide sui due percorsi.
- Se vuoi che siano solo **backup**, dai alla seconda una AD maggiore (es. `... 160.80.7.2 5`): è la **floating static route**. Resta fuori dalla tabella finché la principale è valida, e subentra se l'interfaccia della principale cade.

> Limite del routing statico da citare all'orale: la floating static reagisce solo alla caduta della *propria interfaccia*, non a un guasto due hop più in là. È esattamente il motivo per cui esistono i protocolli dinamici (RIP, OSPF), che il video anticipa alla fine.

---

## 11. Rotta di default: serve qui?

**No, in questa rete no** — e devi saper spiegare perché.

La rotta di default `0.0.0.0 0.0.0.0` è la riga "per tutto il resto", l'ultima della tabella, usata quando nessuna altra riga fa match. Serve quando il router affaccia su un mondo che **non conosce** (tipicamente Internet). Qui le 10 reti sono tutte note e tutte in tabella: una default non aggiungerebbe raggiungibilità.

Diventa utile in due casi che puoi menzionare:

1. **Se aggiungessi un'uscita verso Internet**, per esempio da R_4. Allora su R_4: `ip route 0.0.0.0 0.0.0.0 <ip-del-provider>`, e sugli altri router `ip route 0.0.0.0 0.0.0.0 <next-hop-verso-R_4>`.
2. **Come semplificazione su un router stub.** R_4 ha solo due link: potresti sostituire 6 delle sue 8 rotte con una sola default verso R_1, tenendo esplicite solo quelle che passano da R_5:
   ```
   ip route 160.80.2.0 255.255.255.0 160.80.4.2
   ip route 160.80.6.0 255.255.255.0 160.80.4.2
   ip route 0.0.0.0 0.0.0.0 160.80.8.1
   ```
   Funziona ed è più elegante. Nel documento ho tenuto la versione esplicita perché la traccia chiede la *programmazione statica completa* e perché rende visibile il ragionamento su ogni singola rete.

---

## 12. Test e verifica

### Ordine di verifica (dal basso verso l'alto — non saltare passaggi)

1. **Link fisici**: tutti i triangolini verdi. Un triangolo rosso = interfaccia spenta (`no shutdown` mancante) o cavo sbagliato.
2. **Dentro ogni sottorete**: da ogni PC pinga il **proprio default gateway**.
   `PC A → 160.80.1.1`, `PC C1 → 160.80.5.1`, ecc.
   Se fallisce: quasi certamente manca la mappatura `Modem0 ↔ Ethernet0` nella nuvola.
3. **Fra router adiacenti**: da R_1 `ping 160.80.7.2`, `ping 160.80.10.2`, `ping 160.80.8.2`.
4. **Tabelle**: su ogni router `show ip route`. Devi contare **10 reti**: le `C` (connected) più le `S` (static).
5. **End-to-end**: ping incrociati fra PC di sottoreti diverse.
6. **Percorso**: da un PC, `tracert <ip>` per vedere i router attraversati e confrontarli con la colonna "Percorso" delle tabelle.

### Matrice di ping da compilare

| da \ verso | PC A | PC B | PC C1 | PC D | PC E | PC F |
|---|---|---|---|---|---|---|
| **PC A** | — | | | | | |
| **PC B** | | — | | | | |
| **PC C1** | | | — | | | |
| **PC D** | | | | — | | |
| **PC E** | | | | | — | |
| **PC F** | | | | | | — |

Tutte le 30 caselle devono dare risposta. (Il primo ping può fallire per l'ARP: rilancia.)

### Percorsi attesi (verificati simulando le tabelle)

| Da → a | Router attraversati | Hop |
|---|---|---|
| PC A → PC D | R_1 → R_4 → R_5 | 3 |
| PC C1 → PC F | R_3 → R_2 | 2 |
| PC E → PC B | R_4 → R_1 → R_2 | 3 |
| PC D → PC C2 | R_5 → R_2 → R_3 | 3 |

Il numero massimo di router attraversati in tutta la rete è **3**.

### Modalità Simulation
Passa in **Simulation**, filtra su **ICMP**, manda un ping da PC A a PC D e segui il PDU salto per salto. È il modo più efficace per far vedere all'orale che hai capito il meccanismo: a ogni router puoi aprire il PDU e mostrare che l'IP di destinazione non cambia mai, mentre il MAC di destinazione cambia a ogni tratta.

---

## 13. Diagnosi dei guasti più probabili

| Sintomo | Causa quasi certa |
|---|---|
| PC non pinga il proprio gateway, ma il link è verde | Manca `Modem0 ↔ Ethernet0` nella tab DSL della nuvola |
| PC E non pinga PC F, tutto il resto funziona | Manca lo switch in E o in F: la nuvola non inoltra Ethernet↔Ethernet |
| Interfaccia con triangolo rosso | Manca `no shutdown`, oppure cavo dritto dove serviva incrociato |
| `show ip route` mostra meno di 10 reti | Rotte statiche mancanti, oppure una `ip route` con next hop su una rete non direttamente connessa (IOS la accetta ma non la installa) |
| Ping va in un senso ma non torna | Rotta di ritorno mancante: **il routing è bidirezionale**, ogni router lungo il percorso deve conoscere *sia* la rete destinazione *sia* la rete sorgente |
| Solo il primo ping fallisce | Normale: risoluzione ARP. Ripeti |
| Ping da PC E verso D funziona ma il traceroute mostra un giro strano | È l'*hairpin* su R_4 spiegato al §3. Non è un errore |

Il penultimo punto è la domanda-trabocchetto più frequente: *«se aggiungo una rete nuova, quante tabelle devo toccare?»* → **tutte quelle dei router che devono raggiungerla, non solo quello a cui la attacchi.** Con N router e M reti il routing statico richiede fino a N×M righe: è il motivo per cui non scala.

---

## 14. Domande d'orale probabili — risposte pronte

**Perché le reti fra router hanno un indirizzo se non ci sono host?**
Perché sono sottoreti IP a tutti gli effetti: le due interfacce dei router che vi si affacciano hanno bisogno di indirizzi appartenenti alla stessa rete per potersi parlare a livello 3. Il fatto che non ci siano PC è irrilevante. Nota che con /24 sprechi 252 indirizzi: in una rete reale useresti /30 (2 host utili) o interfacce unnumbered.

**Che differenza c'è fra una nuvola che collega due router e una che contiene host?**
Nessuna, dal punto di vista dell'indirizzamento e del routing. È il punto esplicito del video. La differenza è solo di realizzazione fisica.

**Cos'è il next hop?**
L'indirizzo IP dell'interfaccia del router successivo, che deve trovarsi su una rete **direttamente connessa** al router che sta inoltrando. Non è l'indirizzo finale del pacchetto: quello resta invariato per tutto il percorso.

**Perché la metrica di una rotta diretta è 0?**
Perché non si attraversa nessun router intermedio: il pacchetto viene consegnato direttamente sul mezzo condiviso con la destinazione, dopo una risoluzione ARP.

**Perché hai scelto quel percorso e non l'altro?**
Criterio del minimo numero di hop. Dove i percorsi erano equivalenti l'ho detto esplicitamente, e ho la possibilità di inserirli entrambi (ECMP) o di usare il secondo come backup con distanza amministrativa più alta.

**Che limite ha il routing statico?**
Non si adatta: se cade un link, la tabella resta quella che ho scritto io e il traffico si perde, a meno di floating static che però reagiscono solo ai guasti locali. E il numero di righe cresce come N×M. Servono i protocolli dinamici (RIP distance-vector, OSPF link-state) che ricalcolano le tabelle da soli.

**A cosa serve la rotta di default?**
A gestire tutte le destinazioni non elencate in tabella: senza di essa il router scarta il pacchetto. In questa rete chiusa non serve, perché tutte le 10 reti sono note; servirebbe se ci fosse un'uscita verso Internet.

**Perché il Cloud-PT ha bisogno di essere configurato?**
Perché modella un DSLAM/apparato d'accesso dell'operatore, non uno switch: inoltra solo sulle coppie porta-porta che gli si programmano. Due modem sulla stessa nuvola non si parlano direttamente, il traffico deve risalire al router.

---

## 15. Checklist finale

- [ ] 5 router con il numero giusto di schede FastEthernet, accesi
- [ ] 6 nuvole con 1 modulo Ethernet + 1 modulo RJ-11
- [ ] Switch aggiunti nelle sottoreti E ed F (+ Switch C già presente)
- [ ] 6 modem DSL cablati: `Port 0` phone → nuvola, `Port 1` ethernet → PC/switch
- [ ] Mappatura `Modem0 ↔ Ethernet0` fatta su **tutte e 6** le nuvole
- [ ] Tutte le interfacce router configurate e in `no shutdown`
- [ ] 7 PC con IP, maschera **e default gateway**
- [ ] 34 rotte statiche inserite (6+6+7+8+7)
- [ ] `show ip route` mostra 10 reti su ogni router
- [ ] Matrice di ping 6×6 tutta verde
- [ ] File salvato

---

## Fonti

- [Configurazione del PT Cloud (Frame Relay) — packettracernetwork.com](https://www.packettracernetwork.com/tutorials/framerelay.html)
- [Cloud-PT, DSL-Modem-PT e moduli disponibili — guida ufficiale Packet Tracer](https://tutorials.ptnetacad.net/help/default/devicesAndModules_others.htm)
- [Il Cloud-PT non è uno switch: inoltra solo sulle coppie mappate — Cisco Community](https://community.cisco.com/t5/other-network-architecture-subjects/can-t-make-2-pc-s-on-a-cloud-network-connect-packet-tracer/td-p/4308372)
