/* C-ISO-OSI - Physical layer - Functions */

// Include guard
#ifndef LEVEL1_FISIC_H
#define LEVEL1_FISIC_H

// Initialize fifo
void livello1_init();

// Handle send reqeust for level1
void livello1_send(const char* bitstream);
// Handle receive request for level1
char* livello1_receive();

#endif