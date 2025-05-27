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

char* livello3_receive(const char* pdu) {
    char* data_from_l2 = livello2_receive(pdu); // Get data from Layer 2

    static char forward_datas[256];  // buffer
    const char* header = "[SRC=192.168.1.7] [DST=192.168.1.45] ";

    // Append header and payload
    strcat(forward_datas, header);
    strcat(forward_datas, data_from_l2);

    // Debug print
    printf("[L3] Network - Sending data to L4: \"%s\"\n", forward_datas);

    return forward_datas;
}
