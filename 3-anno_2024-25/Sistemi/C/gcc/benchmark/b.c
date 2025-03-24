#include <stdio.h>
#include <stdlib.h>
#include <time.h>

unsigned long long limite = 0; 
int count_naive = 0;
int count_erato = 0;
clock_t start, end;
double cpu_time_used;

// Metodo ingenuo 
int isPrime(unsigned long long n) {
    if (n <= 1) return 0;  // 0 e 1 non sono primi
    if (n <= 3) return 1;  // 2 e 3 sono primi
    if (n % 2 == 0 || n % 3 == 0) return 0;  // elimino divisibili per 2 e per 3
    
    unsigned long long i = 5;
    while (i * i <= n) {
        if (n % i == 0 || n % (i + 2) == 0) return 0;
        i += 6;
    }
    return 1;
}

// Crivello di Eratostene 
int isPrimeErato(unsigned long long n) {
    if (n <= 1) return 0;  // 0 e 1 non sono primi
    if (n == 2 || n == 3) return 1;  // 2 e 3 sono primi
    if (n % 2 == 0) return 0;  // Pari maggiori di 2 non sono primi
    
    const unsigned long long LIMIT = 1000000000000000; // 10^15
    
    if (n<LIMIT) {
        // Per numeri piccoli, possiamo usare il crivello tradizionale
        char *sieve = (char*)calloc(n + 1, sizeof(char));
        if (!sieve) {
            printf("Errore di allocazione memoria\n");
            exit(1);
        }
        
        // 0 = primo, 1 = non primo nel nostro crivello
        for (unsigned long long i = 2; i * i <= n; i++) {
            if (sieve[i] == 0) {
                for (unsigned long long j = i * i; j <= n; j += i) {
                    sieve[j] = 1;
                }
            }
        }
        
        int result = (sieve[n] == 0) ? 1 : 0;
        free(sieve);
        return result;
    }
    exit(2);
}

int main() {
    scanf("%llu", &limite);
    
    // Test con metodo ingenuo
    start = clock();
    for (unsigned long long i = 2; i <= limite; i++) {
        if (isPrime(i)) {
            count_naive++;
        }
    }
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("Metodo ingenuo: trovati %d numeri primi fino a %llu in %f secondi\n", count_naive, limite, cpu_time_used);
    
    // Test con crivello di Eratostene
    start = clock();
    for (unsigned long long i = 2; i <= limite; i++) {
        if (isPrimeErato(i)) {
            count_erato++;
        }
    }
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("Metodo crivello: trovati %d numeri primi fino a %llu in %f secondi\n", count_erato, limite, cpu_time_used);
    
    // Verifica che i due metodi diano lo stesso risultato
    if (count_naive == count_erato) {
        printf("I due metodi hanno dato lo stesso risultato: %d numeri primi trovati.\n", count_naive);
    } else {
        printf("ERRORE: i due metodi hanno dato risultati diversi!\n");
    }
    
    return 0;
}