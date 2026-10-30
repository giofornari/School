#include <stdio.h> // input/output
#include <stdlib.h> // calloc, free, exit
#include <stdbool.h> // true/false e bool
#include <time.h> // clock, CLOCK_PER_SEC

unsigned long long limite;
unsigned long long conteggio_metodo1 = 0;
unsigned long long conteggio_metodo2 = 0;
clock_t inizio, fine;
double tempo;
// metodo base
bool isPrimo(unsigned long long limite, unsigned long long *contatore) {
    // Inizializza il contatore
    *contatore = 0;
    
    // Verifica ogni numero da 2 fino al limite
    for (unsigned long long numero = 2; numero <= limite; numero++) {
        bool isPrime = true;
        
        // 0 e 1 non sono primi, ma li abbiamo già esclusi partendo da 2
        
        // Verifica se 'numero' è divisibile per qualche intero da 2 a sqrt(numero)
        for (unsigned long long i = 2; i * i <= numero; i++) {
            if (numero % i == 0) {
                isPrime = false;
                break;  // Se troviamo un divisore, non è primo e usciamo dal ciclo
            }
        }
        
        // Se è primo, incrementa il contatore
        if (isPrime) {
            (*contatore)++;
        }
    }
    
    return true;
}

// crivello
void criveloDiEratostene(unsigned long long limite, unsigned long long *contatore) {
    *contatore = 0;
    
    bool *numeriPrimi = (bool*)malloc((limite + 1) * sizeof(bool));
    if (!numeriPrimi) {
        printf("Errore di allocazione memoria\n");
        exit(1);
    }
    
    // considera tutti i numeri primi
    for (unsigned long long i = 0; i <= limite; i++) {
        numeriPrimi[i] = true;
    }
    
    // 0 e 1 non sono primi
    numeriPrimi[0] = numeriPrimi[1] = false;
    
    // Applica il Crivello di Eratostene
    for (unsigned long long i = 2; i * i <= limite; i++) {
        // se i è primo, elimina tutti multipli
        if (numeriPrimi[i]) {
            for (unsigned long long j = i * i; j <= limite; j += i) {
                numeriPrimi[j] = false;
            }
        }
    }
    
    // numeri primi trovati
    for (unsigned long long i = 2; i <= limite; i++) {
        if (numeriPrimi[i]) {
            (*contatore)++;
        }
    }
    
    // Libera la memoria
    free(numeriPrimi);
}

int main() {
    
    printf("Inserire il limite per la ricerca dei numeri primi: ");
    scanf("%llu", &limite);
    
    // m ingenuo
    inizio = clock();
    isPrimo(limite, &conteggio_metodo1);
    fine = clock();
    tempo = (double)(fine - inizio) / CLOCKS_PER_SEC;
    printf("Metodo ingenuo: trovati %llu numeri primi fino a %llu in %.2f secondi\n", conteggio_metodo1, limite, tempo);
    
    // m crivello 
    inizio = clock();
    criveloDiEratostene(limite, &conteggio_metodo2);
    fine = clock();
    tempo = (double)(fine - inizio) / CLOCKS_PER_SEC;
    printf("Metodo crivello: trovati %llu numeri primi fino a %llu in %.2f secondi\n", conteggio_metodo2, limite, tempo);
    
    // Verifica che i due metodi diano lo stesso risultato
    if (conteggio_metodo1 == conteggio_metodo2) {
        printf("I due metodi hanno dato lo stesso risultato: %llu numeri primi trovati.\n", conteggio_metodo1);
    } else {
        printf("ERRORE: i due metodi hanno dato risultati diversi!\n");
        printf("Differenza: metodo1=%llu, metodo2=%llu\n", conteggio_metodo1, conteggio_metodo2);
    }
    
    return 0;
}