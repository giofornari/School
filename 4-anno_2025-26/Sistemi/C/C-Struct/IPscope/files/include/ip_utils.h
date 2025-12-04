#ifndef IP_UTILS_H
#define IP_UTILS_H

#include "ip_types.h"
#include <stdint.h>
#include <stdbool.h>

bool string_to_ip(const char *str, uint32_t *ip);
void ip_to_string(uint32_t ip, char *buffer);
void ip_to_octets(uint32_t ip, uint8_t octets[4]);
uint32_t octets_to_ip(const uint8_t octets[4]);
uint32_t create_netmask(uint8_t prefix_len);
uint32_t calculate_network_address(uint32_t ip, uint32_t netmask);
uint32_t calculate_broadcast_address(uint32_t network, uint32_t netmask);
bool ip_in_subnet(uint32_t ip, uint32_t network, uint32_t netmask);
uint32_t count_available_hosts(uint8_t prefix_len);
void populate_ip_address(IPAddress *ip_addr, uint32_t ip);

#endif // IP_UTILS_H
