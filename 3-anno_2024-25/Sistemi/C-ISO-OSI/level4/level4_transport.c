/* C-ISO-OSI - Transport layer - Functions */
#include <constants.h>  // Library constants
#include "level4_transport.h"
#include "level3_network.h"
#include <stdio.h>

char* livello4_send(const char* dati) {
    printf("[4] Transport - Messaggio da inviare: %s\n", dati);
    return livello3_send(dati);
}

char* livello4_receive(const char* pdu) {
    printf("[4] Transport - Messaggio da inviare: %s\n", pdu);
    return livello3_receive(pdu);
}
