# Relazione tecnica: simulatore di router IPv4

## Obiettivo

Il programma simula un router IPv4 e la sua Tabella di Instradamento (TDI). Dalla pagina si può vedere la TDI completa, inserire ed eliminare route, salvare e caricare la configurazione da file e simulare l'instradamento di un indirizzo IP di destinazione. Durante la simulazione il programma trova tutte le route compatibili, sceglie con il Longest Prefix Match, colora la route scelta e le alternative di fallback e scrive il motivo della scelta.

L'ho scritto in JavaScript e gira nel browser, quindi non serve installare niente per usarlo: la versione pubblicata su GitHub Pages si apre con un link. Per la grafica uso Tailwind CSS (classi di stile scritte direttamente nell'HTML) e Alpine.js, una libreria piccola che collega i campi della pagina agli oggetti JavaScript e aggiorna la tabella quando cambiano.

Il diagramma delle classi è in [UML.md](UML.md).

## Architettura a tre livelli

Il codice è diviso in tre cartelle, una per ogni parte che la consegna chiede di separare.

`src/core` contiene il modello e la logica di instradamento: `ip.js` per le conversioni degli indirizzi e le classi `Route`, `Interface`, `TDI` e `Router`. Qui nessun file usa il DOM, Alpine, `localStorage` o `fetch`, quindi il core funziona uguale anche fuori dal browser, per esempio lanciato con Node.

`src/persistence` si occupa di salvare e caricare. `config.js` converte il JSON in un `Router` e viceversa, senza fare input/output. `storage.js` invece usa le funzioni del browser: scarica il file, legge quello scelto dall'utente, scrive nel `localStorage` e carica l'esempio.

`src/ui`, `src/main.js` e `index.html` sono l'interfaccia grafica. Il componente Alpine `simulator` legge i campi dei form, chiama i metodi del core e mostra il risultato. La UI non ricalcola mai quali route sono compatibili: prende tutto dal risultato di `router.lookup(ip)`. `format.js` trasforma quel risultato nei colori e nei badge di ogni riga della tabella.

Le dipendenze vanno in un solo verso: la UI usa persistenza e core, la persistenza usa il core, il core non usa nessuno dei due. Così se un giorno si cambiasse la grafica, o si aggiungessero altri router (vedi l'ultimo capitolo), la logica di instradamento resterebbe la stessa.

Ogni classe ha un compito preciso:

- `Route` conosce la propria rete e mask, calcola il prefisso e sa dire se un IP è compatibile (`matches`).
- `TDI` tiene le route nell'ordine di inserimento e rifiuta i duplicati. Non conosce le interfacce.
- `Interface` è una porta del router, con nome, IP, mask e stato up/down.
- `Router` tiene insieme interfacce e TDI, controlla che ogni route usi un'interfaccia esistente e sceglie la route con `lookup`.

I controlli sui dati stanno nei costruttori delle classi. In questo modo non può esistere una `Route` con una mask sbagliata, e i dati scritti nel form e quelli letti dal file JSON passano dagli stessi controlli.

## Strutture dati

### Indirizzi IP

Nel modello gli indirizzi restano stringhe puntate (`"192.168.1.0"`), cioè come li scrive l'utente e come finiscono nel file JSON. Diventano numeri solo quando serve fare un calcolo: `parseIp` legge i quattro ottetti e costruisce un intero a 32 bit moltiplicando per 256, senza usare operatori bitwise.

In JavaScript gli operatori bitwise lavorano su interi a 32 bit con segno, quindi `ip & mask` con il primo bit a 1 dà un numero negativo. Per confrontarlo con la rete bisogna riportarlo senza segno con `>>> 0`. Un'altra trappola è la mask `/0`: `0xFFFFFFFF << 32` non vale 0 perchè JavaScript usa solo i 5 bit bassi del numero di shift, quindi lo shift di 32 diventa uno shift di 0. Per questo `maskToPrefix` tratta `/0` a parte.

Il prefisso si ricava dalla mask provando i valori da 0 a 32. Se nessuno corrisponde, la mask ha dei buchi (per esempio `255.0.255.0`) e viene rifiutata.

### La TDI è un array

La TDI è un array di `Route` in ordine di inserimento, e `lookup` lo scorre tutto dall'inizio alla fine.

La simulazione deve comunque passare da tutte le route, anche con una struttura più veloce: la tabella mostra per ogni riga il calcolo `IP AND mask = rete` e l'esito ✓/✗, e per la lista dei fallback servono tutte le route compatibili.

Poi c'è l'ordine. Quando due route hanno lo stesso prefisso e la stessa metrica vince quella inserita prima, e con un array l'ordine di inserimento c'è già. Il `sort` di JavaScript è stabile, cioè a parità lascia gli elementi nell'ordine in cui erano, quindi lo spareggio non richiede codice in più. È anche l'ordine delle righe che l'utente vede nella pagina.

Infine, in un esercizio la TDI ha qualche decina di route al massimo, e una scansione lineare su 30 elementi è istantanea.

### Perché niente trie

I router veri usano un trie (un albero binario in cui ogni livello è un bit dell'indirizzo) o memorie hardware apposite, perché hanno centinaia di migliaia di route e devono trovare il prefisso più lungo senza guardarle tutte. Qui un trie non servirebbe: per mostrare il calcolo di ogni riga e la lista dei fallback il programma dovrebbe visitare lo stesso tutte le route. Renderebbe anche più complicati l'eliminazione, lo spareggio con metrica e ordine di inserimento e le route scartate per interfaccia down, e sarebbe molto più difficile da spiegare riga per riga. Se in futuro le tabelle diventassero grandi, un indice si potrebbe aggiungere cambiando solo `TDI` e `lookup`.

### Interfacce e riferimenti per nome

Anche le interfacce stanno in un array dentro il `Router`, e `findInterface` le cerca per nome: sono poche, quindi va bene una ricerca lineare. La `Route` non contiene l'oggetto `Interface` ma il suo nome (`iface`). Il JSON resta semplice e l'interfaccia esiste in un solo punto, così cambiando il suo stato up/down tutte le route che la usano lo vedono subito. Per evitare route orfane il router controlla che l'interfaccia esista quando si aggiunge una route e non permette di eliminare un interfaccia usata da qualche route.

### Duplicati

Due route sono duplicate quando hanno uguali rete, mask, next hop e interfaccia. La metrica non conta: una route che cambia solo la metrica è lo stesso percorso, e se fosse accettata comparirebbe come fallback anche se cade insieme all'originale quando l'interfaccia va down. La stessa rete con un next hop diverso invece è permessa, perché è proprio il caso del fallback: due strade diverse per la stessa destinazione.

## Instradamento: Longest Prefix Match, metrica e guasti

`router.lookup(ip)` fa questi passi:

1. controlla che l'IP sia valido;
2. per ogni route, nell'ordine della TDI, calcola `rete = ip AND mask`; la route è compatibile se `rete` è uguale alla sua rete. Ogni controllo viene salvato in `controlli`, che la pagina mostra nelle colonne del calcolo e dell'esito;
3. divide le compatibili in usabili (interfaccia up) e scartate (interfaccia down);
4. ordina le usabili per prefisso più lungo e, a parità, per metrica più bassa; se anche la metrica è uguale resta l'ordine della TDI;
5. la prima usabile è la scelta, le altre sono i fallback in ordine di preferenza, e la funzione `explain` scrive il motivo.

Il prefisso viene sempre prima della metrica, come nei router veri: una route più specifica descrive meglio dove si trova la destinazione, e la metrica serve solo a confrontare route verso la stessa rete. Le route con interfaccia down restano nella tabella, barrate, così si capisce perché la scelta è cambiata. Appena l'interfaccia torna up la simulazione attiva viene ricalcolata e tornano usabili.

Il motivo distingue i casi possibili: nessuna route compatibile, compatibili tutte scartate, una sola route usabile, scelta decisa dal prefisso, dalla metrica o dall'ordine di inserimento. In fondo elenca le route scartate.

### Esempio

Il file `esempi/router-esempio.json` configura il router R1 con tre interfacce:

| interfaccia | IP | mask |
| --- | --- | --- |
| eth0 | 192.168.1.1 | 255.255.255.0 |
| eth1 | 10.0.0.1 | 255.255.255.252 |
| eth2 | 10.0.1.1 | 255.255.255.252 |

e questa TDI:

| # | rete | mask | next hop | interfaccia | metrica |
| --- | --- | --- | --- | --- | --- |
| 1 | 192.168.1.0 | /24 | diretta | eth0 | 0 |
| 2 | 10.0.0.0 | /30 | diretta | eth1 | 0 |
| 3 | 10.0.1.0 | /30 | diretta | eth2 | 0 |
| 4 | 172.16.0.0 | /16 | 10.0.1.2 | eth2 | 20 |
| 5 | 172.16.0.0 | /16 | 10.0.0.2 | eth1 | 10 |
| 6 | 172.16.5.0 | /24 | 10.0.1.2 | eth2 | 0 |
| 7 | 0.0.0.0 | /0 | 10.0.0.2 | eth1 | 1 |
| 8 | 0.0.0.0 | /0 | 10.0.1.2 | eth2 | 5 |

Con destinazione `172.16.9.9` le route compatibili sono la 4, la 5 e le due default. La 6 no, perché `172.16.9.9 AND 255.255.255.0` dà `172.16.9.0`. La 4 e la 5 hanno lo stesso prefisso /16 e decide la metrica, quindi vince la 5; la 4 è il fallback 1, la 7 e la 8 sono il fallback 2 e 3. Il motivo mostrato è:

> scelta 172.16.0.0/16 via 10.0.0.2 su eth1: 2 route usabili hanno il prefisso più lungo (/16), decide la metrica più bassa (10).

Con destinazione `172.16.5.5` è compatibile anche la 6, che vince perché ha il prefisso più lungo (/24 contro /16 e /0):

> scelta 172.16.5.0/24 via 10.0.1.2 su eth2: ha il prefisso più lungo (/24) tra 5 route usabili.

Mettendo down eth1 e ripetendo `172.16.9.9`, la 5 e la 7 diventano scartate e il fallback prende il loro posto:

> scelta 172.16.0.0/16 via 10.0.1.2 su eth2: ha il prefisso più lungo (/16) tra 2 route usabili. route scartate per interfaccia down: 172.16.0.0/16 via 10.0.0.2 su eth1, 0.0.0.0/0 via 10.0.0.2 su eth1.

Se vanno down sia eth1 che eth2, per `8.8.8.8` restano solo route scartate e il pacchetto non può essere inoltrato:

> nessuna route usabile per 8.8.8.8: il pachetto non può essere inoltrato. route scartate per interfaccia down: 0.0.0.0/0 via 10.0.0.2 su eth1, 0.0.0.0/0 via 10.0.1.2 su eth2.

### Controllo degli input

Gli errori sono oggetti `Error` con il messaggio in italiano, e la pagina li scrive sotto il form che li ha causati, senza finestre `alert`. I controlli sono:

- IP con quattro numeri da 0 a 255 e senza zeri iniziali (`010` potrebbe sembrare un numero in ottale);
- mask contigua, altrimenti `netmask non contigua: 255.0.255.0`;
- bit di host a zero nella rete: con `192.168.1.5` e mask `255.255.255.0` l'errore è `bit di host non a zero: forse intendevi 192.168.1.0?`;
- metrica intera maggiore o uguale a 0;
- interfaccia della route esistente, nomi delle interfacce senza doppioni, nessuna route duplicata.

## Persistenza

La configurazione si salva in JSON, che JavaScript legge e scrive senza librerie e che ha la stessa forma delle classi: un router con la lista delle interfacce e la lista delle route. Il formato è descritto nel [README](../README.md).

`toJson` copia i campi uno per uno, così nel file non finiscono dati calcolati come il prefisso. `fromJson` costruisce un router nuovo e aggiunge prima le interfacce e poi le route, perché le route cercano l'interfaccia per nome. Il caricamento è atomico: se una voce è sbagliata `fromJson` si ferma con un errore che dice la posizione (`route 1: netmask non contigua: 255.0.255.0`) e il router mostrato nella pagina resta quello di prima, perché viene sostituito solo alla fine.

"salva su file" scarica `router-config.json`, "carica da file" apre la scelta di un file. In più ogni modifica viene salvata nel `localStorage` del browser, quindi ricaricando la pagina non si perde niente. All'avvio il programma usa la configurazione del `localStorage`; se non c'è carica l'esempio, e se quella salvata è rovinata carica l'esempio e lo scrive in un avviso in cima alla pagina. Se anche l'esempio non si riesce a caricare si parte da un router vuoto, così si può almeno aprire un file. Tutti i percorsi sono relativi, perché su GitHub Pages il sito sta sotto `/ROUTER-GUI/` e un percorso che comincia con `/` punterebbe al posto sbagliato.

## Interfaccia grafica

La pagina è una sola. In alto ci sono il campo per l'IP da simulare e i pulsanti per salvare, caricare e ripristinare l'esempio. Sotto c'è il pannello delle interfacce, con l'interruttore up/down e il form per aggiungerne una, e poi la TDI con le colonne rete, netmask, prefisso, next hop ("diretta" se manca), interfaccia, metrica, calcolo `IP AND mask = rete`, esito ✓/✗ e il pulsante per eliminare la riga. Dopo una simulazione la route scelta è verde, i fallback sono color ambra con un badge numerato, le scartate sono barrate con il badge "interfaccia down" e le non compatibili sono grigie. Sotto la tabella c'è il pannello con il motivo e il form per aggiungere una route.

Quando c'è una simulazione attiva, qualunque modifica a TDI o interfacce la rifà subito. Così mettendo down un'interfaccia si vede il fallback prendere il posto della route scelta senza dover premere di nuovo "simula".

Alpine ha un solo componente. Negli attributi dell'HTML ci sono solo espressioni corte, come `@click="toggle(iface)"`, e tutta la logica sta nei metodi JavaScript.

## Limiti e semplificazioni

- Il next hop non viene confrontato con le reti delle interfacce. Per esempio una route con next hop `8.8.8.8` su eth0 viene accettata, mentre un router vero la considererebbe irraggiungibile perché `8.8.8.8` non sta nella rete di eth0. Allo stesso modo una route diretta non viene confrontata con la rete della sua interfaccia. L'ho lasciato fuori per tenere semplici il form e i messaggi di errore; con più router collegati diventerebbe necessario.
- Le route verso le reti direttamente connesse vanno inserite a mano: il router non le crea dalle interfacce. Non viene controllato neanche se due interfacce hanno reti sovrapposte.
- Ci sono solo route statiche. Non c'è la distanza amministrativa e non ci sono protocolli di routing: la metrica la decide chi scrive la route.
- Una route non si può modificare: va eliminata e inserita di nuovo.
- Il `localStorage` vale solo per quel browser; per spostare una configurazione bisogna salvare il file.
- La scansione lineare va bene per qualche decina di route, non per le tabelle di un router su Internet.
- Si simula un router solo, senza pacchetti, TTL o ARP.

## Limiti degli esempi di riferimento

Prima di cominciare ho letto tre progetti di esempio sullo stesso tema, per capire cosa mancava e cosa si poteva fare meglio. Non ho riusato il loro codice.

### Esempio 1 (JavaScript)

Ha le classi `Router`, `TDI`, `Route` e `Interface`, un controller che collega i form alla logica e una parte che disegna la tabella. I limiti più grossi riguardano proprio quello che chiede la consegna:

- la `Route` ha solo destinazione, mask e next hop. Mancano l'interfaccia di uscita e la metrica, e le interfacce non hanno uno stato up/down, quindi un guasto non si può simulare. Il next hop è obbligatorio, per cui non si può scrivere una rete direttamente connessa.
- quando si inserisce una route, il controllo dei duplicati confronta solo l'indirizzo di rete e rifiuta la nuova route con "Subnet già esistente!". Così non si può mettere una seconda strada verso la stessa rete, che è il caso del fallback, e viene rifiutata anche `10.0.0.0/16` se c'è già `10.0.0.0/8`.
- a parità di prefisso vince la prima route trovata, ma non è una regola dichiarata e non c'è la metrica per decidere.
- la simulazione scrive in un paragrafo a parte l'elenco delle route compatibili e quella scelta. Le righe della tabella non vengono evidenziate e non c'è il motivo della scelta.
- gli IP sono controllati solo come quattro numeri da 0 a 255: una mask non contigua o una rete con bit di host a 1 vengono accettate.
- gli errori escono con `alert()`, e il controller legge e scrive il DOM direttamente insieme alla logica.
- l'importazione svuota la pagina prima ancora di leggere il file e non controlla i campi, quindi un file sbagliato lascia la pagina vuota.

### Esempio 2 (documento di progetto, PHP e MySQL)

Non contiene codice ma la descrizione di un'applicazione web con router, interfacce e route salvati in un database MySQL, e JSON solo per importare ed esportare. La divisione in tre livelli è spiegata bene, ed è l'unico esempio che prevede più router e l'inoltro hop per hop. Però:

- nella tabella delle route non c'è l'interfaccia (`routes(id, router_id, network, mask, next_hop, metric)`), anche se il documento dice che le route con interfaccia down vengono escluse. Non spiega come si ricava l'interfaccia dal next hop.
- per la simulazione su più router c'è una classe `Path` con i salti fatti, ma nessuna tabella dei collegamenti tra router, quindi non si capisce come si passa dal next hop al router successivo.
- la scelta usa prefisso e metrica, ma non dice cosa succede se anche la metrica è uguale o se nessuna route è compatibile.
- non parla di evidenziare i fallback, di mostrare il motivo, di controlli sugli input o di duplicati.
- la parte sulle strutture dati (un array filtrato in modo lineare) si interrompe a metà frase, quindi la scelta non è motivata.

### Esempio 3 (Java con JavaFX)

La separazione tra grafica (`RouterSimulatorController` e il file FXML), modello (`Router`, `Tabella`, `Route`, `Interfaccia`) e salvataggio su file (`TDIStorage`) è abbastanza pulita, e dopo la simulazione la tabella si colora: verde la prima route compatibile, giallo le altre. I limiti:

- non c'è nessun testo che spieghi la scelta.
- la route scelta è semplicemente la prima della lista, che `Tabella` riordina per prefisso con un bubble sort a ogni inserimento. Non c'è la metrica. A parità di prefisso resta prima la route inserita prima, ma solo perché il bubble sort non scambia due elementi uguali: la regola non è scritta da nessuna parte.
- le interfacce non hanno lo stato up/down, quindi le route gialle sono solo altre compatibili e non si vede cosa succede con un guasto.
- come nell'esempio 1 il next hop è obbligatorio e non esistono route dirette.
- i controlli sono parziali: gli ottetti delle route non vengono controllati, le mask non contigue passano e i bit di host non sono controllati. Se l'IP da simulare è scritto male, l'eccezione non viene gestita e l'utente non vede nessun messaggio.
- nel caricamento del file le righe non riconosciute vengono ignorate senza dire niente, gli errori di formato non vengono gestiti e due interfacce con lo stesso nome non danno errore. La TDI non rifiuta le route duplicate.
- tutti i messaggi all'utente passano da finestre modali.

### Cosa ho fatto diversamente

Nel mio progetto ogni route ha interfaccia di uscita e metrica e le interfacce hanno lo stato up/down, così la simulazione può mostrare route scartate e fallback. Il controllo dei duplicati tiene conto del next hop, per permettere più strade verso la stessa rete. Lo spareggio è dichiarato (prefisso, metrica, ordine di inserimento) e il motivo lo spiega ogni volta. I controlli sugli input stanno nei costruttori e valgono sia per il form che per il file, il caricamento è atomico con la posizione dell'errore e i messaggi compaiono nella pagina vicino al form, senza finestre.

## Evoluzione verso più router

Per simulare una rete con più router collegati servirebbero tre classi nuove, già disegnate come `<<futura>>` nel diagramma UML.

`Link` collega due interfacce di router diversi e può essere up o down. `Packet` ha IP sorgente, IP destinazione, TTL e la lista dei router attraversati. `Rete` contiene router e link e fa viaggiare i pacchetti.

A `Router` si aggiungerebbe un metodo `forward(packet)` che usa il `lookup` già esistente:

1. toglie 1 al TTL e, se arriva a 0, scarta il pacchetto;
2. chiama `lookup(packet.destination)`; se non c'è una scelta scarta il pacchetto e il motivo spiega perché;
3. se la route scelta è diretta, la destinazione sta in una rete collegata e il pacchetto è arrivato;
4. altrimenti il pacchetto esce dall'interfaccia della route: `Rete` cerca il link attaccato a quell'interfaccia, prende l'interfaccia all'altro capo e passa il pacchetto al router a cui appartiene.

`Rete` ripete questi passi finché il pacchetto arriva o viene scartato, e la pagina potrebbe mostrare il percorso hop per hop con il motivo di ogni scelta.

L'architettura attuale regge questo cambiamento senza modifiche sostanziali. `lookup` non cambia niente nel router e restituisce già la scelta, i fallback e il motivo, quindi `forward` lo può usare così com'è. `Interface` esiste già con lo stato up/down, e un link down può semplicemente rendere down le due interfacce che collega. `Route` e `TDI` restano uguali e il core non dipende dalla pagina, quindi le classi nuove si aggiungono nel core. La persistenza andrebbe estesa per salvare più router e i link, ma ogni router si salverebbe con il formato di adesso. L'unica regola da aggiungere è il controllo che il next hop stia nella rete dell'interfaccia di uscita, descritto nei limiti, perché con più router serve per trovare il router vicino giusto.
