#ifndef IP_TYPES_H
#define IP_TYPES_H

#include <stdint.h>
#include <stdbool.h>

/**
 * Enumerazione per il tipo di indirizzo IP
 * Classifica gli IP in base al loro uso (RFC 1918 e RFC 3330)
 */
typedef enum {
    IP_RESERVED,    // Indirizzi riservati (loopback, multicast, sperimentali)
    IP_PRIVATE,     // Indirizzi privati (RFC 1918)
    IP_PUBLIC       // Indirizzi pubblici routing su Internet
} IPType;

/**
 * Struttura principale per rappresentare un indirizzo IP
 * Contiene sia la rappresentazione numerica che testuale,
 * oltre alle informazioni di classificazione
 */
typedef struct {
    // === Rappresentazione dell'IP ===
    uint32_t ip_num;              // IP in formato numerico (network byte order)
    char ip_str[16];              // IP in formato stringa "xxx.xxx.xxx.xxx"
    uint8_t octets[4];            // Singoli ottetti per accesso rapido
    
    // === Informazioni di rete ===
    uint32_t netmask;             // Netmask in formato numerico
    uint8_t cidr_prefix;          // Lunghezza prefisso CIDR (0-32)
    uint32_t network_addr;        // Indirizzo di rete
    uint32_t broadcast_addr;      // Indirizzo di broadcast
    
    // === Classificazione ===
    char class;                   // Classe IP: 'A', 'B', 'C', 'D', 'E'
    IPType type;                  // Tipo: RESERVED, PRIVATE, PUBLIC
    
    // === Metadati ===
    bool is_valid;                // Flag di validità dell'indirizzo
} IPAddress;

/**
 * Opzioni del programma parsate dalla command line
 */
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

#endif // IP_TYPES_H
