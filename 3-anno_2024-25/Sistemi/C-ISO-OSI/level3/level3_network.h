/* C-ISO-OSI - Network layer - Functions - Fontanesi*/

// Include guard
#ifndef LEVEL3_NETWORK_H
#define LEVEL3_NETWORK_H

/* Funzione - livello3_send()
    Function that adds the network header with hard coded IPs
    -- INPUT --
       -> PDU from level2

    -- OUTPUT --
       -> Sends the final PDU to higher levels
*/
char *livello3_send(const char *dati);

/* Function - livello3_send()
    Takes the value passed as input and sends it to layer 2 using its send function
    -- INPUT --
       -> Data to send to layer 2

    -- OUTPUT --
       -> Sends the data to layer 2
*/
char *livello3_receive();

#endif