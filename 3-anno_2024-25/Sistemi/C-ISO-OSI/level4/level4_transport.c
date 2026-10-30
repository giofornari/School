/* C-ISO-OSI - Transport layer - Functions - Fornari Giordano and Giorgia Folloni*/
#include "constants.h" // per pdu_size
#include "level3_network.h" // per il livello sottostante

#include <stdio.h> // per printf
#include <string.h> // per strlen, snprintf, strdup
#include <stdlib.h> // per malloc, free, strdup

#define MTU_PAYLOAD 20 // dimensione massima di un pacchetto (i frammenti)
#define MAX_FRAGMENTS 16 // numero massimo di frammenti per evitare overflow
#define MAX_MESSAGES 8 // per la gestione della rocomposizione messaggi 

static int transport_pdu_id_counter = 1; // id del pdu, static perchè visibile solo in questo file

static int msg_ids[MAX_MESSAGES] = {-1};                            // ID dei messaggi
static int msg_total_fragments[MAX_MESSAGES] = {0};                 // il numero di frsmmenti per ogni messaggio
static int msg_fragments_received[MAX_MESSAGES] = {0};              // frammenti ricevuti
static int msg_in_use[MAX_MESSAGES] = {0};                          // array di flag per tracciare ??
static char *msg_fragments[MAX_MESSAGES][MAX_FRAGMENTS] = {{NULL}}; // array di frammenti per ogni messaggio


char *livello4_send(const char *sdu_l5)
{
    if (sdu_l5 == NULL) {
        printf("qualcosa è andato storto, gli sviluppatori si scusano per il disagio.\n");
        return NULL;
    }

    size_t sdu_len = strlen(sdu_l5);

    int num_fragments = (sdu_len == 0) ? 1 : (sdu_len + MTU_PAYLOAD - 1) / MTU_PAYLOAD; // operatore ternario (nn avevo voglia di scrivere un if) per calcolare il numero di frammenti
    int current_id = transport_pdu_id_counter++; // assegno 1 e incremento l'id del pdu per il prossimo

    for (int k = 0; k < num_fragments; k++) { // mando frammenti
        char pdu_buffer[PDU_SIZE]; // buffer per il PDU per L3
        char header_l4[75]; // per contenere gli header del livello

        snprintf(header_l4, sizeof(header_l4), "[TRANS][FRAG=%d/%d][ID=%02d]", k /* frammento corrente */+ 1, num_fragments, current_id); // usato snprintf per evitare overflow del buffer

        size_t current_payload_offset = k * MTU_PAYLOAD; // calcolo l'offset del payload id curr * 20 (20, 40, 60, ...)
        size_t current_payload_len; // len del payload

        if (sdu_len == 0)
        {
            current_payload_len = 0;
        } 
        else
        {
            current_payload_len = (k == num_fragments - 1) ? (sdu_len - current_payload_offset) : MTU_PAYLOAD; // se k raggiunge il numero totale dei frammenti, la dim sarà la lunghezza rimanente del SDU, altrimenti sarà MTU_PAYLOAD (si, è stato difficile scriverla su una riga)
        }

        snprintf(pdu_buffer, PDU_SIZE, "%s%.*s", header_l4, (int)current_payload_len, sdu_l5 + current_payload_offset); // utilizzo snprintf per evitare overflow

        printf(" │ \n ├─[4] Trasporto SEND - Invio PDU (ID=%02d, Frag=%d/%d) a L3: \"%s...\"\n", current_id, k + 1, num_fragments, pdu_buffer); // fancy log

        livello3_send(pdu_buffer); // il frame arriverà fino al buffer FIFO (l1)

    }
    return NULL; // non ritorno nulla perchè non lev4 non ha un SDU completo da returnare
}

char *livello4_receive() {
    static int initialized; // static per evitare di init multiple di array di frammenti
    if (!initialized) {
        for (int i = 0; i < MAX_MESSAGES; i++) { // azzero le variabili (tipo memset a 0)
            msg_in_use[i] = 0; // (flag se uso)
            msg_ids[i] = -1; // id a -1 (no msg)
            msg_total_fragments[i] = 0; // 0 fram tot
            msg_fragments_received[i] = 0; // 0 fram ricev
            for (int j = 0; j < MAX_FRAGMENTS; j++) { // per ogni frammento memset a 0
                msg_fragments[i][j] = NULL;
            }
        }
        initialized = 1; // non azzero più dopo
    }

    while (1) { // fino a quando non ritorno perchè ho tutti i frammenti
        char *pdu = livello3_receive(); // ricevo il frammento
        if (!pdu) return NULL; // gestisco errori

        // cerco tok "[trans]" nel pdu
        int k, n, id, parsed = 0; // k = frag attuale, n = tot frag, id = id msg
        const char *trans_start = strstr(pdu, "[TRANS]"); // trovo [trans]
        
        // parse header sec formato send: "[trans][frag=%d/%d][id=%d]"
        sscanf(trans_start, "[TRANS][FRAG=%d/%d][ID=%d]%n", &k, &n, &id, &parsed);

        // payload
        const char *payload = trans_start + parsed;
        
        printf("    │    [4] Trasporto RECV - header: k=%d, n=%d, id=%d. frammenro: \"%s\"\n", k, n, id, payload);
        
        // cerco o setto slot per riassemblare msg
        int msg_index = -1;
        int free_slot = -1;
        for (int i = 0; i < MAX_MESSAGES && msg_index == -1; i++) {
            if (msg_in_use[i] && msg_ids[i] == id)
            msg_index = i;
            else if (!msg_in_use[i] && free_slot == -1)
            free_slot = i;
        }
        if (msg_index == -1) { 
            if (free_slot == -1) { // buffer pieno
            printf("[4] ⚠️ trasporto recv err: buffer pieno\n");
            free(pdu);
            continue;
            }
            msg_index = free_slot;            // uso slot libero
            msg_in_use[msg_index] = 1;          // setto flag in uso
            msg_ids[msg_index] = id;            // salvo id
            msg_total_fragments[msg_index] = n; // salvo tot frag
        }
        
        // salvo il frag nel corrispondente slot (indice = k - 1)
        int frag_index = k - 1;
        msg_fragments[msg_index][frag_index] = strdup(payload); // duplica payload
        msg_fragments_received[msg_index]++; // incremento contatore frag
        printf("    ├─[4] Trasporto RECV - salvato frammento %d/%d (id=%d): \"%s\"\n    │ \n", 
               k, n, id, msg_fragments[msg_index][frag_index]);
        free(pdu);
        
        // se ho tutti i frag, riassemblo il msg completo
        if (msg_fragments_received[msg_index] == msg_total_fragments[msg_index]) {
            size_t total_len = 0;
            int valid = 1; // sempre valido qua
            for (int i = 0; i < n; i++) {
            total_len += strlen(msg_fragments[msg_index][i]); // calcolo lunghezza totale
            }
            char *complete = NULL;
            if (valid) {
            complete = malloc(total_len + 1); // alloco buffer per msg
            if (complete) {
                char *ptr = complete;
                for (int i = 0; i < n; i++) {
                size_t len = strlen(msg_fragments[msg_index][i]);
                strcpy(ptr, msg_fragments[msg_index][i]); // copio frag
                ptr += len; 
                }
                *ptr = '\0';
                printf(" ┌─[4] Trasporto RECV - msg riassemblato! (id=%d): \"%s\"\n", id, complete);
            }
            }
            // libero frag e resetto slot
            for (int i = 0; i < MAX_FRAGMENTS; i++) {
            if (msg_fragments[msg_index][i]) {
                free(msg_fragments[msg_index][i]);
                msg_fragments[msg_index][i] = NULL;
            }
            }
            msg_in_use[msg_index] = 0;
            msg_ids[msg_index] = -1;
            msg_total_fragments[msg_index] = 0;
            msg_fragments_received[msg_index] = 0;
            return complete; // msg completo
        }
    }
}