/* C-ISO-OSI - Network Layer - Fontanesi Francesco
 *
 * Handles the routing of data packets across networks.
 *   - Adding source and destination IP addresses to the PDU
 *   - Establishing logical connections between network nodes
 *
 * In this implementation, the layer receives data from upper layers,
 * adds network headers, and passes it down
 */

// LIBRARY HEADERS
#include "constants.h" // Library constants
#include "level3_network.h"
#include "level2_datalink.h"

// STANDARD HEADERS
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char *livello3_send(const char *dati)
{
    const char *header = "[SRC=192.168.1.7] [DST=192.168.1.45] ";
    
    // len calcs
    int header_len = strlen(header);
    int data_len = strlen(dati);
    int total_len = header_len + data_len + 1; // +1 for '\0'
    
    char *network_pdu = (char *)malloc(total_len);
    
    strcpy(network_pdu, header);
    strcat(network_pdu, dati);
    
    printf(" │    [3] Inviato a livello 2: %s\n", network_pdu);

    return livello2_send(network_pdu);
}

char *livello3_receive()
{
    char *data_from_l2 = livello2_receive();


    // header: "[SRC=xxx.xxx.xxx.xxx] [DST=xxx.xxx.xxx.xxx] "
    char *endSrc = strchr(data_from_l2, ']');

    int srcLen = endSrc - (data_from_l2 + 5);

    char srcIP[16];
    strncpy(srcIP, data_from_l2 + 5, srcLen);
    srcIP[srcLen] = '\0';

    char *dstStart = strstr(endSrc, "[DST=");
    char *endDst = strchr(dstStart, ']');

    int dstLen = endDst - (dstStart + 5);

    char dstIP[16];
    strncpy(dstIP, dstStart + 5, dstLen);
    dstIP[dstLen] = '\0';


    char *pduStart = endDst + 1;
    if (*pduStart == ' ')
        pduStart++;

    char *network_pdu = strdup(pduStart);

    printf("    │    [3] Network - Valid header. Passing data to upper layers: \"%s\"\n", network_pdu);

    free(data_from_l2);

    return network_pdu;
}
