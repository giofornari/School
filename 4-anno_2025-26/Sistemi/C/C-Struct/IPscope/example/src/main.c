/**
 * main.c - Entry point del programma randip
 * 
 * Programma per generare indirizzi IP casuali UNICI con classificazione.
 * 
 * Caratteristiche:
 * - Generazione di IP casuali con garanzia di unicità
 * - Filtro per classe (A, B, C, D, E)
 * - Filtro per subnet CIDR (es. 192.168.1.0/24)
 * - Filtro per range personalizzato
 * - Classificazione: Classe + Tipo (Riservato/Privato/Pubblico)
 * 
 * Architettura:
 * - Modulare: ogni funzionalità in un modulo separato
 * - Strutture dati ben definite
 * - Gestione errori robusta
 * - Documentazione completa
 * 
 * Autore: IPscope Project
 * Data: 2024
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Include dei moduli del progetto
#include "../include/ip_types.h"
#include "../include/ip_utils.h"
#include "../include/classifier.h"
#include "../include/generator.h"
#include "../include/parser.h"
#include "../include/ipset.h"

/**
 * Stampa un singolo IP con le sue informazioni di classificazione
 * 
 * Formato output:
 * xxx.xxx.xxx.xxx    Classe    Tipo
 * 
 * Esempio:
 * 192.168.1.1        C         Pri
 */
void print_ip_info(const IPAddress *ip) {
    if (!ip || !ip->is_valid) {
        fprintf(stderr, "IP non valido\n");
        return;
    }
    
    // Formato tabulare per output leggibile
    printf("%-15s    %c         %s\n", 
           ip->ip_str,
           ip->class,
           ip_type_to_string(ip->type));
}

/**
 * Stampa l'header della tabella di output
 */
void print_header(void) {
    printf("%-15s    %-9s %s\n", "INDIRIZZO IP", "CLASSE", "TIPO");
    printf("%-15s    %-9s %s\n", "---------------", "------", "----");
}

/**
 * Funzione main - Orchestrazione del programma
 * 
 * Flusso:
 * 1. Inizializza il generatore casuale
 * 2. Parsa gli argomenti da command line
 * 3. Valida le opzioni
 * 4. Alloca memoria per gli IP
 * 5. Genera gli IP con i filtri specificati
 * 6. Stampa i risultati
 * 7. Pulisce la memoria
 */
int main(int argc, char *argv[]) {
    // === FASE 1: Inizializzazione ===
    
    // Inizializza il generatore di numeri casuali
    // Deve essere fatto una volta sola all'inizio
    init_random_generator();
    
    // === FASE 2: Parsing Argomenti ===
    
    ProgramOptions opts;
    
    if (!parse_arguments(argc, argv, &opts)) {
        // Parsing fallito, l'errore è già stato stampato
        fprintf(stderr, "Usa -h per vedere l'aiuto\n");
        return EXIT_FAILURE;
    }
    
    // Valida la consistenza delle opzioni
    if (!validate_options(&opts)) {
        return EXIT_FAILURE;
    }
    
    // === FASE 3: Allocazione Memoria ===
    
    // Alloca array per gli IP generati
    IPAddress *generated_ips = (IPAddress*)malloc(opts.count * sizeof(IPAddress));
    if (!generated_ips) {
        fprintf(stderr, "Errore: impossibile allocare memoria per %d IP\n", opts.count);
        return EXIT_FAILURE;
    }
    
    // === FASE 4: Generazione IP ===
    
    int num_generated = generate_unique_ips(&opts, generated_ips);
    
    if (num_generated < 0) {
        // Errore durante la generazione
        fprintf(stderr, "Errore durante la generazione degli IP\n");
        free(generated_ips);
        return EXIT_FAILURE;
    }
    
    if (num_generated < opts.count) {
        // Avviso se non tutti gli IP sono stati generati
        fprintf(stderr, "Attenzione: generati solo %d IP su %d richiesti\n", 
                num_generated, opts.count);
    }
    
    // === FASE 5: Output Risultati ===
    
    if (num_generated > 0) {
        print_header();
        
        for (int i = 0; i < num_generated; i++) {
            print_ip_info(&generated_ips[i]);
        }
        
        // Statistiche finali
        if (num_generated > 1) {
            printf("\nTotale: %d IP generati\n", num_generated);
        }
    } else {
        printf("Nessun IP generato\n");
    }
    
    // === FASE 6: Pulizia ===
    
    free(generated_ips);
    
    return EXIT_SUCCESS;
}

/**
 * === NOTE SUL DESIGN ===
 * 
 * 1. SEPARAZIONE DELLE RESPONSABILITÀ:
 *    Ogni modulo ha un compito specifico e ben definito
 *    - main.c: orchestrazione e I/O
 *    - parser.c: parsing argomenti
 *    - generator.c: generazione IP
 *    - classifier.c: classificazione
 *    - ip_utils.c: operazioni su IP
 *    - ipset.c: gestione unicità
 * 
 * 2. GESTIONE ERRORI:
 *    - Controllo di tutti i valori di ritorno
 *    - Messaggi di errore descrittivi
 *    - Pulizia della memoria anche in caso di errore
 *    - Exit codes appropriati
 * 
 * 3. MEMORIA:
 *    - Allocazione dinamica dove necessario
 *    - Free di tutta la memoria allocata
 *    - Prevenzione di memory leak
 *    - Controllo di NULL dopo malloc/realloc
 * 
 * 4. ESTENDIBILITÀ:
 *    Il design modulare permette facilmente di:
 *    - Aggiungere nuovi filtri
 *    - Cambiare formato output
 *    - Aggiungere statistiche
 *    - Supportare IPv6
 * 
 * 5. TESTING:
 *    La struttura permette testing unitario di ogni modulo:
 *    - Test parser con input validi/non validi
 *    - Test generator con vari filtri
 *    - Test classifier con IP noti
 *    - Test ipset per unicità
 * 
 * 6. PERFORMANCE:
 *    - Uso efficiente della memoria
 *    - Algoritmi O(n) o O(n log n) dove possibile
 *    - Evitati loop infiniti con max_attempts
 *    - Ricerca lineare OK per piccoli set
 * 
 * 7. PORTABILITÀ:
 *    - C standard (C99/C11)
 *    - POSIX per getopt (disponibile su Unix/Linux/macOS)
 *    - Nessuna dipendenza esterna
 *    - Compilabile con gcc/clang
 */
