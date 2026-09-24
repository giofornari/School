# Subnet Tool

Calcolatore IPv4 e routing di livello 3 in un unico file HTML. Funziona offline: font incorporati, nessuna libreria esterna, nessuna richiesta di rete. Si apre con un doppio clic su `subnet-tool.html`.

## Le 8 porte

| Tasto | Porta | A cosa serve |
|---|---|---|
| 1 | Indirizzi | Nome della subnet, broadcast, range, AND bit a bit passo per passo, netId/subnetId/hostId, hex e decimale, indirizzi speciali RFC 1009 con uso (sorgente/destinazione) e classificatore di indirizzi |
| 2 | Subnet | Dai requisiti (sottoreti, host) ai bit di subnetId e hostId e alla mask; elenco di tutte le subnet con subnetId in binario |
| 3 | Classe | Classe e leading bit, netmask classful, netId, reti e host della classe, confronto tra due IP; riconosce le netmask (255.255.255.0 → classe C) |
| 4 | VLSM | Allocazione dalla subnet più grande, dimezzamenti successivi come nel libro, spazio libero in blocchi CIDR, esempi del libro |
| 5 | CIDR | Analisi di un blocco (reti di classe C aggregate, metà, quarti, ottavi) e aggregazione di reti (supernetting) |
| 6 | Routing | Consegna diretta o indiretta, TdI dell'host in stile `route print`, regola vincente in una TdI (preset router R3 del libro), comandi `route` per Windows e Linux |
| 7 | Maschere | Convertitore da /n, dotted, binario, esadecimale e decimale; tabella delle mask, ottetti, potenze di 2 |
| 8 | Teoria | Sigle, RFC, enti, classi, algoritmi di instradamento, CNLS e CONS, TdI e comandi, esempi e refusi del libro, con ricerca |

Scorciatoie: `1`–`8` cambiano porta, `/` apre la ricerca nella teoria, `T` cambia tema.

## Convenzioni

Come nel libro: host per subnet = 2^h − 2 e subnet zero e all-ones utilizzabili. Le varianti (riservare il gateway, escludere subnet zero e all-ones) sono caselle da spuntare, spente di default.
