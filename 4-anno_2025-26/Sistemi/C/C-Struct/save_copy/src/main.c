/**
 * @file main.c
 * @author giordii (admin@giordii.dev)
 * @brief main entry point for safe_copy project
 * @version 0.1
 * @date 2025-12-04
 * 
 * @copyright Copyright (c) 2025
 * 
 */

#include "../include/utils.h"
#include <stdio.h>
#include <stdlib.h>

void print_help() {
    fprintf(stderr, "Uso: %s <sorgente.txt> <destinazione.txt>\n", __FILE__);
    fprintf(stderr, "\nEsempio:\n");
    fprintf(stderr, "  %s input.txt output.txt\n", __FILE__);
    fprintf(stderr, "\nPer separare stdout e stderr:\n");
    fprintf(stderr, "  %s input.txt output.txt 2>err.log\n", __FILE__);
}

int main(int argc, char *argv[]) {
    CopyStats stats;
    int result;
    
    if (argc != 3) {
        fprintf(stderr, "Errore: numero di argomenti non valido\n\n");
        print_help();
        return EXIT_FAILURE;
    }
        
    result = safe_copy(argv[1], argv[2], &stats);
    
    print_stats(&stats);
    
    if (result != 0 || stats.read_errors > 0 || stats.write_errors > 0) {
        fprintf(stderr, "\nOPERAZIONE COMPLETATA CON ERRORI\n");
        
        if (stats.read_errors > 0) {
            fprintf(stderr, "Rilevati %zu errori di lettura\n", stats.read_errors);
        }
        
        if (stats.write_errors > 0) {
            fprintf(stderr, "Rilevati %zu errori di scrittura\n", stats.write_errors);
        }
        
        if (stats.bytes_copied == 0) {
            fprintf(stderr, "Nessun byte copiato\n");
            return EXIT_FAILURE;
        } else {
            fprintf(stderr, "Copia nn completa - %zu byte copiati prima dell'errore\n", 
                    stats.bytes_copied);
        }
        
        return EXIT_FAILURE;
    }
    
    printf("\nCopia completata!\n");
    return EXIT_SUCCESS;
}