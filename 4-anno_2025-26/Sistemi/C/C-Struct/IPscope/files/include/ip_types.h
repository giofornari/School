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
 * @brief struct per raccogliere informazioni su un ip
 * ┌─────────────────────────────────────────────────────────────┐
 * │                    STRUTTURA IPAddress                      │
 * ├─────────────────────────────────────────────────────────────┤
 * │                                                             │
 * │  SEZIONE 1: Rappresentazione dell'IP                        │
 * │  ─────────────────────────────────────────────────────      │
 * │  uint32_t ip_num         [4 byte]  ◄── Master copy          │
 * │  char ip_str[16]         [16 byte] ◄── Per output           │
 * │  uint8_t octets[4]       [4 byte]  ◄── Accesso diretto      │
 * │                                                             │
 * │  SEZIONE 2: Informazioni di Rete                            │
 * │  ─────────────────────────────────────────────────────      │
 * │  uint32_t netmask        [4 byte]  ◄── Es. 0xFFFFFF00       │
 * │  uint8_t cidr_prefix     [1 byte]  ◄── Es. 24               │
 * │  uint32_t network_addr   [4 byte]  ◄── Es. 192.168.1.0      │
 * │  uint32_t broadcast_addr [4 byte]  ◄── Es. 192.168.1.255    │
 * │                                                             │
 * │  SEZIONE 3: Classificazione                                 │
 * │  ─────────────────────────────────────────────────────      │
 * │  char class              [1 byte]  ◄── 'A', 'B', 'C', ...   │
 * │  IPType type             [4 byte]  ◄── Enum                 │
 * │                                                             │
 * │  SEZIONE 4: Metadati                                        │
 * │  ─────────────────────────────────────────────────────      │
 * │  bool is_valid           [1 byte]  ◄── Flag validità        │
 * │                                                             │
 * │  TOTALE: ~47 byte (senza padding)                           │
 * └─────────────────────────────────────────────────────────────┘
 * 
 */
typedef struct {
    uint32_t ip_num;              
    char ip_str[16];              
    uint8_t octets[4];            
    
    uint32_t netmask;             
    uint8_t cidr_prefix;          
    uint32_t network_addr;        
    uint32_t broadcast_addr;      
    
    char class;                   
    IPType type;                  
    
    bool is_valid;                
} IPAddress;

/**
 * @brief struct per le opzioni del programma
 * 
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
