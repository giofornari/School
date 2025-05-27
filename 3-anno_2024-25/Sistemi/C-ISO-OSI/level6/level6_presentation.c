/* C-ISO-OSI - Presentation layer - Functions

    - Responsible for data translation, encryption, and compression.
    - Converts data from the application layer into a common format for transmission.
    - Implements encoding/decoding schemes (e.g., ASCII, EBCDIC, encryption, compression).
    - Ensures that data sent from the application layer of one system can be read by the application layer of another.

    Takes data from the session layer, applies the selected encoding/decoding (e.g., ROT13), and passes it to the next layer.
*/

/* LIBRARY HEADERS */
#include <constants.h>  // Library constants
#include "level6_presentation.h"
#include "level5_session.h"

/* STANDARD HEADERS */
#include <string.h>
#include <stdio.h>

char tmpbuf[PDU_SIZE] = {0};

char* rot13_encrypt(const char* input) {
    char* output = strdup(input);
    for (int i = 0; output[i] != '\0'; i++) {
        char c = output[i];

        if (c >= 'A' && c <= 'Z') {
            output[i] = ((c - 'A' + 13) % 26) + 'A';
        } else if (c >= 'a' && c <= 'z') {
            output[i] = ((c - 'a' + 13) % 26) + 'a';
        }
    }
    return output;
}
char* rot13_decrypt(const char* input){
    char* output = strdup(input);
    for (int i = 0; output[i] != '\0'; i++) {
        char c = output[i];

        if (c >= 'A' && c <= 'Z') {
            output[i] = ((c - 'A' + 13) % 26) + 'A';
        } else if (c >= 'a' && c <= 'z') {
            output[i] = ((c - 'a' + 13) % 26) + 'a';
        }
    }
    return output;
}

char* livello6_send(const char* dati) {
    printf("[6] Sessione - Messaggio da inviare: %s\n", dati);

    return livello5_send(rot13_encrypt(dati));
}

char* livello6_receive(const char* pdu) {
    printf("[6] Sessione - Messaggio da ricevere: %s\n", pdu);
    return rot13_decrypt(livello5_receive(pdu));
}
