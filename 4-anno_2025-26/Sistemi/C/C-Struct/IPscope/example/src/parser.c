/**
 * parser.c - Parsing degli argomenti da command line
 * 
 * Implementa il parsing di:
 * - Argomenti della command line con getopt()
 * - Notazione CIDR (es. 192.168.1.0/24)
 * - Range di IP (es. 10.0.0.1-10.0.0.255)
 * - Validazione degli input
 */

#include "../include/parser.h"
#include "../include/ip_utils.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>
#include <ctype.h>

/**
 * Stampa il messaggio di aiuto con la sintassi del programma
 */
void print_usage(const char *program_name) {
    printf("Uso: %s [OPZIONI]\n\n", program_name);
    printf("Genera indirizzi IP casuali UNICI con informazioni di classificazione.\n\n");
    
    printf("Opzioni:\n");
    printf("  -n <numero>      Numero di IP da generare (default: 1)\n");
    printf("  -c <classe>      Filtra per classe: A, B, C, D, E\n");
    printf("  -i <CIDR>        Genera IP nella subnet specificata (es. 192.168.1.0/24)\n");
    printf("  -r <range>       Genera IP in un range (es. 10.0.0.1-10.0.0.255)\n");
    printf("  -h               Mostra questo aiuto\n\n");
    
    printf("Esempi:\n");
    printf("  %s                              Genera 1 IP casuale\n", program_name);
    printf("  %s -n 7                         Genera 7 IP casuali\n", program_name);
    printf("  %s -n 7 -c A                    Genera 7 IP di classe A\n", program_name);
    printf("  %s -n 5 -i 200.123.88.0/25     Genera 5 IP nella subnet specificata\n", program_name);
    printf("  %s -n 3 -c C -i 192.168.0.0/16  Combina filtri\n", program_name);
    printf("  %s -r 10.0.0.1-10.0.0.50        Genera 1 IP nel range\n\n", program_name);
    
    printf("Output:\n");
    printf("  Per ogni IP mostra: Indirizzo  Classe  Tipo\n");
    printf("  Tipo: Ris=Riservato, Pri=Privato, Pub=Pubblico\n\n");
    
    printf("Classificazione IP:\n");
    printf("  Classe A: 1.0.0.0 - 126.255.255.255\n");
    printf("  Classe B: 128.0.0.0 - 191.255.255.255\n");
    printf("  Classe C: 192.0.0.0 - 223.255.255.255\n");
    printf("  Classe D: 224.0.0.0 - 239.255.255.255 (Multicast)\n");
    printf("  Classe E: 240.0.0.0 - 255.255.255.255 (Riservato)\n");
}

/**
 * Parsa una stringa in notazione CIDR
 * 
 * Formato atteso: "xxx.xxx.xxx.xxx/yy"
 * dove xxx è 0-255 e yy è 0-32
 * 
 * Esempio: "192.168.1.0/24" -> network=0xC0A80100, prefix_len=24
 * 
 * Validazioni:
 * - Presenza del separatore '/'
 * - IP valido
 * - Prefisso nel range 0-32
 * - Network address corretto (bit host a zero)
 */
bool parse_cidr(const char *cidr_str, uint32_t *network, uint8_t *prefix_len) {
    if (!cidr_str || !network || !prefix_len) return false;
    
    // Copia la stringa per poterla modificare (strtok modifica la stringa)
    char buffer[64];
    strncpy(buffer, cidr_str, sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\0';
    
    // Cerca il separatore '/'
    char *slash = strchr(buffer, '/');
    if (!slash) {
        fprintf(stderr, "Errore: formato CIDR non valido (manca '/')\n");
        return false;
    }
    
    // Separa IP e prefisso
    *slash = '\0';
    const char *ip_part = buffer;
    const char *prefix_part = slash + 1;
    
    // Parsa l'IP
    uint32_t ip;
    if (!string_to_ip(ip_part, &ip)) {
        fprintf(stderr, "Errore: indirizzo IP non valido in CIDR: %s\n", ip_part);
        return false;
    }
    
    // Parsa il prefisso
    char *endptr;
    long prefix = strtol(prefix_part, &endptr, 10);
    
    // Verifica che sia un numero valido
    if (*endptr != '\0' || prefix < 0 || prefix > 32) {
        fprintf(stderr, "Errore: lunghezza prefisso CIDR non valida: %s (deve essere 0-32)\n", 
                prefix_part);
        return false;
    }
    
    *prefix_len = (uint8_t)prefix;
    
    // Calcola il network address corretto
    uint32_t mask = create_netmask(*prefix_len);
    *network = ip & mask;
    
    // Verifica che l'IP fornito sia effettivamente il network address
    if (ip != *network) {
        char net_str[16], provided_str[16];
        ip_to_string(*network, net_str);
        ip_to_string(ip, provided_str);
        
        fprintf(stderr, "Attenzione: IP fornito (%s) non è il network address.\n", provided_str);
        fprintf(stderr, "            Uso il network address corretto: %s/%d\n", net_str, *prefix_len);
    }
    
    return true;
}

/**
 * Parsa una stringa che rappresenta un range di IP
 * 
 * Formato atteso: "xxx.xxx.xxx.xxx-yyy.yyy.yyy.yyy"
 * 
 * Esempio: "10.0.0.1-10.0.0.255"
 * 
 * Validazioni:
 * - Presenza del separatore '-'
 * - Entrambi gli IP validi
 * - start_ip <= end_ip
 */
bool parse_range(const char *range_str, uint32_t *start_ip, uint32_t *end_ip) {
    if (!range_str || !start_ip || !end_ip) return false;
    
    // Copia la stringa
    char buffer[64];
    strncpy(buffer, range_str, sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\0';
    
    // Cerca il separatore '-'
    char *dash = strchr(buffer, '-');
    if (!dash) {
        fprintf(stderr, "Errore: formato range non valido (manca '-')\n");
        return false;
    }
    
    // Separa i due IP
    *dash = '\0';
    const char *start_part = buffer;
    const char *end_part = dash + 1;
    
    // Parsa l'IP di inizio
    if (!string_to_ip(start_part, start_ip)) {
        fprintf(stderr, "Errore: IP di inizio range non valido: %s\n", start_part);
        return false;
    }
    
    // Parsa l'IP di fine
    if (!string_to_ip(end_part, end_ip)) {
        fprintf(stderr, "Errore: IP di fine range non valido: %s\n", end_part);
        return false;
    }
    
    // Verifica che start <= end
    if (*start_ip > *end_ip) {
        fprintf(stderr, "Errore: IP di inizio (%s) maggiore di IP di fine (%s)\n", 
                start_part, end_part);
        return false;
    }
    
    return true;
}

/**
 * Parsa gli argomenti della command line con getopt
 * 
 * getopt gestisce automaticamente:
 * - Parsing delle opzioni
 * - Validazione del formato
 * - Gestione degli argomenti delle opzioni
 * 
 * Opzioni supportate:
 * -n <numero>  : specifica il numero di IP
 * -c <classe>  : filtra per classe
 * -i <CIDR>    : subnet CIDR
 * -r <range>   : range di IP
 * -h           : help
 */
bool parse_arguments(int argc, char *argv[], ProgramOptions *opts) {
    if (!opts) return false;
    
    // Inizializza con valori di default
    opts->count = 1;
    opts->class_filter = '\0';
    opts->has_cidr = false;
    opts->has_range = false;
    opts->cidr_network = 0;
    opts->cidr_prefix = 0;
    opts->range_start = 0;
    opts->range_end = 0;
    
    int opt;
    // La stringa "n:c:i:r:h" specifica:
    // - 'n:' significa che -n richiede un argomento
    // - 'h' significa che -h non richiede argomenti
    while ((opt = getopt(argc, argv, "n:c:i:r:h")) != -1) {
        switch (opt) {
            case 'n':
                // Parsing del numero di IP
                opts->count = atoi(optarg);
                if (opts->count <= 0) {
                    fprintf(stderr, "Errore: -n richiede un numero positivo\n");
                    return false;
                }
                break;
            
            case 'c':
                // Parsing della classe
                opts->class_filter = toupper(optarg[0]);
                if (opts->class_filter < 'A' || opts->class_filter > 'E') {
                    fprintf(stderr, "Errore: classe deve essere A, B, C, D o E\n");
                    return false;
                }
                break;
            
            case 'i':
                // Parsing del CIDR
                if (!parse_cidr(optarg, &opts->cidr_network, &opts->cidr_prefix)) {
                    return false;
                }
                opts->has_cidr = true;
                break;
            
            case 'r':
                // Parsing del range
                if (!parse_range(optarg, &opts->range_start, &opts->range_end)) {
                    return false;
                }
                opts->has_range = true;
                break;
            
            case 'h':
                // Help
                print_usage(argv[0]);
                exit(0);
            
            case '?':
                // Opzione non riconosciuta (getopt stampa già un messaggio)
                fprintf(stderr, "Usa -h per vedere l'aiuto\n");
                return false;
            
            default:
                return false;
        }
    }
    
    // Verifica argomenti extra non riconosciuti
    if (optind < argc) {
        fprintf(stderr, "Errore: argomenti non riconosciuti:");
        for (int i = optind; i < argc; i++) {
            fprintf(stderr, " %s", argv[i]);
        }
        fprintf(stderr, "\n");
        return false;
    }
    
    return true;
}

/**
 * Valida la consistenza delle opzioni parsate
 * 
 * Controlli:
 * - Numero di IP positivo
 * - Compatibilità tra filtri
 * - Range/CIDR validi se specificati
 */
bool validate_options(const ProgramOptions *opts) {
    if (!opts) return false;
    
    // Verifica numero positivo
    if (opts->count <= 0) {
        fprintf(stderr, "Errore: numero di IP deve essere positivo\n");
        return false;
    }
    
    // Non si può specificare sia CIDR che range
    if (opts->has_cidr && opts->has_range) {
        fprintf(stderr, "Errore: non è possibile specificare sia -i che -r contemporaneamente\n");
        return false;
    }
    
    // Se specificato CIDR, verifica validità
    if (opts->has_cidr && opts->cidr_prefix > 32) {
        fprintf(stderr, "Errore: prefisso CIDR non valido\n");
        return false;
    }
    
    // Se specificato range, verifica validità
    if (opts->has_range && opts->range_start > opts->range_end) {
        fprintf(stderr, "Errore: range non valido\n");
        return false;
    }
    
    return true;
}

/**
 * === NOTE SUL PARSING ===
 * 
 * getopt() è una funzione POSIX standard per il parsing degli argomenti.
 * Gestisce automaticamente:
 * - Opzioni con e senza argomenti
 * - Opzioni aggregate (es. -abc invece di -a -b -c)
 * - Messaggi di errore per opzioni non valide
 * 
 * Variabili globali usate da getopt:
 * - optind: indice del prossimo argomento da processare
 * - optarg: puntatore all'argomento dell'opzione corrente
 * - opterr: se != 0, getopt stampa messaggi di errore
 * - optopt: carattere dell'opzione che ha causato errore
 * 
 * Formato della stringa di opzioni:
 * - "n:c:i:h" significa:
 *   - n richiede un argomento (:)
 *   - c richiede un argomento (:)
 *   - i richiede un argomento (:)
 *   - h non richiede argomenti
 * 
 * Estensioni GNU:
 * - getopt_long() per opzioni lunghe (--help, --version, ecc.)
 * - "::" per argomenti opzionali
 */
