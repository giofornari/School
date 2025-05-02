// functions.c
#include "functions.h"

double A[SIZE][SIZE], B[SIZE][SIZE], C[SIZE][SIZE];

void initialize_matrices() {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            A[i][j] = (double)rand() / RAND_MAX;
            B[i][j] = (double)rand() / RAND_MAX;
            C[i][j] = 0.0;
        }
    }
}

void multiply_matrices() {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            for (int k = 0; k < SIZE; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

void print_execution_time(clock_t start, clock_t end) {
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Tempo impiegato per la moltiplicazione delle matrici: %.3f secondi\n", time_spent);
}
