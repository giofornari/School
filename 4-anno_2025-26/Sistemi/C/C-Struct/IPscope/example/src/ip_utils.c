/**
 * ip_utils.c - Implementazione delle funzioni di utilità per indirizzi IP
 * 
 * Questo modulo fornisce le funzioni base per la manipolazione degli indirizzi IP:
 * - Conversioni tra formati (stringa, numerico, ottetti)
 * - Calcoli di rete (netmask, network address, broadcast)
 * - Operazioni su subnet
 */

#include "../include/ip_utils.h"
#include "../include/classifier.h"
#include <stdio.h>
#include <string.h>

/**
 * Converte una stringa IP in uint32_t
 * Utilizza sscanf per parsare i 4 ottetti e li combina in un uint32_t
 */
bool string_to_ip(const char *str, uint32_t *ip) {
    if (!str || !ip) return false;
    
    unsigned int oct1, oct2, oct3, oct4;
    
    // sscanf ritorna il numero di elementi letti con successo
    if (sscanf(str, "%u.%u.%u.%u", &oct1, &oct2, &oct3, &oct4) != 4) {
        return false;
    }
    
    // Validazione: ogni ottetto deve essere <= 255
    if (oct1 > 255 || oct2 > 255 || oct3 > 255 || oct4 > 255) {
        return false;
    }
    
    // Combinazione degli ottetti in un uint32_t
    // Primo ottetto nei bit più significativi (big endian / network byte order)
    *ip = ((uint32_t)oct1 << 24) |
          ((uint32_t)oct2 << 16) |
          ((uint32_t)oct3 << 8) |
          (uint32_t)oct4;
    
    return true;
}

/**
 * Converte uint32_t in stringa IP formato dotted decimal
 */
void ip_to_string(uint32_t ip, char *buffer) {
    if (!buffer) return;
    
    // Estrazione degli ottetti tramite shift e mask
    uint8_t oct1 = (ip >> 24) & 0xFF;
    uint8_t oct2 = (ip >> 16) & 0xFF;
    uint8_t oct3 = (ip >> 8) & 0xFF;
    uint8_t oct4 = ip & 0xFF;
    
    // Formattazione in stringa
    sprintf(buffer, "%u.%u.%u.%u", oct1, oct2, oct3, oct4);
}

/**
 * Estrae i singoli ottetti da un IP
 */
void ip_to_octets(uint32_t ip, uint8_t octets[4]) {
    if (!octets) return;
    
    octets[0] = (ip >> 24) & 0xFF;  // Ottetto più significativo
    octets[1] = (ip >> 16) & 0xFF;
    octets[2] = (ip >> 8) & 0xFF;
    octets[3] = ip & 0xFF;          // Ottetto meno significativo
}

/**
 * Compone un IP dai singoli ottetti
 */
uint32_t octets_to_ip(const uint8_t octets[4]) {
    if (!octets) return 0;
    
    return ((uint32_t)octets[0] << 24) |
           ((uint32_t)octets[1] << 16) |
           ((uint32_t)octets[2] << 8) |
           (uint32_t)octets[3];
}

/**
 * Crea una netmask dalla lunghezza del prefisso CIDR
 * 
 * Esempio: prefix_len = 24
 * 1. 32 - 24 = 8 bit per gli host
 * 2. 1 << 8 = 256 = 0x00000100
 * 3. 256 - 1 = 255 = 0x000000FF (tutti gli host bit a 1)
 * 4. ~255 = 0xFFFFFF00 = 255.255.255.0
 */
uint32_t create_netmask(uint8_t prefix_len) {
    // Casi edge
    if (prefix_len == 0) return 0x00000000;
    if (prefix_len >= 32) return 0xFFFFFFFF;
    
    // Crea una maschera con prefix_len bit a 1 a sinistra
    // e (32-prefix_len) bit a 0 a destra
    return ~((1U << (32 - prefix_len)) - 1);
}

/**
 * Calcola il network address: operazione AND tra IP e netmask
 * Azzera tutti i bit della parte host
 */
uint32_t calculate_network_address(uint32_t ip, uint32_t netmask) {
    return ip & netmask;
}

/**
 * Calcola il broadcast address: network OR ~netmask
 * Imposta a 1 tutti i bit della parte host
 */
uint32_t calculate_broadcast_address(uint32_t network, uint32_t netmask) {
    return network | ~netmask;
}

/**
 * Verifica se un IP appartiene a una subnet
 * Due IP appartengono alla stessa subnet se hanno lo stesso network address
 */
bool ip_in_subnet(uint32_t ip, uint32_t network, uint32_t netmask) {
    return (ip & netmask) == (network & netmask);
}

/**
 * Calcola il numero di host disponibili in una subnet
 * Formula: 2^(32-prefix_len) - 2
 * -2 perché network address e broadcast address non sono usabili
 * 
 * Casi speciali:
 * - /32 (host singolo): 1 indirizzo (utilizzato per host routes)
 * - /31 (point-to-point): 2 indirizzi (RFC 3021)
 */
uint32_t count_available_hosts(uint8_t prefix_len) {
    if (prefix_len > 32) return 0;
    if (prefix_len == 32) return 1;  // Single host
    if (prefix_len == 31) return 2;  // Point-to-point link (RFC 3021)
    
    uint32_t host_bits = 32 - prefix_len;
    uint32_t total_addresses = 1U << host_bits;
    
    // Sottrai network e broadcast
    return total_addresses - 2;
}

/**
 * Popola completamente una struttura IPAddress con tutte le informazioni
 * Coordina le varie funzioni per calcolare tutti i campi
 */
void populate_ip_address(IPAddress *ip_addr, uint32_t ip) {
    if (!ip_addr) return;
    
    // Azzera la struttura
    memset(ip_addr, 0, sizeof(IPAddress));
    
    // Rappresentazione base
    ip_addr->ip_num = ip;
    ip_to_string(ip, ip_addr->ip_str);
    ip_to_octets(ip, ip_addr->octets);
    
    // Classificazione
    ip_addr->class = classify_ip(ip);
    ip_addr->type = get_ip_type(ip);
    
    // Determina netmask di default basata sulla classe
    // (utile anche se non sempre applicabile nelle reti moderne)
    switch (ip_addr->class) {
        case 'A':
            ip_addr->cidr_prefix = 8;
            break;
        case 'B':
            ip_addr->cidr_prefix = 16;
            break;
        case 'C':
            ip_addr->cidr_prefix = 24;
            break;
        default:
            ip_addr->cidr_prefix = 0;  // D ed E non hanno netmask standard
    }
    
    // Calcola netmask, network e broadcast
    if (ip_addr->cidr_prefix > 0) {
        ip_addr->netmask = create_netmask(ip_addr->cidr_prefix);
        ip_addr->network_addr = calculate_network_address(ip, ip_addr->netmask);
        ip_addr->broadcast_addr = calculate_broadcast_address(ip_addr->network_addr, 
                                                              ip_addr->netmask);
    }
    
    ip_addr->is_valid = true;
}
