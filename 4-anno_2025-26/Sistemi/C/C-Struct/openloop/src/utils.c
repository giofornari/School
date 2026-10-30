/**
 * @file utils.c
 * @author giordii (admin@giordii.dev)
 * @brief Funzioni di utilità per openloop
 * @version 1.0
 * @date 2025-12-04
 * 
 * @copyright Copyright (c) 2025 giordii
 * 
 */

#define _POSIX_C_SOURCE 200809L
#include "../include/utils.h"
#include <stdlib.h>
#include <string.h>

void init_open_info(OpenInfo *info) {
    info->tot_opens = 0;
    info->failed_opens = 0;
    info->records = NULL;
    info->records_size = 0;
}

/**
 * @brief add file record to lista dinamica
 * @param info *point alla struct OpenInfo
 * @param fp file pointer da aggiungere
 * @return 0 in caso di successo, -1 in caso di errore
 */
int add_file_record(OpenInfo *info, FILE *fp) {
    int new_size = info->records_size + 1;
    FileRecord *new_records = realloc(info->records, new_size * sizeof(FileRecord));
    
    if (new_records == NULL) return -1;
    
    info->records = new_records;
    
    int fd = fileno(fp);
    
    info->records[info->records_size].fp = fp;
    info->records[info->records_size].index = info->tot_opens + 1;
    info->records[info->records_size].handle = fd;
    
    info->records_size = new_size;
    info->tot_opens++;
    
    return 0;
}

void close_all_files(OpenInfo *info) {
    int closed_count = 0;
    int error_count = 0;
    
    for (int i = 0; i < info->records_size; i++) {
        if (info->records[i].fp != NULL) {
            if (fclose(info->records[i].fp) == 0) {
                closed_count++;
            } else {
                fprintf(stderr, "ERRORE: Impossibile chiudere il file con indice %d (fd=%d)\n", info->records[i].index, info->records[i].handle);
                error_count++;
            }
            info->records[i].fp = NULL;
        }
    }
    
    printf("File chiusi con successo: %d\n", closed_count);
    if (error_count > 0) {
        fprintf(stderr, "ATTENZIONE: %d file non sono stati chiusi correttamente\n", error_count);
    }
}

void print_report(const OpenInfo *info) {
    printf("aperture riuscite: %d\n", info->tot_opens);
    printf("aperture fallite: %d\n", info->failed_opens);
    printf("file aperti: %d\n", info->records_size);
}

/**
 * @brief freee all
 * @param info point struct OpenInfo
 */
void cleanup_open_info(OpenInfo *info) {
    if (info->records != NULL) {
        free(info->records);
        info->records = NULL;
    }
    info->records_size = 0;
}
