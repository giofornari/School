#ifndef IPSET_H
#define IPSET_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

typedef struct {
    uint32_t *ips;
    size_t count;
    size_t capacity;
} IPSet;

IPSet* ipset_create(size_t initial_capacity);
bool ipset_add(IPSet *set, uint32_t ip);
bool ipset_contains(const IPSet *set, uint32_t ip);
size_t ipset_size(const IPSet *set);
void ipset_destroy(IPSet *set);
void ipset_clear(IPSet *set);

#endif
