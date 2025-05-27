/* C-ISO-OSI - Network layer - Functions */
#include "constants.h"  // Library constants
#include "level3_network.h"
#include "level2_datalink.h"

char* livello3_send(const char* dati) {
    return livello2_send(dati);
}
char* livello3_receive(const char* pdu) {
    return livello2_receive(pdu);
}
