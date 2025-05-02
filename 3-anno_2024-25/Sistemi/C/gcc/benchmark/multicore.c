#include <stdio.h> // input/output
#include <stdlib.h> // calloc, free, exit
#include <time.h> // clock, CLOCK_PER_SEC
#include <omp.h> // utilizzo multicore
#include <stdbool.h> // per bool
unsigned long long limite = 0;
unsigned long long count_inge = 0;
unsigned long long count_erato = 0;
double start_time, end_time;

// m ingenuo 
int isPrime(unsigned long long n) {
    if (n <= 1) return 0;  // 0 e 1 non sono primi
    if (n <= 3) return 1;  // 2 e 3 sono primi
    if (n % 2 == 0 || n % 3 == 0) return 0;  // elimino divisibili per 2 e per 3
    
    unsigned long long i = 5;
    while (i * i <= n) { // basta controllare fino alla radice quadrata
        if (n % i == 0 || n % (i + 2) == 0) return 0; // utilizza il metodo 6k +1
        i += 6;
    }
    return 1;
}

// m crivello
void isPrimeErato(unsigned long long limite, unsigned long long *contatore) {
    // add 2 pk  primo pari
    *contatore = 1;
    
    // solo numeri dispari (3, 5, 7, ...)
    unsigned long long dimensione = (limite - 1) / 2;
    
    //  l'array (false = primo, true = no)
    bool *nonPrimi = (bool*)calloc(dimensione, sizeof(bool));
    if (!nonPrimi) {
        printf("Errore di allocazione memoria\n");
        exit(1);
    }
    
    // Usando OpenMP per parallelizzare il crivello
    #pragma omp parallel
    {
        // crivello (non parallelizzabile)
        #pragma omp single
        {
            for (unsigned long long i = 0; i < dimensione; i++) {
                if (!nonPrimi[i]) {
                    unsigned long long numero = 2 * i + 3;
                    
                    // Marchiamo i multipli come non primi
                    unsigned long long indice_iniziale = (numero * numero - 3) / 2;
                    if (indice_iniziale < dimensione) {
                        for (unsigned long long j = indice_iniziale; j < dimensione; j += numero) {
                            nonPrimi[j] = true;
                        }
                    }
                }
            }
        }
        
        // Conteggio 
        unsigned long long contatore_locale = 0;
        #pragma omp for schedule(dynamic, 1000)
        for (unsigned long long i = 0; i < dimensione; i++) {
            if (!nonPrimi[i]) {
                contatore_locale++;
            }
        }
        
        // Aggiorniamo il contatore 
        #pragma omp atomic
        *contatore += contatore_locale;
    }
    
    free(nonPrimi);
}

int main() {
    unsigned long long limite;
    unsigned long long count_inge = 0;
    unsigned long long count_erato = 0;
    double start_time, end_time;
    
    printf("Inserire il limite per la ricerca dei numeri primi: ");
    scanf("%llu", &limite);
    
    // Metodo ingenuo con OpenMP - usa omp_get_wtime() per misurare il tempo reale
    start_time = omp_get_wtime();
    #pragma omp parallel for reduction(+:count_inge)
    for (unsigned long long i = 2; i <= limite; i++) {
        if (isPrime(i)) {
            count_inge++;
        }
    }
    end_time = omp_get_wtime();
    printf("Metodo ingenuo: trovati %llu numeri primi fino a %llu in %f secondi\n", count_inge, limite, end_time - start_time);
    
    // crivello migliorato
    start_time = omp_get_wtime();
    isPrimeErato(limite, &count_erato);
    end_time = omp_get_wtime();
    printf("Metodo crivello: trovati %llu numeri primi fino a %llu in %f secondi\n", count_erato, limite, end_time - start_time);
    
    // verifica 
    if (count_inge == count_erato) {
        printf("I due metodi hanno dato lo stesso risultato: %llu numeri primi trovati.\n", count_inge);
    } else {
        printf("ERRORE: i due metodi hanno dato risultati diversi!\n");
        printf("Differenza: ingenuo=%llu, eratostene=%llu\n", count_inge, count_erato);
    }
    
    return 0;
}