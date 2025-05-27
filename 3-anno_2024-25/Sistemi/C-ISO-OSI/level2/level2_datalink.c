/* C-ISO-OSI - Data Link Layer - Functions - Francesco Fontanesi

    - Appends a control code (checksum) at the end of the payload for error detection.
    - On receiving a frame, verifies the checksum (CRC).
    - If the checksum is correct, forwards the payload to the upper layer.
    - If errors are detected, discards the frame without forwarding.

    Ensures reliable data transfer across the physical link by detecting and handling transmission errors.
*/

/* LIBRARY HEADERS */
#include "constants.h"  // Library constants
#include "level1_fisic.h"
#include "level2_datalink.h"

/* STANDARD HEADERS */
#include <stdlib.h>


char* livello2_receive(const char* pdu) {
    return livello1_receive();
}
char* livello2_send(const char* dati) {
    livello1_send(dati);
    return NULL;
}
