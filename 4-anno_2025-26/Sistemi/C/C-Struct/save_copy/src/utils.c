/**
 * @file utils.c
 * @author giordii (admin@giordii.dev)
 * @brief safe copy util with structs
 * @version 0.1
 * @date 2025-12-04
 * 
 * @copyright Copyright (c) 2025
 * 
 */
#include "../include/utils.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

#define BUFFER_SIZE 256

int safe_copy(const char *source, const char *dest, CopyStats *stats) {
    FILE *src_file = NULL;
    FILE *dest_file = NULL;
    unsigned char buffer[BUFFER_SIZE];
    size_t bytes_read, bytes_written;
    int result = 0;

    stats->bytes_copied = 0;
    stats->read_errors = 0;
    stats->write_errors = 0;

    src_file = fopen(source, "rb");
    if (src_file == NULL) {
        perror("Errore apertura sorgente");
        return -1;
    }

    dest_file = fopen(dest, "wb");
    if (dest_file == NULL) {
        perror("Errore apertura destinazione");
        fclose(src_file);
        return -1;
    }

    while ((bytes_read = fread(buffer, 1, BUFFER_SIZE, src_file)) > 0) {
        bytes_written = fwrite(buffer, 1, bytes_read, dest_file);
        
        if (bytes_written < bytes_read) {
            perror("Errore durante la scrittura");
            stats->write_errors++;
            fprintf(stderr, "errore di scrittura - scritti %zu byte su %zu richiesti\n", bytes_written, bytes_read);
            result = -1;
            break;
        }
        
        stats->bytes_copied += bytes_written;
    }

    if (ferror(src_file)) {
        perror("Errore durante la lettura");
        stats->read_errors++;
        fprintf(stderr, "errore di lettura dopo %zu byte copiati\n", stats->bytes_copied);
        result = -1;
    }

    if (fclose(src_file) != 0) {
        perror("Errore chiusura sorgente");
    }
    
    if (fclose(dest_file) != 0) {
        perror("Errore chiusura destinazione");
    }

    return result;
}

void print_stats(const CopyStats *stats) {
    printf("Byte copiati: %zu\n", stats->bytes_copied);
    printf("Errori di lettura: %zu\n", stats->read_errors);
    printf("Errori di scrittura: %zu\n", stats->write_errors);
}