#include <stdio.h>  // input/output (printf e scanf).
#include <time.h>   // time(), utilizzata per il generatore casuale.
#include <stdlib.h> // rand() e srand() per numeri casuali.

int launch, num_dadi;

int main()
{
    int faccie, i, j;
    printf("Inserisci il numero di dadi: ");
    scanf("%d", &num_dadi);
    printf("Inserisci il numero di facce del dado: ");
    scanf("%d", &faccie);
    int max_sum = num_dadi * faccie;
    int result[max_sum + 1]; // Array per contare il num di somme possibile
    for (i = 0; i <= max_sum; i++) {
        result[i] = 0; // Inizializza l'array a zero
    }
    srand(time(NULL)); // Inizializza il generatore di numeri casuali

    printf("Inserisci il numero di lanci: ");
    scanf("%d", &launch);

    for (i = 0; i < launch; i++)
    {
        int sum = 0;
        for (j = 0; j < num_dadi; j++)
        {
            sum += (rand() % faccie) + 1; // Genera un numero casuale tra 1 e faccie
        }
        result[sum]++;
    }
    for (i = num_dadi; i <= max_sum; i++)
    {
        printf("Number %d: %d\n", i, result[i]);
    }
    return 0;
}