# Subnet Tool

Calcolatore IPv4 e routing di livello 3 in un unico file HTML. Funziona offline: nessuna libreria esterna, nessuna richiesta di rete. Font monospace e logo sono incorporati nel file. Si apre con un doppio clic su `subnet-tool.html`.

L'aspetto segue il design system della piattaforma Moodle: navbar, box info a sinistra ("Strumento N"), formulation azzurra per quello che scrivi, box pesca (outcome) per le risposte, tabelle riepilogo con le etichette in grigio, blocco "Navigazione" a destra con i pulsanti a semaforo, link freccia tra gli strumenti e pulsante primario arancione. Il semaforo dice lo stato di ogni strumento: verde pronto, rosso se un campo non è valido, giallo con un avviso, grigio per la teoria. I campi mostrano ✓ o ✗ come i form-control validati. Tema chiaro predefinito, scuro opzionale.

## Gli 8 strumenti

| Tasto | Strumento | A cosa serve |
|---|---|---|
| 1 | Indirizzi | Nome della subnet, broadcast, range, AND bit a bit passo per passo, netId/subnetId/hostId, hex e decimale, indirizzi speciali RFC 1009 con uso (sorgente/destinazione) e classificatore di indirizzi |
| 2 | Subnet | Dai requisiti (sottoreti, host) ai bit di subnetId e hostId e alla mask; elenco di tutte le subnet con subnetId in binario |
| 3 | Classe | Classe e leading bit, netmask classful, netId, reti e host della classe, confronto tra due IP; riconosce le netmask (255.255.255.0 → classe C) |
| 4 | VLSM | Allocazione dalla subnet più grande, dimezzamenti successivi come nel libro, spazio libero in blocchi CIDR, esempi del libro |
| 5 | CIDR | Analisi di un blocco (reti di classe C aggregate, metà, quarti, ottavi) e aggregazione di reti (supernetting) |
| 6 | Routing | Consegna diretta o indiretta, TdI dell'host in stile `route print`, regola vincente in una TdI (preset router R3 del libro), comandi `route` per Windows e Linux |
| 7 | Maschere | Convertitore da /n, dotted, binario, esadecimale e decimale; tabella delle mask, ottetti, potenze di 2 |
| 8 | Teoria | Sigle, termini, RFC, enti, classi, indirizzi speciali, algoritmi, CNLS e CONS, TdI e comandi, esempi e refusi del libro |

## Uso rapido

- **Teoria**: scrivi e premi `Invio` per copiare la risposta. Dalla sigla o dal termine copia il significato o la definizione, da parole della definizione copia la sigla o il termine. `↑` `↓` scelgono un altro risultato, `Maiusc`+`Invio` copia l'altro campo, `Esc` svuota. Nella teoria basta iniziare a scrivere.
- **Clic su un valore** (IP, mask, numeri, binario) per copiarlo. I numeri si copiano senza separatori: nel quiz `4.094` verrebbe letto come 4,094.
- **Incolla la domanda** nel primo campo di Indirizzi, Classe, Subnet, CIDR o Routing, o nel classificatore: IP, mask, gateway e destinazione vengono estratti da soli.
- **Classificatore**: le righe scritte come `a.b.c.d/n` vengono classificate nella propria subnet, quelle senza prefisso rispetto alla subnet in alto.
- `1`–`8` cambiano strumento e mettono il cursore nel primo campo, `Esc` esce dal campo, `/` apre la teoria, `T` cambia tema.

## Convenzioni

Come nel libro: host per subnet = 2^h − 2 e subnet zero e all-ones utilizzabili. Le varianti (riservare il gateway, escludere subnet zero e all-ones) sono caselle da spuntare, spente di default.
