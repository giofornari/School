#include <stdio.h>   // input/output

int main(void) {
    int num;
    printf("Inserisci un numero da convertire in binario: ");
    scanf("%d", &num);

    // per valore assoluto
    unsigned int u;
    
    
    if (num < 0) {
        printf("-");
        u = ~((unsigned int)num) + 1;
    } else {
        u = (unsigned int) num;
    }
    
    int start = sizeof(int) * 8 - 1;
    while (start >= 0 && ((u >> start) & 1) == 0) {
        start--;
    }
    
    for (int i = start; i >= 0; i--) {
        if ((u >> i) & 1)
            printf("1");
        else
            printf("0");
    }
    printf("\n");
    
    return 0;
}
