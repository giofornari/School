/* C-ISO-OSI - Network layer - Functions */
#include "constants.h" // Library constants
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "level3_network.h"
#include "level2_datalink.h"

char *livello3_send(const char *dati)
{
    printf("[L3] Ricevuto da livello 2: %s\n", dati);
    return livello2_send(dati);
}

char *livello3_receive(const char *pdu)
{

    // const char* header = "[SRC=192.168.1.2] [DST=192.168.1.5]";
    char datas = calloc(100, 1);
    strcat(*datas, livello2_receive(pdu));
    /*
    char* src[50] = {'\0'};
    strcat(*src, livello2_receive(pdu));
    printf("[L3: Sending to L4] %s", src);
    return *src;
    */
   printf("\n\n%s\n\n", datas);
   return *datas;
}

/*
char* livello3_receive(const char* pdu) {
    return livello2_receive(pdu);
}*/