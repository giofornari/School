#include "../include/ipset.h"
#include <stdlib.h>
#include <string.h>

IPSet* ipset_create(size_t initial_capacity) {
    if (initial_capacity < 1) initial_capacity = 16;
    
    IPSet *set = (IPSet*)malloc(sizeof(IPSet));
    if (!set) return NULL;
    
    set->ips = (uint32_t*)malloc(initial_capacity * sizeof(uint32_t));
    if (!set->ips) {
        free(set);
        return NULL;
    }
    
    set->count = 0;
    set->capacity = initial_capacity;
    return set;
}

bool ipset_contains(const IPSet *set, uint32_t ip) {
    if (!set) return false;
    
    for (size_t i = 0; i < set->count; i++) {
        if (set->ips[i] == ip) return true;
    }
    return false;
}

bool ipset_add(IPSet *set, uint32_t ip) {
    if (!set) return false;
    if (ipset_contains(set, ip)) return false;
    
    if (set->count >= set->capacity) {
        size_t new_capacity = set->capacity * 2;
        uint32_t *new_ips = (uint32_t*)realloc(set->ips, new_capacity * sizeof(uint32_t));
        if (!new_ips) return false;
        
        set->ips = new_ips;
        set->capacity = new_capacity;
    }
    
    set->ips[set->count++] = ip;
    return true;
}


size_t ipset_size(const IPSet *set) {
    return set ? set->count : 0;
}


void ipset_clear(IPSet *set) {
    if (set) set->count = 0;
}

void ipset_destroy(IPSet *set) {
    if (set) {
        if (set->ips) free(set->ips);
        free(set);
    }
}
