#include <stdio.h> // printf, fgets, fopen, fclose, perror
#include <stdlib.h> // malloc, free, atoi
#include <string.h> // strlen, strcpy, strcat, strcmp, strcspn
#include <ctype.h> // toupper


int main(void) {
    while (1) {
        /* Menu */
        printf("\n=== Questionario ===\n");
        printf("1) Aggiungi domanda\n");
        printf("2) Quiz\n");
        printf("3) Cancella domanda\n");
        printf("0) Esci\n");
        printf("Scelta: ");
        
        char line[32];
        fgets(line, sizeof(line), stdin); // leggo con fgets per evitare overflow
        int scelta = atoi(line); // converto in intero

        if (scelta == 0) { // esco
            return 0;
        }
        else if (scelta == 1) { // aggiungi domanda
            FILE *f = fopen("questionario.txt", "a"); // apro in append per aggiungere righe
            if (!f) { 
                printf("errore file\n");
                continue; 
            }

            char ques[1024], a[1024], b[1024], c[1024], d[1024]; // un buffer per ogni campo (1 KB)

            printf("Domanda > "); 
            fgets(ques, sizeof(ques), stdin);
            printf("A >"); 
            fgets(a, sizeof(a), stdin);
            printf("B > "); 
            fgets(b, sizeof(b), stdin);
            printf("C > "); 
            fgets(c, sizeof(c), stdin);
            printf("D > "); 
            fgets(d, sizeof(d), stdin);

            ques[strcspn(ques, "\n")] = 0; // necessario per rimuovere il newline (da strcspn ottengo l'indice del newline e poi lo sostituisco con null)
            a[strcspn(a, "\n")] = 0;
            b[strcspn(b, "\n")] = 0;
            c[strcspn(c, "\n")] = 0;
            d[strcspn(d, "\n")] = 0;
            
            char good = 'Z';
            while (good < 'A' || good > 'D') { // ripeto finché non ottengo un carattere valido
                printf("Corretta (A,B,C,D): ");
                scanf(" %c", &good);
                good = toupper(good);
            }
            
            fgets(line, sizeof(line), stdin); // senza rimane fuori un newline che fa crashare
            
            fprintf(f, "%s\n%s\n%s\n%s\n%s\n%c\n\n", ques, a, b, c, d, good);
            fclose(f);
            printf("Aggiunta!\n");
        }
        else if (scelta == 2) { // quiz

            FILE *f = fopen("questionario.txt", "r");
            if (!f) { 
                printf("errore file\n");
                return 1;
            }

            int tot = 0, ok = 0;
            char ques[1024], a[1024], b[1024], c[1024], d[1024], good;
            
            while (fgets(ques, sizeof(ques), f)) {
                if (strlen(ques) <= 1) continue; // salto righe vuote (passo direttamente al prossimo ciclo del while)

                ques[strcspn(ques, "\n")] = 0; // rimuovo newline

                fgets(a, sizeof(a), f);
                fgets(b, sizeof(b), f);
                fgets(c, sizeof(c), f);
                fgets(d, sizeof(d), f);
                fscanf(f, " %c", &good); // qui uso scanf perchè leggo 1 char

                a[strcspn(a, "\n")] = 0; // rimuovo newline
                b[strcspn(b, "\n")] = 0;
                c[strcspn(c, "\n")] = 0;
                d[strcspn(d, "\n")] = 0;
                
                tot++;
                printf("\n%d) %s\n", tot, ques);
                printf("A) %s\nB) %s\nC) %s\nD) %s\n", a, b, c, d);
                
                char risp;
                printf("Risposta: ");
                scanf(" %c", &risp);
                risp = toupper(risp);


                int ind_good = (good - 'A'); // verifico corretta con bitwise: trasformo il char in indice (toglieno 'A') --> A=0, B=1, C=2, D=3
                int ind_risp = (risp - 'A');
                if (ind_risp < 0 || ind_risp > 3) {
                    printf("Risposta non valida\n");
                    continue;
                }

                if (ind_good == ind_risp) {
                    printf("Giusto!\n");
                    ok++;
                } else {
                    printf("Sbagliato. Era %c\n", good);
                }
                fgets(line, sizeof(line), f); // leggo la riga vuota di spazio tra le domande
            }
            fclose(f);
            printf("\nPunteggio: %d/%d\n", ok, tot);
        }

        else if (scelta == 3) {
            FILE *f = fopen("questionario.txt", "r");
            if (!f) { 
                printf("errore file o file vuoto\n");
                continue;
            }

            char ques[1024], a[1024], b[1024], c[1024], d[1024], good;
            int num_domande = 0;
            
            char domande[100][1024];  // creo un array per memorizzare in memoria tutte le domande contenute nel file, scartare quella da eliminare e riscriverle nel file
            char risposte_a[100][1024], risposte_b[100][1024], risposte_c[100][1024], risposte_d[100][1024];
            char corrette[100];
            
            printf("\n=== Domande: ===\n");
            
            while (fgets(ques, sizeof(ques), f)) { // finchè ci sono righe
                if (strlen(ques) < 2) continue; // salto righe vuote
                
                ques[strcspn(ques, "\n")] = 0;
                
                fgets(a, sizeof(a), f);
                fgets(b, sizeof(b), f);
                fgets(c, sizeof(c), f);
                fgets(d, sizeof(d), f);
                fscanf(f, " %c", &good);
                
                a[strcspn(a, "\n")] = 0;
                b[strcspn(b, "\n")] = 0;
                c[strcspn(c, "\n")] = 0;
                d[strcspn(d, "\n")] = 0;
                
                // copio le domande nell'array
                strcpy(domande[num_domande], ques);
                strcpy(risposte_a[num_domande], a);
                strcpy(risposte_b[num_domande], b);
                strcpy(risposte_c[num_domande], c);
                strcpy(risposte_d[num_domande], d);
                corrette[num_domande] = good;
                
                printf("%d) %s\n", num_domande + 1, ques);
                num_domande++;
                
                fgets(line, sizeof(line), f); // leggo la riga vuota
            }
            fclose(f);
            
            if (num_domande == 0) {
                printf("file voto\n");
                continue;
            }
            
            // Chiedo quale cancellare
            printf("\n domanda da cancellare: (1-%d, 0 annulla)? ", num_domande);
            fgets(line, sizeof(line), stdin);
            int da_cancellare = atoi(line);
            
            if (da_cancellare == 0) {
                printf("Operazione annullata\n");
                continue;
            }
            
            if (da_cancellare < 1 || da_cancellare > num_domande) {
                printf("Numero non valido\n");
                continue;
            }
            
            // riscrivo il file senza la domanda selezionata
            f = fopen("questionario.txt", "w");
            if (!f) {
                printf("errore nella riscrittura del file\n");
                continue;
            }
            
            for (int i = 0; i < num_domande; i++) {
                if (i != (da_cancellare - 1)) { // salto la domanda da cancellare
                    fprintf(f, "%s\n%s\n%s\n%s\n%s\n%c\n\n", 
                           domande[i], risposte_a[i], risposte_b[i], 
                           risposte_c[i], risposte_d[i], corrette[i]);
                }
            }
            fclose(f);

            printf("Domanda cancellata!\n");
        }
        else {
            printf("Scelta non valida\n");
        }
    }
}