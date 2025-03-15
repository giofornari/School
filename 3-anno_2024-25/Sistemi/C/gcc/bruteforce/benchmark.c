#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define DIM 1000 // Dimensione della matrice

// Dichiarazione delle matrici statiche
double A[DIM][DIM];
double B[DIM][DIM];
double C[DIM][DIM];

int main()
{

    // Inizializza il generatore di numeri casuali
    srand((unsigned int)time(NULL));

    // Inizializza le matrici A e B con numeri casuali
    for (int i = 0; i < DIM; i++)
    {
        for (int j = 0; j < DIM; j++)
        {
            A[i][j] = (double)rand() / RAND_MAX;
            B[i][j] = (double)rand() / RAND_MAX;
        }
    }

    // Inizia la misura del tempo
    clock_t start = clock();

    // Moltiplicazione delle matrici: C = A * B
    for (int i = 0; i < DIM; i++)
    {
        for (int j = 0; j < DIM; j++)
        {
            C[i][j] = 0.0;
            for (int k = 0; k < DIM; k++)
            {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }

    // Termina la misura del tempo
    clock_t end = clock();
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Tempo impiegato per la moltiplicazione delle matrici: %.3f secondi\n", time_spent);

    return 0;
}
