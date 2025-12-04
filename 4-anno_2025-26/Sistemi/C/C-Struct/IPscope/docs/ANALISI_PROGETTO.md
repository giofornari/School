# RANDIP - Analisi del Progetto e Guida allo Sviluppo

## 📋 Indice
1. [Analisi dei Requisiti](#analisi-dei-requisiti)
2. [Progettazione della Soluzione](#progettazione-della-soluzione)
3. [Strutture Dati](#strutture-dati)
4. [Architettura Modulare](#architettura-modulare)
5. [Algoritmi Principali](#algoritmi-principali)
6. [Gestione della Memoria](#gestione-della-memoria)
7. [Testing e Validazione](#testing-e-validazione)
8. [Concetti C Avanzati](#concetti-c-avanzati)

---

## 1. Analisi dei Requisiti

### 1.1 Obiettivo Generale
Creare un programma C chiamato `randip` che generi indirizzi IP casuali UNICI con informazioni sulla loro classificazione.

### 1.2 Requisiti Funzionali

#### Input
- **Nessun argomento**: genera 1 IP casuale
- **`-n <numero>`**: specifica quanti IP generare
- **`-c <classe>`**: filtra per classe (A, B, C, D, E)
- **`-i <NetID/CIDR>`**: genera IP all'interno di una rete specifica (es. 192.168.1.0/24)
- **Parametro aggiuntivo `-r <range>`**: genera IP in un range specifico (es. 10.0.0.1-10.0.0.255)

#### Output
Per ogni IP generato, stampare:
1. **Indirizzo IP** in formato dotted decimal (es. 192.168.1.1)
2. **Classe**: A, B, C, D, o E
3. **Tipo**: Riservato (Ris), Privato (Pri), o Pubblico (Pub)

#### Vincoli
- **Unicità**: gli IP generati devono essere tutti diversi
- **Validità**: devono rispettare le regole di classificazione IP
- **Efficienza**: generazione casuale efficiente anche per grandi numeri

### 1.3 Classificazione degli Indirizzi IP

#### Classi di Indirizzi
| Classe | Range Primo Ottetto | Primo Bit(s) | Netmask Predefinita | Utilizzo |
|--------|---------------------|--------------|---------------------|----------|
| A      | 1-126              | 0            | 255.0.0.0           | Reti molto grandi |
| B      | 128-191            | 10           | 255.255.0.0         | Reti medie |
| C      | 192-223            | 110          | 255.255.255.0       | Reti piccole |
| D      | 224-239            | 1110         | N/A                 | Multicast |
| E      | 240-255            | 1111         | N/A                 | Riservato/Sperimentale |

#### Indirizzi Speciali

**Riservati (Ris):**
- 0.0.0.0/8 - "This network"
- 127.0.0.0/8 - Loopback
- 169.254.0.0/16 - Link-local (APIPA)
- 224.0.0.0/4 - Multicast (Classe D)
- 240.0.0.0/4 - Riservato (Classe E)

**Privati (Pri):**
- 10.0.0.0/8 - Classe A privata
- 172.16.0.0/12 - Classe B privata
- 192.168.0.0/16 - Classe C privata

**Pubblici (Pub):**
- Tutti gli altri indirizzi validi

---

## 2. Progettazione della Soluzione

### 2.1 Approccio Problem Solving

#### Fase 1: Decomposizione del Problema
1. **Parsing degli argomenti**: getopt() per gestire le opzioni
2. **Generazione casuale**: algoritmo per generare IP casuali validi
3. **Verifica unicità**: struttura dati per tracciare IP già generati
4. **Classificazione**: funzioni per determinare classe e tipo
5. **Validazione**: controllo dei vincoli CIDR/range
6. **Output formattato**: presentazione dei risultati

#### Fase 2: Identificazione dei Sottoproblemi
- Come generare numeri casuali di qualità?
- Come garantire l'unicità in modo efficiente?
- Come parsare e validare la notazione CIDR?
- Come calcolare se un IP appartiene a una subnet?
- Come organizzare il codice in modo modulare?

#### Fase 3: Scelta delle Strutture Dati
- **Struct IP**: contenitore per tutte le informazioni di un indirizzo
- **Hash Set**: per verificare rapidamente l'unicità
- **Array dinamico**: per memorizzare gli IP generati

### 2.2 Diagramma dell'Architettura

```
┌─────────────────────────────────────────────────────────────┐
│                         MAIN PROGRAM                         │
│                         (randip.c)                           │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
┌────────▼────────┐ ┌───▼────────┐ ┌───▼──────────┐
│   IP Library    │ │   Parser   │ │  Generator   │
│   (ip_utils.c)  │ │ (parser.c) │ │ (generator.c)│
└─────────────────┘ └────────────┘ └──────────────┘
         │
┌────────▼────────┐
│  Classification │
│  (classify.c)   │
└─────────────────┘
```

---

## 3. Strutture Dati

### 3.1 Struttura Principale: IPAddress

```c
typedef struct {
    // Rappresentazione dell'IP
    uint32_t ip_num;              // IP come numero a 32 bit (network byte order)
    char ip_str[16];              // IP in formato stringa "xxx.xxx.xxx.xxx"
    uint8_t octets[4];            // Singoli ottetti [0-3]
    
    // Informazioni di rete
    uint32_t netmask;             // Netmask in formato numerico
    uint8_t cidr_prefix;          // Lunghezza del prefisso CIDR (0-32)
    uint32_t network_addr;        // Indirizzo di rete
    uint32_t broadcast_addr;      // Indirizzo di broadcast
    
    // Classificazione
    char class;                   // Classe: 'A', 'B', 'C', 'D', 'E'
    IPType type;                  // RESERVED, PRIVATE, PUBLIC
    
    // Metadati
    bool is_valid;                // Flag di validità
} IPAddress;

typedef enum {
    IP_RESERVED,
    IP_PRIVATE,
    IP_PUBLIC
} IPType;
```

**Rationale delle scelte:**
- `uint32_t ip_num`: permette operazioni bitwise efficienti
- `octets[4]`: accesso rapido ai singoli ottetti
- `ip_str[16]`: buffer per formato leggibile (max "255.255.255.255\0")
- Separazione tra rappresentazione e classificazione

### 3.2 Struttura per la Gestione dell'Unicità

```c
typedef struct {
    uint32_t *ips;          // Array di IP generati (formato numerico)
    size_t count;           // Numero di IP attualmente memorizzati
    size_t capacity;        // Capacità allocata
} IPSet;
```

**Strategia di verifica unicità:**
1. **Per piccoli set (n < 1000)**: ricerca lineare nell'array
2. **Per grandi set**: ordinamento + ricerca binaria
3. **Alternativa avanzata**: hash table per O(1) lookup

### 3.3 Struttura per il Parsing dei Parametri

```c
typedef struct {
    int count;                    // Numero di IP da generare (-n)
    char class_filter;            // Filtro per classe (-c), '\0' se non specificato
    bool has_cidr;                // Flag: è stato specificato -i?
    uint32_t cidr_network;        // Network address del CIDR
    uint8_t cidr_prefix;          // Lunghezza prefisso CIDR
    bool has_range;               // Flag: è stato specificato -r?
    uint32_t range_start;         // Inizio range
    uint32_t range_end;           // Fine range
} ProgramOptions;
```

---

## 4. Architettura Modulare

### 4.1 Struttura del Progetto

```
IPscope/
├── example/
│   ├── src/
│   │   ├── main.c              # Entry point del programma
│   │   ├── ip_utils.c          # Funzioni di utilità per IP
│   │   ├── ip_utils.h
│   │   ├── classifier.c        # Classificazione IP (classe e tipo)
│   │   ├── classifier.h
│   │   ├── generator.c         # Generazione IP casuali
│   │   ├── generator.h
│   │   ├── parser.c            # Parsing argomenti e CIDR
│   │   ├── parser.h
│   │   └── ipset.c             # Gestione set di IP unici
│   │       ipset.h
│   ├── include/                # Header pubblici
│   ├── Makefile
│   └── README.md
└── docs/
    └── ANALISI_PROGETTO.md     # Questo documento
```

### 4.2 Responsabilità dei Moduli

#### main.c
- Entry point del programma
- Parsing degli argomenti con getopt()
- Coordinamento dei vari moduli
- Output formattato

#### ip_utils.c/h
- Conversione tra formati (string ↔ uint32_t ↔ octets)
- Validazione di indirizzi IP
- Operazioni su netmask
- Calcolo di network e broadcast address
- Verifica se un IP appartiene a una subnet

#### classifier.c/h
- Determinazione della classe (A, B, C, D, E)
- Determinazione del tipo (Reserved, Private, Public)
- Tabelle dei range speciali
- Funzioni di lookup efficienti

#### generator.c/h
- Generazione di IP casuali
- Applicazione dei filtri (classe, CIDR, range)
- Garanzia di unicità
- Inizializzazione del generatore casuale

#### parser.c/h
- Parsing della notazione CIDR (es. 192.168.1.0/24)
- Parsing del range (es. 10.0.0.1-10.0.0.255)
- Validazione degli input
- Conversione degli argomenti in strutture dati

#### ipset.c/h
- Gestione del set di IP generati
- Verifica di duplicati
- Allocazione dinamica efficiente
- Pulizia della memoria

---

## 5. Algoritmi Principali

### 5.1 Generazione di IP Casuali

#### Algoritmo Base
```
FUNZIONE genera_ip_casuale():
    GENERA 4 numeri casuali nell'intervallo [0, 255]
    COMBINA in un uint32_t (network byte order)
    RITORNA l'IP
```

#### Algoritmo con Filtro Classe
```
FUNZIONE genera_ip_classe(classe):
    RIPETI:
        ip = genera_ip_casuale()
        SE classe_di(ip) == classe:
            RITORNA ip
    FINCHÉ non trovato
```

**Ottimizzazione:**
```
FUNZIONE genera_ip_classe_ottimizzato(classe):
    primo_ottetto = genera_casuale_in_range(range_classe[classe])
    altri_ottetti = genera_casuali(3)
    COMBINA e RITORNA
```

#### Algoritmo con CIDR
```
FUNZIONE genera_ip_in_cidr(network, prefix_len):
    host_bits = 32 - prefix_len
    max_hosts = 2^host_bits - 2  // Escludi network e broadcast
    
    RIPETI:
        host_id = genera_casuale(0, max_hosts)
        ip = network | host_id
        SE ip != network E ip != broadcast:
            RITORNA ip
    FINCHÉ non valido
```

### 5.2 Verifica Unicità

#### Approccio 1: Array + Ricerca Lineare (Semplice)
```
FUNZIONE è_unico(ip, set):
    PER ogni ip_esistente IN set:
        SE ip == ip_esistente:
            RITORNA false
    RITORNA true
```
**Complessità:** O(n) per ogni verifica → O(n²) totale

#### Approccio 2: Array Ordinato + Ricerca Binaria
```
FUNZIONE è_unico_binario(ip, set_ordinato):
    indice = ricerca_binaria(ip, set_ordinato)
    RITORNA indice == NON_TROVATO
```
**Complessità:** O(log n) per verifica, O(n log n) per ordinamento

#### Approccio 3: Hash Set (Avanzato)
```
FUNZIONE è_unico_hash(ip, hash_set):
    hash = calcola_hash(ip)
    bucket = hash_set[hash % DIMENSIONE_TABELLA]
    RITORNA ip NON IN bucket
```
**Complessità:** O(1) medio per verifica

### 5.3 Classificazione dell'IP

#### Determinazione della Classe
```
FUNZIONE determina_classe(ip):
    primo_ottetto = (ip >> 24) & 0xFF
    
    SE primo_ottetto >= 1 E primo_ottetto <= 126:
        RITORNA 'A'
    ALTRIMENTI SE primo_ottetto >= 128 E primo_ottetto <= 191:
        RITORNA 'B'
    ALTRIMENTI SE primo_ottetto >= 192 E primo_ottetto <= 223:
        RITORNA 'C'
    ALTRIMENTI SE primo_ottetto >= 224 E primo_ottetto <= 239:
        RITORNA 'D'
    ALTRIMENTI:
        RITORNA 'E'
```

#### Determinazione del Tipo
```
FUNZIONE determina_tipo(ip):
    // Check range riservati
    PER ogni range IN ranges_riservati:
        SE ip_in_range(ip, range):
            RITORNA RESERVED
    
    // Check range privati
    PER ogni range IN ranges_privati:
        SE ip_in_range(ip, range):
            RITORNA PRIVATE
    
    RITORNA PUBLIC
```

**Ottimizzazione con lookup table:**
```c
static const struct {
    uint32_t network;
    uint32_t netmask;
    IPType type;
} special_ranges[] = {
    {0x00000000, 0xFF000000, IP_RESERVED}, // 0.0.0.0/8
    {0x7F000000, 0xFF000000, IP_RESERVED}, // 127.0.0.0/8
    {0x0A000000, 0xFF000000, IP_PRIVATE},  // 10.0.0.0/8
    // ... altri range
};
```

### 5.4 Parsing CIDR

#### Algoritmo di Parsing
```
FUNZIONE parse_cidr(stringa):
    // Es: "192.168.1.0/24"
    
    DIVIDI stringa su '/'
    SE non contiene '/':
        ERRORE "Formato CIDR non valido"
    
    parte_ip = prima_parte
    prefisso = converti_a_numero(seconda_parte)
    
    SE prefisso < 0 O prefisso > 32:
        ERRORE "Prefisso CIDR non valido"
    
    ip = parse_ip_string(parte_ip)
    netmask = crea_netmask(prefisso)
    network = ip & netmask
    
    RITORNA (network, prefisso)
```

#### Calcolo della Netmask
```
FUNZIONE crea_netmask(prefix_len):
    SE prefix_len == 0:
        RITORNA 0x00000000
    SE prefix_len == 32:
        RITORNA 0xFFFFFFFF
    
    // Crea una maschera con prefix_len bit a 1 a sinistra
    netmask = ~((1 << (32 - prefix_len)) - 1)
    RITORNA netmask
```

**Esempio:** prefix_len = 24
```
32 - 24 = 8
1 << 8 = 256 = 0x00000100
256 - 1 = 255 = 0x000000FF
~255 = 0xFFFFFF00 = 255.255.255.0
```

---

## 6. Gestione della Memoria

### 6.1 Allocazione Dinamica

#### IPSet con Crescita Dinamica
```c
IPSet* ipset_create(size_t initial_capacity) {
    IPSet *set = malloc(sizeof(IPSet));
    if (!set) return NULL;
    
    set->ips = malloc(initial_capacity * sizeof(uint32_t));
    if (!set->ips) {
        free(set);
        return NULL;
    }
    
    set->count = 0;
    set->capacity = initial_capacity;
    return set;
}

bool ipset_add(IPSet *set, uint32_t ip) {
    // Verifica se serve espandere
    if (set->count >= set->capacity) {
        size_t new_capacity = set->capacity * 2;
        uint32_t *new_ips = realloc(set->ips, new_capacity * sizeof(uint32_t));
        if (!new_ips) return false;
        
        set->ips = new_ips;
        set->capacity = new_capacity;
    }
    
    set->ips[set->count++] = ip;
    return true;
}

void ipset_destroy(IPSet *set) {
    if (set) {
        free(set->ips);
        free(set);
    }
}
```

### 6.2 Prevenzione dei Memory Leak

**Checklist:**
1. Ogni `malloc()` ha un corrispondente `free()`
2. In caso di errore, liberare la memoria già allocata
3. Usare valgrind per verificare leak
4. Gestire correttamente `realloc()` falliti

**Esempio di cleanup in caso di errore:**
```c
IPAddress* generate_ips(int count) {
    IPAddress *ips = malloc(count * sizeof(IPAddress));
    if (!ips) return NULL;
    
    IPSet *set = ipset_create(count);
    if (!set) {
        free(ips);  // Cleanup!
        return NULL;
    }
    
    // ... generazione ...
    
    ipset_destroy(set);
    return ips;
}
```

---

## 7. Testing e Validazione

### 7.1 Test Cases

#### Test Funzionalità Base
```bash
# Test 1: Generazione singolo IP
./randip
# Output atteso: 1 IP con classe e tipo

# Test 2: Generazione multipla
./randip -n 10
# Output atteso: 10 IP unici

# Test 3: Filtro per classe
./randip -n 5 -c A
# Output atteso: 5 IP di classe A

# Test 4: CIDR
./randip -n 5 -i 192.168.1.0/24
# Output atteso: 5 IP nel range 192.168.1.1-192.168.1.254

# Test 5: Combinazione
./randip -n 3 -c C -i 192.168.0.0/16
# Output atteso: 3 IP classe C nella subnet 192.168.0.0/16
```

#### Test Unicità
```bash
# Generare molti IP e verificare duplicati
./randip -n 10000 | sort | uniq -d
# Output atteso: nessun output (nessun duplicato)
```

#### Test Edge Cases
```bash
# Numero massimo in una subnet piccola
./randip -n 10 -i 192.168.1.0/29
# Max: 6 IP validi (2^3 - 2)

# Classe D (multicast)
./randip -n 5 -c D
# Verificare range 224-239

# Argomenti non validi
./randip -n -5          # Errore
./randip -c Z           # Errore
./randip -i 300.1.1.1/24  # Errore
```

### 7.2 Validazione della Classificazione

**Test per ogni classe:**
```c
assert(classify_ip(str_to_ip("10.0.0.1")) == 'A');
assert(classify_ip(str_to_ip("172.16.0.1")) == 'B');
assert(classify_ip(str_to_ip("192.168.1.1")) == 'C');
assert(classify_ip(str_to_ip("224.0.0.1")) == 'D');
assert(classify_ip(str_to_ip("240.0.0.1")) == 'E');
```

**Test per ogni tipo:**
```c
assert(get_ip_type(str_to_ip("127.0.0.1")) == IP_RESERVED);
assert(get_ip_type(str_to_ip("10.0.0.1")) == IP_PRIVATE);
assert(get_ip_type(str_to_ip("8.8.8.8")) == IP_PUBLIC);
```

---

## 8. Concetti C Avanzati

### 8.1 Manipolazione Bit

#### Estrazione di Ottetti
```c
// Da uint32_t a ottetti
uint8_t octet1 = (ip >> 24) & 0xFF;  // Primo ottetto
uint8_t octet2 = (ip >> 16) & 0xFF;  // Secondo ottetto
uint8_t octet3 = (ip >> 8) & 0xFF;   // Terzo ottetto
uint8_t octet4 = ip & 0xFF;          // Quarto ottetto
```

#### Composizione di un IP
```c
// Da ottetti a uint32_t
uint32_t ip = ((uint32_t)oct1 << 24) |
              ((uint32_t)oct2 << 16) |
              ((uint32_t)oct3 << 8) |
              (uint32_t)oct4;
```

#### Operazioni su Subnet
```c
// Calcolo network address
uint32_t network = ip & netmask;

// Calcolo broadcast address
uint32_t broadcast = network | ~netmask;

// Verifica appartenenza alla subnet
bool in_subnet = (ip & netmask) == (network & netmask);

// Conta host disponibili
uint32_t host_bits = 32 - prefix_len;
uint32_t num_hosts = (1 << host_bits) - 2;  // -2 per network e broadcast
```

### 8.2 Gestione degli Argomenti con getopt()

```c
#include <getopt.h>

void parse_arguments(int argc, char *argv[], ProgramOptions *opts) {
    int opt;
    
    // Inizializza opzioni di default
    opts->count = 1;
    opts->class_filter = '\0';
    opts->has_cidr = false;
    opts->has_range = false;
    
    // Parse argomenti
    while ((opt = getopt(argc, argv, "n:c:i:r:h")) != -1) {
        switch (opt) {
            case 'n':
                opts->count = atoi(optarg);
                if (opts->count <= 0) {
                    fprintf(stderr, "Errore: -n richiede un numero positivo\n");
                    exit(1);
                }
                break;
            
            case 'c':
                opts->class_filter = toupper(optarg[0]);
                if (opts->class_filter < 'A' || opts->class_filter > 'E') {
                    fprintf(stderr, "Errore: classe deve essere A, B, C, D o E\n");
                    exit(1);
                }
                break;
            
            case 'i':
                if (!parse_cidr(optarg, &opts->cidr_network, &opts->cidr_prefix)) {
                    fprintf(stderr, "Errore: formato CIDR non valido\n");
                    exit(1);
                }
                opts->has_cidr = true;
                break;
            
            case 'r':
                if (!parse_range(optarg, &opts->range_start, &opts->range_end)) {
                    fprintf(stderr, "Errore: formato range non valido\n");
                    exit(1);
                }
                opts->has_range = true;
                break;
            
            case 'h':
                print_usage(argv[0]);
                exit(0);
            
            default:
                print_usage(argv[0]);
                exit(1);
        }
    }
}
```

### 8.3 Generazione di Numeri Casuali

#### Inizializzazione del Seed
```c
#include <time.h>
#include <stdlib.h>

void init_random() {
    srand(time(NULL));
}

// Alternativa migliore (se disponibile)
#include <sys/random.h>

void init_random_secure() {
    unsigned int seed;
    getrandom(&seed, sizeof(seed), 0);
    srand(seed);
}
```

#### Generazione in un Range
```c
// Genera numero casuale in [min, max] (inclusivo)
uint32_t random_range(uint32_t min, uint32_t max) {
    if (min >= max) return min;
    return min + (rand() % (max - min + 1));
}

// Generazione più uniforme
uint32_t random_range_uniform(uint32_t min, uint32_t max) {
    uint32_t range = max - min + 1;
    uint32_t limit = RAND_MAX - (RAND_MAX % range);
    uint32_t value;
    
    do {
        value = rand();
    } while (value >= limit);
    
    return min + (value % range);
}
```

### 8.4 String Formatting e Parsing

#### Conversione IP a Stringa
```c
void ip_to_string(uint32_t ip, char *buffer) {
    uint8_t oct1 = (ip >> 24) & 0xFF;
    uint8_t oct2 = (ip >> 16) & 0xFF;
    uint8_t oct3 = (ip >> 8) & 0xFF;
    uint8_t oct4 = ip & 0xFF;
    
    sprintf(buffer, "%u.%u.%u.%u", oct1, oct2, oct3, oct4);
}

// Con controllo dimensione buffer
int ip_to_string_safe(uint32_t ip, char *buffer, size_t size) {
    uint8_t oct1 = (ip >> 24) & 0xFF;
    uint8_t oct2 = (ip >> 16) & 0xFF;
    uint8_t oct3 = (ip >> 8) & 0xFF;
    uint8_t oct4 = ip & 0xFF;
    
    return snprintf(buffer, size, "%u.%u.%u.%u", oct1, oct2, oct3, oct4);
}
```

#### Parsing Stringa a IP
```c
bool string_to_ip(const char *str, uint32_t *ip) {
    unsigned int oct1, oct2, oct3, oct4;
    
    // sscanf ritorna il numero di elementi letti con successo
    if (sscanf(str, "%u.%u.%u.%u", &oct1, &oct2, &oct3, &oct4) != 4) {
        return false;
    }
    
    // Validazione range
    if (oct1 > 255 || oct2 > 255 || oct3 > 255 || oct4 > 255) {
        return false;
    }
    
    *ip = ((uint32_t)oct1 << 24) |
          ((uint32_t)oct2 << 16) |
          ((uint32_t)oct3 << 8) |
          (uint32_t)oct4;
    
    return true;
}
```

### 8.5 Gestione degli Errori

#### Pattern con errno
```c
#include <errno.h>
#include <string.h>

IPAddress* generate_ips(int count) {
    IPAddress *ips = malloc(count * sizeof(IPAddress));
    if (!ips) {
        fprintf(stderr, "Errore allocazione memoria: %s\n", strerror(errno));
        return NULL;
    }
    
    // ... operazioni ...
    
    return ips;
}
```

#### Codici di Errore Personalizzati
```c
typedef enum {
    RANDIP_SUCCESS = 0,
    RANDIP_ERR_MEMORY = 1,
    RANDIP_ERR_INVALID_ARG = 2,
    RANDIP_ERR_INVALID_CIDR = 3,
    RANDIP_ERR_NO_IPS_AVAILABLE = 4
} RandIPError;

RandIPError generate_ips_checked(int count, IPAddress **out_ips) {
    if (count <= 0) {
        return RANDIP_ERR_INVALID_ARG;
    }
    
    IPAddress *ips = malloc(count * sizeof(IPAddress));
    if (!ips) {
        return RANDIP_ERR_MEMORY;
    }
    
    // ... generazione ...
    
    *out_ips = ips;
    return RANDIP_SUCCESS;
}

// Utilizzo
IPAddress *ips;
RandIPError err = generate_ips_checked(10, &ips);
if (err != RANDIP_SUCCESS) {
    fprintf(stderr, "Errore: %d\n", err);
    exit(err);
}
```

---

## 9. Ottimizzazioni e Considerazioni Avanzate

### 9.1 Performance

#### Generazione con Vincoli Stretti
Quando i vincoli sono molto restrittivi (es. pochi IP disponibili), l'approccio "genera e verifica" diventa inefficiente.

**Soluzione:** Pre-calcolare tutti gli IP validi e selezionarne casualmente.

```c
uint32_t* precalculate_valid_ips(ProgramOptions *opts, size_t *out_count) {
    // Calcola tutti gli IP validi dato i filtri
    // Ritorna array e la dimensione
}

void generate_by_sampling(uint32_t *valid_ips, size_t valid_count, 
                         int n, IPAddress *output) {
    // Algoritmo di Fisher-Yates per sampling casuale senza ripetizioni
    for (int i = 0; i < n; i++) {
        int j = random_range(i, valid_count - 1);
        // Swap
        uint32_t temp = valid_ips[i];
        valid_ips[i] = valid_ips[j];
        valid_ips[j] = temp;
        
        // Usa valid_ips[i]
        ip_from_uint32(valid_ips[i], &output[i]);
    }
}
```

### 9.2 Estensioni Possibili

1. **Output in diversi formati:**
   - JSON: `{"ip": "192.168.1.1", "class": "C", "type": "Private"}`
   - CSV: `192.168.1.1,C,Private`
   - XML

2. **Filtri aggiuntivi:**
   - Esclusione di range specifici
   - Solo IP pubblici/privati
   - Solo IP validi per host (no network/broadcast)

3. **Statistiche:**
   - Distribuzione per classe
   - Percentuale pubblici/privati
   - Tempo di generazione

4. **Salvataggio su file:**
   - `randip -n 1000 -o output.txt`

---

## 10. Checklist di Implementazione

### Fase 1: Setup Base
- [ ] Creare struttura directory
- [ ] Creare Makefile base
- [ ] Definire strutture dati principali
- [ ] Implementare conversioni base (string ↔ uint32_t)

### Fase 2: Classificazione
- [ ] Implementare determinazione classe
- [ ] Implementare determinazione tipo
- [ ] Creare tabella range speciali
- [ ] Test classificazione

### Fase 3: Generazione Base
- [ ] Implementare generazione IP casuale
- [ ] Implementare IPSet per unicità
- [ ] Test generazione senza filtri

### Fase 4: Parsing Argomenti
- [ ] Implementare getopt loop
- [ ] Parser CIDR
- [ ] Parser range
- [ ] Validazione input

### Fase 5: Filtri
- [ ] Filtro per classe
- [ ] Filtro per CIDR
- [ ] Filtro per range
- [ ] Test combinazioni filtri

### Fase 6: Output e Refinement
- [ ] Formattazione output
- [ ] Gestione errori completa
- [ ] Messaggi di help
- [ ] Testing finale

### Fase 7: Documentazione
- [ ] Commenti nel codice
- [ ] README con esempi
- [ ] Man page (opzionale)

---

## 11. Risorse e Riferimenti

### Documentazione Standard C
- `man 3 getopt` - Parsing argomenti
- `man 3 malloc` - Allocazione dinamica
- `man 3 sscanf` - Parsing stringhe
- `man 3 rand` - Numeri casuali

### RFC e Standard IP
- RFC 791 - Internet Protocol
- RFC 1918 - Private Address Space
- RFC 3330 - Special-Use IPv4 Addresses

### Tool per Testing
```bash
# Valgrind per memory leak
valgrind --leak-check=full ./randip -n 100

# GDB per debugging
gdb --args ./randip -n 10 -c A

# Strace per system calls
strace ./randip -n 5
```

### Compilazione con Warning
```bash
gcc -Wall -Wextra -Wpedantic -std=c11 -O2 -g \
    -o randip *.c
```

---

## Conclusione

Questo progetto offre un'eccellente opportunità per apprendere:

1. **Strutture dati** complesse e loro gestione
2. **Algoritmi** di generazione e verifica
3. **Manipolazione bit** e operazioni low-level
4. **Parsing** e validazione input
5. **Gestione memoria** dinamica
6. **Architettura modulare** in C
7. **Testing** e debugging sistematico

L'approccio modulare e ben documentato permetterà di costruire un programma robusto, mantenibile ed efficiente.

**Prossimi passi:** Consultare l'implementazione completa nella directory `example/` per vedere tutti questi concetti applicati in pratica.
