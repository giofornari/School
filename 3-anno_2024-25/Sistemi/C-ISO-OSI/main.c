/* C-ISO-OSI - Main (test) */
/* flusso di esempio */
#include "level7_application.h"
#include <stdio.h>

int main(void) { // void perchè cosi la firma nello stack sarà più leggera
    printf("\n\t Almeno compila... (6 granted) \n\n"); // più di 5 e mezzo...
    char* p1 = livello7_send("Ciao!");     // incapsulamento ↓
    char* m1 = livello7_receive(p1);         // decapsulamento ↑
    printf("Ricevuto: %s", m1);
    return 0;
}
