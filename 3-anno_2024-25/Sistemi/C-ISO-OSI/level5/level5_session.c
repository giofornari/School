/* livello 5: funzioni dello strato sessione - Giorgia Folloni */
#include "constants.h"  // costanti della libreria
#include "level5_session.h"
#include "level4_transport.h"
#include "level6_presentation.h" // necessario per livello6_receive
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* livello5_send(const char* dati, const char* action) {
    printf("[5] - sessione send: ricevuto payload: '%s', azione: '%s'\n", dati, action);
    char header_buffer[128];                // creazione dell'header per il livello sessione
    static int sess_id = -1; // id di sessione statico per coerenza
    if (strcmp(action, "INIT") == 0) {
        sess_id = rand() % 10000 + 1; // genera un id dinamico compreso tra 1 e 10000
        
        snprintf(header_buffer, sizeof(header_buffer), "[SESS][INIT][ID=%d]", sess_id); // formatta l'header per inizializzazione
    }
    else if(strcmp(action, "CLOSE") == 0) {
        snprintf(header_buffer, sizeof(header_buffer), "[SESS][CLOSE][ID=%d]", sess_id);
        sess_id = -1; // reset dell'id dopo la chiusura
        sess_id = 0;  // impostazione a 0
    }
    else {
        snprintf(header_buffer, sizeof(header_buffer), "[SESS][NORMAL][ID=%d]", sess_id);
    }
    size_t total_len = strlen(header_buffer) + strlen(dati) + 1;
    char* pack = malloc(total_len);
    snprintf(pack, total_len, "%s%s", header_buffer, dati);
    livello4_send(pack);
    return pack;
}

char* livello5_receive() {
    char *pdu = livello4_receive(); // riceve pdu dal livello trasporto

    // estrae l'azione e l'id della sessione
    const char* action_start = strchr(pdu + 6, '[');
    const char* action_end = NULL;
    
    if (action_start) {
        action_end = strchr(action_start, ']');
    }
 
    // estrae l'azione
    size_t action_len = action_end - action_start - 1;
    char action[32];
    strncpy(action, action_start + 1, action_len);
    action[action_len] = '\0';
    
    // ricerca la sezione dell'id
    const char* id_part = action_end + 1;
    while (*id_part == ' ') id_part++; // salta spazi bianchi
        
    // estrae l'id della sessione
    static int sess_id = -1; // id di sessione statico per coerenza tra le chiamate
    sscanf(id_part, "[ID=%d]", &sess_id);
    
    printf("[5] - Sessione RECV: azione '%s', id sessione %d\n\n\n", action, sess_id);
    static int current_session_id = 0;
    if (strcmp(action, "INIT") == 0) {
        current_session_id = sess_id; // id di sessione corrente
        return livello5_receive();
    } else if (strcmp(action, "CLOSE") == 0) {
        current_session_id = -1;
    }
    
    // individua la fine della sezione id
    const char* id_end = strchr(id_part, ']');
    
    // estrae il payload dopo le intestazioni della sessione
    const char* payload_start = id_end + 1;
    
    // salta gli spazi iniziali del payload
    while (*payload_start == ' ') payload_start++;
    
    // cerca l'header del livello presentazione nel payload
    char* pres_header = strstr(payload_start, "[PRES]");
       
    return pres_header; // restituisce il payload decodificato al livello 6
}