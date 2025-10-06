// **Verifica se gli elementi di un array sono tutti dispari (1) o meno (0)**

#define MAX 100
#include <stdio.h>

int num[MAX], dim;

int contrPar(int i[], int dim) {
	if (dim == 0) {
		return 1;
	}
	if ((i[dim-1] % 2) != 0) {
		return 0;
	}
	return contrPar(i, dim-1);
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
	char *string;
	printf("\nValori di array: ");
	string = (contrPar(num, dim) == 1) ? "pari" : "dispari";
	printf("%s\n", string);
	return 0;
}
