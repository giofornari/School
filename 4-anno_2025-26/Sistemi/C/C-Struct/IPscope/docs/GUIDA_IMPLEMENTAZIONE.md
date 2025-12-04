# RANDIP - Guida Completa all'Implementazione

## 📚 Panoramica

Questo documento spiega in dettaglio l'implementazione del programma **randip**, seguendo un approccio strutturato per l'apprendimento del C e del problem solving.

---

## 1️⃣ Analisi del Problema

### Cosa ci viene chiesto?

Un programma che generi **indirizzi IP casuali UNICI** con queste caratteristiche:

✅ **Parametri supportati:**
- `-n <numero>`: quanti IP generare
- `-c <classe>`: filtra per classe (A, B, C, D, E)
- `-i <CIDR>`: genera in una subnet (es. 192.168.1.0/24)
- `-r <range>`: genera in un range personalizzato (parametro aggiunto)

✅ **Output richiesto:**
Per ogni IP mostrare:
- Indirizzo IP (es. 192.168.1.1)
- Classe (A, B, C, D, E)
- Tipo (Ris/Pri/Pub)

✅ **Vincolo fondamentale:** UNICITÀ

### Come approcciare il problema?

**Step 1: Decomposizione**
Dividiamo il problema in sottoproblemi:
1. Come genero un IP casuale?
2. Come garantisco l'unicità?
3. Come applico i filtri?
4. Come classifico un IP?
5. Come parso gli argomenti?

**Step 2: Scelta delle strutture dati**
- `IPAddress`: contiene tutte le informazioni di un IP
- `IPSet`: gestisce l'unicità
- `ProgramOptions`: memorizza i parametri

**Step 3: Design modulare**
Ogni funzionalità in un modulo separato → manutenibilità e testabilità

---

## 2️⃣ Strutture Dati (ip_types.h)

### La struttura IPAddress

```c
typedef struct {
    // Rappresentazione
    uint32_t ip_num;        // IP come numero (0xC0A80101 = 192.168.1.1)
    char ip_str[16];        // IP come stringa "192.168.1.1"
    uint8_t octets[4];      // Array [192, 168, 1, 1]
    
    // Informazioni di rete
    uint32_t netmask;       // Es. 0xFFFFFF00 = 255.255.255.0
    uint8_t cidr_prefix;    // Es. 24
    uint32_t network_addr;  // Es. 192.168.1.0
    uint32_t broadcast_addr;// Es. 192.168.1.255
    
    // Classificazione
    char class;             // 'A', 'B', 'C', 'D', 'E'
    IPType type;            // RESERVED, PRIVATE, PUBLIC
    
    bool is_valid;
} IPAddress;
```

**Perché questa struttura?**
- `uint32_t ip_num`: operazioni bitwise veloci
- `ip_str[16]`: output leggibile immediato
- `octets[4]`: accesso diretto agli ottetti
- Campi separati per ogni informazione → Single Responsibility

### L'enumerazione IPType

```c
typedef enum {
    IP_RESERVED,    // 127.0.0.0/8, 224.0.0.0/4, etc.
    IP_PRIVATE,     // 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
    IP_PUBLIC       // Tutto il resto
} IPType;
```

**Perché enum invece di int?**
- Type safety: non posso assegnare valori arbitrari
- Leggibilità: `IP_PRIVATE` è più chiaro di `1`
- Autocomplete nell'IDE

---

## 3️⃣ Conversioni e Manipolazioni (ip_utils.c)

### Perché servono conversioni?

Gli IP possono essere rappresentati in 3 modi:
1. **Stringa**: "192.168.1.1" → leggibile dall'utente
2. **uint32_t**: 0xC0A80101 → operazioni matematiche/bitwise
3. **Array ottetti**: [192, 168, 1, 1] → accesso individuale

### Conversione String → uint32_t

```c
bool string_to_ip(const char *str, uint32_t *ip) {
    unsigned int oct1, oct2, oct3, oct4;
    
    // sscanf parsa la stringa in 4 numeri
    if (sscanf(str, "%u.%u.%u.%u", &oct1, &oct2, &oct3, &oct4) != 4) {
        return false;  // Formato non valido
    }
    
    // Valida che ogni ottetto sia 0-255
    if (oct1 > 255 || oct2 > 255 || oct3 > 255 || oct4 > 255) {
        return false;
    }
    
    // Combina in uint32_t (big endian)
    *ip = (oct1 << 24) | (oct2 << 16) | (oct3 << 8) | oct4;
    return true;
}
```

**Concetti chiave:**
- `sscanf`: parsing potente di stringhe formattate
- Shift left (`<<`): mette ogni ottetto nella posizione corretta
- OR bitwise (`|`): combina gli ottetti
- Return value: `true`/`false` per successo/errore

### Conversione uint32_t → String

```c
void ip_to_string(uint32_t ip, char *buffer) {
    uint8_t oct1 = (ip >> 24) & 0xFF;  // Estrae ottetto 1
    uint8_t oct2 = (ip >> 16) & 0xFF;  // Estrae ottetto 2
    uint8_t oct3 = (ip >> 8) & 0xFF;   // Estrae ottetto 3
    uint8_t oct4 = ip & 0xFF;          // Estrae ottetto 4
    
    sprintf(buffer, "%u.%u.%u.%u", oct1, oct2, oct3, oct4);
}
```

**Concetti chiave:**
- Shift right (`>>`): porta l'ottetto desiderato nei bit meno significativi
- Mask `& 0xFF`: estrae solo gli 8 bit meno significativi
- `sprintf`: formattazione in stringa

### Calcolo della Netmask

```c
uint32_t create_netmask(uint8_t prefix_len) {
    if (prefix_len == 0) return 0x00000000;
    if (prefix_len >= 32) return 0xFFFFFFFF;
    
    // Crea maschera con prefix_len bit a 1 a sinistra
    return ~((1U << (32 - prefix_len)) - 1);
}
```

**Come funziona? Esempio con /24:**

```
Step 1: 32 - 24 = 8
Step 2: 1U << 8 = 0x00000100 (256 in decimale)
Step 3: 256 - 1 = 0x000000FF (255 in decimale)
Step 4: ~0x000000FF = 0xFFFFFF00 (255.255.255.0)
```

---

## 4️⃣ Classificazione (classifier.c)

### Determinazione della Classe

```c
char classify_ip(uint32_t ip) {
    uint8_t first_octet = (ip >> 24) & 0xFF;
    
    if (first_octet >= 1 && first_octet <= 126) return 'A';
    if (first_octet >= 128 && first_octet <= 191) return 'B';
    if (first_octet >= 192 && first_octet <= 223) return 'C';
    if (first_octet >= 224 && first_octet <= 239) return 'D';
    return 'E';
}
```

**Logica:**
- Classe basata sul primo ottetto
- Range definiti dallo standard IP

**Tabella delle Classi:**

| Classe | Primo Ottetto | Bit Pattern | Uso |
|--------|---------------|-------------|-----|
| A | 1-126 | 0xxxxxxx | Reti molto grandi (16M host) |
| B | 128-191 | 10xxxxxx | Reti medie (65K host) |
| C | 192-223 | 110xxxxx | Reti piccole (254 host) |
| D | 224-239 | 1110xxxx | Multicast |
| E | 240-255 | 1111xxxx | Sperimentale |

### Determinazione del Tipo

Usiamo una **lookup table** con i range speciali:

```c
typedef struct {
    uint32_t network;
    uint32_t netmask;
    IPType type;
    const char *description;
} SpecialRange;

static const SpecialRange special_ranges[] = {
    // RISERVATI
    {0x00000000, 0xFF000000, IP_RESERVED, "This network"},    // 0.0.0.0/8
    {0x7F000000, 0xFF000000, IP_RESERVED, "Loopback"},        // 127.0.0.0/8
    {0xA9FE0000, 0xFFFF0000, IP_RESERVED, "Link-local"},      // 169.254.0.0/16
    {0xE0000000, 0xF0000000, IP_RESERVED, "Multicast"},       // 224.0.0.0/4
    {0xF0000000, 0xF0000000, IP_RESERVED, "Reserved"},        // 240.0.0.0/4
    
    // PRIVATI (RFC 1918)
    {0x0A000000, 0xFF000000, IP_PRIVATE, "Private Class A"},  // 10.0.0.0/8
    {0xAC100000, 0xFFF00000, IP_PRIVATE, "Private Class B"},  // 172.16.0.0/12
    {0xC0A80000, 0xFFFF0000, IP_PRIVATE, "Private Class C"},  // 192.168.0.0/16
};
```

**Algoritmo di lookup:**

```c
IPType get_ip_type(uint32_t ip) {
    for (size_t i = 0; i < num_special_ranges; i++) {
        const SpecialRange *range = &special_ranges[i];
        
        // Verifica se l'IP appartiene a questo range
        if ((ip & range->netmask) == (range->network & range->netmask)) {
            return range->type;
        }
    }
    
    // Se non appartiene a nessun range speciale → pubblico
    return IP_PUBLIC;
}
```

**Concetti:**
- Iterazione su array statico
- Operazione `&` per verificare appartenenza a subnet
- Early return appena trovato un match
- Default case: pubblico

---

## 5️⃣ Gestione Unicità (ipset.c)

### Perché serve un set?

Dobbiamo garantire che ogni IP generato sia **unico**. Serve una struttura dati per tracciare gli IP già generati.

### Implementazione: Array Dinamico

```c
typedef struct {
    uint32_t *ips;      // Array dinamico
    size_t count;       // Numero elementi
    size_t capacity;    // Capacità allocata
} IPSet;
```

### Creazione del Set

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
```

**Pattern importante:**
- Alloca struttura
- Alloca array interno
- Se fallisce, cleanup parziale
- Inizializza campi

### Verifica Duplicati

```c
bool ipset_contains(const IPSet *set, uint32_t ip) {
    for (size_t i = 0; i < set->count; i++) {
        if (set->ips[i] == ip) return true;
    }
    return false;
}
```

**Complessità:** O(n) - ricerca lineare
**Quando è OK?** Per n < 10000 è veloce abbastanza

### Aggiunta con Crescita Automatica

```c
bool ipset_add(IPSet *set, uint32_t ip) {
    if (ipset_contains(set, ip)) return false;  // Duplicato
    
    // Espandi se necessario
    if (set->count >= set->capacity) {
        size_t new_capacity = set->capacity * 2;
        uint32_t *new_ips = realloc(set->ips, new_capacity * sizeof(uint32_t));
        
        if (!new_ips) return false;  // Realloc fallita
        
        set->ips = new_ips;
        set->capacity = new_capacity;
    }
    
    set->ips[set->count++] = ip;
    return true;
}
```

**Concetti chiave:**
1. **Verifica unicità** prima di aggiungere
2. **Espansione dinamica** quando pieno
3. **Growth factor 2x** (strategia comune)
4. **realloc** per ridimensionare
5. **Controllo errori** su realloc

---

## 6️⃣ Generazione (generator.c)

### Generazione Base

```c
uint32_t generate_random_ip(void) {
    uint8_t octets[4];
    
    for (int i = 0; i < 4; i++) {
        octets[i] = (uint8_t)random_range(0, 255);
    }
    
    return octets_to_ip(octets);
}
```

### Generazione per Classe (Ottimizzata)

Invece di generare e verificare, **generiamo direttamente nel range corretto**:

```c
uint32_t generate_ip_by_class(char class_filter) {
    uint8_t first_octet;
    
    switch (class_filter) {
        case 'A':
            first_octet = random_range(1, 126);
            break;
        case 'B':
            first_octet = random_range(128, 191);
            break;
        case 'C':
            first_octet = random_range(192, 223);
            break;
        case 'D':
            first_octet = random_range(224, 239);
            break;
        case 'E':
            // Include 0, 127, e 240-255
            if (rand() % 2) {
                first_octet = random_range(240, 255);
            } else {
                first_octet = (rand() % 2) ? 0 : 127;
            }
            break;
    }
    
    // Genera altri 3 ottetti casualmente
    uint8_t octets[4] = {
        first_octet,
        random_range(0, 255),
        random_range(0, 255),
        random_range(0, 255)
    };
    
    return octets_to_ip(octets);
}
```

**Vantaggio:** Molto più efficiente del rejection sampling

### Generazione in CIDR

```c
uint32_t generate_ip_in_cidr(uint32_t network, uint8_t prefix_len,
                             int max_attempts, bool *success) {
    uint32_t netmask = create_netmask(prefix_len);
    uint32_t broadcast = calculate_broadcast_address(network, netmask);
    
    uint32_t host_bits = 32 - prefix_len;
    uint32_t max_hosts = (1U << host_bits);
    
    for (int attempt = 0; attempt < max_attempts; attempt++) {
        uint32_t host_id = random_range(0, max_hosts - 1);
        uint32_t ip = network | host_id;
        
        // Escludi network e broadcast
        if (ip != network && ip != broadcast) {
            *success = true;
            return ip;
        }
    }
    
    *success = false;
    return 0;
}
```

**Algoritmo:**
1. Calcola quanti host bit ci sono
2. Genera un host_id casuale
3. Combina network | host_id
4. Verifica che non sia network/broadcast
5. Retry fino a max_attempts

**Esempio 192.168.1.0/24:**
```
network = 0xC0A80100
host_bits = 8
host_id = random(0, 255)
ip = 0xC0A80100 | host_id
```

### Coordinamento Generale

```c
int generate_unique_ips(const ProgramOptions *opts, IPAddress *output) {
    IPSet *used_ips = ipset_create(opts->count);
    
    int generated = 0;
    int consecutive_failures = 0;
    
    while (generated < opts->count) {
        uint32_t ip;
        
        // Genera IP secondo i filtri
        if (opts->has_cidr) {
            ip = generate_ip_in_cidr(...);
        } else if (opts->has_range) {
            ip = generate_ip_in_range(...);
        } else if (opts->class_filter != '\0') {
            ip = generate_ip_by_class(...);
        } else {
            ip = generate_random_ip();
        }
        
        // Verifica unicità
        if (ipset_contains(used_ips, ip)) {
            consecutive_failures++;
            if (consecutive_failures >= MAX_FAILURES) break;
            continue;
        }
        
        // Aggiungi
        ipset_add(used_ips, ip);
        populate_ip_address(&output[generated], ip);
        generated++;
        consecutive_failures = 0;
    }
    
    ipset_destroy(used_ips);
    return generated;
}
```

**Pattern:**
1. Crea IPSet per unicità
2. Loop fino a generare tutti gli IP
3. Applica filtri appropriati
4. Verifica unicità
5. Gestisci fallimenti consecutivi
6. Cleanup finale

---

## 7️⃣ Parsing (parser.c)

### Uso di getopt

```c
bool parse_arguments(int argc, char *argv[], ProgramOptions *opts) {
    int opt;
    
    while ((opt = getopt(argc, argv, "n:c:i:r:h")) != -1) {
        switch (opt) {
            case 'n':
                opts->count = atoi(optarg);
                if (opts->count <= 0) {
                    fprintf(stderr, "Errore: -n deve essere positivo\n");
                    return false;
                }
                break;
            
            case 'c':
                opts->class_filter = toupper(optarg[0]);
                if (opts->class_filter < 'A' || opts->class_filter > 'E') {
                    fprintf(stderr, "Errore: classe deve essere A-E\n");
                    return false;
                }
                break;
            
            case 'i':
                if (!parse_cidr(optarg, &opts->cidr_network, &opts->cidr_prefix)) {
                    return false;
                }
                opts->has_cidr = true;
                break;
            
            // ... altri case
        }
    }
    
    return true;
}
```

**Concetti getopt:**
- `"n:c:i:r:h"`: definisce le opzioni
- `:` dopo una lettera = richiede argomento
- `optarg`: contiene l'argomento
- Loop fino a `-1`
- Switch sul carattere dell'opzione

### Parsing CIDR

```c
bool parse_cidr(const char *cidr_str, uint32_t *network, uint8_t *prefix_len) {
    char buffer[64];
    strncpy(buffer, cidr_str, sizeof(buffer) - 1);
    
    // Cerca '/'
    char *slash = strchr(buffer, '/');
    if (!slash) return false;
    
    *slash = '\0';
    const char *ip_part = buffer;
    const char *prefix_part = slash + 1;
    
    // Parsa IP
    uint32_t ip;
    if (!string_to_ip(ip_part, &ip)) return false;
    
    // Parsa prefisso
    long prefix = strtol(prefix_part, NULL, 10);
    if (prefix < 0 || prefix > 32) return false;
    
    *prefix_len = (uint8_t)prefix;
    
    // Calcola network corretto
    uint32_t mask = create_netmask(*prefix_len);
    *network = ip & mask;
    
    return true;
}
```

**Step by step:**
1. Copia la stringa (strtok la modifica)
2. Cerca il separatore `/`
3. Separa IP e prefisso
4. Parsa entrambe le parti
5. Valida i valori
6. Calcola il network address corretto

---

## 8️⃣ Main (main.c)

### Orchestrazione

```c
int main(int argc, char *argv[]) {
    // 1. Inizializza random
    init_random_generator();
    
    // 2. Parsa argomenti
    ProgramOptions opts;
    if (!parse_arguments(argc, argv, &opts)) {
        return EXIT_FAILURE;
    }
    
    // 3. Alloca memoria
    IPAddress *ips = malloc(opts.count * sizeof(IPAddress));
    if (!ips) return EXIT_FAILURE;
    
    // 4. Genera IP
    int num_generated = generate_unique_ips(&opts, ips);
    
    // 5. Stampa risultati
    print_header();
    for (int i = 0; i < num_generated; i++) {
        print_ip_info(&ips[i]);
    }
    
    // 6. Cleanup
    free(ips);
    return EXIT_SUCCESS;
}
```

**Flusso chiaro e lineare:**
1. Setup
2. Input
3. Processing
4. Output
5. Cleanup

---

## 9️⃣ Concetti C Approfonditi

### 1. Operazioni Bitwise

```c
// Shift left: sposta bit a sinistra
uint32_t x = 1 << 8;     // 0x00000100 (256)

// Shift right: sposta bit a destra
uint32_t y = 0xFF000000 >> 24;  // 0x000000FF (255)

// AND: mette a 0 i bit non mascherati
uint32_t z = 0x12345678 & 0xFF;  // 0x00000078

// OR: combina bit
uint32_t w = 0x1200 | 0x0034;    // 0x1234

// NOT: inverte tutti i bit
uint32_t v = ~0x00FF;             // 0xFFFFFF00
```

### 2. Puntatori e Memoria

```c
// Allocazione
int *ptr = malloc(sizeof(int) * 10);

// Verifica sempre
if (!ptr) {
    // Gestisci errore
}

// Uso
ptr[0] = 42;

// Deallocazione
free(ptr);
ptr = NULL;  // Buona pratica
```

### 3. Strutture e Typedef

```c
// Definizione con typedef
typedef struct {
    int x;
    int y;
} Point;

// Uso semplificato
Point p = {10, 20};
Point *pp = &p;
pp->x = 30;  // Equivalente a (*pp).x = 30
```

### 4. Enumerazioni

```c
typedef enum {
    RED,      // 0
    GREEN,    // 1
    BLUE      // 2
} Color;

Color c = RED;

// Valori personalizzati
typedef enum {
    ERROR = -1,
    SUCCESS = 0,
    PENDING = 1
} Status;
```

### 5. Array e Puntatori

```c
int arr[5] = {1, 2, 3, 4, 5};
int *p = arr;  // arr decade in puntatore

// Equivalenti
arr[2] == *(arr + 2) == *(p + 2) == p[2]
```

---

## 🔟 Best Practices Implementate

### 1. Gestione Errori Consistente

```c
// Ritorna bool per successo/fallimento
bool function(int *output) {
    if (!output) return false;
    // ...
    return true;
}

// Uso
int result;
if (!function(&result)) {
    fprintf(stderr, "Errore\n");
    return EXIT_FAILURE;
}
```

### 2. Controllo Puntatori NULL

```c
void safe_function(const Data *data) {
    if (!data) return;  // Guard clause
    // ... uso sicuro di data
}
```

### 3. Const Correctness

```c
// Input che non viene modificato
void print_ip(const IPAddress *ip);

// Protegge da modifiche accidentali
```

### 4. Naming Conventions

```c
// Tipi: PascalCase
typedef struct IPAddress IPAddress;

// Funzioni: snake_case
void generate_random_ip(void);

// Costanti: UPPER_SNAKE_CASE
#define MAX_ATTEMPTS 1000

// Variabili: snake_case
int num_generated = 0;
```

### 5. Documentazione

```c
/**
 * Brief description
 * 
 * Detailed explanation...
 * 
 * @param input Description
 * @return Description
 */
int function(int input);
```

---

## 🎯 Riepilogo Algoritmi

### Generazione IP

1. **Random puro**: 4 ottetti casuali
2. **Per classe**: primo ottetto nel range corretto
3. **Per CIDR**: network OR host_id_casuale
4. **Per range**: random_in_range

### Unicità

1. Usa IPSet (array dinamico)
2. Controlla prima di aggiungere
3. Espandi quando pieno
4. Complessità O(n) per lookup

### Classificazione

1. **Classe**: switch sul primo ottetto
2. **Tipo**: lookup table con range speciali
3. Complessità O(1) per classe, O(k) per tipo (k=8 range)

---

## 📝 Esercizi Proposti

### Livello 1: Modifiche Base
1. Aggiungi opzione `-v` (verbose) per stampare info dettagliate
2. Aggiungi contatore di tentativi nella generazione
3. Implementa output in formato CSV

### Livello 2: Nuove Funzionalità
4. Aggiungi opzione per escludere IP privati
5. Implementa salvataggio su file
6. Aggiungi statistiche (% per classe, % per tipo)

### Livello 3: Ottimizzazioni
7. Implementa hash table per unicità (O(1))
8. Usa ricerca binaria per grandi set
9. Pre-calcola tutti gli IP validi per subnet piccole

### Livello 4: Estensioni Avanzate
10. Supporto IPv6
11. Lettura configurazione da file JSON
12. Interfaccia grafica con ncurses

---

## 🏁 Conclusione

Questo progetto dimostra:

✅ **Analisi strutturata** del problema
✅ **Design modulare** ben pensato
✅ **Implementazione robusta** con gestione errori
✅ **Documentazione completa** del codice
✅ **Testing** delle funzionalità
✅ **Best practices** C moderne

È un esempio completo di come affrontare un progetto C reale, dall'analisi all'implementazione.

---

**Prossimi passi:**
1. Studia il codice modulo per modulo
2. Compila ed esegui gli esempi
3. Modifica e sperimenta
4. Implementa le estensioni proposte

Buono studio! 🚀
