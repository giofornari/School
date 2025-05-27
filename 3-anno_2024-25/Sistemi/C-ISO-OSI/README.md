
# C-ISO-OSI: Simulazione Didattica dello Stack ISO/OSI in C 💻🌐

Questo progetto implementa una versione semplificata ("giocattolo") dello stack di protocolli ISO/OSI utilizzando il linguaggio C. L'obiettivo è dimostrare i concetti fondamentali di incapsulamento e decapsulamento dei dati attraverso i sette livelli del modello, simulando l'invio di un semplice messaggio di chat.

## 🎯 Obiettivo del Progetto

L'obiettivo principale è implementare 7 librerie C, una per ciascun livello dello stack ISO/OSI. Ogni livello è responsabile di:
1.  Aggiungere un **header specifico** durante la fase di invio (`*_send()`).
2.  Rimuovere e validare l'header corrispondente durante la fase di ricezione (`*_receive()`).
3.  Chiamare il livello sottostante durante l'invio e quello sovrastante durante la ricezione.

Questo progetto è pensato per essere sviluppato in team, con ogni membro responsabile di un singolo livello.

## ✨ Funzionalità Chiave

* **Simulazione Completa dei 7 Livelli:** Dall'Applicazione al Fisico.
* **Incapsulamento e Decapsulamento:** Dimostrazione chiara di come i dati vengono "avvolti" con header ad ogni livello durante l'invio e "svolti" durante la ricezione.
* **Header Personalizzati:** Ogni livello (eccetto l'Applicazione) aggiunge un header specifico come da specifiche.
* **Funzionalità Specifiche per Livello:**
    * **Livello Presentazione (6):** Codifica/decodifica del messaggio (es. ROT13).
    * **Livello Sessione (5):** Gestione semplificata dell'apertura/chiusura di una sessione con ID.
    * **Livello Trasporto (4):** Frammentazione dei dati se superano una MTU (Maximum Transmission Unit) definita (20 byte di payload per frammento).
    * **Livello Rete (3):** Aggiunta di indirizzi IP sorgente/destinazione fittizi e un campo TTL (Time To Live).
    * **Livello Collegamento Dati (2):** Aggiunta di indirizzi MAC fittizi (non implementa checksum nella versione attuale dei file).
    * **Livello Fisico (1):** Simulazione della trasmissione di un "bitstream" (stringa) su un mezzo fisico tramite una coda FIFO.
* **Test Semplice:** Un `main.c` fornito per testare il flusso di invio e ricezione di un messaggio.

## 📂 Struttura del Progetto

Il progetto è organizzato con una directory per ogni livello, contenente i file `.c` e `.h` corrispondenti, più alcuni file globali:

```
progetto/
├── constants.h                 # Costanti globali (es. PDU_SIZE)
├── main.c                      # Funzione main per testare lo stack
├── README.md                   # Questo file
│
├── level7_application/
│   ├── level7_application.c
│   └── level7_application.h
├── level6_presentation/
│   ├── level6_presentation.c
│   └── level6_presentation.h
├── level5_session/
│   ├── level5_session.c
│   └── level5_session.h
├── level4_transport/
│   ├── level4_transport.c
│   └── level4_transport.h
├── level3_network/
│   ├── level3_network.c
│   └── level3_network.h
├── level2_datalink/
│   ├── level2_datalink.c
│   └── level2_datalink.h
└── level1_physical/            # (Nei file attuali, chiamato 'level1_fisic')
    ├── level1_fisic.c
    └── level1_fisic.h
```
*Nota: La specifica originale menziona `mezzo_trasmissivo/.h` che è implementato concettualmente all'interno di `level1_fisic.c`.*

## 層 Livelli dello Stack ISO/OSI Implementati

Ogni livello implementa due funzioni principali:
* `char* livelloX_send(const char* dati, ...)`: Prende i dati dal livello superiore, aggiunge il proprio header e passa la PDU risultante al livello inferiore.
* `char* livelloX_receive(const char* pdu)`: Prende la PDU dal livello inferiore, processa (rimuove e valida) il proprio header e passa i dati risultanti (SDU) al livello superiore.

---

### Livello 7: Applicazione
* **Descrizione:** Interfaccia diretta con l'utente o l'applicazione. Riceve l'input dell'utente e visualizza l'output.
* **Header:** Nessun header aggiunto a questo livello; gestisce solo il testo utente.
* **Funzionalità:** Legge il messaggio da inviare e visualizza il messaggio ricevuto.

---

### Livello 6: Presentazione
* **Descrizione:** Responsabile della traduzione, cifratura e compressione dei dati. Assicura che i dati siano in un formato utilizzabile dal livello Applicazione.
* **Header da Prependere:** `[PRES][ENC=ROT13]` (o altre codifiche come UPPER, BASE64, ecc., anche se ROT13 è implementato).
* **Funzionalità Implementate:**
    * Codifica il messaggio in uscita utilizzando ROT13.
    * Decodifica il messaggio in entrata utilizzando ROT13.

---

### Livello 5: Sessione
* **Descrizione:** Stabilisce, gestisce e termina le connessioni (sessioni) tra applicazioni.
* **Header da Prependere:** `[SESS][INIT|CLOSE|ID=XXXXX]` o `[SESS][NORMAL][ID=XXXXX]`.
* **Funzionalità Implementate:**
    * Aggiunge un header di sessione che può indicare `INIT`, `CLOSE` (non usate attivamente nel `main.c` base) o `NORMAL`.
    * Utilizza un ID di sessione (semplificato a 0 per `NORMAL` o 4 per `INIT` nel codice fornito).
    * La funzione `livello5_send` accetta un parametro `action` per determinare il tipo di header di sessione.

---

### Livello 4: Trasporto
* **Descrizione:** Fornisce un trasferimento dati affidabile e trasparente tra gli host. Si occupa di segmentazione, controllo di flusso e controllo degli errori.
* **Header da Prependere:** `[TRANS][FRAG=k/N][ID=XX]`
    * `k`: Numero del frammento corrente.
    * `N`: Numero totale di frammenti.
    * `XX`: ID univoco del gruppo di frammenti.
* **Funzionalità Implementate:**
    * Frammenta il payload (SDU dal Livello 5) se la sua lunghezza supera `MTU_PAYLOAD` (definita a 20 byte).
    * Ogni frammento viene inviato come una PDU separata al Livello 3.
    * In ricezione, estrae il payload dal frammento. La versione attuale non implementa il riassemblaggio completo dei frammenti ma inoltra il singolo frammento ricevuto.

---

### Livello 3: Rete
* **Descrizione:** Responsabile dell'instradamento dei pacchetti attraverso la rete, determinando il percorso migliore.
* **Header da Prependere:** `[NET][SRC=ip_src][DST=ip_dst][TTL=n]` (la versione attuale del codice usa `[SRC=192.168.1.7] [DST=192.168.1.45] ` senza `[NET]` o `[TTL]`).
* **Funzionalità Implementate (semplificate):**
    * Aggiunge indirizzi IP sorgente e destinazione fissi (`192.168.1.7`, `192.168.1.45`) nell'header durante la ricezione (specifica `source.pdf` indica aggiunta in send, decremento TTL in receive; il codice attuale aggiunge header fisso in receive).
    * Non implementa logica di routing o decremento TTL nel codice fornito.

---

### Livello 2: Collegamento Dati (Data Link)
* **Descrizione:** Fornisce un trasferimento dati affidabile tra due nodi direttamente connessi (su un collegamento fisico). Si occupa di framing e controllo degli errori a livello di collegamento.
* **Header da Prependere:** `[MAC][SRC=AA:BB][DST=CC:DD]` (non implementato nel codice fornito).
* **Funzionalità Implementate (molto semplificate):**
    * Passa semplicemente i dati al Livello 1 in invio e riceve dati da Livello 1.
    * La specifica indica l'aggiunta di un checksum, ma non è presente nel codice attuale.

---

### Livello 1: Fisico
* **Descrizione:** Responsabile della trasmissione e ricezione del flusso di bit grezzi sul mezzo fisico.
* **Header da Prependere (concettuale):** `[BITSTREAM]` (non effettivamente prepeso come stringa nel codice fornito, ma il concetto è simulare un flusso di bit).
* **Funzionalità Implementate:**
    * Simula un mezzo trasmissivo utilizzando una coda FIFO (First-In, First-Out) implementata con un array circolare.
    * `livello1_send` (che agisce come `mezzo_fisico_send`) aggiunge la stringa di dati ("bitstream") alla coda.
    * `livello1_receive` (che agisce come `mezzo_fisico_receive`) preleva la stringa di dati dalla testa della coda.

---

## ⚙️ Come Funziona: Flusso dei Dati

1.  **Invio (Incapsulamento):**
    * Un messaggio di testo (es. "Ciao!") origina dal Livello 7 (Applicazione).
    * Scende attraverso i livelli (6, 5, 4, 3, 2, 1).
    * Ogni livello (da 6 a scendere, secondo le specifiche) aggiunge il proprio header alla SDU (Service Data Unit) ricevuta dal livello superiore, creando una PDU (Protocol Data Unit).
    * Il Livello 1 invia la PDU finale (concettualmente un flusso di bit) attraverso il mezzo trasmissivo simulato (la FIFO).

2.  **Ricezione (Decapsulamento):**
    * Il Livello 1 riceve la PDU dal mezzo trasmissivo.
    * La PDU sale attraverso i livelli (2, 3, 4, 5, 6, 7).
    * Ogni livello processa e rimuove il proprio header, passando la SDU risultante al livello superiore.
    * Infine, il Livello 7 riceve il messaggio originale e lo presenta.

## 🚀 Esecuzione e Test

Il file `main.c` fornisce un semplice flusso di test:
1.  Invia il messaggio "Ciao!" usando `livello7_send()`. Questa chiamata propaga il messaggio verso il basso attraverso tutti i livelli, che incapsulano i dati. Il risultato finale (la PDU del livello più basso che sarebbe inviata sul "filo") viene restituito e memorizzato.
2.  Questo risultato (PDU) viene passato a `livello7_receive()`. Questa chiamata propaga la PDU verso l'alto attraverso i livelli, che decapsulano i dati.
3.  Il messaggio originale decapsulato viene stampato a schermo.

**Input di Esempio (da `main.c`):**
```c
char* p1 = livello7_send("Ciao!");
```

**Output Atteso a Console (esempio semplificato del flusso):**
Il programma stamperà i log di ogni livello durante l'incapsulamento e il decapsulamento, mostrando gli header aggiunti/rimossi. L'output finale dovrebbe essere:
```
Ricevuto: Ciao!
```
Esempio di imbustamento (da `Consegna.md`):
| Livello      | Operazione     | Dati Risultanti (Esempio con "Ciao!\n")                     |
| :----------- | :------------- | :---------------------------------------------------------- |
| 7            | Applicazione   | `"Ciao!\n"`                                                 |
| 6            | Presentazione  | `[PRES][ENC=ROT13]Pvnob!\a`                                 |
| 5            | Sessione       | `[SESS][ID=12345][PRES][ENC=ROT13]Pvnob!\a`                 |
| 4            | Trasporto      | `[TRANS][FRAG=1/1][ID=01][SESS]...`                         |
| 3            | Rete           | `[NET][SRC=192.168.1.1][DST=192.168.1.2][TTL=5][TRANS]...`  |
| 2            | Collegamento   | `[MAC][SRC=AA:BB][DST=CC:DD][NET]...`                       |
| 1            | Fisico         | `[BITSTREAM][MAC][SRC=AA:BB][DST=CC:DD][NET]...`            |

*(Nota: `\a` nell'esempio del PDF è probabilmente un typo per `\n`. Gli header effettivi prodotti dal codice potrebbero variare leggermente rispetto all'esempio se le implementazioni dei livelli si discostano dalla tabella.)*

## 💡 Costanti Principali

* **`PDU_SIZE`**: Definisce la dimensione massima dei buffer utilizzati per contenere le PDU in vari livelli. Impostato a `1024` in `constants.h`.
* **`MTU_PAYLOAD`**: Utilizzato dal Livello Trasporto, definisce la dimensione massima del payload di un singolo frammento. Impostato a `20` in `level4_transport.c`.
* **`FIFO_SIZE`**: Dimensione della coda FIFO nel Livello Fisico per simulare il mezzo trasmissivo (non definita in `constants.h` ma usata implicitamente da `PDU_SIZE` in `level1_fisic.c` per l'array `fifo`, o dovrebbe essere una costante separata come da specifica `source.pdf`). La specifica `source.pdf` indica `#define FIFO_SIZE 1024`.

---

Questo README mira a fornire una panoramica completa del progetto C-ISO-OSI. Buona esplorazione e apprendimento!
```
