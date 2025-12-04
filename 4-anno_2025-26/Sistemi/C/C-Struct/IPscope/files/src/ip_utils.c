#include "../include/ip_utils.h"
#include "../include/classifier.h"
#include <stdio.h>


void ip_to_octets(uint32_t ip, uint8_t octets[4]) {
    octets[0] = (ip >> 24) & 0xFF;
    octets[1] = (ip >> 16) & 0xFF;
    octets[2] = (ip >> 8) & 0xFF;
    octets[3] = ip & 0xFF;
}


uint32_t octets_to_ip(const uint8_t octets[4]) {
    return ((uint32_t)octets[0] << 24) |
           ((uint32_t)octets[1] << 16) |
           ((uint32_t)octets[2] << 8)  |
           ((uint32_t)octets[3]);
}


bool string_to_ip(const char *str, uint32_t *ip) {
    uint8_t octets[4];
    if (sscanf(str, "%hhu.%hhu.%hhu.%hhu", &octets[0], &octets[1], &octets[2], &octets[3]) == 4){
        *ip = octets_to_ip(octets);
        return true;
    }
    return false;
}


void ip_to_string(uint32_t ip, char *buffer) {
    sprintf(buffer, "%u.%u.%u.%u", 
            (ip >> 24) & 0xFF, (ip >> 16) & 0xFF, 
            (ip >> 8) & 0xFF, ip & 0xFF);
}


uint32_t create_netmask(uint8_t prefix_len) {
    if (prefix_len > 32) return 0;
    return prefix_len == 0 ? 0 : (~0U << (32 - prefix_len));
}


uint32_t calculate_network_address(uint32_t ip, uint32_t netmask) {
    return ip & netmask;
}

uint32_t calculate_broadcast_address(uint32_t network, uint32_t netmask) {
    return network | ~netmask;
}

bool ip_in_subnet(uint32_t ip, uint32_t network, uint32_t netmask) {
    return (ip & netmask) == network;
}

uint32_t count_available_hosts(uint8_t prefix_len) {
    if (prefix_len >= 32) return 0;
    if (prefix_len == 31) return 2;
    uint32_t total = (1U << (32 - prefix_len));
    return total > 2 ? total - 2 : 0;
}

void populate_ip_address(IPAddress *ip_addr, uint32_t ip) {
    if (!ip_addr) return;
    
    ip_addr->ip_num = ip;
    ip_to_string(ip, ip_addr->ip_str);
    ip_to_octets(ip, ip_addr->octets);
    
    ip_addr->netmask = 0xFFFFFFFF;
    ip_addr->cidr_prefix = 32;
    ip_addr->network_addr = ip;
    ip_addr->broadcast_addr = ip;
    
    ip_addr->class = classify_ip(ip);
    ip_addr->type = get_ip_type(ip);
    ip_addr->is_valid = true;
}