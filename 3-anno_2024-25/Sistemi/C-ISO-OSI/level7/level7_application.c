/* C-ISO-OSI - Application layer - Functions

    - Receives input from the user and displays output, typically in the form of text, images, commands.
    - Allows the application to use network protocols (such as HTTP, FTP, SMTP, DNS).
    - Provides network services directly to end-user applications.
    - Interfaces with the presentation layer to send and receive data.

    Takes data from an application (e.g., a chat message), passes it to the presentation layer for further processing, and handles received data from the presentation layer for use by the application.
*/

/* LIBRARY HEADERS */
#include "constants.h"  // Library constants
#include "level7_application.h"
#include "level6_presentation.h"

/* STANDARD HEADERS */
#include <stdio.h>

char* livello7_send(const char* dati) {
    printf("[7] Application - Message to send: %s\n", dati);

    return livello6_send(dati);
}

char* livello7_receive(const char* pdu) {
//    char* dati = livello6_receive(pdu);
    printf("[7] Application - Message received: %s\n", pdu);
    return livello6_receive(pdu);
}
