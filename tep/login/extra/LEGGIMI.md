# Extra: oltre le slide

**Niente di questa cartella è nel programma (slide 1-54).** Serve per capire, non per la verifica.

| Cosa | Dove | Perché |
| :--- | :--- | :--- |
| Hash delle password con `crypto.scryptSync` + sale | `creaHash`, `passwordGiusta` | Nel codice non resta la password in chiaro |
| Confronto con `crypto.timingSafeEqual` | `passwordGiusta` | Il tempo di risposta non rivela quanti byte sono giusti |
| Sessione: id da `crypto.randomBytes(32)` | `riceviLogin` | Un id corto o progressivo si indovina |
| Cookie `HttpOnly; SameSite=Strict; Path=/` | `riceviLogin`, `/logout` | Lo script della pagina non lo legge, gli altri siti non lo mandano |
| Redirect 303 dopo il POST | `riceviLogin` | Ricaricare la pagina non rimanda il form |
| Pagina protetta `/area` e `/logout` | `requestHandler` | Senza cookie valido: 401 |

Avvio: `node extra/server-extra.js`, poi http://127.0.0.1:3001 (stessi utenti: mario / Rossi2026).

**Conviene rischiarlo in verifica?** No. Le sessioni con cookie sono 40 righe in più fuori programma, e ognuna è un punto dove sbagliare; il prof valuta quello che ha spiegato. Al massimo, finito tutto e ricontrollato, scrivi in un commento: "in produzione le password vanno salvate come hash (crypto.scrypt), non in chiaro". Ti dà il punto di consapevolezza senza il rischio.
