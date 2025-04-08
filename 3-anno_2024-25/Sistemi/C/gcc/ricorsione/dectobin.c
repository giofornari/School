// **Stampa la conversione in base 2 di N**

#include <stdio.h>
int num, res;

void convBin(int n) {
    if (n > 1) {
        convBin(n / 2);
    }
    printf("%d", n % 2);
}

int main() {
	printf("\nNumero: ");
	scanf("%d", &num);
	convBin(num);
	return 0;
}
