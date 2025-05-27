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

    const char *header = "[SRC=192.168.1.7] [DST=192.168.1.45]";

    if (data_from_l2 == NULL) {
        printf("[L3] Network - No data received from L2.\n");
        return NULL; // Propagate the NULL up the stack
    }

    //printf("[L3] Network - Received PDU from L2: \"%s\"\n", data_from_l2);

    printf("[L3] Network - Sending data to L4: \"%s\"\n", data_from_l2);

    return data_from_l2;
}
/*
char *livello3_receive(const char *pdu)
{

    // const char* header = "[SRC=192.168.1.2] [DST=192.168.1.5]";
    char datas = calloc(100, 1);
    strcat(*datas, livello2_receive(pdu));

    char* src[50] = {'\0'};
    strcat(*src, livello2_receive(pdu));
    printf("[L3: Sending to L4] %s", src);
    return *src;

   printf("\n\n%s\n\n", datas);
   return *datas;
}
*/
/*
char* livello3_receive(const char* pdu) {
    return livello2_receive(pdu);
}
*/