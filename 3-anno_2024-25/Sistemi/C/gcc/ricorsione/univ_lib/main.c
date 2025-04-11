#include <stdio.h>
#include <string.h>
#include "mylib.h"

int main() {
    int choice;
    int num[MAX];
    int dim;
    int target;
    char str[100];
    long long int longNum;
    
    printf("===== Recursive Functions Library Demo =====\n");
    printf("1. Binary Search\n");
    printf("2. Generate Anagrams\n");
    printf("3. Print Numbers from 1 to N\n");
    printf("4. Print Array in Reverse\n");
    printf("5. Sum of Numbers up to N\n");
    printf("6. Sum of Digits in a Number\n");
    printf("7. Check if Array Elements are Even\n");
    printf("8. Check if String is Palindrome\n");
    printf("9. Find Minimum in Array\n");
    printf("10. Decimal to Binary Conversion\n");
    printf("Choose a function (1-10): ");
    scanf("%d", &choice);
    
    switch(choice) {
        case 1: 
            printf("\n=== Binary Search ===\n");
            printf("Array size: ");
            scanf("%d", &dim);
            printf("Enter %d elements in ascending order:\n", dim);
            for (int i = 0; i < dim; i++) {
                printf("Element %d: ", i+1);
                scanf("%d", &num[i]);
            }
            printf("Enter target number to find: ");
            scanf("%d", &target);
            
            int index = cerca(num, 0, dim - 1, target);
            if (index != -1) {
                printf("%d found at position %d\n", target, index+1);
            } else {
                printf("%d not found\n", target);
            }
            break;
            
        case 2: 
            printf("\n=== Generate Anagrams ===\n");
            printf("Enter a string: ");
            scanf("%s", str);
            
            int n = strlen(str);
            printf("Anagrams:\n");
            permute(str, 0, n - 1);
            break;
            
        case 3: 
            printf("\n=== Print Numbers from 1 to N ===\n");
            printf("Enter a positive number: ");
            scanf("%d", &target);
            
            if (target > 0) {
                printf("Numbers from 1 to %d: ", target);
                stampaNumeri(target);
                printf("\n");
            } else {
                printf("Error: Number must be greater than 0.\n");
            }
            break;
            
        case 4: 
            printf("\n=== Print Array in Reverse ===\n");
            printf("Array size: ");
            scanf("%d", &dim);
            printf("Enter %d elements:\n", dim);
            for (int i = 0; i < dim; i++) {
                printf("Element %d: ", i+1);
                scanf("%d", &num[i]);
            }
            
            printf("Array in reverse: ");
            printArray(num, dim);
            printf("\n");
            break;
            
        case 5: 
            printf("\n=== Sum of Numbers up to N ===\n");
            printf("Enter a number: ");
            scanf("%d", &target);
            
            printf("Sum of numbers from 1 to %d: %d\n", target, sommaNum(target));
            break;
            
        case 6: 
            printf("\n=== Sum of Digits ===\n");
            printf("Enter a number: ");
            scanf("%lld", &longNum);
            
            printf("Sum of digits in %lld: %lld\n", longNum, sommaCifre(longNum));
            break;
            
        case 7: 
            printf("\n=== Check if Array Elements are Even ===\n");
            printf("Array size: ");
            scanf("%d", &dim);
            printf("Enter %d elements:\n", dim);
            for (int i = 0; i < dim; i++) {
                printf("Element %d: ", i+1);
                scanf("%d", &num[i]);
            }
            
            if (contrPar(num, dim)) {
                printf("All elements are even\n");
            } else {
                printf("Not all elements are even\n");
            }
            break;
            
        case 8: 
            printf("\n=== Palindrome Check ===\n");
            printf("Enter a string: ");
            scanf("%s", str);
            
            if (ctrlPalidr(str, 0, strlen(str)-1)) {
                printf("\"%s\" is a palindrome\n", str);
            } else {
                printf("\"%s\" is not a palindrome\n", str);
            }
            break;
            
        case 9: 
            printf("\n=== Find Minimum in Array ===\n");
            printf("Array size: ");
            scanf("%d", &dim);
            printf("Enter %d elements:\n", dim);
            for (int i = 0; i < dim; i++) {
                printf("Element %d: ", i+1);
                scanf("%d", &num[i]);
            }
            
            printf("Minimum value: %d\n", cercaMin(num, dim));
            break;
            
        case 10: 
            printf("\n=== Decimal to Binary Conversion ===\n");
            printf("Enter a decimal number: ");
            scanf("%d", &target);
            
            printf("%d in binary: ", target);
            convBin(target);
            printf("\n");
            break;
            
        default:
            printf("Invalid choice!\n");
    }
    
    return 0;
}