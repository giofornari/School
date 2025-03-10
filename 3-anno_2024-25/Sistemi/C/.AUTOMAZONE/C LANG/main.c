#include <stdio.h>
#include <stdlib.h>

#define ROWS 8
#define COLS 13

void printMatrix(int matrix[ROWS][COLS]) {
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            printf("%d ", matrix[i][j]);
        }
        printf("\n");
    }
}

int main() {
    int matrix[ROWS][COLS];

    for (int i=0; i<12; i++) {
        // matrix[i]
    }

    printf("Matrix:\n");
    printMatrix(matrix);

    return 0;
}