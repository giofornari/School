/* C-ISO-OSI - Session layer - Functions */
#include "constants.h"  // Library constants
#include "level5_session.h"
#include "level4_transport.h"
#include <stdio.h>

char* livello5_send(const char* dati) {
    printf("[5] Sessione - Messaggio da inviare: %s\n", dati);
    return livello4_send(dati);
}

char* livello5_receive(const char* pdu) {
    printf("[5] Sessione - Messaggio da inviare: %s\n", pdu);
    return livello4_receive(pdu);
}
// da fare
