#include "liiib.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char selected[20] = "Invalid";
int main() {
    float n1;
    float n2;
    printf("Benvenuti in ssmd extreme\n");
    scanf("%s", selected);
    printf("n1=");
    scanf("%f", &n1);
    printf("n2=");
    scanf("%f", &n2);
    

    if (strcmp(selected, "somma") == 0) {
        somma(n1, n2);  
    }
    else if (strcmp(selected, "differenza") == 0) {
        diff(n1, n2);  
    }
    else if (strcmp(selected, "moltiplicazione") == 0) {
        molt(n1, n2); 
    }
    else if (strcmp(selected, "divisione") == 0) {
        divis(n1, n2); 
    }
    else {
        printf("Errore: Operazione non valida\n");
    }
}