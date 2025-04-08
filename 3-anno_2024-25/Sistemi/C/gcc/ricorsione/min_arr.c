// **Trova il minimo in un array di dimensione dim**
#define MAX 100
#include <stdio.h>
int num[MAX], dim;
int min;
int cercaMin(int n[], int dim) {
	if (dim == 1) {
		return n[dim-1];
	}
    int m = cercaMin(n, dim - 1);
    return (n[dim - 1] < m) ? n[dim - 1] : m;
}
void printArray(int n[], int dim) {
	if (dim > 0) {
	printf("%d", n[dim-1]);
	printArray(n, dim -1);
}
}

int main()
{
	printf("Dimensione: ");
	scanf("%d", &dim);
	printf("\n");
	for (int i =0; i < dim;i++) {
		printf("\033[A                       ");
		printf("\rValore %d: ", i+1);
		scanf("%d", &num[i]);
	}
	min = cercaMin(num, dim);

	printf("\033[A                    ");
	printf("\rValori di arr: ");
	printArray(num, dim);
	printf("\nIl numero trovato è: %d", min);
	return 0;
}
