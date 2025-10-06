#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "myNetLib.h"

/* Prints an ASCII banner and menu */
void printMenu(void) {
    puts("┌───────────────────────────────────────────┐");
    puts("│   ███╗   ██╗███████╗████████╗██╗    ██╗   │");
    puts("│   ████╗  ██║██╔════╝╚══██╔══╝██║    ██║   │");
    puts("│   ██╔██╗ ██║█████╗     ██║   ██║ █╗ ██║   │");
    puts("│   ██║╚██╗██║██╔══╝     ██║   ██║███╗██║   │");
    puts("│   ██║ ╚████║███████╗   ██║   ╚███╔███╔╝   │");
    puts("│   ╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚══╝╚══╝    │");
    puts("│     Network Utility Tool v1.0             │");
    puts("├───────────────────────────────────────────┤");
    puts("│ 1) Inserisci indirizzo IP                 │");
    puts("│ 2) Visualizza IP in binario               │");
    puts("│ 3) Verifica validità IPv4                 │");
    puts("│ 4) Calcola indirizzo di rete (CIDR)       │");
    puts("│ 5) Genera tutti gli host disponibili      │");
    puts("│ 0) Esci                                   │");
    puts("└───────────────────────────────────────────┘");
    printf("Seleziona opzione: ");
}

int main(void) {
    char ip[16];
    int cidr, scelta;
    char* binaryIp;

    while (1) {
        printMenu();
        if (scanf("%d", &scelta) != 1) {
            fprintf(stderr, "Input non valido\n");
            return 1;
        }

        switch (scelta) {
            case 1:
                printf("Inserisci IP (es. 192.168.1.20): ");
                if (scanf("%15s", ip) != 1) { puts("Errore lettura IP"); break; }
                printf("IP impostato su \"%s\"\n", ip);
                break;

            case 2:
                if (strlen(ip) == 0) { puts("IP non ancora impostato."); break; }
                binaryIp = ipToBinary(ip);
                if (binaryIp) {
                    printf("IP in binario: %s\n", binaryIp);
                    free(binaryIp);
                } else {
                    puts("Errore allocazione memoria");
                }
                break;

            case 3:
                if (isValidIPv4(ip)) puts("IP valido");
                else puts("IP non valido");
                break;

            case 4:
                printf("Inserisci CIDR (0-32): ");
                if (scanf("%d", &cidr) != 1 || cidr < 0 || cidr > 32) {
                    puts("CIDR non valido");
                } else {
                    calculateNetworkAddress(ip, cidr);
                }
                break;

            case 5:
                printf("Inserisci CIDR (0-32): ");
                if (scanf("%d", &cidr) != 1 || cidr < 0 || cidr > 32) {
                    puts("CIDR non valido");
                } else {
                    generateHostAddresses(ip, cidr);
                }
                break;

            case 0:
                puts("Uscita. Grazie e arrivederci!");
                return 0;

            default:
                puts("Opzione non riconosciuta.");
        }
        putchar('\n');
    }
    return 0;
}
