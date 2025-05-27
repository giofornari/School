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
    char *forward_datas = calloc(100, 1);
    const char *header = "[SRC=192.168.1.7] [DST=192.168.1.45] ";

    if (data_from_l2 == NULL) {
        printf("[L3] Network - No data received from L2.\n");
        return NULL; // Propagate the NULL up the stack
    }
    
    strcat(forward_datas, header);
    strcat(forward_datas, data_from_l2);
    //printf("[L3] Network - Received PDU from L2: \"%s\"\n", data_from_l2);
    // data_forward = strdup(data_from_l2); // Removed undefined variable usage
    
    printf("[L3] Network - Sending data to L4: \"%s\"\n", forward_datas);

    return data_from_l2;
}
