// **Stampa un array di interi di dimensione dim al contrario**
#define MAX_DIM 1000
#include <stdio.h>
int dim;
int num[MAX_DIM];

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
	for (int i =0; i < dim;i++) {
		printf("Valore %d\n", i+1);
		scanf("%d", &num[i]);
	}
	printf("Valori di array: \n");
	printArray(num, dim);
	return 0;
}