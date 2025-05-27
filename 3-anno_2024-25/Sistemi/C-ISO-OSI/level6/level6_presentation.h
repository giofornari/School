/* C-ISO-OSI - Presentation layer - Functions */

// Include guard
#ifndef LEVEL6_PRESENTATION_H
#define LEVEL6_PRESENTATION_H

char* livello6_send(const char* dati);
char* livello6_receive(const char* pdu);
char* rot13_encrypt(const char* input);
char* rot13_decrypt(const char* input);
#endif
