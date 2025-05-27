/* C-ISO-OSI - Transport layer - Functions */
#include <constants.h>  // Library constants
#include "level4_transport.h"
#include "level5_session.h"
#include "level3_network.h"

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MTU 1500

static int transport_pdu_id_counter = 1;

char* livello4_send(const char* sdu_from_l5) {

    size_t sdu_len = strlen(sdu_from_l5);
    printf("[4] Transport SEND - Ricevuto SDU da L5 (len: %zu): \"%.20s...\"\n", sdu_len, sdu_from_l5);

    if (sdu_len > MTU) {
        printf("[4] Transport SEND WARNING: SDU (len %zu) supera MTU (%d). Verrà inviato come singolo segmento sovradimensionato.\n", sdu_len, MTU);
    }

    char pdu_buffer[PDU_SIZE];
    char header_l4[75];
    
    int current_id = transport_pdu_id_counter++;
    snprintf(header_l4, sizeof(header_l4), "[TRANS][FRAG=1/1][ID=%02d]", current_id); //

    size_t header_len = strlen(header_l4);
    size_t available_for_sdu = PDU_SIZE - header_len - 1;

    if (sdu_len > available_for_sdu) {
        fprintf(stderr, "[4] Transport SEND ERROR: SDU troppo lungo per PDU_SIZE dopo header. SDU verrà troncato.\n");
        snprintf(pdu_buffer, PDU_SIZE, "%s%.*s", header_l4, (int)available_for_sdu, sdu_from_l5);
    } else {
        snprintf(pdu_buffer, PDU_SIZE, "%s%s", header_l4, sdu_from_l5);
    }
    
    printf("[4] Transport SEND - Invio PDU (ID=%02d) a L3: \"%.30s...\"\n", current_id, pdu_buffer);
    return livello3_send(pdu_buffer);
}

char* livello4_receive(const char* pdu_from_l3) {
    if (pdu_from_l3 == NULL) {
        fprintf(stderr, "[4] Transport RECV ERROR: PDU da L3 è NULL.\n");
        return livello5_receive(NULL);
    }
    printf("[4] Transport RECV - Ricevuto PDU da L3: \"%.30s...\"\n", pdu_from_l3);
    
    int k_frag, n_total_frags, pdu_id_received;
    const char* payload_start_ptr = NULL;
    char actual_payload[PDU_SIZE]; 
    
    if (sscanf(pdu_from_l3, "[TRANS][FRAG=%d/%d][ID=%d]%n", &k_frag, &n_total_frags, &pdu_id_received, (int*)&payload_start_ptr) == 3) {
        if (payload_start_ptr == NULL || *payload_start_ptr != ']') {
             fprintf(stderr, "[4] Transport RECV ERROR: Formato header L4 non valido (manca ']'). PDU: \"%s\"\n", pdu_from_l3);
             return livello5_receive(NULL); // PDU malformato
        }
        payload_start_ptr++; 
        
        strncpy(actual_payload, payload_start_ptr, PDU_SIZE - 1);
        actual_payload[PDU_SIZE - 1] = '\0';

        printf("[4] Transport RECV - Header L4 parsato: K=%d, N=%d, ID=%d.\n", k_frag, n_total_frags, pdu_id_received);
        
    } else {
        fprintf(stderr, "[4] Transport RECV ERROR: Header L4 non parsabile: \"%s\"\n", pdu_from_l3);
        return livello5_receive(NULL);
    }

    if (n_total_frags != 1 || k_frag != 1) {
        fprintf(stderr, "[4] Transport RECV ERROR: Ricevuto PDU frammentato (K=%d, N=%d, ID=%d), ma questa versione non supporta la frammentazione/riassemblaggio. PDU scartato.\n", k_frag, n_total_frags, pdu_id_received);
        return livello5_receive(NULL);
    }

    printf("[4] Transport RECV - PDU (ID=%d) singolo (1/1) valido. Payload: \"%.20s...\". Passo a L5.\n", pdu_id_received, actual_payload);
    
    char* sdu_for_l5 = strdup(actual_payload);
    if (!sdu_for_l5) {
        perror("[4] Transport RECV ERROR: strdup fallito per SDU");
        return livello5_receive(NULL);
    }
    
    char* result_from_l5 = livello5_receive(sdu_for_l5);
    free(sdu_for_l5); 
    
    return result_from_l5;
    
    char* livello4_send(const char* dati) {
        printf("[4] Transport - Messaggio da inviare: %s\n", dati);
        return livello3_send(dati);
    }
    
    char* livello4_receive(const char* pdu) {
        printf("[4] Transport - Messaggio da inviare: %s\n", pdu);
        return livello3_receive(pdu);
    }
}