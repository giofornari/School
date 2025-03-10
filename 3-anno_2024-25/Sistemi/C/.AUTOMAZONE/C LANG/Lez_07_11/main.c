#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main() {
    double numero = 2, risultato = 0;
    printf("Numero: ");
    scanf("%lf", &numero);
    risultato = sqrt(numero);    
    printf("Il numero vale %lf, la radice vale %lf", numero, risultato);
    return 0;
}