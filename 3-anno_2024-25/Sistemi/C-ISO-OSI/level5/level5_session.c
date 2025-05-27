/* C-ISO-OSI - Session layer - Functions */
#include "constants.h"  // Library constants
#include "level5_session.h"
#include "level4_transport.h"
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* livello5_send(const char* dati, const char* action) {
    printf("[Livello 5 - Sessione] SEND: Ricevuto payload: '%s', Azione: '%s'\n", dati, action);
    char header_buffer[128];                // inizializza l'header del livello di sessione
    int sess_id = 0;     
    if (strcmp(action, "INIT") == 0){
        sess_id = 4;
        snprintf(header_buffer, sizeof(header_buffer), "[SESS] [INIT] [ID = %d]", sess_id);     // print and copy into the header_buffer
    }
    else if(strcmp(action, "CLOSE") == 0){
        snprintf(header_buffer, sizeof(header_buffer), "[SESS] [CLOSE] [ID = %d]", sess_id);
        sess_id = 0;
    }
    else {
        snprintf(header_buffer, sizeof(header_buffer), "[SESS] [NORMAL] [ID= %d]", sess_id);
    }
    size_t total_len = strlen(header_buffer) + strlen(dati) + 1;
    char* pack = malloc(total_len);
    snprintf(pack, total_len, "%s%s", header_buffer, dati);

    return livello4_send(pack);
}

/*
char* livello5_receive(const char* pdu) {
    if(pdu == NULL) return NULL;
    char data[PDU_SIZE];
    if(strncmp(pdu, "[SESS]", 6) != 0) {
        printf("ERRORE! header SESS mancante!");
        return NULL;}
    const char* action_start = strchr(pdu + 6, '[');
    const char* action_end = strchr(action_start, ']');
    if (!action_end || !action_start){
        printf("ERRORE! action mancante o malformato!");
        return NULL;}
    


    return 0;
}
// da fare
*/
char* livello5_receive(const char* pdu) {
    if (pdu == NULL) {
        fprintf(stderr, "[Livello 5 - Sessione] RECV ERROR: PDU è NULL.\n");
        return NULL;
    }
    
    printf("[Livello 5 - Sessione] RECV: Ricevuto PDU: '%s'\n", pdu);
    
    // Verifica che il PDU inizi con il header di sessione
    if (strncmp(pdu, "[SESS]", 6) != 0) {
        fprintf(stderr, "[Livello 5 - Sessione] RECV ERROR: Header di sessione mancante.\n");
        return NULL;
    }
    
    // Trova l'azione e l'ID della sessione
    const char* action_start = strchr(pdu + 6, '[');
    const char* action_end = strchr(action_start, ']');
    
    if (!action_end || !action_start) {
        fprintf(stderr, "[Livello 5 - Sessione] RECV ERROR: Azione malformata.\n");
        return NULL;
    }
    
    // Estrai l'azione
    size_t action_len = action_end - action_start - 1;
    char action[32];
    strncpy(action, action_start + 1, action_len);
    action[action_len] = '\0';
    
    // Estrai l'ID della sessione
    int sess_id;
    sscanf(action_end + 1, "[ID = %d]", &sess_id);
    
    printf("[Livello 5 - Sessione] RECV: Azione '%s', ID sessione %d\n", action, sess_id);
    
    // Passa i dati al livello di trasporto
    const char* payload_start = action_end + 1;
    
    return livello4_receive(payload_start);
}