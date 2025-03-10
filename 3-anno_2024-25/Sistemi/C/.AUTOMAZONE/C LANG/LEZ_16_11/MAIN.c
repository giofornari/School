#include <stdio.h>
#include <math.h>

int main() {
    float x, y;
    
    printf("Inserici valore primo numero: ");
    scanf("%f", &x);
    printf("Inserici valore secondo numero: ");
    scanf("%f", &y);
        
    while ((y < x) == 1) {
        printf("Riinserisci il secondo numero che deve essere maggiore del primo: ");
        scanf("%f", &y);
    }
    for (float i = x; i <= y; i++) {
        printf("%0.f\n", i);
    }
    return 0;
}

