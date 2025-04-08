// **Stampa la somma delle cifre di un numero intero N**

#include <stdio.h> //printf

long long int sommaCifre(long long n) {
	if (n == 0) {
		return 0;
	}
	return (n % 10) + sommaCifre(n / 10);
}

long long int num, scifre = 0;
int main() {
	printf("\n\nNumero: ");
	scanf("%lld", &num);
	scifre = sommaCifre(num);
	printf("La somma delle cifre è: %lld\n", scifre);
	return 0;
}