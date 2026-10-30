# Documentazione — WAN routing statico

## 1. Rete

Ho realizzato una rete WAN con 5 router (R1-R5) collegati in una topologia a maglia parziale, con 6 sottoreti di accesso (A-F) raggiunte tramite modem DSL e 4 reti di transito tra router. Ho indirizzato l'intera rete con blocchi /24 in 160.80.0.0/16 e ho implementato il routing esclusivamente in modo statico, senza protocolli dinamici.

## 2. Indirizzamento

Ho assegnato un indirizzo di rete proprio anche ai collegamenti punto-punto tra router, perché due router adiacenti devono condividere una rete IP per scambiarsi pacchetti a livello 3, anche se quel collegamento non ospita host. All'interno di ogni sottorete ho attribuito .1 al router con indice più basso, .2 all'eventuale secondo router e ho numerato gli host a partire da .10, una convenzione che ho adottato solo per rendere la documentazione più leggibile.

## 3. Criticità Cloud-PT e soluzione adottata

Durante la progettazione ho scoperto che il Cloud-PT di Packet Tracer non si comporta come uno switch o un hub, perché inoltra il traffico solo sulle coppie di porte che ho mappato esplicitamente nella configurazione, tipicamente Modem con Ethernet, e non esiste alcuna mappatura nativa tra due porte Ethernet. Questo vincolo non crea problemi nelle sottoreti A, B, C e D, dove ogni nuvola collega un solo router, ma diventa determinante nelle sottoreti E ed F, che nella topologia richiesta collegano due router ciascuna, rispettivamente R4-R5 e R2-R5, per cui il traffico tra i due router attraverso la nuvola verrebbe scartato. Ho risolto il problema inserendo uno switch di livello 2 in ciascuna delle due sottoreti, SW45 per la rete E e SW25 per la rete F, collegando ad esso entrambi i router e la porta Ethernet della nuvola, in modo che il Cloud-PT rappresenti il DSLAM di accesso mentre lo switch realizzi il dominio di broadcast della sottorete, esattamente come avviene in una rete di accesso reale. Questa soluzione non ha richiesto alcuna modifica al piano di indirizzamento né alle tabelle di routing, e ho verificato la sua correttezza facendo pingare tra loro due host della stessa sottorete posizionati dietro router diversi.

## 4. Metodo di costruzione delle tabelle di routing

Per costruire la tabella di ciascun router ho verificato per ogni rete di destinazione se fosse direttamente connessa, nel qual caso ho inserito una rotta diretta senza next hop e con metrica zero, oppure se richiedesse l'attraversamento di altri router, nel qual caso ho scelto il percorso con il minor numero di hop, applicando lo stesso criterio dei protocolli distance-vector come RIP, e ho impostato come next hop l'indirizzo dell'interfaccia del router adiacente sulla rete condivisa, non l'indirizzo della rete di destinazione finale. Dove ho trovato percorsi equivalenti per numero di hop ho scelto una rotta primaria e ho documentato le alternative, inserendone alcune come rotte ridondanti. Il risultato finale sono 34 rotte statiche distribuite sui 5 router, che sommate alle rotte dirette permettono a ciascun router di conoscere tutte le 10 reti della topologia.

## 5. Limiti del routing statico

Sono consapevole dei limiti della scelta progettuale adottata. Non essendoci alcun adattamento automatico ai guasti, se un collegamento cade il traffico verso le reti raggiungibili solo tramite quel collegamento viene perso, a meno di predisporre rotte di riserva che però reagiscono solo alla caduta dell'interfaccia locale. Il numero di righe di configurazione cresce inoltre in proporzione al prodotto tra router e reti, per cui su una rete più grande la configurazione manuale diventerebbe rapidamente impraticabile. Non ho inserito una rotta di default perché tutte le dieci reti sono note ed enumerate in tabella, e l'avrei introdotta solo in presenza di un'uscita verso una rete esterna non enumerabile. Per superare questi limiti su reti più complesse ricorrerei a un protocollo di routing dinamico come RIP o OSPF.

## 6. Verifica

Ho verificato la rete procedendo dal basso verso l'alto, controllando prima lo stato dei collegamenti fisici, poi la raggiungibilità del gateway da ogni host per validare la mappatura DSL e la configurazione IP, poi la connettività tra le interfacce di router adiacenti, poi il contenuto della tabella di routing di ciascun router con show ip route per accertarmi che comparissero tutte le dieci reti, e infine la connettività end-to-end tra host di sottoreti diverse, confrontando il percorso restituito da tracert con quello previsto dalle mie tabelle.

## 7. Tabelle di instradamento (TdI)

Maschera 255.255.255.0 su tutte le righe. Le righe indicate come alternative sono percorsi equivalenti per numero di hop, non inseriti nella configurazione CLI ma documentati come ridondanza possibile.

### TdI — R1 (connesso a A, 7, 8, 10)

| Rete destinazione | Tipo | Next hop | Interfaccia uscita | Metrica |
|---|---|---|---|---|
| 160.80.1.0 (A) | diretta | - | 160.80.1.1 | 0 |
| 160.80.2.0 (D) | indiretta | 160.80.8.2 | 160.80.8.1 | 2 |
| 160.80.2.0 (D) | indiretta (alt) | 160.80.7.2 | 160.80.7.1 | 2 |
| 160.80.3.0 (B) | indiretta | 160.80.7.2 | 160.80.7.1 | 1 |
| 160.80.4.0 (E) | indiretta | 160.80.8.2 | 160.80.8.1 | 1 |
| 160.80.5.0 (C) | indiretta | 160.80.10.2 | 160.80.10.1 | 1 |
| 160.80.6.0 (F) | indiretta | 160.80.7.2 | 160.80.7.1 | 1 |
| 160.80.7.0 | diretta | - | 160.80.7.1 | 0 |
| 160.80.8.0 | diretta | - | 160.80.8.1 | 0 |
| 160.80.9.0 | indiretta | 160.80.7.2 | 160.80.7.1 | 1 |
| 160.80.9.0 | indiretta (alt) | 160.80.10.2 | 160.80.10.1 | 1 |
| 160.80.10.0 | diretta | - | 160.80.10.1 | 0 |

### TdI — R2 (connesso a B, F, 7, 9)

| Rete destinazione | Tipo | Next hop | Interfaccia uscita | Metrica |
|---|---|---|---|---|
| 160.80.1.0 (A) | indiretta | 160.80.7.1 | 160.80.7.2 | 1 |
| 160.80.2.0 (D) | indiretta | 160.80.6.2 | 160.80.6.1 | 1 |
| 160.80.3.0 (B) | diretta | - | 160.80.3.1 | 0 |
| 160.80.4.0 (E) | indiretta | 160.80.6.2 | 160.80.6.1 | 1 |
| 160.80.5.0 (C) | indiretta | 160.80.9.2 | 160.80.9.1 | 1 |
| 160.80.6.0 (F) | diretta | - | 160.80.6.1 | 0 |
| 160.80.7.0 | diretta | - | 160.80.7.2 | 0 |
| 160.80.8.0 | indiretta | 160.80.7.1 | 160.80.7.2 | 1 |
| 160.80.9.0 | diretta | - | 160.80.9.1 | 0 |
| 160.80.10.0 | indiretta | 160.80.7.1 | 160.80.7.2 | 1 |
| 160.80.10.0 | indiretta (alt) | 160.80.9.2 | 160.80.9.1 | 1 |

### TdI — R3 (connesso a C, 9, 10)

| Rete destinazione | Tipo | Next hop | Interfaccia uscita | Metrica |
|---|---|---|---|---|
| 160.80.1.0 (A) | indiretta | 160.80.10.1 | 160.80.10.2 | 1 |
| 160.80.2.0 (D) | indiretta | 160.80.9.1 | 160.80.9.2 | 2 |
| 160.80.3.0 (B) | indiretta | 160.80.9.1 | 160.80.9.2 | 1 |
| 160.80.4.0 (E) | indiretta | 160.80.9.1 | 160.80.9.2 | 2 |
| 160.80.4.0 (E) | indiretta (alt) | 160.80.10.1 | 160.80.10.2 | 2 |
| 160.80.5.0 (C) | diretta | - | 160.80.5.1 | 0 |
| 160.80.6.0 (F) | indiretta | 160.80.9.1 | 160.80.9.2 | 1 |
| 160.80.7.0 | indiretta | 160.80.10.1 | 160.80.10.2 | 1 |
| 160.80.7.0 | indiretta (alt) | 160.80.9.1 | 160.80.9.2 | 1 |
| 160.80.8.0 | indiretta | 160.80.10.1 | 160.80.10.2 | 1 |
| 160.80.9.0 | diretta | - | 160.80.9.2 | 0 |
| 160.80.10.0 | diretta | - | 160.80.10.2 | 0 |

### TdI — R4 (connesso a E, 8)

| Rete destinazione | Tipo | Next hop | Interfaccia uscita | Metrica |
|---|---|---|---|---|
| 160.80.1.0 (A) | indiretta | 160.80.8.1 | 160.80.8.2 | 1 |
| 160.80.2.0 (D) | indiretta | 160.80.4.2 | 160.80.4.1 | 1 |
| 160.80.3.0 (B) | indiretta | 160.80.8.1 | 160.80.8.2 | 2 |
| 160.80.3.0 (B) | indiretta (alt) | 160.80.4.2 | 160.80.4.1 | 2 |
| 160.80.4.0 (E) | diretta | - | 160.80.4.1 | 0 |
| 160.80.5.0 (C) | indiretta | 160.80.8.1 | 160.80.8.2 | 2 |
| 160.80.6.0 (F) | indiretta | 160.80.4.2 | 160.80.4.1 | 1 |
| 160.80.7.0 | indiretta | 160.80.8.1 | 160.80.8.2 | 1 |
| 160.80.8.0 | diretta | - | 160.80.8.2 | 0 |
| 160.80.9.0 | indiretta | 160.80.8.1 | 160.80.8.2 | 2 |
| 160.80.10.0 | indiretta | 160.80.8.1 | 160.80.8.2 | 1 |

### TdI — R5 (connesso a D, E, F)

| Rete destinazione | Tipo | Next hop | Interfaccia uscita | Metrica |
|---|---|---|---|---|
| 160.80.1.0 (A) | indiretta | 160.80.6.1 | 160.80.6.2 | 2 |
| 160.80.1.0 (A) | indiretta (alt) | 160.80.4.1 | 160.80.4.2 | 2 |
| 160.80.2.0 (D) | diretta | - | 160.80.2.1 | 0 |
| 160.80.3.0 (B) | indiretta | 160.80.6.1 | 160.80.6.2 | 1 |
| 160.80.4.0 (E) | diretta | - | 160.80.4.2 | 0 |
| 160.80.5.0 (C) | indiretta | 160.80.6.1 | 160.80.6.2 | 2 |
| 160.80.6.0 (F) | diretta | - | 160.80.6.2 | 0 |
| 160.80.7.0 | indiretta | 160.80.6.1 | 160.80.6.2 | 1 |
| 160.80.8.0 | indiretta | 160.80.4.1 | 160.80.4.2 | 1 |
| 160.80.9.0 | indiretta | 160.80.6.1 | 160.80.6.2 | 1 |
| 160.80.10.0 | indiretta | 160.80.6.1 | 160.80.6.2 | 2 |
| 160.80.10.0 | indiretta (alt) | 160.80.4.1 | 160.80.4.2 | 2 |

## 8. Conclusione

Ritengo che la rete realizzata soddisfi pienamente il requisito di raggiungibilità reciproca tra tutte le sottoreti tramite routing esclusivamente statico, e che la scoperta e risoluzione del limite del Cloud-PT dimostri una comprensione della differenza tra il comportamento simulato e quello reale di una rete di accesso.
