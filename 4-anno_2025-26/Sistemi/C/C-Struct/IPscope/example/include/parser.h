#ifndef PARSER_H
#define PARSER_H

#include "ip_types.h"
#include <stdbool.h>
#include <stdint.h>

/**
 * Parsa una stringa in notazione CIDR (es. "192.168.1.0/24")
 * 
 * @param cidr_str Stringa in formato CIDR
 * @param network Puntatore dove salvare il network address
 * @param prefix_len Puntatore dove salvare la lunghezza del prefisso
 * @return true se il parsing ha successo, false altrimenti
 * 
 * Validazioni effettuate:
 * - Formato corretto (IP/prefisso)
 * - IP valido
 * - Prefisso nel range 0-32
 * - Network address corretto (bit host a zero)
 */
bool parse_cidr(const char *cidr_str, uint32_t *network, uint8_t *prefix_len);

/**
 * Parsa una stringa che rappresenta un range di IP (es. "10.0.0.1-10.0.0.255")
 * 
 * @param range_str Stringa in formato "IP1-IP2"
 * @param start_ip Puntatore dove salvare l'IP di inizio
 * @param end_ip Puntatore dove salvare l'IP di fine
 * @return true se il parsing ha successo, false altrimenti
 * 
 * Validazioni:
 * - Formato corretto (IP1-IP2)
 * - Entrambi gli IP validi
 * - start_ip <= end_ip
 */
bool parse_range(const char *range_str, uint32_t *start_ip, uint32_t *end_ip);

/**
 * Parsa gli argomenti della command line usando getopt
 * 
 * @param argc Numero di argomenti
 * @param argv Array di stringhe argomenti
 * @param opts Struttura dove salvare le opzioni parsate
 * @return true se il parsing ha successo, false in caso di errore
 * 
 * Opzioni supportate:
 * -n <numero>     Numero di IP da generare (default: 1)
 * -c <classe>     Filtro per classe (A, B, C, D, E)
 * -i <CIDR>       Genera IP in una specifica subnet
 * -r <range>      Genera IP in un range specifico
 * -h              Mostra help
 */
bool parse_arguments(int argc, char *argv[], ProgramOptions *opts);

/**
 * Stampa il messaggio di aiuto con la sintassi del programma
 * 
 * @param program_name Nome del programma (argv[0])
 */
void print_usage(const char *program_name);

/**
 * Valida le opzioni parsate per verificare la consistenza
 * 
 * @param opts Opzioni da validare
 * @return true se le opzioni sono valide e consistenti
 * 
 * Controlli effettuati:
 * - Numero di IP positivo
 * - Se specificato CIDR, verificare che sia valido
 * - Se specificato range, verificare che sia valido
 * - Compatibilità tra filtri (es. classe + CIDR)
 */
bool validate_options(const ProgramOptions *opts);

#endif // PARSER_H
