/* C-ISO-OSI - Session layer - Functions */
#include "constants.h"  // Library constants
#include "level5_session.h"
#include "level4_transport.h"
char* livello5_send(const char* dati) {
    return livello4_send(dati);
}

char* livello5_receive(const char* pdu) {
    return livello4_receive(pdu);
}
