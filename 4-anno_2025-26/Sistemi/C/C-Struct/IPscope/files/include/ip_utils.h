#ifndef IP_UTILS_H
#define IP_UTILS_H

#include "ip_types.h"
#include <stdint.h>
#include <stdbool.h>

/**
 * Converte una stringa IP in formato dotted decimal a uint32_t
 * 
 * @param str Stringa in formato "xxx.xxx.xxx.xxx"
 * @param ip Puntatore dove salvare il risultato
 * @return true se la conversione ha successo, false altrimenti
 * 
 * Esempio: "192.168.1.1" -> 0xC0A80101
 */
bool string_to_ip(const char *str, uint32_t *ip);

/**
 * Converte un uint32_t in stringa formato dotted decimal
 * 
 * @param ip IP in formato numerico
 * @param buffer Buffer dove scrivere la stringa (min 16 byte)
 * 
 * Esempio: 0xC0A80101 -> "192.168.1.1"
 */
void ip_to_string(uint32_t ip, char *buffer);

/**
 * Estrae i singoli ottetti da un IP numerico
 * 
 * @param ip IP in formato numerico
 * @param octets Array di 4 byte dove salvare gli ottetti
 */
void ip_to_octets(uint32_t ip, uint8_t octets[4]);

/**
 * Compone un IP dai singoli ottetti
 * 
 * @param octets Array di 4 ottetti
 * @return IP in formato numerico
 */
uint32_t octets_to_ip(const uint8_t octets[4]);

/**
 * Crea una netmask dalla lunghezza del prefisso CIDR
 * 
 * @param prefix_len Lunghezza del prefisso (0-32)
 * @return Netmask in formato numerico
 * 
 * Esempio: prefix_len=24 -> 0xFFFFFF00 (255.255.255.0)
 */
uint32_t create_netmask(uint8_t prefix_len);

/**
 * Calcola l'indirizzo di rete dato un IP e una netmask
 * 
 * @param ip Indirizzo IP
 * @param netmask Netmask
 * @return Network address
 */
uint32_t calculate_network_address(uint32_t ip, uint32_t netmask);

/**
 * Calcola l'indirizzo di broadcast dato network address e netmask
 * 
 * @param network Network address
 * @param netmask Netmask
 * @return Broadcast address
 */
uint32_t calculate_broadcast_address(uint32_t network, uint32_t netmask);

/**
 * Verifica se un IP appartiene a una subnet specifica
 * 
 * @param ip IP da verificare
 * @param network Network address della subnet
 * @param netmask Netmask della subnet
 * @return true se l'IP appartiene alla subnet
 */
bool ip_in_subnet(uint32_t ip, uint32_t network, uint32_t netmask);

/**
 * Calcola il numero di host disponibili in una subnet
 * 
 * @param prefix_len Lunghezza del prefisso CIDR
 * @return Numero di host (esclusi network e broadcast)
 */
uint32_t count_available_hosts(uint8_t prefix_len);

/**
 * Popola completamente una struttura IPAddress
 * 
 * @param ip_addr Struttura da popolare
 * @param ip IP in formato numerico
 */
void populate_ip_address(IPAddress *ip_addr, uint32_t ip);

#endif // IP_UTILS_H
