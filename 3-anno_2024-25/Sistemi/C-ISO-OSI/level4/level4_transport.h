/* C-ISO-OSI - Transport layer - Functions */

// Include guard
#ifndef LEVEL4_TRANSPORT_H
#define LEVEL4_TRANSPORT_H

// Initialize transport layer buffers and state
void livello4_init();

// Send data through the transport layer
char* livello4_send(const char* dati);

// Receive data from the transport layer
char* livello4_receive();

#endif
