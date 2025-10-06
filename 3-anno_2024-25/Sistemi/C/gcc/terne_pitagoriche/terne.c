#include <stdio.h>  // printf, scanf
#include <time.h>  // clock, CLOCKS_PER_SEC
#include <unistd.h> // write(), STDOUT_FILENO
#define N 1000000000  // Numero massimo di terne
int le_terne[N][3];  // Array di terne
int a, b, c, t = 0;
void terne(int max) {
    for (int m = 1; m * m <= max; m++) { // Per ogni m
        for (int n = m + 1; n * n <= max; n++) { // Per ogni n > m. +1 perche m < n
            /*
            Euclid's formula:
            a = n^2 - m^2
            b = 2 * m * n
            c = n^2 + m^2
            Perche? Perche se (m, n) è una coppia di numeri interi positivi, allora (a, b, c) è una terna pitagorica
            */
            a = n * n - m * m;
            b = 2 * m * n;
            c = n * n + m * m;
            if (c > max) {
                break;
            }

            /*
            Dato un tripletta (a, b, c) salva tutte le terne pitagoriche (k * a, k * b, k * c) con k <= N.
            Perche? Perche se (a, b, c) è una terna pitagorica, allora (k * a, k * b, k * c) è una terna pitagorica per ogni k.
            */

            for (int k = 1; k * c <= max; k++) {                
                le_terne[t][0] = k * a;
                le_terne[t][1] = k * b;
                le_terne[t][2] = k * c;
                t++;
            }
        }
    }
}

int main(void) {
    int max;
    printf("Inserisci il valore max: ");
    scanf("%d", &max);
    clock_t start = clock(); // Inizio del calcolo del tempo
    terne(max);
    clock_t end = clock(); // Fine del calcolo del tempo
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Le terne pitagoriche sono:\n");
    for (int i = 0; i < t; i++) {
        printf("Terna %d: %d \t %d \t %d\n", i, le_terne[i][0], le_terne[i][1], le_terne[i][2]);
    }
    printf("Tempo di esecuzione: %f\n", time_spent);
    return 0;
}
