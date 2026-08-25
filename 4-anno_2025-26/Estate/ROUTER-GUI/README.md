# Simulatore Grafico di Router

Applicazione web che simula un router IP e la sua Tabella di Instradamento (TDI):
visualizzazione della tabella, inserimento ed eliminazione di rotte, salvataggio e
caricamento della configurazione da file, e simulazione dell'instradamento di un
pacchetto con **Longest Prefix Match** spiegato regola per regola.

## Come si usa

Doppio click su **`index.html`**. Non c'è niente da installare: nessun `npm install`,
nessuna compilazione, nessuna connessione a internet. Solo HTML, CSS e JavaScript.

Doppio click su **`test.html`** per far girare i test.

## Cosa fa

All'avvio carica una tabella d'esempio costruita sulla TDI dell'host A di pag. 129, più
due righe che quel programma in C non poteva esprimere: la stessa destinazione
raggiungibile per due strade diverse, dove a decidere è la metrica.

Scrivendo un indirizzo di destinazione e premendo **Instrada**, il programma:

- valuta **tutte** le regole della tabella e mostra per ciascuna il calcolo
  `indirizzo & netmask` confrontato con la rete — lo stesso conto che il programma in C
  stampava con `printf`;
- evidenzia in verde la rotta scelta, in giallo le alternative compatibili, in grigio le
  regole che non corrispondono;
- ordina le alternative per preferenza, così si vede quale sarebbe il percorso di riserva
  se il principale cadesse;
- scrive per esteso **perché** ha scelto quella rotta: quanti bit di prefisso, e se a
  parità di prefisso ha deciso la metrica.

## Com'è organizzato

Tre strati, con confini che si possono verificare cercando nel codice.

| Strato | File | Regola |
|---|---|---|
| **Logica** | `js/ip.js` `js/rotta.js` `js/tdi.js` `js/iface.js` `js/pacchetto.js` `js/router.js` | Nessun riferimento al DOM. Gira anche senza browser. |
| **Persistenza** | `js/persistenza.js` | Traduce fra oggetti del dominio e JSON. |
| **Vista** | `js/vista-tdi.js` `js/vista-sim.js` `js/app.js` | Nessuna aritmetica sugli indirizzi. Disegna e basta. |

Le classi: `Ip` (conversioni), `Rotta` (una riga di TDI), `Tdi` (la tabella e l'algoritmo
di scelta), `Iface`, `Pacchetto`, `Router`, `Persistenza`, più le viste.

Il punto architetturale centrale è che **`Tdi.cerca()` restituisce anche la spiegazione**,
non solo la rotta vincente: la motivazione nasce nella logica, la vista si limita a
impaginarla.

## Documentazione

- [`docs/superpowers/specs/2026-08-15-router-gui-design.md`](docs/superpowers/specs/2026-08-15-router-gui-design.md)
  — documento di design: diagramma UML delle classi, motivazione delle strutture dati
  (perché interi a 32 bit e non ottetti separati, perché un array e non un trie),
  evoluzione verso il multi-router, e l'analisi dei limiti dell'esempio di pag. 129.
- [`docs/superpowers/plans/2026-08-15-router-gui.md`](docs/superpowers/plans/2026-08-15-router-gui.md)
  — piano di implementazione.

## Formato del file di configurazione

```json
{
  "versione": 1,
  "router": {
    "nome": "R1",
    "ifaces": [ { "nome": "eth0", "ip": "196.13.1.1", "msk": "255.255.255.0", "su": true } ],
    "tdi": [
      { "rete": "196.13.2.0", "msk": "255.255.255.0", "gw": "196.13.1.2", "iface": "eth0", "metr": 5 }
    ]
  }
}
```

Gli indirizzi sono in notazione dotted perché il file resti leggibile e modificabile a mano.
Si serializza il router intero, non la sola tabella: così il futuro formato multi-router
sarà un superset di questo e i file salvati oggi continueranno a caricarsi.
