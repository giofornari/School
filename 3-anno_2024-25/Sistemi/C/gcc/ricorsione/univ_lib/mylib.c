#include "mylib.h"

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

void stampaNumeri(int n) {
    if (n > 0) {
        stampaNumeri(n - 1);
        printf("%d ", n);
    }
}

void printArray(int n[], int dim) {
    if (dim > 0) {
        printf("%d", n[dim-1]);
        printArray(n, dim -1);
    }
}

int sommaNum(int num) {
    if (num == 0) {
        return 0;
    }
    return num + sommaNum(num - 1);
}

long long int sommaCifre(long long n) {
    if (n == 0) {
        return 0;
    }
    return (n % 10) + sommaCifre(n / 10);
}

int contrPar(int i[], int dim) {
    if (dim == 0) {
        return 1;
    }
    if ((i[dim-1] % 2) != 0) {
        return 0;
    }
    return contrPar(i, dim-1);
}

int ctrlPalidr(char s[], int start, int end) {
    if (start >= end) {
        return 1;
    }
    if (s[start] != s[end]) {
        return 0;
    }
    return ctrlPalidr(s, start + 1, end - 1);
}

int cercaMin(int n[], int dim) {
    if (dim == 1) {
        return n[dim-1];
    }
    int m = cercaMin(n, dim - 1);
    return (n[dim - 1] < m) ? n[dim - 1] : m;
}

void convBin(int n) {
    if (n > 1) {
        convBin(n / 2);
    }
    printf("%d", n % 2);
}