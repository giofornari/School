#include "constants.h"
#include "level4_transport.h"
#include "level3_network.h"
#include "level5_session.h"

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MTU_PAYLOAD 20

static int transport_pdu_id_counter = 1;

char* livello4_send(const char* sdu_from_l5) {
    if (sdu_from_l5 == NULL) {
        fprintf(stderr, "[4] Trasporto SEND ERRORE: SDU da L5 è NULL. Invio PDU vuota a L3.\n");
        char pdu_buffer[100];
        int temp_id = transport_pdu_id_counter++;
        snprintf(pdu_buffer, sizeof(pdu_buffer), "[TRANS][FRAG=1/1][ID=%02d]", temp_id);
        livello3_send(pdu_buffer);
        return strdup(pdu_buffer);
    }

    size_t sdu_len = strlen(sdu_from_l5);
    printf("[4] Trasporto SEND - Ricevuto SDU da L5 (len: %zu): \"%.*s\"\n", sdu_len, MTU_PAYLOAD, sdu_from_l5);

    int num_fragments = (sdu_len == 0) ? 1 : (sdu_len + MTU_PAYLOAD - 1) / MTU_PAYLOAD;
    int current_id = transport_pdu_id_counter++;
    char* first_pdu_to_return = NULL;

    printf("[4] Trasporto SEND - SDU (len %zu) richiede %d frammento/i con MTU_PAYLOAD %d.\n", sdu_len, num_fragments, MTU_PAYLOAD);

    for (int k = 0; k < num_fragments; k++) {
        char pdu_buffer[PDU_SIZE];
        char header_l4[75];
        
        snprintf(header_l4, sizeof(header_l4), "[TRANS][FRAG=%d/%d][ID=%02d]", k + 1, num_fragments, current_id);

        size_t current_payload_offset = k * MTU_PAYLOAD;
        size_t current_payload_len;

        if (sdu_len == 0) {
            current_payload_len = 0;
        } else {
            current_payload_len = (k == num_fragments - 1) ? (sdu_len - current_payload_offset) : MTU_PAYLOAD;
        }
        
        snprintf(pdu_buffer, PDU_SIZE, "%s%.*s", header_l4, (int)current_payload_len, sdu_from_l5 + current_payload_offset);

        printf("[4] Trasporto SEND - Invio PDU (ID=%02d, Frag=%d/%d) a L3: \"%.30s...\"\n", current_id, k + 1, num_fragments, pdu_buffer);
        
        livello3_send(pdu_buffer);

        first_pdu_to_return = strdup(pdu_buffer);
        }
        return first_pdu_to_return;
}



char* livello4_receive(const char* pdu_from_l3) {
    
    int k_frag, n_total_frags, pdu_id_received;
    int header_actual_len = 0;
    
    if (sscanf(pdu_from_l3, "[TRANS][FRAG=%d/%d][ID=%d]%n",
               &k_frag, &n_total_frags, &pdu_id_received, &header_actual_len) == 3 &&
        header_actual_len > 0 && pdu_from_l3[header_actual_len - 1] == ']') {

        const char* payload_start_ptr = pdu_from_l3 + header_actual_len;
        
        printf("[4] Trasporto RECV - Header L4 analizzato: K=%d, N=%d, ID=%d. Payload (frammento) inizia da: \"%.20s...\"\n",
               k_frag, n_total_frags, pdu_id_received, payload_start_ptr);
        
        if (n_total_frags > 1) {
            printf("[4] Trasporto RECV INFO: Ricevuto frammento %d di %d (ID=%d). Questa versione semplificata non esegue il riassemblaggio completo ma inoltra il payload del frammento corrente.\n",
                   k_frag, n_total_frags, pdu_id_received);
        }

        char* sdu_chunk_for_l5 = strdup(payload_start_ptr);
        if (!sdu_chunk_for_l5) {
            perror("[4] Trasporto RECV ERRORE: strdup fallito per sdu_chunk_for_l5");
            return livello5_receive(NULL);
        }
        
        char* result_from_l5 = livello5_receive(sdu_chunk_for_l5);
        free(sdu_chunk_for_l5);
        return result_from_l5;

    } else {
        fprintf(stderr, "[4] Trasporto RECV ERRORE: Header L4 non analizzabile o formato PDU non riconosciuto: \"%.30s...\"\n", pdu_from_l3);
        return livello5_receive(NULL);
    }
}