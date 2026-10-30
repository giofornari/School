#include <stdio.h> // printf, fopen, fgets, fclose

#define FILENAME "mac_list.txt"

int main(void) {
    FILE *f = fopen(FILENAME, "r"); // lettura
    if (!f) {
        printf("errore file");
        return 1;
    }

    int mac_found = 0;     // conto i MAC
    char line[64];         // buf per righe

    while (fgets(line, sizeof line, f)) {
        for (int i = 0; line[i]; i++) {
            if (line[i] == '\n') { // tolgo newline
                line[i] = '\0';
                break;
            }
        }
        if (!line[0]) continue; // se il primo carattere è nullo, salto (riga vuota)

        
        printf("%s\n", line); // stampo la riga
        mac_found++;
    }

    printf("\n%d MAC in tutto\n", mac_found);

    fclose(f);
    return 0;
}