/* C-ISO/OSI - Datalink - Fornari Giordano at 02:53 AM
    - add/verifica cksum, passa payload se ok 
*/

#include "level1_fisic.h"  // funzioni livello sotto
#include "constants.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

// calc cksum (somma byte dei char)
unsigned char calculate_checksum(const char* d) {
      unsigned int s = 0;
      for (int i = 0; d[i]; ++i) {
                s += (unsigned char)d[i]; // somma byte
      }
      return s % 256; // modulo 256 (byte)
}


// ricevi frame, verif cksum, ritorna payload
char* livello2_receive() {
      char* frame = livello1_receive(); // prendi frame dal lv fisic

      if (frame == NULL) {
                printf("[l2] dl - nessun frame dal lvl fisic\n");
                return NULL;
      }

      char r_ck[3];         // cksum in "xx"
      char r_data[PDU_SIZE]; // buffer dati
      unsigned char calc_ck;

      // trova marker "[chk=" nel frame
      char* m = strstr(frame, "[chk=");
      size_t l = m - frame; // len dati

      if (l >= PDU_SIZE) {
                printf("[l2] err - dati troppo lunghi. l=%zu, frame:%s\n", l, frame);
                free(frame);
                return NULL;
      }
      strncpy(r_data, frame, l); // cp dati
      r_data[l] = '\0';

      // copia 2 caratteri cksum
      strncpy(r_ck, m + 5, 2);
      r_ck[2] = '\0';

      calc_ck = calculate_checksum(r_data);

      // converte cksum calcolato in hex
      char h_ck[3];
      snprintf(h_ck, sizeof(h_ck), "%02x", calc_ck);

      printf("    │    [2] Datalink - frame ok, cksum giusto. dati:\"%.*s...\"\n", (int)(l > 30 ? 30 : l), r_data);

      char* d = strdup(r_data);
      free(frame);
      return d;
}
        
// invia frame: aggiungi cksum e manda a lv fisic
char* livello2_send(const char* d) {
      printf(" │    [2] Datalink - invio: %s\n", d);

      unsigned char ck = calculate_checksum(d);
      char f[PDU_SIZE];
      snprintf(f, sizeof(f), "%s[chk=%02x]", d, ck);
        
      livello1_send(f);
        
      return strdup(d);
}