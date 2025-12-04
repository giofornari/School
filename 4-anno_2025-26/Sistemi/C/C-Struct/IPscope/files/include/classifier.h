#ifndef CLASSIFIER_H
#define CLASSIFIER_H

#include "ip_types.h"
#include <stdint.h>

/**
 * Determina la classe di un indirizzo IP (A, B, C, D, E)
 * basandosi sul valore del primo ottetto
 * 
 * Classi:
 * - A: 1-126     (0xxxxxxx)
 * - B: 128-191   (10xxxxxx)
 * - C: 192-223   (110xxxxx)
 * - D: 224-239   (1110xxxx) - Multicast
 * - E: 240-255   (1111xxxx) - Riservato/Sperimentale
 * 
 * @param ip IP in formato numerico
 * @return Carattere rappresentante la classe ('A', 'B', 'C', 'D', 'E')
 */
char classify_ip(uint32_t ip);

/**
 * Determina il tipo di un indirizzo IP (RESERVED, PRIVATE, PUBLIC)
 * 
 * Ranges Riservati:
 * - 0.0.0.0/8        "This network"
 * - 127.0.0.0/8      Loopback
 * - 169.254.0.0/16   Link-local (APIPA)
 * - 224.0.0.0/4      Multicast (Classe D)
 * - 240.0.0.0/4      Riservato (Classe E)
 * 
 * Ranges Privati (RFC 1918):
 * - 10.0.0.0/8       Classe A privata
 * - 172.16.0.0/12    Classe B privata
 * - 192.168.0.0/16   Classe C privata
 * 
 * @param ip IP in formato numerico
 * @return Tipo dell'IP (IP_RESERVED, IP_PRIVATE, IP_PUBLIC)
 */
IPType get_ip_type(uint32_t ip);

/**
 * Converte il tipo IP in una stringa leggibile
 * 
 * @param type Tipo dell'IP
 * @return Stringa descrittiva ("Ris", "Pri", "Pub")
 */
const char* ip_type_to_string(IPType type);

/**
 * Verifica se un IP è valido per essere usato come host
 * (non è network address né broadcast address)
 * 
 * @param ip IP da verificare
 * @param network Network address della subnet
 * @param broadcast Broadcast address della subnet
 * @return true se l'IP può essere usato da un host
 */
bool is_valid_host_ip(uint32_t ip, uint32_t network, uint32_t broadcast);

#endif // CLASSIFIER_H
