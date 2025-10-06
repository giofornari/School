// **Stampa la somma dei numeri fino a N**

#include <stdio.h> //printf
int res = 0;
int x = 0;
int sommaNum(int num) {
	if (num==0) {
		return 0;
	}
	return num + sommaNum(num -1);
}
int num;
int main() {
	printf("\n\a\nNumero: ");
	scanf("%d", &num);
	if (num != 0) {
		res = sommaNum(num);
		printf("La somma dei num è: %d", res);
		return 0;
	}
	printf("La somma dei numeri è 0");
	return 0;
}