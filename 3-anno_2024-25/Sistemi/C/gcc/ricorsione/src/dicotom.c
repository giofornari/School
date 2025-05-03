#include <stdio.h>
#define MAX 100
int num[MAX];
int dim;
int target;

int cerca(int num[], int left, int right, int target) {
    if (left > right) {
        return -1;  
    }

    int mid = (left + right) / 2;  
    if (num[mid] == target) {
        return mid;  
    }
    else if (target < num[mid]) {
        return cerca(num, left, mid - 1, target);
    }
    else {
        return cerca(num, mid + 1, right, target);
    }
}

int main() {
    printf("Dimensione: ");
	scanf("%d", &dim);
    printf("\n");
    for (int i =0; i < dim;i++) {
        printf("\033[A                       ");
		printf("\rValore %d: ", i+1);
		scanf("%d", &num[i]);
	}
    printf("Num: ");
    scanf("%d", &target);

    int index = cerca(num, 0, dim - 1, target);

    if (index != -1) {
        printf("%d trovato a pos %d\n", target, index+1);
    } else {
        printf("%d non presente\n", target);
    }

    return 0;
}
