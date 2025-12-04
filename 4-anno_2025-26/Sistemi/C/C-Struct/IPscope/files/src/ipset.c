#include "../include/ipset.h"
#include <stdlib.h>
#include <string.h>

IPSet* ipset_create(size_t initial_capacity) {
    if (initial_capacity < 1) {
        initial_capacity = 16;
    }
    
    IPSet *set = (IPSet*)malloc(sizeof(IPSet));
    if (!set) {
        return NULL;  // Allocazione fallita
    }
    
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
    
    // Ricerca lineare nell'array
    for (size_t i = 0; i < set->count; i++) {
        if (set->ips[i] == ip) {
            return true;  // Trovato
        }
    }
    
    return false;  // Non trovato
}

bool ipset_add(IPSet *set, uint32_t ip) {
    if (!set) return false;
    
    // Verifica se l'IP è già presente
    if (ipset_contains(set, ip)) {
        return false;  // Duplicato, non aggiunto
    }
    
    // Verifica se serve espandere l'array
    if (set->count >= set->capacity) {
        // Raddoppia la capacità
        size_t new_capacity = set->capacity * 2;
        
        // Rialloca l'array con la nuova capacità
        uint32_t *new_ips = (uint32_t*)realloc(set->ips, 
                                               new_capacity * sizeof(uint32_t));
        if (!new_ips) {
            // Realloc fallita, il set rimane invariato
            return false;
        }
        
        // Aggiorna i puntatori
        set->ips = new_ips;
        set->capacity = new_capacity;
    }
    
    // Aggiungi l'IP in fondo all'array
    set->ips[set->count] = ip;
    set->count++;
    
    return true;  // Aggiunto con successo
}

/**
 * Ritorna il numero di IP nel set
 */
size_t ipset_size(const IPSet *set) {
    return set ? set->count : 0;
}

/**
 * Svuota il set senza deallocare memoria
 * Utile per riutilizzare il set mantenendo la capacità allocata
 */
void ipset_clear(IPSet *set) {
    if (set) {
        set->count = 0;
        // Non tocchiamo set->ips e set->capacity
    }
}

void ipset_destroy(IPSet *set) {
    if (set) {
        // Prima libera l'array
        if (set->ips) {
            free(set->ips);
        }
        // Poi libera la struttura
        free(set);
    }
}
