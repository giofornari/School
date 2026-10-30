#include <stdio.h>
#include <string.h>

void gira(char *x, char *y) {
    char temp = *x;
    *x = *y;
    *y = temp;
}

void permute(char str[], int left, int right) {
    if (left == right) {
        printf("%s\n", str);  
    } else {
        for (int i = left; i <= right; i++) {
            gira(&str[left], &str[i]);           
            permute(str, left + 1, right);       
            gira(&str[left], &str[i]);
        }
    }
}

int main() {
    char str[100];

    printf("Inserisci una stringa: ");
    scanf("%s", str);  

    int n = strlen(str);
    printf("Anagrammi: \n");
    permute(str, 0, n - 1);

    return 0;
}
