#include <stdio.h>
#include <string.h>

int ctrlPalidr(char s[], int start, int end) {
    if (start >= end) {
        return 1;
    }
    if (s[start] != s[end]) {
        return 0;
    }
    return ctrlPalidr(s, start + 1, end - 1);
}


int main() {
    char s[100];
    
    printf("Inserisci una stringa: ");
    scanf("%s", s);
    
    if (ctrlPalidr(s, 0, strlen(s)-1)) {
        printf("> \"%s\" = palindroma.\n", s);
    } else {
        printf("> \"%s\" = non palindroma.\n", s);
    }
    
    return 0;
}
