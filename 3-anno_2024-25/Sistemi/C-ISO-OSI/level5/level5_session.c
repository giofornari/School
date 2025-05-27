/* C-ISO-OSI - Session layer - Functions */
#include "constants.h"  // Library constants
#include "level5_session.h"
#include "level4_transport.h"
#include <time.h>
int id_session_generator(){
    time_t now = time(NULL);
    int random = (rand()%1000);
    int new_id = (now % 1000000) * 1000 + random;
    return new_id;
}
char* livello5_send(const char* dati, const char* action) {
    printf("[Livello 5 - Sessione] SEND: Ricevuto payload: '%s', Azione: '%s'\n", dati, action);
    char header_buffer[128];                // inizializza l'header del livello di sessione
    size_t header_len;
    int sess_id;     
    if (*action == "INIT"){
        sess_id = id_session_generator();
        snprintf(header_buffer, sizeof(header_buffer), "[SESS] [INIT] [ID = %d]", sess_id);}     // print and copy into the header_buffer
    else if(*action == "CLOSE"){
        snprintf(header_buffer, sizeof(header_buffer), "[SESS] [CLOSE] [ID = %d]", sess_id);
        sess_id = 0;}
    else
       snprintf(header_buffer, sizeof(header_buffer), "[SESS] [NORMAL] [ID= %d]", sess_id);
       size_t total_len = strlen(header_buffer) + strlen(dati) + 1;
       char* pacchetto = malloc(total_len);
       if (!pacchetto) return NULL;
       snprintf(pacchetto, total_len, "%s%s", header_buffer, dati);

       return livello4_send(pacchetto);
}

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
