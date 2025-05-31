# C-ISO-OSI: Simulazione Didattica dello Stack ISO/OSI in C 💻🌐

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/Franciuto/C-ISO-OSI)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/Franciuto/C-ISO-OSI)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue)](https://www.gnu.org/licenses/gpl-3.0.html)
![Stato](https://img.shields.io/badge/Stato-In%20fase%20di%20sviluppo-orange)
![Autori](https://img.shields.io/badge/Autori-Giorgia%20Folloni%7CGiordano%20Fornari%7CFrancesco%20Fontanesi-black)
[![Repo Views](https://komarev.com/ghpvc/?username=Franciuto&label=Repository%20Views&color=brightgreen)](https://github.com/Franciuto/C-ISO-OSI)

## 🎯 Obiettivo del Progetto

Questo progetto implementa una versione semplificata ("giocattolo") dello stack di protocolli ISO/OSI utilizzando il linguaggio C. L'obiettivo principale è fornire uno strumento didattico per:
1.  Comprendere i concetti fondamentali di **incapsulamento** e **decapsulamento** dei dati attraverso i sette livelli del modello ISO/OSI.
2.  Simulare l'invio di un semplice messaggio di chat attraverso lo stack.
3.  Offrire un'esperienza pratica di sviluppo collaborativo di un sistema a più livelli.

## ✨ Funzionalità Chiave

* **Simulazione dei 7 Livelli ISO/OSI:** Implementazione di tutti i livelli, dall'Applicazione al Fisico.
* **Incapsulamento e Decapsulamento Dettagliati:** Visualizzazione degli header aggiunti/rimossi ad ogni livello durante il transito dei dati.
* **Header Personalizzati per Livello:** Ogni livello (eccetto l'Applicazione) aggiunge un header specifico (PDU) ai dati ricevuti dal livello superiore (SDU).
* **Interfaccia Utente Interattiva:** Un file `main.c` permette di inviare messaggi e osservare il comportamento dello stack in tempo reale.
* **Portabilità:** Scritto in C standard, facilmente compilabile su sistemi Linux e Windows.

## 📂 Struttura del Progetto

Il progetto è organizzato con una directory per ogni livello (contenente i file `.c` e `.h`), più file di configurazione e utility globali:

```

C-ISO-OSI/
├── constants.h                 \# Costanti globali (es. PDU\_SIZE)
├── main.c                      \# Funzione main per testare lo stack
├── README.md                   \# Questo file
├── Consegna.md                 \# Specifiche del progetto
├── Consegna.pdf                \# Specifiche del progetto (PDF)
├── out.txt                     \# Esempio di output di una sessione di test
│
├── level7\_application/
│   ├── level7\_application.c
│   └── level7\_application.h
├── level6\_presentation/
│   ├── level6\_presentation.c
│   └── level6\_presentation.h
├── level5\_session/
│   ├── level5\_session.c
│   └── level5\_session.h
├── level4\_transport/
│   ├── level4\_transport.c
│   └── level4\_transport.h
├── level3\_network/
│   ├── level3\_network.c
│   └── level3\_network.h
├── level2\_datalink/
│   ├── level2\_datalink.c
│   └── level2\_datalink.h
└── level1\_fisic/
├── level1\_fisic.c
└── level1\_fisic.h

````
*Nota: La specifica originale (`Consegna.md`) menziona `mezzo_trasmissivo/.h`, che è concettualmente implementato all'interno di `level1_fisic.c`.*

##  OSI Livelli Implementati e Funzionalità

Ogni livello `X` implementa due funzioni principali:
* `char* livelloX_send(const char* dati, ...)`: Riceve dati (SDU) dal livello superiore, aggiunge l'header del livello X (creando una PDU) e passa la PDU al livello inferiore.
* `char* livelloX_receive()`: Riceve una PDU dal livello inferiore, processa (rimuove e valida) l'header del livello X e passa i dati risultanti (SDU) al livello superiore.

---
### Livello 7: Applicazione
* **Descrizione:** Interfaccia diretta con l'utente. Riceve l'input dell'utente per l'invio e visualizza l'output ricevuto.
* **Header:** Nessun header specifico aggiunto a questo livello.
* **Funzionalità:** `livello7_send()` prende il messaggio testuale dall'utente. `livello7_receive()` visualizza il messaggio decodificato finale.

---
### Livello 6: Presentazione
* **Descrizione:** Responsabile della traduzione, cifratura e compressione dei dati. Assicura che i dati siano in un formato utilizzabile dal livello Applicazione del sistema ricevente.
* **Header Implementato:** `[PRES][ENC=ROT13]`.
* **Funzionalità:**
    * Codifica il messaggio in uscita utilizzando la cifratura ROT13.
    * Decodifica il messaggio in entrata (cifrato con ROT13).

---
### Livello 5: Sessione
* **Descrizione:** Stabilisce, gestisce e termina le connessioni (sessioni) tra applicazioni.
* **Header Implementato:** `[SESS][AZIONE][ID=XXXX]` dove `AZIONE` può essere `INIT`, `NORMAL`, `CLOSE` e `XXXX` è un ID di sessione generato dinamicamente per `INIT`.
* **Funzionalità:**
    * `livello5_send()` accetta un parametro `action` per determinare il tipo di PDU di sessione da inviare.
    * Gestisce l'apertura (`INIT`), il mantenimento (`NORMAL`) e la chiusura (`CLOSE`) di una sessione simulata.

---
### Livello 4: Trasporto
* **Descrizione:** Fornisce un trasferimento dati affidabile e trasparente. Si occupa di segmentazione/frammentazione, controllo di flusso e controllo degli errori end-to-end.
* **Header Implementato:** `[TRANS][FRAG=k/N][ID=XX]`.
    * `k`: Numero del frammento corrente.
    * `N`: Numero totale di frammenti.
    * `XX`: ID univoco del gruppo di frammenti (messaggio originale).
* **Funzionalità:**
    * Frammenta il payload (SDU dal Livello 5) se la sua lunghezza supera `MTU_PAYLOAD` (definita a 20 byte nel codice).
    * In ricezione, riassembla i frammenti appartenenti allo stesso ID per ricostruire il messaggio originale.

---
### Livello 3: Rete
* **Descrizione:** Responsabile dell'instradamento dei pacchetti attraverso la rete, determinando il percorso logico.
* **Header Implementato:** `[SRC=indirizzo_ip_sorgente] [DST=indirizzo_ip_destinazione]`.
* **Funzionalità (Semplificate):**
    * Aggiunge indirizzi IP sorgente (`192.168.1.7`) e destinazione (`192.168.1.45`) fissi e hardcoded.
    * *Non implementa logica di routing o decremento TTL come da specifica completa `Consegna.md`.*

---
### Livello 2: Collegamento Dati (Data Link)
* **Descrizione:** Fornisce un trasferimento dati affidabile tra due nodi direttamente connessi (su un collegamento fisico). Si occupa di framing e controllo degli errori a livello di collegamento.
* **Suffisso Implementato:** Appende un checksum calcolato sul payload: `[CHK=XX]` (dove XX è il checksum esadecimale).
* **Funzionalità (Semplificate):**
    * Calcola un checksum sui dati ricevuti da Livello 3 e lo appende.
    * In ricezione, verifica il checksum. Se non valido, il frame potrebbe essere scartato (la gestione errori avanzata non è implementata).
    * *Non implementa indirizzi MAC come da specifica completa `Consegna.md`.*

---
### Livello 1: Fisico
* **Descrizione:** Responsabile della trasmissione e ricezione del flusso di bit grezzi sul mezzo fisico.
* **Header:** Nessun header specifico aggiunto; simula la trasmissione di un "bitstream" (stringa).
* **Funzionalità:**
    * Simula un mezzo trasmissivo (cavo) utilizzando una coda FIFO (First-In, First-Out) implementata con un array circolare di dimensione 16.
    * `livello1_send()` accoda il "bitstream" (frame) ricevuto da Livello 2.
    * `livello1_receive()` preleva il "bitstream" (frame) dalla testa della coda.
    * `livello1_init()` inizializza la coda FIFO.

---
## ⚙️ Compilazione ed Esecuzione

### Prerequisiti
* Un compilatore C (es. GCC).

### Compilazione
Il progetto può essere compilato navigando nella directory radice `C-ISO-OSI/` ed eseguendo un semplice comando:

#### **Manuale**
```bash
nano Makefile; # modifica cio che ti serve
make
````

#### **Automatico**
```bash
chmod +x install.sh
./install.sh
```

(Assicurati che i percorsi e i flag `-I` per gli header siano corretti per la tua struttura di directory se diversa da quella standard del progetto).

### Esecuzione

Dopo la compilazione, esegui il simulatore:

```bash
./ISOSI_Simulator
```

Il programma `main.c` guiderà l'utente:

1.  Inizializzerà la sessione.
2.  Chiederà di inserire un messaggio da inviare.
3.  Mostrerà il percorso di incapsulamento (send stack) e decapsulamento (receive stack) con log dettagliati per ogni livello.
4.  Verificherà se il messaggio ricevuto corrisponde a quello inviato.
5.  L'utente può digitare "CLOSE" per terminare la sessione e il programma.

Un esempio di output di una sessione di test è disponibile nel file `out.txt`.

## 🛠️ Limitazioni Note e Discrepanze dalla Specifica (`Consegna.md`)

  * **Livello 3 (Rete):**
      * L'header implementato è `[SRC=ip_src][DST=ip_dst]` e non `[NET][SRC=...][DST=...][TTL=n]`.
      * La funzionalità di decremento del TTL non è implementata.
  * **Livello 2 (Collegamento Dati):**
      * Non vengono aggiunti indirizzi MAC sorgente/destinazione. Viene solo aggiunto un checksum.
  * **Livello 1 (Fisico):**
      * La dimensione della coda FIFO è 16 (`FIFO_SIZE` in `level1_fisic.c`), mentre la specifica `Consegna.md` indicava una `FIFO_SIZE` di 1024.
  * **Error Handling:** La gestione degli errori è semplificata e principalmente didattica.

## 📜 Licenza

Questo progetto è rilasciato sotto la **GNU General Public License v3.0**.
Per i dettagli completi della licenza, si prega di visitare: [https://www.gnu.org/licenses/gpl-3.0.html](https://www.gnu.org/licenses/gpl-3.0.html)

## 🤝 Contributi e Sviluppo Futuro

Essendo un progetto didattico e "in fase di sviluppo", ci sono diverse aree per possibili miglioramenti e contributi, come l'implementazione completa delle specifiche mancanti, una gestione degli errori più robusta, e l'aggiunta di più opzioni di codifica/cifratura.

-----

> Ci scusiamo per l'utilizzo di due lingue diverse (italiano e inglese nei commenti del codice). Purtroppo non tutti i developer originali conoscevano l'italiano.
