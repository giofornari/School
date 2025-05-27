/* C-ISO-OSI - Network layer - Functions */
#include "constants.h" // Library constants
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "level3_network.h"
#include "level2_datalink.h"

char *livello3_send(const char *dati)
{
    printf("[L3] Inviato a livello 2: %s\n", dati);
    return livello2_send(dati);
}

char *livello3_receive(const char *pdu) {
    char *data_from_l2 = livello2_receive(pdu);

    if (data_from_l2 == NULL) {
        printf("[L3] Network - No data received from L2.\n");
        return NULL; // Propagate the NULL up the stack
    }

    printf("[L3] Network - Received PDU from L2: \"%s\"\n", data_from_l2);

    char *data_for_l4 = strdup(data_from_l2);
    if (data_for_l4 == NULL) {
        fprintf(stderr, "[L3] Memory allocation failed for data_for_l4.\n");
        free(data_from_l2);
        return NULL;
    }

    printf("[L3] Network - Sending data to L4: \"%s\"\n", data_for_l4);

    free(data_from_l2);

    return data_for_l4;
}
