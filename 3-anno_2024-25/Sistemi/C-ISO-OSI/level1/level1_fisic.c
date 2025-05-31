/* C-ISO-OSI - Physical layer - Franciuto */

// LIBRARY HEADERS
#include "constants.h"  // pdu size
#include "level1_fisic.h"

// STANDARD HEADERS
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#define FIFO_SIZE 16

// FIFO init
static char* fifo[FIFO_SIZE];
static int fifo_head = 0;
static int fifo_tail = 0;
static int fifo_count = 0;

// pointing pos
static int current_recv_pos = 0;

void livello1_send(const char* bitstream) {
    fifo[fifo_tail] = strdup(bitstream);
    
    printf(" │    [1] Physical - Stored in FIFO: %s\n", bitstream);
    
    fifo_tail = (fifo_tail + 1) % FIFO_SIZE;
    fifo_count++;
}

char* livello1_receive() {
    char* data = fifo[fifo_head];
    
    fifo_head = (fifo_head + 1) % FIFO_SIZE;
    fifo_count--;
    
    printf("    │    [1] Physical - POP from FIFO: %s\n", data);
    
    return data;
}

void livello1_init() {
    for (int i = 0; i < FIFO_SIZE; i++) {
        if (fifo[i] != NULL) {
            free(fifo[i]);
            fifo[i] = NULL;
        }
    }
    
    fifo_head = 0;
    fifo_tail = 0;
    fifo_count = 0;
    current_recv_pos = 0;
}
