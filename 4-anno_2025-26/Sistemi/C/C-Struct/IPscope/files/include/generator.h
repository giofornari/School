#ifndef GENERATOR_H
#define GENERATOR_H

#include "ip_types.h"
#include "ipset.h"
#include <stdint.h>
#include <stdbool.h>

/**
 * Inizializza il generatore di numeri casuali
 * Deve essere chiamata una volta all'inizio del programma
 */
void init_random_generator(void);

/**
 * Genera un numero casuale in un range specifico [min, max] (inclusivo)
 * 
 * @param min Valore minimo
 * @param max Valore massimo
 * @return Numero casuale nel range specificato
 */
uint32_t random_range(uint32_t min, uint32_t max);

/**
 * Genera un IP casuale completamente random
 * 
 * @return IP in formato numerico
 */
uint32_t generate_random_ip(void);

/**
 * Genera un IP casuale di una classe specifica
 * 
 * @param class_filter Classe desiderata ('A', 'B', 'C', 'D', 'E')
 * @return IP in formato numerico, o 0 se la classe non è valida
 */
uint32_t generate_ip_by_class(char class_filter);

/**
 * Genera un IP casuale all'interno di una subnet CIDR
 * Esclude automaticamente network e broadcast address
 * 
 * @param network Network address della subnet
 * @param prefix_len Lunghezza del prefisso CIDR
 * @param max_attempts Numero massimo di tentativi (per evitare loop infiniti)
 * @param success Puntatore a flag di successo (opzionale)
 * @return IP generato, o 0 se fallisce dopo max_attempts
 */
uint32_t generate_ip_in_cidr(uint32_t network, uint8_t prefix_len, 
                             int max_attempts, bool *success);

/**
 * Genera un IP casuale in un range specifico
 * 
 * @param start_ip IP di inizio range
 * @param end_ip IP di fine range
 * @return IP nel range specificato
 */
uint32_t generate_ip_in_range(uint32_t start_ip, uint32_t end_ip);

/**
 * Genera un array di IP unici secondo le opzioni specificate
 * Questa è la funzione principale che coordina la generazione
 * 
 * @param opts Opzioni del programma (filtri, numero, ecc.)
 * @param output Array di IPAddress dove salvare i risultati (pre-allocato)
 * @return Numero di IP effettivamente generati, -1 in caso di errore
 * 
 * Note:
 * - L'array output deve essere già allocato con almeno opts->count elementi
 * - Se i vincoli sono troppo restrittivi, potrebbe generare meno IP del richiesto
 */
int generate_unique_ips(const ProgramOptions *opts, IPAddress *output);

/**
 * Verifica se le opzioni permettono di generare il numero richiesto di IP
 * 
 * @param opts Opzioni da verificare
 * @return true se è possibile, false se i vincoli sono troppo restrittivi
 */
bool check_generation_feasibility(const ProgramOptions *opts);

#endif // GENERATOR_H
