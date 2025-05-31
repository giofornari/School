/* C-ISO-OSI - Presentation layer - Fontanesi

    - Responsible for data translation and encryption (ROT13 only).
    - Converts data from the application layer into a common format for transmission.
    - Implements ROT13 encoding/decoding scheme.
    - Ensures that data sent from the application layer of one system can be read by the application layer of another.

    Takes data from the session layer, applies ROT13 cryptography, and passes it to the next layer.
*/

/* LIBRARY HEADERS */
#include "constants.h"  // Library constants
#include "level5_session.h"

/* STANDARD HEADERS */
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

char* rot13(const char* input) {
    if (input == NULL) return NULL;
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

/* Function - livello6_send()
    Handle send request for level 6
    -- INPUT --
       -> dati: PDU from the caller (level7)
       -> enc_type: Type of encryption to be performed {"active" : "ROT13", "To develop" : "Base64, Hash"}

    -- OUTPUT --
       -> String decrypted
*/
char* livello6_send(const char* dati, const char* enc_type) {
    printf("[6] Presentation - Message to send: %s\n", dati);
    printf("\n\n");
    // Check for enc_type
    if (strcmp(enc_type, "ROT13") != 0) {
        printf("Invalid encoding: %s Only ROT13 supprted at the moment", enc_type);
        return NULL;
    }
    // Data encryption
    char *dati_enc = rot13(dati);
    // Header definition (Rot13 hard coded for now)
    const char* header_l6_str = "[PRES][ENC=ROT13]";

    // Calculate sizes
    int header_len = strlen(header_l6_str);
    int enc_len = dati_enc ? strlen(dati_enc) : 0; // If dati_enc != NULL => enc_len = strlen(dati_enc) else enc_len = 0
    
    // Declare some space to store the final PDU
    char* pdu_l6 = (char*)malloc(header_len + enc_len + 1);

    // Compose the final PDU
    strcpy(pdu_l6, header_l6_str);
    strcat(pdu_l6, dati_enc);
    free(dati_enc);
    char *p6 = livello5_send(pdu_l6, "NORMAL");
    printf("\n\n");
    return p6;
}

/* Function - livello6_receive()
    Handle receive request for level 6
    -- INPUT --
       -> dati: PDU from the caller (level5)
    -- OUTPUT --
       -> Decoded content for perfect usage by level 7
*/
char* livello6_receive() {
    // Header to append definition
    char *sdu_l5 = livello5_receive();
    const char* pres_header_tag = "[PRES][ENC=ROT13]";
    const char* payload_ptr;
    char* decoded_sdu;

    // store the entire message
    payload_ptr = sdu_l5 + strlen(pres_header_tag);
    
    // Decode message and print result
    decoded_sdu = rot13(payload_ptr); 
    printf("\033[2A[6] Presentation ROT13 PDU decoded to: \"%s\"\n", decoded_sdu);
    
    return decoded_sdu;
}