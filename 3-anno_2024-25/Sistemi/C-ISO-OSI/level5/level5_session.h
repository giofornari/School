/* C-ISO-OSI - Session layer - Functions */

// Include guard
#ifndef LEVEL5_SESSION_H
#define LEVEL5_SESSION_H

int id_session_generator();
char* livello5_send(const char* dati, const char* action);
char* livello5_receive(const char* pdu);

#endif