#include <stdio.h> // printf, fgets, fopen, fclose, fputs, fflush
#include <string.h> // strchr, strcmp, strlen
#include <stdlib.h> // exit
 
#define FILENAME "arp_table.txt"   
#define MAXXLINE 100             // max caratteri per evitare overflow (e quindi vulnerabilità)
#define EXIT "fine"              // parola per uscire dal loop di input

// per compararlo esattamente con "fine" devo rimuovere il newline
void noslashn(char *s) {
    char *newline = strchr(s, '\n'); // ritorna il puntatore al primo '\n' se c'è
    if (newline)
        *newline = '\0';             // la sostituisce col terminatore
}

// per l'utente che inserisce per sbaglio degli spazi all'inizio o alla fine
void strip(char *s) {
    char *p = s; // parto dall'inizio della stringa

    while (*p && *p == ' ')
        p++; // avanti fino alla prima cifra o lettera

    // se ci sono degli spazi sposto l'inizio della stringa
    if (p != s) {
        char *dest = s;
        while (*p) // (fino al terminatore)
            *dest++ = *p++;
        *dest = '\0';
    }

    size_t len = strlen(s);
    if (len == 0) return;

    char *end = s + len - 1; // alla fine controllo se ci sono spazi anche dopo
    while (end >= s && *end == ' ') {
        *end = '\0';
        end--;
    }
}

int isValidIp4(char *s) {
    if (!*s) return 0;               // se è vuoto nn valido
    int segs = 0;

    while (*s) {                           // scorro l'intera stringa per controllare che ci siano 4 segmenti, ognuno tra 0 e 255 
        int val = 0, digits = 0;

        // controllo se ci sono cifre e quante ce ne sono
        while (*s >= '0' && *s <= '9') {
            val = val * 10 + (*s - '0');   // accumolo le cifre in intero e cotrollo il range
            if (val > 255) return 0;
            s++; 
            digits++;
        }

        if (digits == 0) return 0;         // se non ci sono cifre nn valido
        segs++;                            

        if (segs == 4)                     
            return *s == '\0';             
        
        if (*s != '.') return 0;           // controllo che il separatore sia '.'
        s++;                               
    }

    return 0; // se ci sono meno di 4 seg o se c'e un errore
}
int isValidMac(const char *s) {
    if (!s) return 0;

    unsigned char b[6]; // 6 byte per i valori hex
    int counter = 0; // 
    int ok = sscanf(s, "%2hhx:%2hhx:%2hhx:%2hhx:%2hhx:%2hhx%n", &b[0], &b[1], &b[2], &b[3], &b[4], &b[5], &counter); // "%2hhx" 2 sono le cifre massime, hh per unsigned char e x per esadecimale. "%n" salva il numero di caratteri letti
    if (ok != 6 || s[counter] != '\0') return 0;

    return 1; // se valido
}

int main() {
    char line[MAXXLINE];
    FILE *storage = fopen(FILENAME, "a+"); // aggiungo in coda o creo il file se non esiste
    
    if (!storage) {
        printf("impossibile aprire il file '%s'\n", FILENAME);
        return 1;
    }
 
    printf("Arp table. Inserisci ip e mac. '%s' x chiudere:\n", EXIT);
 
    while (1) {
        printf("> ");
        if (!fgets(line, sizeof(line), stdin))
            break;
 
        noslashn(line); // rimuovo newline di fgets
        strip(line);
                
        if (strcmp(line, EXIT) == 0)
            break;

        // separo IP e MAC sul primo spazio
        char *ip = line;
        char *mac = NULL;
        for (char *p = line; *p; p++) {
            if (*p == ' ') {
                *p = '\0';
                mac = p + 1;
                while (*mac == ' ') mac++; // salto se più di uno spazio
                break;
            }
        }

        if (!mac || *mac == '\0') {
            printf("solo uno spazio tra IP e MAC\n");
            continue; // continuo senza salvare
        }
        
        if (!isValidIp4(ip)) {
            printf("'%s' non è un IP\n", ip);
            continue;
        }
        if (!isValidMac(mac)) {
            printf("'%s' non è un MAC\n", mac);
            continue;
        }
        
        fprintf(storage, "%s %s\n", ip, mac); // salvo la coppia IP–MAC
        fflush(storage); // necessario per scrivere subito su disco (senza rimarrebbe in cache)
    }

    printf("\narp table salvata su %s\n\n", FILENAME);
    fclose(storage);

    // riapro il file in sola lettura e stampo tutta la ARP table
    storage = fopen(FILENAME, "r");
    if (!storage) {
        printf("errore file '%s'\n", FILENAME);
        return 1;
    }

    while (fgets(line, sizeof(line), storage)) // finchè fgets ritorna un puntatore non nullo
        fputs(line, stdout); // stampo direttamente la ARP table

    fclose(storage);
    return 0;
}