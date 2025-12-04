/**
 * @file ip_utils.c
 * @author giordii (admin@giordii.dev)
 * @brief utilità ip per gestione e conversione
 * @version 0.1
 * @date 2025-12-02
 * 
 * @copyright Copyright (c) 2025
 * 
 */

#include "include/ip_utils.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

/**
 * @brief etrai ip in ottetti
 * 
 * @param ip puntatore a ip num
 * @param octets array di 4 ottetti
 */
void ip_to_octets(uint32_t ip, uint8_t octets[4]) {
    octets[0] = (ip >> 24) & 0xFF;
    octets[1] = (ip >> 16) & 0xFF;
    octets[2] = (ip >> 8) & 0xFF;
    octets[3] = ip & 0xFF;
}

/**
 * @brief ottetti -> ip num
 * 
 * @param octets array di 4 ottetti
 * @return uint32_t ip num
 */
uint32_t octets_to_ip(const uint8_t octets[4]) {
    return ((uint32_t)octets[0] << 24) |
           ((uint32_t)octets[1] << 16) |
           ((uint32_t)octets[2] << 8)  |
           ((uint32_t)octets[3]);
}

/**
 * solita funzione stringa -> ip num
 * 
 * @param str ip in stringa ("xxx.xxx.xxx.xxx")
 * @param ip puntatore a ip num
 * @return
 * 
 * Esempio: "192.168.1.1" -> 0xC0A80101
 */
bool string_to_ip(const char *str, uint32_t *ip) {
    uint8_t octets[4];
    if (sscanf(str, "%hhu.%hhu.%hhu.%hhu", &octets[0], &octets[1], &octets[2], &octets[3]) == 4){
        *ip = octets_to_ip(octets);
        return true;
    }
    return false;
}

/**
 * @brief ip num -> stringa
 * 
 * @param ip puntatore a ip numerico
 * @param buffer buffer di destinazione (almeno 16 byte)
 */
void ip_to_string(uint32_t ip, char *buffer) {
    uint8_t octets[4];
    ip_to_octets(ip, octets);
    sprintf(buffer, "%u.%u.%u.%u", octets[0], octets[1], octets[2], octets[3]);
}


/**
 * Crea una netmask dalla lunghezza del prefisso CIDR
 * 
 * @param prefix_len Lunghezza del prefisso (0-32)
 * @return Netmask in formato numerico
 * 
 * Esempio: prefix_len=24 -> 0xFFFFFF00 (255.255.255.0)
 */
uint32_t create_netmask(uint8_t prefix_len) {
    if (prefix_len > 32) {
        return 0;
    }
    return prefix_len == 0 ? 0 : (~0U << (32 - prefix_len)); // prendo 0U (0 a 32 bit), faccio not per ottenere tutti a 1, shifto di tot posizioni (32-CIDR) per spostare i bit a 1 solo sul net id
}

/**
 * @brief Indirizzo di rete dato IP e netmask
 * 
 * @param ip  ip num
 * @param netmask netmask num
 * @return net address
 */
uint32_t calculate_network_address(uint32_t ip, uint32_t netmask) {
    return ip & netmask;
}

/**
 * @brief calcolo l'indirizzo di broadcast dato net addr e netmask
 * 
 * @param network net addr
 * @param netmask netmask
 * @return broadcast addr
 */
uint32_t calculate_broadcast_address(uint32_t network, uint32_t netmask) {
    return network | ~netmask; // dato che ho netmask e net adrr, faccio or tra netmask invertita (per ottenere host id a 255) e network addr
}

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