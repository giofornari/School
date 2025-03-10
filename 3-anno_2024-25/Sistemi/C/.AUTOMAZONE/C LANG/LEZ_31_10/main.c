#include <stdio.h>

int main() {
    int x;
    float y;
    printf("Inserisci quante uova: ");
    scanf("%d", &x);
    while (x <= 0) {
        printf("La quantità di uova deve essere superiore a 0");
        scanf("%d", &x);
        
    }
    printf("Inserisci il costo di ogni uovo: ");
    scanf("%f", &y);
    while (y <= 0) {
        printf("Il costo di uova deve essere superiore a 0");
        scanf("%f", &y);
    }
    float spesa;
    spesa = x*y;
    printf("La mamma va a fare spesa, compra %d uova che costano ciascuno %f, spendfe quindi in tutto %f\n", x, y, spesa);    
}