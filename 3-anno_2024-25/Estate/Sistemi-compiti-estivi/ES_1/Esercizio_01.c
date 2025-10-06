#include <stdio.h> // printf, fgets, fopen, fclose, fputs, fflush
#include <string.h> // strchr, strcmp, strlen
#include <stdlib.h> // exit
 
#define FILENAME "ip_list.txt"   
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
 
int main() {
    char line[MAXXLINE];
    FILE *storage = fopen(FILENAME, "w+");
    
    if (!storage) {
        printf("impossibile aprire il file '%s'\n", FILENAME);
        return 1;
    }
 
    printf("Inserisci gli IP ('%s' x chiudere):\n", EXIT);
 
    while (1) {
        printf("> ");
        if (!fgets(line, sizeof(line), stdin))
            break;
 
        noslashn(line); // rimuovo newline di fgets
        strip(line);
                
        if (strcmp(line, EXIT) == 0)
            break;
        
        if (!isValidIp4(line)) {
            printf("'%s' non è un Ip\n", line);
            continue; // continuo senza salvare
        }
        
        fprintf(storage, "%s\n", line); // salvo l'IP
        fflush(storage); // necessario per scrivere subito su disco (senza rimarrebbe in cache)
    }
    printf("\nIndirizzi salvati su %s\n\n", FILENAME);
    rewind(storage);
    while (fgets(line, sizeof(line), storage))
        fputs(line, stdout); // stampo direttamente gli IP
    fclose(storage);
    return 0;
}