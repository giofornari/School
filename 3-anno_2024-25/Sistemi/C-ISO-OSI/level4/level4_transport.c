/* C-ISO-OSI - Transport layer - Functions */
#include <constants.h>  // Library constants
#include "level4_transport.h"
#include "level3_network.h"

char* livello4_send(const char* dati) {
    return livello3_send(dati);
}

char* livello4_receive(const char* pdu) {
    return livello4_send(pdu);
}
