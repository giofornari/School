/**
 * @file main.c
 * @author giordii (admin@giordii.dev)
 * @brief interfaccia utente
 * @version 0.1
 * @date 2025-12-01
 * 
 * @copyright Copyright (c) 2025
 * 
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../include/ip_types.h"
#include "../include/ip_utils.h"
#include "../include/classifier.h"
#include "../include/generator.h"
#include "../include/parser.h"
#include "../include/ipset.h"

/**
 * @brief stampo singolo ip
 * 
 * @param ip puntatore alla struct
 */
void print_ip_info(const IPAddress *ip) {
    if (!ip || !ip->is_valid) {
        fprintf(stderr, "IP non valido\n");
        return;
    }
    printf("%-15s    %c         %s\n", ip->ip_str, ip->class, ip_type_to_string(ip->type));
}

/**
 * @brief stampa intro
 * 
 */
void print_header(void) {
    printf("%-15s    %-9s %s\n", "INDIRIZZO IP", "CLASSE", "TIPO");
    printf("%-15s    %-9s %s\n", "---------------", "------", "----");
}

/**
 * @brief interfaccia utente principale
 * 
 * @details:
 * 1. init del generatore casuale
 * 2. parsing degli args da CLI
 * 3. check opzioni
 * 4. allocazione per IP
 * 5. genera IP con filtri
 * 6. stampa i risultati
 * 7. free tutti
 */
int main(int argc, char *argv[]) {
    init_random_generator();

    ProgramOptions opts;
    
    if (!parse_arguments(argc, argv, &opts)) {
        fprintf(stderr, "Usa -h per vedere l'aiuto\n");
        return EXIT_FAILURE;
    }
    
    if (!validate_options(&opts)) {
        return EXIT_FAILURE;
    }
    
    IPAddress *generated_ips = (IPAddress*)malloc(opts.count * sizeof(IPAddress));
    if (!generated_ips) {
        fprintf(stderr, "impossibile allocare memoria per %d IP\n", opts.count);
        return EXIT_FAILURE;
    }
        
    int num_generated = generate_unique_ips(&opts, generated_ips);
    
    if (num_generated < 0) {
        fprintf(stderr, "error generazione IP\n");
        free(generated_ips);
        return EXIT_FAILURE;
    }
    
    if (num_generated < opts.count) {
        fprintf(stderr, "! generati solo %d IP su %d \n", 
                num_generated, opts.count);
    }
    
    if (num_generated > 0) {
        print_header();
        
        for (int i = 0; i < num_generated; i++) {
            print_ip_info(&generated_ips[i]);
        }
        
        if (num_generated > 1) {
            printf("\nTotale: %d IP generati\n", num_generated);
        }
    } else {
        printf("Nessun IP generato\n");
    }
    
    free(generated_ips);
    
    return EXIT_SUCCESS;
}