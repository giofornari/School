#include <stdio.h>
int e = 0;
int maxum = 100;
int main() {
    printf("Inserisci quante volte ripetere: ");
    scanf("%d", &maxum);
    for (size_t i = 0; i < (maxum); i++) {
        e++;
        printf("%d) Oggi .......... \n", e);
    }
    return 0;
}