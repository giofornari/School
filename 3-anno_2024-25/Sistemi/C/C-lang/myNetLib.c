/*
#######################################################################################################################################
Esercizio 1: Conversione da Decimale Puntato a Binario 
Scrivere una funzione char* ipToBinary(char* ip) che accetta un IPv4 in formato stringa (es. "192.168.1.1") e stampa la rappresentazione binaria a 32 bit (NB. se riuscite fate ritornare il puntatore ad una stringa allocata dinamicamente con malloc() in cui avrete salvato la rappresentazione binaria come stringa). 
Esempio: Input: "192.168.1.1" →  11000000 10101000 00000001 00000001 
Suggerimento: 
●  Usare strtok() per separare i singoli ottetti. 
●  Convertire ogni ottetto in un intero e poi in binario. 
●  se tornate il puntatore al buffer dinamico, ricordate di deallocare nel 
chiamante con free().

-----------------------------------------------------------------------------------------------------------------------------

Esercizio 2: Verifica Validità di un IPv4 
Scrivere una funzione int isValidIPv4(char* ip) che controlla se una stringa è un IPv4 valido. Un indirizzo è valido se: 
1.  Ha 4 ottetti separati da punti. 
2.  Ogni ottetto è un numero tra 0 e 255. 
Esempio: Input: "256.1.2.3" → Output: false (perché 256 > 255). 
Suggerimento: 
●  Usare sscanf() per estrarre i numeri.

------------------------------------------------------------------------------------------------------------------------------

Esercizio 3: Calcolo Network Address 
Scrivere una funzione void calculateNetworkAddress(char* ip, int cidr) che, dato un IPv4 e un CIDR (es. 192.168.1.10/24), stampi l’indirizzo di rete. 
Esempio: Input: "192.168.1.10", 24 → Output: 192.168.1.0 
Suggerimento: 
1.  Convertire l’IP in un intero a 32 bit (es. uint32_t). 
2.  Applicare una maschera di bit per estrarre la rete. 
3.  c 
4.  Copy 
5.  Download 
6.  network_address = ip_integer & (0xFFFFFFFF << (32 - cidr));

------------------------------------------------------------------------------------------------------------------------------

Esercizio 4: Generazione Indirizzi Host 
Scrivere una funzione void generateHostAddresses(char* networkIp, int cidr) che, dato un network address (es. 192.168.1.0/24), stampi tutti gli indirizzi host possibili (da 192.168.1.1 a 192.168.1.254). 
Suggerimento: 
●  Usare un ciclo per iterare da network_address + 1 a broadcast_address - 
●  conviene implementare la funzione char* uint2ip(unsigned ip_32b, char* ipOctet) che riceve un indirizzo IPv4 come variabile unsigned a 4 Byte e lo converte in stringa, nella notazione ad ottetti. In questo caso lo ritorna sul 
buffer passato dal chiamante nel secondo parametro, ma anche dal puntatore di ritorno (così potete utilizzarla direttamente in una funzione di stampa: per 
es. puts()) 

######################################################################################################################################
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "myNetLib.h"


char* ipToBinary(const char* ip_input) {
    char* binIp = malloc(36);
    if (!binIp) return NULL;
    binIp[0] = '\0';

    char ip[16];
    strncpy(ip, ip_input, sizeof(ip));
    ip[15] = '\0';

    char* num = strtok(ip, ".");
    while (num) {
        int decimal = atoi(num);
        char bin_str[9];
        for (int i = 7; i >= 0; i--) {
            bin_str[i] = (decimal & 1) ? '1' : '0';
            decimal >>= 1;
        }
        bin_str[8] = '\0';
        strcat(binIp, bin_str);

        num = strtok(NULL, ".");
        if (num) strcat(binIp, " ");
    }

    return binIp;
}

void generateHostAddresses(const char* networkIp, int cidr) {
    unsigned seg[4];
    if (sscanf(networkIp, "%u.%u.%u.%u",
               &seg[0], &seg[1], &seg[2], &seg[3]) != 4) {
        printf("IP non valido\n");
        return;
    }
    for (int i = 0; i < 4; i++) {
        if (seg[i] > 255) {
            printf("IP non valido\n");
            return;
        }
    }

    unsigned netInt = 0;
    for (int i = 0; i < 4; i++) {
        netInt = (netInt << 8) | (seg[i] & 0xFF);
    }

    unsigned mask = (cidr == 0) ? 0 : (0xFFFFFFFFu << (32 - cidr));
    unsigned broadcast = netInt | ~mask;

    if (cidr >= 31) {
        printf("Nessun indirizzo host valido per /%d\n", cidr);
        return;
    }

    for (unsigned addr = netInt + 1; addr < broadcast; addr++) {
        printf("Indirizzo di rete: %u.%u.%u.%u\n",
            (addr >> 24) & 0xFF,
            (addr >> 16) & 0xFF,
            (addr >> 8)  & 0xFF,
             addr        & 0xFF);

    }
}


int isValidIPv4(char* ip) {
    int seg[4];
    int count = sscanf(ip, "%d.%d.%d.%d", &seg[0], &seg[1], &seg[2], &seg[3]);
    if (count != 4) {
        printf("c = %d\n", count);
        return 0;
    }
    for (int i = 0; i < 4; i++) {
        if (seg[i] < 0 || seg[i] > 255) {
            return 0;
        }
    }
    return 1;
}

void calculateNetworkAddress(char* ip, int cidr) {
    unsigned int ip_integer = 0;
    int seg2[4];

    if (sscanf(ip, "%d.%d.%d.%d", &seg2[0], &seg2[1], &seg2[2], &seg2[3]) != 4) {
        printf("IP non valido\n");
    }

    
    for (int i = 0; i < 4; i++) {
        ip_integer = (ip_integer << 8) | (seg2[i] & 0xFF);
    }
    unsigned int mask = 0xFFFFFFFF << (32 - cidr);
    unsigned int net = ip_integer & mask;

    printf("Indirizzo di rete: %u.%u.%u.%u\n",
        (net >> 24) & 0xFF,
        (net >> 16) & 0xFF,
        (net >> 8)  & 0xFF,
         net        & 0xFF);
}
