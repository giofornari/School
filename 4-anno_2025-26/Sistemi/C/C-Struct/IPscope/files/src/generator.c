/**
 * generator.c - the IMPOSSIBLE ONE
 * 
 * generare IP casuali con vari filtri:
 * - casuale
 * - filtro per classe
 * - fltro per CIDR
 * - filtro per range
 * - unicità er dio
 * 
 */

#include "../include/generator.h"
#include "../include/ip_utils.h"
#include "../include/classifier.h"
#include <stdlib.h>
#include <time.h>
#include <stdio.h>

#define MAX_GENERATION_ATTEMPTS 10000 // se troppi tentativi, errore

/**
 * @brief random??
 * 
 */
void init_random_generator(void) {
    srand((unsigned int)time(NULL));
}

/**
 * numero casuale in un range [min, max]
 * 
 */
uint32_t random_range(uint32_t min, uint32_t max) {
    if (min >= max) return min;
    
    uint32_t range = max - min + 1;
    return min + (rand() % range);
}

/**
 * @brief genera ottetti IP casuali
 * 
 * @return IP in  num uint32_t
 */
uint32_t generate_random_ip(void) {
    uint8_t octets[4];
    
    for (int i = 0; i < 4; i++) {
        octets[i] = (uint8_t)random_range(0, 255);
    }
    
    return octets_to_ip(octets);
}

/**
 * @brief IP random di classe X
 * 
 * genero direttamente nel range corretto per ottetto [0]
 */
uint32_t generate_ip_by_class(char class_filter) {
    uint8_t first_octet;
    
    switch (class_filter) {
        case 'A':
            first_octet = (uint8_t)random_range(1, 126);
            break;
        case 'B':
            first_octet = (uint8_t)random_range(128, 191);
            break;
        case 'C':
            first_octet = (uint8_t)random_range(192, 223);
            break;
        case 'D':
            first_octet = (uint8_t)random_range(224, 239);
            break;
        case 'E':
            if (rand() % 2) {
                first_octet = (uint8_t)random_range(240, 255);
            } else {
                first_octet = (rand() % 2) ? 0 : 127;
            }
            break;
        default:
            return generate_random_ip();
    }
    
    // genero gli altri 3 ottetti casualmente
    uint8_t octets[4] = {
        first_octet,
        (uint8_t)random_range(0, 255),
        (uint8_t)random_range(0, 255),
        (uint8_t)random_range(0, 255)
    };
    
    return octets_to_ip(octets);
}

/**
 * @brief IP rand all'interno di subnet CIDR
 * 
 * stepss:
 * 1. trovo n bit per host (32 - prefix_len)
 * 2. genero host_id rand
 * 3. network | host_id
 * 4. check che non sia net o broad addr
 *  * 
 * @param max_attempts max attempt prima di error
 * @param success out code
 */
uint32_t generate_ip_in_cidr(uint32_t network, uint8_t prefix_len, int max_attempts, bool *success) {
    if (success) *success = false;
    if (prefix_len > 32) return 0;
    if (prefix_len == 32) {
        if (success) *success = true;
        return network;
    }
    
    uint32_t netmask = create_netmask(prefix_len);
    uint32_t broadcast = calculate_broadcast_address(network, netmask);
    
    uint32_t host_bits = 32 - prefix_len;
    uint32_t max_hosts = (1U << host_bits);
    
    bool is_p2p = (prefix_len == 31);
    
    for (int attempt = 0; attempt < max_attempts; attempt++) {
        uint32_t host_id = random_range(0, max_hosts - 1);
        uint32_t ip = network | host_id;
        
        if (is_p2p || (ip != network && ip != broadcast)) {
            if (success) *success = true;
            return ip;
        }
    }    
    return 0;
}


/**
 * @brief IP in range [start_ip, end_ip]
 * 
 * offset rand e aggiungo a start_ip
 */
uint32_t generate_ip_in_range(uint32_t start_ip, uint32_t end_ip) {
    if (start_ip > end_ip) { // swap se invertiti
        uint32_t temp = start_ip;
        start_ip = end_ip;
        end_ip = temp;
    }
    
    return random_range(start_ip, end_ip);
}



/**
 * @brief check se si possono generare N IP con i filtri
 */
 bool check_gen(const ProgramOptions *opts) {
    if (!opts || opts->count <= 0) return false;
    
    // chack host disponibili
    if (opts->has_cidr) {
        uint32_t ok = count_available_hosts(opts->cidr_prefix);
        if ((uint32_t)opts->count > ok) {
            fprintf(stderr, "subnet /%d ha solo %u host disponibili, ma richiesti %d IP\n", opts->cidr_prefix, ok, opts->count);
            return false;
        }
    }
    if (opts->has_range) {
        uint64_t range_size = (uint64_t)opts->range_end - opts->range_start + 1;
        if ((uint32_t)opts->count > range_size) {
            fprintf(stderr, "range ha solo %llu IP disponibili, ma richiesti %d IP\n", (unsigned long long)range_size, opts->count);
            return false;
        }
    }
    
    return true;
}

/**
 * FUNZIONE PRINCIPALE: Genera un array di IP unici secondo le opzioni
 * 
 * Algoritmo generale (rejection sampling con unicità):
 * 1. Crea un IPSet per tracciare gli IP già generati
 * 2. Per ogni IP da generare:
 *    a. Genera un IP casuale applicando i filtri
 *    b. Verifica unicità
 *    c. Se unico, aggiungilo al set e all'output
 *    d. Altrimenti riprova
 * 3. Se troppi fallimenti consecutivi, esci
 * 
 * Gestisce:
 * - Filtro per classe (-c)
 * - Filtro per CIDR (-i)
 * - Filtro per range (-r)
 * - Combinazioni di filtri
 * 
 * @param opts Opzioni di generazione
 * @param output Array pre-allocato dove salvare i risultati
 * @return Numero di IP generati, -1 in caso di errore
 */
int generate_unique_ips(const ProgramOptions *opts, IPAddress *output) {
    if (!opts || !output) return -1;
    
    // Verifica fattibilità
    if (!check_gen(opts)) {
        return -1;
    }
    
    // Crea un set per tracciare l'unicità
    IPSet *used_ips = ipset_create(opts->count);
    if (!used_ips) {
        fprintf(stderr, "Errore: allocazione memoria per IPSet\n");
        return -1;
    }
    
    int generated = 0;
    int consecutive_failures = 0;
    const int max_consecutive_failures = 1000;
    
    // Genera gli IP uno alla volta
    while (generated < opts->count) {
        uint32_t ip;
        bool valid = false;
        
        // === FASE 1: Genera IP base applicando i filtri ===
        
        if (opts->has_cidr) {
            // Genera dentro la subnet CIDR
            bool success;
            ip = generate_ip_in_cidr(opts->cidr_network, opts->cidr_prefix,
                                    100, &success);
            if (!success) {
                consecutive_failures++;
                if (consecutive_failures >= max_consecutive_failures) {
                    fprintf(stderr, "Errore: impossibile generare IP nella subnet specificata\n");
                    break;
                }
                continue;
            }
            valid = true;
            
        } else if (opts->has_range) {
            // Genera dentro il range
            ip = generate_ip_in_range(opts->range_start, opts->range_end);
            valid = true;
            
        } else if (opts->class_filter != '\0') {
            // Genera per classe
            ip = generate_ip_by_class(opts->class_filter);
            valid = true;
            
        } else {
            // Genera completamente casuale
            ip = generate_random_ip();
            valid = true;
        }
        
        if (!valid) {
            consecutive_failures++;
            continue;
        }
        
        // === FASE 2: Applica filtri aggiuntivi se necessario ===
        
        // Se c'è filtro per classe E subnet/range, verifica la classe
        if (opts->class_filter != '\0' && (opts->has_cidr || opts->has_range)) {
            char ip_class = classify_ip(ip);
            if (ip_class != opts->class_filter) {
                consecutive_failures++;
                if (consecutive_failures >= max_consecutive_failures) {
                    fprintf(stderr, "Errore: impossibile trovare IP di classe %c "
                                   "nel range/subnet specificato\n", opts->class_filter);
                    break;
                }
                continue;
            }
        }
        
        // === FASE 3: Verifica unicità ===
        
        if (ipset_contains(used_ips, ip)) {
            // IP duplicato, riprova
            consecutive_failures++;
            if (consecutive_failures >= max_consecutive_failures) {
                fprintf(stderr, "Errore: troppi IP duplicati, probabilmente esauriti "
                               "gli IP disponibili\n");
                break;
            }
            continue;
        }
        
        // === FASE 4: IP valido e unico, aggiungilo ===
        
        if (!ipset_add(used_ips, ip)) {
            fprintf(stderr, "Errore: impossibile aggiungere IP al set\n");
            break;
        }
        
        // Popola la struttura IPAddress completa
        populate_ip_address(&output[generated], ip);
        
        generated++;
        consecutive_failures = 0;  // Reset del contatore
    }
    
    // Pulizia
    ipset_destroy(used_ips);
    
    return generated;
}

/**
 * === NOTE SULLE OTTIMIZZAZIONI ===
 * 
 * Per subnet molto piccole o vincoli molto restrittivi, il rejection sampling
 * può essere inefficiente. Possibili ottimizzazioni:
 * 
 * 1. PRE-CALCOLO + SHUFFLING (per subnet piccole):
 *    - Calcola tutti gli IP validi nella subnet
 *    - Usa Fisher-Yates shuffle per selezionarne N casualmente
 *    - O(k) dove k = numero IP disponibili
 * 
 * 2. RESERVOIR SAMPLING (per grandi subnet):
 *    - Genera N IP garantendo distribuzione uniforme
 *    - O(N) sempre
 * 
 * 3. HASH-BASED (per evitare collision):
 *    - Usa una funzione hash per mappare [0, N) → IP validi
 *    - Più complesso ma efficiente per grandi N
 */
