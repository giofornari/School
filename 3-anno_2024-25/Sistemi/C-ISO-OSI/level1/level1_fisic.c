/* C-ISO-OSI - Physical layer - Functions */
#include "constants.h"  // Library constants
#include "level1_fisic.h"
#include <string.h>


char* fifo[PDU_SIZE];
int fifo_head = 0;
int fifo_tail = 0;

void livello1_send(const char* bitstream) {
    fifo[fifo_tail] = strdup(bitstream); // Copia stringa
    fifo_tail = (fifo_tail + 1) % PDU_SIZE;
}

char* livello1_receive() {
    if (fifo_head == fifo_tail) return NULL; // FIFO vuota
    char* data = fifo[fifo_head];
    fifo_head = (fifo_head + 1) % PDU_SIZE;
    return data;
}
