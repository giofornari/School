#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../include/ip_types.h"
#include "../include/ip_utils.h"
#include "../include/classifier.h"
#include "../include/generator.h"
#include "../include/parser.h"
#include "../include/ipset.h"

void print_ip_info(const IPAddress *ip) {
    if (!ip || !ip->is_valid) {
        fprintf(stderr, "IP non valido\n");
        return;
    }
    
    printf("%-15s    %c         %s\n", 
           ip->ip_str,
           ip->class,
           ip_type_to_string(ip->type));
}

void print_header(void) {
    printf("%-15s    %-9s %s\n", "INDIRIZZO IP", "CLASSE", "TIPO");
    printf("%-15s    %-9s %s\n", "---------------", "------", "----");
}

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
    
    IPAddress *ips = (IPAddress*)malloc(opts.count * sizeof(IPAddress));
    if (!ips) {
        fprintf(stderr, "Errore: impossibile allocare memoria per %d IP\n", opts.count);
        return EXIT_FAILURE;
    }
    
    int n = generate_unique_ips(&opts, ips);
    
    if (n < 0) {
        fprintf(stderr, "Errore durante la generazione degli IP\n");
        free(ips);
        return EXIT_FAILURE;
    }
    
    if (n < opts.count) {
        fprintf(stderr, "Attenzione: generati solo %d IP su %d richiesti\n", 
                n, opts.count);
    }
    
    if (n > 0) {
        print_header();
        
        for (int i = 0; i < n; i++) {
            print_ip_info(&ips[i]);
        }
        
        if (n > 1) {
            printf("\nTotale: %d IP generati\n", n);
        }
    } else {
        printf("Nessun IP generato\n");
    }
    
    free(ips);
    
    return EXIT_SUCCESS;
}
