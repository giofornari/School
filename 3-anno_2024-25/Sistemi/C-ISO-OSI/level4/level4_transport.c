/* C-ISO-OSI - Livello Trasporto - Funzioni */
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

    size_t sdu_len = strlen(sdu_from_l5);
    printf("[4] Trasporto SEND - Ricevuto SDU da L5 (len: %zu): \"%.*s...\"\n", sdu_len, MTU_PAYLOAD, sdu_from_l5);

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
        current_payload_len = (k == num_fragments - 1) ? (sdu_len - current_payload_offset) : MTU_PAYLOAD;

        strcpy(pdu_buffer, header_l4);
        if (current_payload_len > 0) {
            if (strlen(header_l4) + current_payload_len < PDU_SIZE) {
                strncat(pdu_buffer, sdu_from_l5 + current_payload_offset, current_payload_len);
            } else {
                fprintf(stderr, "[4] Trasporto SEND ERRORE: PDU_SIZE troppo piccolo per header e payload del frammento. Payload troncato.\n");
                strncat(pdu_buffer, sdu_from_l5 + current_payload_offset, PDU_SIZE - strlen(header_l4) - 1);
            }
        }
        if (sdu_len == 0) {
             snprintf(pdu_buffer, PDU_SIZE, "%s", header_l4);
        } else {
             snprintf(pdu_buffer, PDU_SIZE, "%s%.*s", header_l4, (int)current_payload_len, sdu_from_l5 + current_payload_offset);
        }


        printf("[4] Trasporto SEND - Invio PDU (ID=%02d, Frag=%d/%d) a L3: \"%.30s...\"\n", current_id, k + 1, num_fragments, pdu_buffer);
        
        char* L3_response = livello3_send(pdu_buffer);
        if(L3_response != NULL) {
        }

        if (sdu_len == 0 && first_pdu_to_return == NULL) { // Dovrebbe essere impostato nel ciclo
            char temp_pdu_for_empty_sdu[100];
            snprintf(temp_pdu_for_empty_sdu, sizeof(temp_pdu_for_empty_sdu), "[TRANS][FRAG=1/1][ID=%02d]", current_id);
            first_pdu_to_return = strdup(temp_pdu_for_empty_sdu);
            if (!first_pdu_to_return) {
                perror("[4] Trasporto SEND ERRORE: strdup fallito per PDU SDU vuota");
            }
        }
    }

    return first_pdu_to_return;
}

char* livello4_receive(const char* pdu_from_l3) {
    if (pdu_from_l3 == NULL) {
        fprintf(stderr, "[4] Trasporto RECV ERRORE: PDU da L3 è NULL.\n");
        return livello5_receive(NULL);
    }
    printf("[4] Trasporto RECV - Ricevuto PDU da L3: \"%.40s...\"\n", pdu_from_l3);
    
    int k_frag, n_total_frags, pdu_id_received;
    int header_actual_len = 0;
    
    if (sscanf(pdu_from_l3, "[TRANS][FRAG=%d/%d][ID=%d]%n",
               &k_frag, &n_total_frags, &pdu_id_received, &header_actual_len) == 3) {
        
        if (header_actual_len <= 0 || pdu_from_l3[header_actual_len -1] != ']') {
             fprintf(stderr, "[4] Trasporto RECV ERRORE: Formato header L4 non valido (manca ']' o problema sscanf). PDU: \"%.30s...\"\n", pdu_from_l3);
             return livello5_receive(NULL); // PDU malformata
        }

        const char* payload_start_ptr = pdu_from_l3 + header_actual_len;
        
        printf("[4] Trasporto RECV - Header L4 analizzato: K=%d, N=%d, ID=%d. Payload (frammento) inizia da: \"%.20s...\"\n",
               k_frag, n_total_frags, pdu_id_received, payload_start_ptr);
        
        if (n_total_frags > 1) {
            printf("[4] Trasporto RECV INFO: Ricevuto frammento %d di %d (ID=%d). Questa versione semplificata non esegue il riassemblaggio completo ma inoltra il payload del frammento corrente.\n",
                   k_frag, n_total_frags, pdu_id_received);
        }

        char* sdu_chunk_for_l5 = strdup(payload_start_ptr);
        
        // Passa la SDU (potenzialmente parziale) al Livello 5
        // return livello5_receive(sdu_chunk_for_l5); 
        // Nota: livello5_receive sarà responsabile della deallocazione di sdu_chunk_for_l5 se necessario,
        // o lo usa e il livello applicazione finale/main dealloca il risultato finale.
        // Basandosi sul pattern, il livello superiore di solito processa e poi il suo risultato è deallocato dal suo chiamante.
        // Quindi se L5 restituisce un nuovo char*, L4 dovrebbe deallocare sdu_chunk_for_l5 *dopo* che L5 restituisce.
        // Adattiamo:
        // char* result_from_l5 = livello5_receive(sdu_chunk_for_l5);
        // free(sdu_chunk_for_l5); // Dealloca il chunk passato a L5
        // return result_from_l5; 
        // Questo è un pattern comune: passare la proprietà, o copiare e deallocare.
        // Dato che L5 riceve `const char* pdu` in alcune implementazioni, e `char*` in altre,
        // è più sicuro se L5 fa `strdup` di ciò di cui ha bisogno se intende modificarlo o memorizzarlo a lungo termine.
        // Se L5 lo legge soltanto, allora `sdu_chunk_for_l5` può essere deallocato qui dopo che L5 ha finito.
        // Il `level5_session.c` fornito `livello5_receive` prende `const char* pdu`
        // e la sua chiamata a `livello4_receive` implica che non dealloca la `pdu` che riceve.
        // Quindi, se `livello5_receive` riceve `sdu_chunk_for_l5`, lo userà.
        // La stringa restituita da `livello5_receive` sarà gestita da L6, ecc.
        // Quindi, `sdu_chunk_for_l5` deve esistere finché L5 non ha finito.
        // Se `livello5_receive` fa `strdup` internamente e lo restituisce, allora `sdu_chunk_for_l5` può essere deallocato qui.
        // Il `level5_session.c` `livello5_receive` chiama `livello4_receive(payload_start)` - questo è un BUG in L5.
        // L5 receive dovrebbe chiamare L4 receive. No, L4 receive chiama L5 receive.
        // Il `level5_session.c` `livello5_receive` ha:
        // `return livello4_receive(payload_start);` -> QUESTO È UN BUG in L5. Dovrebbe essere `livello6_receive(actual_payload_from_L5_PDU);` o passare all'app.
        // Assumendo che L5 sia corretto per chiamare L6 o app:
        // `sdu_chunk_for_l5` è passato a `livello5_receive`. `livello5_receive` lo processerà.
        // Il risultato da `livello5_receive` è ciò che L4_receive restituisce.
        // Il flusso di test di `main.c` `m1 = livello7_receive(p1)` suggerisce che `m1` è la stringa finale.
        // Ogni `livelloX_receive` di solito fa `strdup` del payload dalla PDU che processa e passa quella nuova stringa.
        // Quindi, `sdu_chunk_for_l5` è il payload estratto da L4. L5 lo processerà.
        // Assumiamo che `livello5_receive` faccia la sua copia se necessario, o le funzioni `livelloX_receive`
        // restituiscano un puntatore a una parte della loro PDU di input dopo l'analisi, e il livello finale (L7) faccia `strdup`.
        // Per essere sicuri e semplici, se L4 crea `sdu_chunk_for_l5` tramite `strdup`, dovrebbe essere gestito.
        // Se `livello5_receive` lo processa e restituisce il proprio `char*` (es. dopo la propria analisi), allora
        // `sdu_chunk_for_l5` dovrebbe essere deallocato da L4 dopo che `livello5_receive` restituisce.

        char* result_from_l5 = livello5_receive(sdu_chunk_for_l5);
        free(sdu_chunk_for_l5); // L4 lo ha allocato, L5 lo ha usato, L4 lo dealloca.
        return result_from_l5;

    } else {
        fprintf(stderr, "[4] Trasporto RECV ERRORE: Header L4 non analizzabile o formato PDU non riconosciuto: \"%.30s...\"\n", pdu_from_l3);
        return livello5_receive(NULL); // Passa NULL verso l'alto se la PDU non è analizzabile
    }
}