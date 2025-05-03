// main.c
#include "functions.h"

int main() {
    srand(time(NULL));
    
    initialize_matrices();
    
    clock_t start = clock();
    multiply_matrices();
    clock_t end = clock();
    
    print_execution_time(start, end);
    
    return 0;
}
