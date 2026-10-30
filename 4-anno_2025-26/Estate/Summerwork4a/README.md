# Lavoro estivo — Sistemi e Reti (4ª → 5ª)

Indice di tutto il materiale, punto per punto della consegna.

## La consegna

> 1. Ripassare/Studiare capitoli **B1 (fino a pag. 94)** e **B3 (fino a pag. 144)**.
>    Fare il **porting dei sorgenti C** proposti, **in linguaggio Python**.
>    Svolgere gli **esercizi da pag. 101 a pag. 102** sul quaderno.
>    I capitoli saranno oggetto di **verifica la seconda settimana di scuola**.
> 2. Realizzare il progetto qui spiegato.
> 3. Realizzare **Progetto CPT - Smart Home IoT** qui spiegato.
> 4. Dopo aver studiato questo video, riprodurre la rete proposta, **completando
>    la programmazione statica di tutti i router**, in modo che tutte le
>    sottoreti possano raggiungere tutte le altre.
>    *Nota: trattandosi di una WAN, gli host si trovano nelle sottoreti (i nodi
>    PT cloud — le nuvolette), quindi dovrete aggiungerne almeno uno per
>    sottorete.*

## Stato

| # | Punto | Stato | Dove |
|---|---|---|---|
| 1a | Ripasso B1 + B3 | ✅ fatto | [`✅punto1_ripasso&esercizi/ripasso_B1_B3.md`](✅punto1_ripasso&esercizi/ripasso_B1_B3.md) |
| 1b | Porting C → Python | ✅ fatto | [`✅punto2_porting_python/`](✅punto2_porting_python/) — da consegnare: [`consegna/`](✅punto2_porting_python/consegna/) |
| 1c | Esercizi pag. 101–102 | ✅ svolti | [`✅punto1_ripasso&esercizi/esercizi_B1_p101-102.md`](✅punto1_ripasso&esercizi/esercizi_B1_p101-102.md) — **da ricopiare sul quaderno** |
| 2 | Progetto (link «qui spiegato») | ⛔ non iniziato | manca la traccia |
| 3 | Progetto CPT — Domotica e IoT | ✅ progettato | [`punto3_smart_home_iot/`](punto3_smart_home_iot/) — **da costruire in Packet Tracer** |
| 4 | WAN, routing statico su 5 router | ✅ **completato** | [`✅punto4_WAN_packet_tracer/`](✅punto4_WAN_packet_tracer/) — `WAN.pkt` costruito |

**Resta aperto il punto 3:** il progetto è completo sulla carta, va costruito il
`.pkt` seguendo `guida_costruzione_pkt.md`. Il punto 4 è chiuso (`WAN.pkt`).

**Per il punto 2 serve la traccia**: nella consegna il link era la parola «qui»,
che nel copia-incolla si è persa. Senza quella non si può partire.

---

## Punto 1 — Ripasso, porting, esercizi

### `✅punto1_ripasso&esercizi/ripasso_B1_B3.md`
Sintesi per la verifica scritta. Copre B1 (livello 3, routing, CNLS/CONS, label
swapping, classificazione degli algoritmi) e B3 (classful, subnetting, indirizzi
speciali, internetwork, VLSM, supernetting/CIDR), più una checklist finale.

> ⚠️ **Da chiarire col prof.** Gli esercizi 13–17 di pag. 101–102 usano
> **distance vector** e **link state**, che sul libro stanno alle **pp. 95–100**,
> cioè *oltre* il limite di pag. 94 indicato nella consegna. Il documento ha
> un'appendice con l'essenziale per risolverli, ma vale la pena chiedere se
> quelle pagine rientrano o no nella verifica: cambia parecchio cosa studiare.

### `✅punto2_porting_python/`
Cinque programmi del libro tradotti in Python 3, senza dipendenze, più i
flowchart Mermaid e una suite di test.

```bash
cd ✅punto2_porting_python
python3 b1_p087_hops.py
```

Il codice è **lineare come il C**: quello che il libro fa dentro `main()` sta
nel flusso principale anche in Python, nello stesso ordine, con il riferimento
alle righe originali nei commenti (`# C righe 31-44`). Le uniche due funzioni
sono quelle che sono funzioni anche nel C — `DottedToDecimal` e `DectoszBin`.

Il README della cartella documenta le corrispondenze C → Python, **i bug del
sorgente C del libro** e la verifica riga per riga contro i box OUTPUT stampati.
Il bug più vistoso è a pag. 134: il `case 2` stampa `id2` due volte, quindi
l'output sul libro dice `192.168.168.0`, `192.168.168.64`… mentre le sottoreti
corrette di `192.168.0.0/24` con mask `/26` sono `192.168.0.0`, `.64`, `.128`,
`.192`. Il porting stampa quelle corrette e la nota spiega perché diverge dalla
pagina: così la differenza è dimostrabile, non sospetta.

Questa è la parte da citare all'orale se il prof chiede «cosa hai imparato
facendo il porting»: la risposta forte non è «ho tradotto la sintassi», è
«ho trovato e motivato gli errori dell'originale».

### `punto2_porting_python/guida_al_porting.md`
**Il documento da studiare per saper difendere il porting a voce.** Analizza i
cinque sorgenti C **riga per riga**, e per ogni scelta di traduzione spiega
*cosa* faceva il C, *come* l'ho reso in Python e **perché**.

* **Parte 0** — le 10 differenze che tornano in tutti i programmi: tipizzazione,
  `struct` → tupla, `sizeof` → `len`, puntatori e `malloc`, aritmetica sui
  caratteri (`- '0'`), `printf` → f-string, stringhe immutabili, `getche()`,
  interi a 32 bit vs illimitati.
* **Programmi 1-5** — sorgente C completo, analisi blocco per blocco, verifica
  del risultato con traccia a mano.
* **Parte 6** — tabella di conversione C → Python, i 9 bug del libro in ordine
  di gravità, e **7 domande probabili con la risposta già pronta**.

### `✅punto1_ripasso&esercizi/esercizi_B1_p101-102.md`
I 17 esercizi svolti con lo schema **traccia → metodo → svolgimento passo passo
→ risultato**. All'inizio ci sono le convenzioni usate (`Add | P | h | c`,
notazione delle intestazioni L2/L3, look-up table CONS) con la verifica di dove
sono state ricavate dalle figure del libro — utile se il prof contesta una
notazione.

**Vanno ricopiati sul quaderno**: la consegna dice «sul quaderno», il file serve
come brutta copia ragionata, non come consegna.

---

## Punto 4 — WAN con 5 router, PT Cloud e modem DSL

Cartella [`✅punto4_WAN_packet_tracer/`](✅punto4_WAN_packet_tracer/):

| File | Cosa contiene |
|---|---|
| `guida_configurazione.md` | Guida completa: moduli da inserire, cablaggio, configurazione delle nuvole, tabelle di routing di tutti e 5 i router, comandi CLI, piano di test, domande d'orale con risposte |
| `tabelle_routing.html` | Le stesse tabelle in versione interattiva, con modalità quiz che nasconde next hop e metrica |
| `verifica_routing.py` | Verifica automatica delle tabelle **prima** di configurare |

```bash
cd ✅punto4_WAN_packet_tracer
python3 verifica_routing.py     # 50 casi router→rete + 40 ping host→host
```

### I tre punti da saper spiegare

**1. Il Cloud-PT non è uno switch.** Inoltra solo sulle coppie porta-porta che
gli si mappano nella tab `Config → DSL` (Modem ↔ Ethernet). Non esiste una
mappatura Ethernet ↔ Ethernet. Conseguenza: le nuvole **E** ed **F**, che nello
schema stanno *in mezzo* a due router, non farebbero passare il traffico fra
loro. Servono due switch, uno per sottorete, a cui si attestano i due router e
la porta Ethernet della nuvola. Il Cloud-PT modella il **DSLAM**, cioè
l'apparato d'accesso, non il dominio di broadcast.

**2. Una nuvola è una sottorete come tutte le altre.** È il punto esplicito del
video: che dentro ci siano host o che sia solo un collegamento fra due router,
per l'indirizzamento e per il routing non cambia niente. Anche le reti
punto-punto fra router hanno bisogno del loro indirizzo di rete.

**3. Metrica sulla carta ≠ metrica in IOS.** Nella tabella cartacea la metrica è
il numero di hop. In IOS il numero dopo il next hop è la **distanza
amministrativa**: due rotte equivalenti con la stessa AD danno load balancing,
per avere un backup serve una AD più alta (*floating static route*).

### Piano di indirizzamento in breve

Schema `160.80.X.0/24` ripreso dal video.

| Sottoreti popolate | | Reti di transito | |
|---|---|---|---|
| A | 160.80.1.0 | R1–R2 | 160.80.7.0 |
| D | 160.80.2.0 | R1–R4 | 160.80.8.0 |
| B | 160.80.3.0 | R2–R3 | 160.80.9.0 |
| E | 160.80.4.0 | R1–R3 | 160.80.10.0 |
| C | 160.80.5.0 | | |
| F | 160.80.6.0 | | |

10 reti, 34 rotte statiche (6 su R1, 6 su R2, 7 su R3, 8 su R4, 7 su R5).
Massimo 3 router attraversati fra due host qualsiasi.

---

## Punto 3 — Domotica e IoT

Cartella [`punto3_smart_home_iot/`](punto3_smart_home_iot/): villa su un piano
con garage e giardino, 6 VLAN, 3 SSID su wireless ibrido (WLC + LAP e AP
autonomi), 21 dispositivi IoT, accesso da Internet e
un sottosistema a microcontrollore per il punteggio extra.

| File | Cosa contiene |
|---|---|
| `relazione_progettuale.md` | Il documento valutato: architettura, VLAN, Wi-Fi, servizi, sicurezza, limiti — ogni scelta motivata |
| `planimetria.svg` | Pianta con la posizione di tutti gli apparati |
| `dispositivi_e_automazioni.md` | I 21 dispositivi e le 10 regole di automazione |
| `configurazioni_cli.md` | Configurazioni complete di router, switch, AP, server |
| `guida_costruzione_pkt.md` | 12 fasi, ognuna con il suo test |
| `mcu/` | Codice della centralina, JavaScript e Python |

Copre tutti e sette i requisiti della traccia più il punteggio extra. La cosa da
sapere: la traccia dice che *«non saranno valutate soltanto le funzionalità
implementate, ma anche la capacità di motivare e descrivere le soluzioni
adottate»*, quindi la relazione conta quanto il `.pkt`.

**Non verificato:** il supporto WPA3 in Packet Tracer 8.2.1. Controlla il menu
`Authentication` del tuo access point prima di scriverlo in relazione — WPA2
soddisfa comunque il requisito «WPA2/WPA3».

---

## Punto 2 — manca la traccia

Nel testo della consegna il link era sulla parola «qui» e non è sopravvissuto al
copia-incolla. Serve la pagina o il PDF del progetto per poter partire.

---

## Ordine di lavoro consigliato

1. **Recuperare la traccia del punto 2** — è la cosa che blocca di più e non
   dipende da te; chiedila subito.
2. **Chiedere se pp. 95–100 rientrano nella verifica** (vedi sopra).
3. **Costruire il `.pkt` del punto 3**: 3–4 ore, la fase lunga sono i 21
   dispositivi IoT. Segui le 12 fasi e testa a ogni fase.
5. **Ricopiare gli esercizi sul quaderno.**
6. **Punto 2** appena arriva la traccia.
7. **Ripasso finale** con la checklist in fondo a `ripasso_B1_B3.md`.
