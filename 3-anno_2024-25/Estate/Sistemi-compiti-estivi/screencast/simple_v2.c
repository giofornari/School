#include <stdio.h> // printf, puts, snprintf
#include <stdlib.h> // malloc, free, atoi
#include <string.h> // strcpy, strlen
/* GLOB */
const char *exename = "Rubrica Telefonica";  // .rodata (la stringa) + .data (puntatore)
int tot_cc = 0;                             // .data
char *rubr_dyn[100];                       // .bss (array di puntatori inizializzati a NULL)

void add_cc(int index, const char *name, const char *phone) {
    char buffer[128]; // stack (variabile locale)
    snprintf(buffer, sizeof(buffer), "%s - %s", name, phone);

    rubr_dyn[index] = malloc(strlen(buffer) + 1);
    strcpy(rubr_dyn[index], buffer);

    tot_cc++;
}
void printrub(void) {
    printf("\n--- Rubrica ---\n");
    for (int i = 0; i < tot_cc; i++) {
        printf("rubr_dyn[%d] -> %s\n", i, rubr_dyn[i]);
    }
}


void memoryLayout(void) {
    printf("\n--- Memory Layout ---\n");

    printf(".text  funzione memoryLayout: %p\n", (void*)memoryLayout);
    
    printf(".rodata exename (stringa): %p -> %s\n", (void*)exename, exename);
    
    printf(".data   &tot_cc: %p -> %d\n", (void*)&tot_cc, tot_cc);
    
    printf(".bss    rubr_dyn[0] (slot): %p -> %p\n", (void*)&rubr_dyn[0], (void*)rubr_dyn[0]);

    int local_var = 42;
    printf("stack  &local_var: %p\n", (void*)&local_var);

    if (tot_cc > 0)
        printf("heap  rubr_dyn[0]: %p -> %s\n", (void*)rubr_dyn[0], rubr_dyn[0]);
    else
        printf("heap  rubr_dyn[0]: non ancora allocato\n");
}

int main(void) {
    printf("\n\n\t\t %s \n\n\n", exename);

    char *nomi[] = {"Mario", "Anna", "Luca"};
    char *telefoni[] = {"3331234567", "3209876543", "3485554433"};
	
    for (int i = 0; i < 3; i++)
        add_cc(i, nomi[i], telefoni[i]);

    printrub();
    memoryLayout();

    for (int i = 0; i < tot_cc; i++)
        free(rubr_dyn[i]);

    return 0;
}
