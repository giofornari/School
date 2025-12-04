#include "../include/classifier.h"
#include "../include/ip_utils.h"
#include <stddef.h>

typedef struct {
    uint32_t network;
    uint32_t netmask;
    IPType type;
} SpecialRange;

static const SpecialRange special_ranges[] = {
    {0x00000000, 0xFF000000, IP_RESERVED},
    {0x7F000000, 0xFF000000, IP_RESERVED},
    {0xA9FE0000, 0xFFFF0000, IP_RESERVED},
    {0xE0000000, 0xF0000000, IP_RESERVED},
    {0xF0000000, 0xF0000000, IP_RESERVED},
    {0x0A000000, 0xFF000000, IP_PRIVATE},
    {0xAC100000, 0xFFF00000, IP_PRIVATE},
    {0xC0A80000, 0xFFFF0000, IP_PRIVATE},
};

static const size_t num_special_ranges = sizeof(special_ranges) / sizeof(special_ranges[0]);


char classify_ip(uint32_t ip) {
    uint8_t first_octet = (ip >> 24) & 0xFF;
    
    if (first_octet >= 1 && first_octet <= 126) return 'A';
    if (first_octet >= 128 && first_octet <= 191) return 'B';
    if (first_octet >= 192 && first_octet <= 223) return 'C';
    if (first_octet >= 224 && first_octet <= 239) return 'D';
    return 'E';
}

IPType get_ip_type(uint32_t ip) {
    for (size_t i = 0; i < num_special_ranges; i++) {
        const SpecialRange *range = &special_ranges[i];
        if ((ip & range->netmask) == (range->network & range->netmask)) {
            return range->type;
        }
    }
    return IP_PUBLIC;
}


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


bool is_valid_host_ip(uint32_t ip, uint32_t network, uint32_t broadcast) {
    return (ip != network) && (ip != broadcast);
}
