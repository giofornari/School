/**
 * ipset.c - Gestione di un set di indirizzi IP unici
 * 
 * Implementa una struttura dati per memorizzare IP unici con:
 * - Array dinamico che cresce automaticamente
 * - Verifica rapida di duplicati
 * - Gestione efficiente della memoria
 * 
 * Strategie di crescita:
 * - Capacità iniziale configurabile
 * - Raddoppio della capacità quando pieno (growth factor = 2)
 * - Ricerca lineare per semplicità (per piccoli set è efficiente)
 */

#include "../include/ipset.h"
#include <stdlib.h>
#include <string.h>

/**
 * Crea un nuovo IPSet allocando memoria
 * 
 * @param initial_capacity Capacità iniziale (quanti IP può contenere senza realloc)
 * @return Puntatore al nuovo set, NULL se allocazione fallisce
 */
IPSet* ipset_create(size_t initial_capacity) {
    // Capacità minima sensata
    if (initial_capacity < 1) {
        initial_capacity = 16;
    }
    
    // Alloca la struttura IPSet
    IPSet *set = (IPSet*)malloc(sizeof(IPSet));
    if (!set) {
        return NULL;  // Allocazione fallita
    }
    
    // Alloca l'array di IP
    set->ips = (uint32_t*)malloc(initial_capacity * sizeof(uint32_t));
    if (!set->ips) {
        // Allocazione array fallita, libera la struttura
        free(set);
        return NULL;
    }
    
    // Inizializza i campi
    set->count = 0;
    set->capacity = initial_capacity;
    
    return set;
}

/**
 * Verifica se un IP è già presente nel set
 * 
 * Implementazione: ricerca lineare
 * Complessità: O(n)
 * 
 * Per set grandi (>10000 elementi) si potrebbe usare:
 * - Ricerca binaria su array ordinato: O(log n)
 * - Hash table: O(1) medio
 */
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

/**
 * Aggiunge un IP al set se non è già presente
 * 
 * Gestisce automaticamente la crescita dell'array quando necessario
 * Strategia: raddoppia la capacità quando pieno
 * 
 * @return true se aggiunto con successo, false se già presente o errore
 */
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

/**
 * Distrugge il set liberando tutta la memoria
 * 
 * IMPORTANTE: Dopo questa chiamata, il puntatore set non è più valido
 * Pattern corretto:
 *   IPSet *set = ipset_create(100);
 *   // ... uso ...
 *   ipset_destroy(set);
 *   set = NULL;  // Buona pratica
 */
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

/**
 * === OTTIMIZZAZIONI POSSIBILI (per set molto grandi) ===
 * 
 * 1. RICERCA BINARIA:
 *    Mantenere l'array ordinato e usare bsearch()
 *    - ipset_add: O(n) per l'inserimento ordinato
 *    - ipset_contains: O(log n)
 * 
 * 2. HASH TABLE:
 *    Usare una hash table per O(1) lookup
 *    - Richiede gestione collisioni
 *    - Più complessa ma più efficiente per set grandi
 * 
 * 3. BIT SET:
 *    Per lo spazio degli IP (2^32), usare un bitset
 *    - 2^32 bit = 512 MB
 *    - O(1) lookup e insert
 *    - Efficiente solo se il numero di IP generati è grande
 */
