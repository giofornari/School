// functions.h
#ifndef FUNCTIONS_H
#define FUNCTIONS_H

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define SIZE 1000

extern double A[SIZE][SIZE], B[SIZE][SIZE], C[SIZE][SIZE];

void initialize_matrices();
void multiply_matrices();
void print_execution_time(clock_t start, clock_t end);

#endif // FUNCTIONS_H
