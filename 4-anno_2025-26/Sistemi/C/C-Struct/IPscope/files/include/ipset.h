#ifndef IPSET_H
#define IPSET_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

/**
 * Struttura per gestire un set di indirizzi IP unici
 * Implementa un array dinamico con crescita automatica
 */
typedef struct {
    uint32_t *ips;          // Array di IP (formato numerico)
    size_t count;           // Numero di IP attualmente memorizzati
    size_t capacity;        // Capacità allocata dell'array
} IPSet;

/**
 * Crea un nuovo IPSet con capacità iniziale specificata
 * 
 * @param initial_capacity Capacità iniziale dell'array
 * @return Puntatore al nuovo IPSet, NULL in caso di errore
 */
IPSet* ipset_create(size_t initial_capacity);

/**
 * Aggiunge un IP al set se non è già presente
 * L'array si espande automaticamente se necessario (raddoppia la capacità)
 * 
 * @param set Set dove aggiungere l'IP
 * @param ip IP da aggiungere
 * @return true se l'IP è stato aggiunto, false se già presente o errore
 */
bool ipset_add(IPSet *set, uint32_t ip);

/**
 * Verifica se un IP è già presente nel set
 * 
 * @param set Set dove cercare
 * @param ip IP da cercare
 * @return true se l'IP è presente nel set
 */
bool ipset_contains(const IPSet *set, uint32_t ip);

/**
 * Restituisce il numero di IP nel set
 * 
 * @param set Set da interrogare
 * @return Numero di IP nel set
 */
size_t ipset_size(const IPSet *set);

/**
 * Libera tutta la memoria allocata dal set
 * 
 * @param set Set da distruggere
 */
void ipset_destroy(IPSet *set);

/**
 * Svuota il set mantenendo la capacità allocata
 * 
 * @param set Set da svuotare
 */
void ipset_clear(IPSet *set);

#endif // IPSET_H
