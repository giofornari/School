#include "../include/generator.h"
#include "../include/ip_utils.h"
#include "../include/classifier.h"
#include <stdlib.h>
#include <time.h>
#include <stdio.h>

#define MAX_GENERATION_ATTEMPTS 10000


void init_random_generator(void) {
    srand((unsigned int)time(NULL));
}


uint32_t random_range(uint32_t min, uint32_t max) {
    if (min >= max) return min;
    
    uint32_t range = max - min + 1;
    return min + (rand() % range);
}


uint32_t generate_random_ip(void) {
    return ((uint32_t)random_range(0, 255) << 24) |
           ((uint32_t)random_range(0, 255) << 16) |
           ((uint32_t)random_range(0, 255) << 8)  |
           (uint32_t)random_range(0, 255);
}


uint32_t generate_ip_by_class(char class_filter) {
    uint8_t first_octet;
    
    switch (class_filter) {
        case 'A':
            first_octet = (uint8_t)random_range(1, 126);
            break;
        case 'B':
            first_octet = (uint8_t)random_range(128, 191);
            break;
        case 'C':
            first_octet = (uint8_t)random_range(192, 223);
            break;
        case 'D':
            first_octet = (uint8_t)random_range(224, 239);
            break;
        case 'E':
            if (rand() % 2) {
                first_octet = (uint8_t)random_range(240, 255);
            } else {
                first_octet = (rand() % 2) ? 0 : 127;
            }
            break;
        default:
            return generate_random_ip();
    }
    
    return ((uint32_t)first_octet << 24) |
           ((uint32_t)random_range(0, 255) << 16) |
           ((uint32_t)random_range(0, 255) << 8)  |
           (uint32_t)random_range(0, 255);
}


uint32_t generate_ip_in_cidr(uint32_t network, uint8_t prefix_len, int max_attempts, bool *success) {
    if (success) *success = false;
    if (prefix_len > 32) return 0;
    if (prefix_len == 32) {
        if (success) *success = true;
        return network;
    }
    
    uint32_t netmask = create_netmask(prefix_len);
    uint32_t broadcast = calculate_broadcast_address(network, netmask);
    
    uint32_t host_bits = 32 - prefix_len;
    uint32_t max_hosts = (1U << host_bits);
    
    bool is_p2p = (prefix_len == 31);
    
    for (int attempt = 0; attempt < max_attempts; attempt++) {
        uint32_t host_id = random_range(0, max_hosts - 1);
        uint32_t ip = network | host_id;
        
        if (is_p2p || (ip != network && ip != broadcast)) {
            if (success) *success = true;
            return ip;
        }
    }    
    return 0;
}



uint32_t generate_ip_in_range(uint32_t start_ip, uint32_t end_ip) {
    if (start_ip > end_ip) {
        uint32_t temp = start_ip;
        start_ip = end_ip;
        end_ip = temp;
    }
    return random_range(start_ip, end_ip);
}



bool check_generation_feasibility(const ProgramOptions *opts) {
    if (!opts || opts->count <= 0) return false;
    
    if (opts->has_cidr) {
        uint32_t ok = count_available_hosts(opts->cidr_prefix);
        if ((uint32_t)opts->count > ok) {
            fprintf(stderr, "subnet /%d ha solo %u host disponibili, ma richiesti %d IP\n", opts->cidr_prefix, ok, opts->count);
            return false;
        }
    }
    if (opts->has_range) {
        uint64_t range_size = (uint64_t)opts->range_end - opts->range_start + 1;
        if ((uint32_t)opts->count > range_size) {
            fprintf(stderr, "range ha solo %llu IP disponibili, ma richiesti %d IP\n", (unsigned long long)range_size, opts->count);
            return false;
        }
    }
    
    return true;
}


int generate_unique_ips(const ProgramOptions *opts, IPAddress *output) {
    if (!opts || !output) return -1;
    
    if (!check_generation_feasibility(opts)) {
        return -1;
    }
    
    // Crea un set per tracciare l'unicità
    IPSet *used_ips = ipset_create(opts->count);
    if (!used_ips) {
        fprintf(stderr, "Errore: allocazione memoria per IPSet\n");
        return -1;
    }
    
    int generated = 0;
    int consecutive_failures = 0;
    const int max_consecutive_failures = 1000;
    
    while (generated < opts->count) {
        uint32_t ip;
        bool valid = false;
        
        if (opts->has_cidr) {
            bool success;
            ip = generate_ip_in_cidr(opts->cidr_network, opts->cidr_prefix,
                                    100, &success);
            if (!success) {
                consecutive_failures++;
                if (consecutive_failures >= max_consecutive_failures) {
                    fprintf(stderr, "Errore: impossibile generare IP nella subnet specificata\n");
                    break;
                }
                continue;
            }
            valid = true;
        } else if (opts->has_range) {
            ip = generate_ip_in_range(opts->range_start, opts->range_end);
            valid = true;
        } else if (opts->class_filter != '\0') {
            ip = generate_ip_by_class(opts->class_filter);
            valid = true;
        } else {
            ip = generate_random_ip();
            valid = true;
        }
        
        if (!valid) {
            consecutive_failures++;
            continue;
        }
        
        if (opts->class_filter != '\0' && (opts->has_cidr || opts->has_range)) {
            char ip_class = classify_ip(ip);
            if (ip_class != opts->class_filter) {
                consecutive_failures++;
                if (consecutive_failures >= max_consecutive_failures) {
                    fprintf(stderr, "Errore: impossibile trovare IP di classe %c "
                                   "nel range/subnet specificato\n", opts->class_filter);
                    break;
                }
                continue;
            }
        }
        
        if (ipset_contains(used_ips, ip)) {
            consecutive_failures++;
            if (consecutive_failures >= max_consecutive_failures) {
                fprintf(stderr, "Errore: troppi IP duplicati, probabilmente esauriti "
                               "gli IP disponibili\n");
                break;
            }
            continue;
        }
        
        if (!ipset_add(used_ips, ip)) {
            fprintf(stderr, "Errore: impossibile aggiungere IP al set\n");
            break;
        }
        
        populate_ip_address(&output[generated], ip);
        generated++;
        consecutive_failures = 0;
    }
    
    ipset_destroy(used_ips);
    
    return generated;
}


