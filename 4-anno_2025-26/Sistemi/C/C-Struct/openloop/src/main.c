/**
 * @file main.c
 * @author giordii (admin@giordii.dev)
 * @brief Programma openloop - test apertura file fino al limite di sistema
 * @version 1.0
 * @date 2025-12-04
 * 
 * @copyright Copyright (c) 2025 giordii
 * 
 */

#include "../include/utils.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main(int argc, char *argv[]) {
    OpenInfo info;
    init_open_info(&info);

    printf("Avvio openloop - apertura ripetuta di file.txt\n\n");

    while (true) {
        FILE *fp = fopen("file.txt", "r");
        
        if (fp != NULL) {
            if (add_file_record(&info, fp) != 0) {
                fprintf(stderr, "Allocation error\n");
                fclose(fp);
                break;
            }
        } else {
            // Apertura fallita
            perror("fopen");
            info.failed_opens++;
            break;
        }
    }

    printf("Chiusura di tutti i file aperti: \n");
    close_all_files(&info);
    print_report(&info);

    cleanup_open_info(&info);
    
    return EXIT_SUCCESS;
}