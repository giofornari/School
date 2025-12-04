# RANDIP - Generatore di Indirizzi IP Casuali

Un programma C modulare per generare indirizzi IP casuali **UNICI** con classificazione automatica.

## 📋 Caratteristiche

- ✅ Generazione di IP casuali con **garanzia di unicità**
- ✅ Filtro per **classe** (A, B, C, D, E)
- ✅ Filtro per **subnet CIDR** (es. `192.168.1.0/24`)
- ✅ Filtro per **range personalizzato** (es. `10.0.0.1-10.0.0.255`)
- ✅ Classificazione automatica: **Classe + Tipo**
  - Classe: A, B, C, D, E
  - Tipo: Riservato (Ris), Privato (Pri), Pubblico (Pub)
- ✅ Architettura **modulare** ben documentata
- ✅ Gestione robusta degli errori
- ✅ Zero memory leak

## 🏗️ Struttura del Progetto

```
example/
├── src/                    # Codice sorgente
│   ├── main.c             # Entry point
│   ├── ip_utils.c         # Utilità per IP (conversioni, calcoli)
│   ├── classifier.c       # Classificazione IP (classe, tipo)
│   ├── generator.c        # Generazione IP casuali
│   ├── parser.c           # Parsing argomenti
│   └── ipset.c            # Gestione set di IP unici
├── include/               # Header files
│   ├── ip_types.h         # Definizioni tipi e strutture
│   ├── ip_utils.h
│   ├── classifier.h
│   ├── generator.h
│   ├── parser.h
│   └── ipset.h
├── obj/                   # File oggetto (generati)
├── bin/                   # Eseguibile (generato)
├── Makefile              # Build system
└── README.md             # Questo file
```

## 🚀 Compilazione

### Prerequisiti
- GCC o Clang
- Make
- Sistema POSIX (Linux, macOS, WSL)

### Compilazione Rapida

```bash
make
```

L'eseguibile sarà in `bin/randip`

### Comandi Make Disponibili

```bash
make              # Compila il progetto
make clean        # Rimuove file compilati
make rebuild      # Pulisce e ricompila
make run          # Compila ed esegue un esempio
make test         # Esegue una serie di test
make memcheck     # Controlla memory leak con valgrind
make install      # Installa in /usr/local/bin (richiede sudo)
make info         # Mostra informazioni sul progetto
```

## 📖 Utilizzo

### Sintassi Generale

```bash
randip [OPZIONI]
```

### Opzioni

| Opzione | Argomento | Descrizione |
|---------|-----------|-------------|
| `-n` | `<numero>` | Numero di IP da generare (default: 1) |
| `-c` | `<classe>` | Filtra per classe: A, B, C, D, E |
| `-i` | `<CIDR>` | Genera IP nella subnet specificata |
| `-r` | `<range>` | Genera IP in un range specifico |
| `-h` | - | Mostra aiuto |

### Esempi Pratici

#### 1. Genera un singolo IP casuale
```bash
$ ./bin/randip
INDIRIZZO IP        CLASSE    TIPO
---------------     ------    ----
142.251.46.238      B         Pub
```

#### 2. Genera 7 IP casuali
```bash
$ ./bin/randip -n 7
INDIRIZZO IP        CLASSE    TIPO
---------------     ------    ----
201.45.123.89       C         Pub
172.16.5.200        B         Pri
10.128.64.32        A         Pri
192.168.100.50      C         Pri
224.0.0.251         D         Ris
8.8.8.8             A         Pub
127.0.0.1           E         Ris

Totale: 7 IP generati
```

#### 3. Genera 5 IP di classe A
```bash
$ ./bin/randip -n 5 -c A
INDIRIZZO IP        CLASSE    TIPO
---------------     ------    ----
10.23.45.67         A         Pri
45.123.78.90        A         Pub
23.56.89.12         A         Pub
10.0.0.1            A         Pri
34.101.102.103      A         Pub

Totale: 5 IP generati
```

#### 4. Genera IP in una subnet specifica
```bash
$ ./bin/randip -n 5 -i 200.123.88.0/25
INDIRIZZO IP        CLASSE    TIPO
---------------     ------    ----
200.123.88.45       C         Pub
200.123.88.103      C         Pub
200.123.88.12       C         Pub
200.123.88.78       C         Pub
200.123.88.126      C         Pub

Totale: 5 IP generati
```

Nota: `/25` significa netmask `255.255.255.128`, quindi 126 host disponibili (2^7 - 2).

#### 5. Genera IP in un range personalizzato
```bash
$ ./bin/randip -n 3 -r 10.0.0.1-10.0.0.50
INDIRIZZO IP        CLASSE    TIPO
---------------     ------    ----
10.0.0.23           A         Pri
10.0.0.7            A         Pri
10.0.0.41           A         Pri

Totale: 3 IP generati
```

#### 6. Combina filtri (classe + CIDR)
```bash
$ ./bin/randip -n 3 -c C -i 192.168.0.0/16
INDIRIZZO IP        CLASSE    TIPO
---------------     ------    ----
192.168.45.123      C         Pri
192.168.200.67      C         Pri
192.168.10.255      C         Pri

Totale: 3 IP generati
```

## 🎓 Concetti C Implementati

Questo progetto dimostra numerosi concetti avanzati di programmazione in C:

### 1. Strutture Dati
- **Struct complesse** con diversi tipi di dati
- **Enumerazioni** per tipi ben definiti
- **Array dinamici** con crescita automatica
- **Puntatori e gestione memoria**

### 2. Manipolazione Bit
```c
// Estrazione ottetti da uint32_t
uint8_t oct1 = (ip >> 24) & 0xFF;
uint8_t oct2 = (ip >> 16) & 0xFF;

// Composizione IP da ottetti
uint32_t ip = (oct1 << 24) | (oct2 << 16) | (oct3 << 8) | oct4;

// Calcolo netmask
uint32_t netmask = ~((1U << (32 - prefix_len)) - 1);
```

### 3. Allocazione Dinamica
```c
// Malloc con controllo errori
IPAddress *ips = malloc(count * sizeof(IPAddress));
if (!ips) {
    // Gestione errore
}

// Realloc per espansione array
uint32_t *new_ips = realloc(set->ips, new_capacity * sizeof(uint32_t));

// Free della memoria
free(ips);
```

### 4. Parsing e Validazione
```c
// getopt per argomenti command line
while ((opt = getopt(argc, argv, "n:c:i:r:h")) != -1) {
    switch (opt) {
        case 'n':
            count = atoi(optarg);
            break;
        // ...
    }
}

// sscanf per parsing stringhe
sscanf(str, "%u.%u.%u.%u", &oct1, &oct2, &oct3, &oct4);
```

### 5. Modularità
- **Separazione delle responsabilità** in moduli distinti
- **Header files** con interfacce pubbliche
- **Information hiding** con static
- **Riusabilità** del codice

### 6. Gestione Errori
```c
// Pattern con bool per successo/fallimento
bool parse_cidr(const char *str, uint32_t *network, uint8_t *prefix) {
    if (!str || !network || !prefix) return false;
    // ...
    return true;
}

// Cleanup in caso di errore
if (!generate_ips(&opts, ips)) {
    free(ips);
    return EXIT_FAILURE;
}
```

## 📚 Approfondimenti Tecnici

### Classificazione degli IP

#### Classi (basate sul primo ottetto)
| Classe | Range | Primo Bit(s) | Uso |
|--------|-------|--------------|-----|
| A | 1-126 | 0 | Reti molto grandi |
| B | 128-191 | 10 | Reti medie |
| C | 192-223 | 110 | Reti piccole |
| D | 224-239 | 1110 | Multicast |
| E | 240-255 | 1111 | Riservato/Sperimentale |

#### Indirizzi Speciali

**Riservati:**
- `0.0.0.0/8` - "This network"
- `127.0.0.0/8` - Loopback
- `169.254.0.0/16` - Link-local (APIPA)
- `224.0.0.0/4` - Multicast
- `240.0.0.0/4` - Riservato

**Privati (RFC 1918):**
- `10.0.0.0/8` - Classe A privata
- `172.16.0.0/12` - Classe B privata
- `192.168.0.0/16` - Classe C privata

### Notazione CIDR

CIDR (Classless Inter-Domain Routing) usa il formato `IP/prefisso`:

```
192.168.1.0/24
│          │
│          └─ Prefisso: primi 24 bit sono rete
└─────────── Network address
```

- `/24` = `255.255.255.0` = 256 indirizzi (254 host)
- `/25` = `255.255.255.128` = 128 indirizzi (126 host)
- `/30` = `255.255.255.252` = 4 indirizzi (2 host, usato per P2P)
- `/32` = `255.255.255.255` = 1 indirizzo (singolo host)

### Algoritmo di Generazione

1. **Inizializzazione**: crea IPSet per tracciare unicità
2. **Loop di generazione**:
   ```
   for i = 0 to count:
       repeat:
           genera IP con filtri
           se già presente:
               riprova
       fino a IP unico
       aggiungi a IPSet
       popola IPAddress
   ```
3. **Ottimizzazioni**:
   - Generazione diretta nel range per classe
   - Calcolo matematico per CIDR
   - Max attempts per evitare loop infiniti

## 🧪 Testing

### Test Automatici
```bash
make test
```

### Test Unicità
```bash
# Genera 10000 IP e verifica duplicati
./bin/randip -n 10000 | sort | uniq -d
# Output atteso: vuoto (nessun duplicato)
```

### Test Memory Leak
```bash
make memcheck
# o manualmente:
valgrind --leak-check=full ./bin/randip -n 1000
```

### Test Edge Cases
```bash
# Subnet piccola (max 6 host)
./bin/randip -n 6 -i 192.168.1.0/29

# Single host
./bin/randip -n 1 -i 192.168.1.1/32

# Classe D (multicast)
./bin/randip -n 5 -c D

# Range minimo
./bin/randip -n 2 -r 10.0.0.1-10.0.0.2
```

## 🐛 Debugging

### Con GDB
```bash
gdb --args ./bin/randip -n 5 -c A

(gdb) break generate_unique_ips
(gdb) run
(gdb) print opts->count
(gdb) next
(gdb) continue
```

### Log di Debug
Aggiungi temporaneamente print per debug:
```c
fprintf(stderr, "DEBUG: Generato IP %s\n", ip_str);
```

## ⚡ Ottimizzazioni Possibili

### Per Piccoli Set (< 1000 IP)
✅ Ricerca lineare (implementato) - O(n)

### Per Grandi Set (> 10000 IP)
Possibili miglioramenti:
1. **Ricerca binaria** su array ordinato - O(log n)
2. **Hash table** - O(1) medio
3. **Pre-calcolo + shuffling** per subnet piccole

### Esempio Hash Table
```c
typedef struct {
    uint32_t *buckets[HASH_SIZE];
    size_t counts[HASH_SIZE];
} HashSet;

uint32_t hash(uint32_t ip) {
    return ip % HASH_SIZE;
}
```

## 📖 Riferimenti

### Standard e RFC
- **RFC 791** - Internet Protocol
- **RFC 1918** - Private Address Space
- **RFC 3330** - Special-Use IPv4 Addresses
- **RFC 3927** - Dynamic Configuration of IPv4 Link-Local Addresses

### Documentazione C
- `man 3 getopt` - Parsing argomenti
- `man 3 malloc` - Gestione memoria
- `man 3 rand` - Numeri casuali
- `man 3 sscanf` - Parsing stringhe

## 🤝 Contribuire

Idee per estensioni:
1. Supporto IPv6
2. Output in JSON/CSV/XML
3. Statistiche dettagliate
4. Salvataggio su file
5. Filtri aggiuntivi (solo pubblici, solo privati)
6. GUI con ncurses

## 📄 Licenza

Progetto educativo - Uso libero per scopi didattici

## 👨‍💻 Autore

IPscope Project - 2024

---

**Nota**: Questo progetto è stato creato come esempio didattico completo per imparare:
- Programmazione C avanzata
- Strutture dati e algoritmi
- Architettura software modulare
- Networking e protocolli IP
- Best practices di sviluppo

Per domande o suggerimenti, consulta la documentazione completa in `../docs/ANALISI_PROGETTO.md`
