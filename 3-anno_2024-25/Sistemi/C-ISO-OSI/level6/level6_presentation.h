/* C-ISO-OSI - Presentation layer - Fontanesi */

// Include guard
#ifndef LEVEL6_PRESENTATION_H
#define LEVEL6_PRESENTATION_H

// Layer functions
char* livello6_send(const char* dati, const char* enc_type);
char* livello6_receive();
// Fucntions to encrypt/decrypt
char* rot13(const char* input);
#endif
