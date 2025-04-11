// Stampa di numeri naturali fino a N

#include <stdio.h>

int num;
void stampaNumeri(int n) {
    if (n > 0) {
        stampaNumeri(n - 1);
        printf("%d ", n);
    }
}

int main() {
    printf("Inserisci un numero positivo: ");
    scanf("%d", &num);
    
    if (num > 0) {
        printf("I numeri da 1 a %d sono: ", num);
        stampaNumeri(num);
        printf("\n");
    } else {
        printf("Errore: il numero deve essere maggiore di 0.\n");
    }
    
    return 0;
}
