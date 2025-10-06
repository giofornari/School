#include <stdio.h> // printf
#include <time.h>  // clock, CLOCKS_PER_SEC
#include <stdlib.h> // malloc, free

#define MAX_TERNE 1000000000 // 1 miliardo

typedef struct {
    int a;
    int b;
    int c;
} Terna; // struttura le terne

Terna *terne; // init delle terne
int t = 0; // indice delle terne

void salvaTerne(int a, int b, int c, int N) {
    /*
    Dato un tripletta (a, b, c) salva tutte le terne pitagoriche (k * a, k * b, k * c) con k <= N.
    Perche? Perche se (a, b, c) è una terna pitagorica, allora (k * a, k * b, k * c) è una terna pitagorica per ogni k.
    */
    int k = 1;
    while (k * c <= N) {
        terne[t].a = k * a;
        terne[t].b = k * b;
        terne[t].c = k * c;
        t++;
        k++;
    }
}

void generaTerne(int a, int b, int c, int N) {
    /**
     * Genera nuove terne pitagoriche primitive usando le trasformazioni di Berggren.
     *
     * Da una terna primitiva (a, b, c), si possono generare altre tre terne primarie:
     * 
     * 1. (a', b', c') dove:
     *    a' = a - 2b + 2c
     *    b' = 2a - b + 2c
     *    c' = 2a - 2b + 3c
     * 
     * 2. (a', b', c') dove:
     *    a' = a + 2b + 2c
     *    b' = 2a + b + 2c
     *    c' = 2a + 2b + 3c
     * 
     * 3. (a', b', c') dove:
     *    a' = -a + 2b + 2c
     *    b' = -2a + b + 2c
     *    c' = -2a + 2b + 3c
     * 
     * Questa tecnica permette di generare ricorsivamente tutte le terne primitive.
    **/
    if (c > N)
        return;
    
    salvaTerne(a, b, c, N);

    generaTerne(a - 2 * b + 2 * c, 2 * a - b + 2 * c, 2 * a - 2 * b + 3 * c, N);
    generaTerne(a + 2 * b + 2 * c, 2 * a + b + 2 * c, 2 * a + 2 * b + 3 * c, N);
    generaTerne(-a + 2 * b + 2 * c, -2 * a + b + 2 * c, -2 * a + 2 * b + 3 * c, N);
}

int main() {
    int N;
    printf("Inserisci il valore massimo N: ");
    if (scanf("%d", &N) != 1) {
        printf("Input non valido.\n");
        return 1;
    }

    terne = (Terna *)malloc(MAX_TERNE * sizeof(Terna));
    if (terne == NULL) {
        printf("Errore di allocazione della memoria.\n");
        return 1;
    }

    clock_t start = clock(); // Inizio del calcolo del tempo

    generaTerne(3, 4, 5, N);

    clock_t end = clock(); // Fine del calcolo del tempo
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;

    printf("Terne pitagoriche fino a %d:\n", N);
    for (int i = 0; i < t; i++) {
        printf("(%d, %d, %d)\n", terne[i].a, terne[i].b, terne[i].c);
    }

    printf("Tempo di esecuzione: %f secondi\n", time_spent);

    free(terne);
    return 0;
}
