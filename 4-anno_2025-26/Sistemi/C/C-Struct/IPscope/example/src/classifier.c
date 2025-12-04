/**
 * classifier.c - Classificazione degli indirizzi IP
 * 
 * Implementa la logica per determinare:
 * 1. La classe di un IP (A, B, C, D, E) basandosi sul primo ottetto
 * 2. Il tipo di IP (Reserved, Private, Public) basandosi su range predefiniti
 * 
 * References:
 * - RFC 791: Internet Protocol
 * - RFC 1918: Address Allocation for Private Internets
 * - RFC 3330: Special-Use IPv4 Addresses
 */

#include "../include/classifier.h"
#include "../include/ip_utils.h"
#include <stddef.h>

/**
 * Tabella dei range speciali (riservati e privati)
 * Ogni entry contiene network address, netmask e tipo
 */
typedef struct {
    uint32_t network;
    uint32_t netmask;
    IPType type;
    const char *description;
} SpecialRange;

// Array statico con tutti i range speciali
static const SpecialRange special_ranges[] = {
    // === INDIRIZZI RISERVATI ===
    // 0.0.0.0/8 - "This network" (RFC 1122)
    {0x00000000, 0xFF000000, IP_RESERVED, "This network"},
    
    // 127.0.0.0/8 - Loopback (RFC 1122)
    {0x7F000000, 0xFF000000, IP_RESERVED, "Loopback"},
    
    // 169.254.0.0/16 - Link-local / APIPA (RFC 3927)
    {0xA9FE0000, 0xFFFF0000, IP_RESERVED, "Link-local"},
    
    // 224.0.0.0/4 - Multicast (Classe D, RFC 3171)
    {0xE0000000, 0xF0000000, IP_RESERVED, "Multicast"},
    
    // 240.0.0.0/4 - Riservato/Sperimentale (Classe E, RFC 1112)
    {0xF0000000, 0xF0000000, IP_RESERVED, "Reserved"},
    
    // === INDIRIZZI PRIVATI (RFC 1918) ===
    // 10.0.0.0/8 - Classe A privata
    {0x0A000000, 0xFF000000, IP_PRIVATE, "Private Class A"},
    
    // 172.16.0.0/12 - Classe B privata (172.16.0.0 - 172.31.255.255)
    {0xAC100000, 0xFFF00000, IP_PRIVATE, "Private Class B"},
    
    // 192.168.0.0/16 - Classe C privata
    {0xC0A80000, 0xFFFF0000, IP_PRIVATE, "Private Class C"},
};

static const size_t num_special_ranges = sizeof(special_ranges) / sizeof(special_ranges[0]);

/**
 * Determina la classe di un IP basandosi sul primo ottetto
 * 
 * Struttura dei bit:
 * - Classe A: 0xxxxxxx (0-127)     ma 0 e 127 sono riservati → 1-126
 * - Classe B: 10xxxxxx (128-191)
 * - Classe C: 110xxxxx (192-223)
 * - Classe D: 1110xxxx (224-239)   Multicast
 * - Classe E: 1111xxxx (240-255)   Riservato
 */
char classify_ip(uint32_t ip) {
    // Estrai il primo ottetto (8 bit più significativi)
    uint8_t first_octet = (ip >> 24) & 0xFF;
    
    // Determina la classe basandosi sui range
    if (first_octet >= 1 && first_octet <= 126) {
        return 'A';
    } else if (first_octet >= 128 && first_octet <= 191) {
        return 'B';
    } else if (first_octet >= 192 && first_octet <= 223) {
        return 'C';
    } else if (first_octet >= 224 && first_octet <= 239) {
        return 'D';
    } else {
        // 240-255 oppure 0 e 127 (riservati)
        return 'E';
    }
}

/**
 * Determina il tipo di un IP controllando i range speciali
 * 
 * Algoritmo:
 * 1. Itera su tutti i range riservati
 * 2. Se l'IP appartiene a un range riservato, ritorna RESERVED
 * 3. Itera su tutti i range privati
 * 4. Se l'IP appartiene a un range privato, ritorna PRIVATE
 * 5. Altrimenti ritorna PUBLIC
 * 
 * Complessità: O(n) dove n è il numero di range speciali (piccolo e costante)
 */
IPType get_ip_type(uint32_t ip) {
    // Controlla tutti i range speciali
    for (size_t i = 0; i < num_special_ranges; i++) {
        const SpecialRange *range = &special_ranges[i];
        
        // Verifica se l'IP appartiene a questo range
        // Un IP appartiene al range se (IP & netmask) == (network & netmask)
        if ((ip & range->netmask) == (range->network & range->netmask)) {
            return range->type;
        }
    }
    
    // Se non appartiene a nessun range speciale, è pubblico
    return IP_PUBLIC;
}

/**
 * Converte il tipo IP in stringa abbreviata per l'output
 */
const char* ip_type_to_string(IPType type) {
    switch (type) {
        case IP_RESERVED:
            return "Ris";
        case IP_PRIVATE:
            return "Pri";
        case IP_PUBLIC:
            return "Pub";
        default:
            return "???";
    }
}

/**
 * Verifica se un IP è valido come indirizzo host
 * Un IP è valido per un host se:
 * 1. Non è il network address (tutti i bit host a 0)
 * 2. Non è il broadcast address (tutti i bit host a 1)
 * 
 * Nota: per subnet /31 (point-to-point) e /32 (single host)
 * le regole sono diverse (RFC 3021)
 */
bool is_valid_host_ip(uint32_t ip, uint32_t network, uint32_t broadcast) {
    // L'IP non deve essere né network né broadcast
    return (ip != network) && (ip != broadcast);
}
