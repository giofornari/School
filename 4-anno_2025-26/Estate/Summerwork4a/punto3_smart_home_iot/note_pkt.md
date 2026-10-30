# Note da inserire nel `.pkt`

17 blocchi di testo da posare sul Logical Workspace, ognuno accanto a ciò che
racconta. Testo già impaginato: copia e incolla, non riscrivere.

Le note sono scritte **in prima persona** e **raccontano le scelte fatte**: non
danno istruzioni e non spiegano come si configura. Chi apre il `.pkt` legge un
progettista che spiega perché ha deciso così.

**Come si inseriscono:** barra degli strumenti → icona **Note** (`Place Note`) →
clic sul punto della mappa → incolla. Doppio clic per rileggere o correggere.

**Vincoli rispettati:** solo ASCII, righe sotto i 62 caratteri, accenti con
l'apostrofo, frecce `->`. Le note di PT sono testo semplice e rendono male i
simboli tipografici.

---

## Mappa di posa

| # | Nota | Dove |
|---|---|---|
| 1 | Il progetto e i criteri che mi sono dato | Alto a sinistra, sopra tutto |
| 2 | La catena di accesso | Sopra `CLOUD-ISP` e `MODEM-DSL` |
| 3 | L'indirizzo pubblico statico | Vicino al link `203.0.113.0/30` |
| 4 | Router-on-a-stick | Sotto `R-HOME` |
| 5 | NAT e cosa ho esposto | A destra di `R-HOME` |
| 6 | Le ACL e `established` | Sotto la nota 5 |
| 7 | Come ho segmentato | Sopra `SW-HOME` |
| 8 | La native VLAN | A fianco della nota 7 |
| 9 | La VLAN IoT | Nella fascia dei dispositivi IoT |
| 10 | La VLAN dei server | Vicino ai cinque server |
| 11 | Il DHCP | Vicino a `SRV-DHCP` |
| 12 | Il wireless ibrido | Fra `WLC-HOME` e i due AP autonomi |
| 12b | Enterprise e canali | Sotto la nota 12 |
| 13 | Perché il LAP è in VLAN 60 | Accanto a `LAP-MYHOME` |
| 14 | La centralina MCU | In giardino, vicino all'MCU |
| 15 | I limiti | In basso a sinistra |
| 16 | Il collaudo | In basso, accanto alla 15 |

---

## 1 — Il progetto e i criteri

```
PROGETTO CPT - DOMOTICA E IoT
Villa unifamiliare su un piano.
6 VLAN | 3 SSID | 21 dispositivi IoT | accesso da Internet

Prima di posare un apparato mi sono dato cinque criteri, e
tutte le decisioni che ho preso discendono da questi.

1. Cio' che e' critico non deve dipendere da un elemento
   centrale.
2. Un dispositivo IoT compromesso non deve poter fare danni.
3. Verso l'esterno espongo il minimo indispensabile.
4. Ogni scelta dev'essere difendibile, non solo funzionante.
5. I limiti li dichiaro, non li nascondo.

I criteri 1 e 2 sono in tensione fra loro: isolando gli IoT
li ho resi piu' sicuri ma anche piu' dipendenti dal server
locale. Come ho composto i due sta nelle note 9, 12 e 14.
```

## 2 — La catena di accesso

```
LA CATENA DI ACCESSO

Non ho collegato il router di casa direttamente a quello
dell'operatore: in una casa reale in mezzo ci sono la rete
di accesso del provider e il modem installato dal cliente.
Ho costruito la catena completa.

R-ISP -> DSLAM (nuvola) -> modem in bridge -> R-HOME

Nuvola e modem li ho tenuti trasparenti al livello 3: non
hanno indirizzo, non instradano, non decrementano il TTL.
Per il routing sono un cavo lungo che passa dalla centrale.

Per questo R-ISP e R-HOME sono rimasti direttamente
connessi sulla stessa 203.0.113.0/30 anche se fisicamente
stanno a chilometri di distanza. Ed e' lo stesso motivo per
cui il modem di casa non compare mai in un tracert.

Nella nuvola ho mappato Modem0 su Ethernet0: il Cloud-PT
non e' uno switch, inoltra solo sulle coppie di porte che
gli si programmano.
```

## 3 — L'indirizzo pubblico statico

```
PERCHE' HO SCELTO UN IP PUBBLICO STATICO

Il port forwarding pubblica un servizio su un INDIRIZZO.
Con un indirizzo dinamico, dopo una riconnessione da fuori
non saprei piu' dove chiamare.

Le strade erano due: un servizio di DNS dinamico che
aggiorna il record a ogni cambio, oppure una linea con IP
statico. Per un sistema che comanda serrature e telecamere
ho scelto la seconda, che e' anche quella che si
sottoscrive davvero quando si vuole raggiungere casa da
remoto in modo affidabile.

Ho valutato PPPoE, piu' realistico per una linea consumer,
ma non cambia nulla a valle del modem.

Come indirizzi pubblici ho usato quelli della RFC 5737,
riservati alla documentazione: non appartengono a nessuno.
```

## 4 — Router-on-a-stick

```
HO USATO ROUTER-ON-A-STICK

Ho portato un solo collegamento fisico verso lo switch,
configurato a trunk 802.1Q, con una sottointerfaccia per
ogni VLAN.

Ho scartato l'idea di un cavo per VLAN: servirebbero sei
cavi e sei porte su un router che ne ha due.

In un'azienda sceglierei uno switch multilayer con
interfacce SVI, che instrada in hardware invece che in
software. Ha senso dove il traffico inter-VLAN e' pesante;
qui e' qualche Mb/s di telecamera e telemetria, quindi il
collo di bottiglia del link condiviso resta teorico.
```

## 5 — NAT e cosa ho esposto

```
NAT E COSA HO DECISO DI ESPORRE

In uscita ho configurato PAT sull'unico indirizzo pubblico.
Ho tenuto le VLAN 10, 30 e 60 FUORI dalla lista del NAT:
management, IoT e infrastruttura wireless non hanno motivo
di uscire, e cio' che non e' nella lista non esce.

In ingresso ho pubblicato due soli servizi:
  :443  -> 192.168.50.11:443   cruscotto domotico
  :8443 -> 192.168.50.10:443   registration server IoT

Li ho pubblicati solo in HTTPS. Su HTTP le credenziali
viaggerebbero in chiaro, e questo sistema comanda serrature
e telecamere.

La telecamera non l'ho pubblicata affatto: si raggiunge
solo passando dal cruscotto autenticato. Le webcam esposte
su Internet finiscono indicizzate dai motori di ricerca, e
un solo punto d'ingresso cifrato e' piu' difendibile di
cinque servizi aperti.
```

## 6 — Le ACL e `established`

```
PERCHE' NELLE MIE ACL C'E' "established"

Le ACL di Cisco sono stateless: guardano un pacchetto alla
volta e non sanno che fa parte di una conversazione gia'
aperta. Quando ho bloccato la VLAN 50 verso la VLAN 20 ho
bloccato anche le RISPOSTE dei server ai PC, e il cruscotto
ha smesso di caricare.

Ho aggiunto "permit tcp any any established", che lascia
passare i segmenti con i flag ACK o RST - quelli di una
connessione gia' stabilita - mentre un SYN di apertura
resta bloccato.

So che e' una soluzione approssimata: un ACK si puo'
falsificare. La soluzione corretta sarebbe un firewall
stateful con tabella delle connessioni, su IOS il CBAC o la
Zone-Based Firewall. Non l'ho usata perche' e'
sproporzionata per una rete domestica e perche' qui il
concetto che volevo dimostrare e' la segmentazione.
```

## 7 — Come ho segmentato

```
COME HO SEGMENTATO LA RETE

 10 MGMT      192.168.10.0/24   apparati di rete
 20 MYHOME    192.168.20.0/24   PC e portatili di famiglia
 30 IOT       192.168.30.0/24   21 dispositivi domotici
 40 OSPITI    192.168.40.0/24   visitatori
 50 SERVIZI   192.168.50.0/24   i cinque server
 60 WIRELESS  192.168.60.0/24   WLC e LAP, solo CAPWAP
 99 NATIVE    nessuna porta assegnata

La traccia ne chiedeva quattro. Le due che ho aggiunto le
motivo nelle note 10 e 13, la 99 nella nota 8.

La politica che ho scritto nelle ACL:
  ospiti      solo Internet, nient'altro
  IoT         solo VLAN 50, niente Internet, niente MyHome
  management  raggiunge tutto, non esce su Internet
```

## 8 — La native VLAN

```
PERCHE' HO SPOSTATO LA NATIVE SULLA 99

I frame della native VLAN viaggiano senza tag. Lasciando la
native a 1, un attaccante collegato a una porta di accesso
puo' iniettare un frame che ha gia' un tag 802.1Q dentro:
lo switch toglie il tag della native e inoltra il frame
nella VLAN indicata dal tag interno. E' il VLAN hopping a
doppio tag.

Ho messo la native su una VLAN a cui non ho assegnato
nessuna porta, cosi' l'attacco non ha un punto d'appoggio.

Ho fatto una sola eccezione: la porta verso il WLC ha
native 60, perche' l'interfaccia di management del
controller dev'essere untagged. E' una deroga circoscritta
a una porta e verso un apparato dell'infrastruttura.
```

## 9 — La VLAN IoT

```
LA DECISIONE DI SICUREZZA PIU' IMPORTANTE

Ho fatto in modo che gli IoT non escano su Internet e non
entrino in MyHome. Parlano solo con la VLAN 50, dove sta il
registration server.

I dispositivi domotici commerciali sono il punto debole di
una casa: firmware non aggiornati, credenziali di default,
servizi esposti. Confinandoli cosi', anche un dispositivo
compromesso non ha strada verso i PC di famiglia e non puo'
essere arruolato in una botnet, perche' non raggiunge
Internet.

Le automazioni non ne risentono: avvengono tutte fra la
VLAN 30 e la VLAN 50.

Sulle porte IoT ho attivato anche port-security con un solo
MAC per porta: se qualcuno stacca la telecamera e attacca
un portatile, la porta si spegne.
```

## 10 — La VLAN dei server

```
PERCHE' HO DATO AI SERVER UNA VLAN DEDICATA

I server sono l'unica cosa che tutte le altre VLAN devono
raggiungere: gli IoT ci registrano lo stato, i PC aprono il
cruscotto, il WLC interroga il RADIUS, e il web domotico e'
pubblicato verso Internet.

Se li avessi lasciati dentro MyHome, per far parlare gli
IoT con il registration server avrei dovuto aprire un varco
dalla VLAN meno affidabile della casa verso quella che
contiene i PC personali: esattamente cio' che la
segmentazione dovrebbe impedire.

Isolandoli ho ottenuto una regola netta: tutti raggiungono
la VLAN 50 sulle porte dei servizi, nessuno raggiunge le
altre VLAN. E' il ragionamento di una DMZ aziendale,
applicato in piccolo.
```

## 11 — Il DHCP

```
PERCHE' IL DHCP STA SU UN SERVER E NON SUL ROUTER

Le richieste DHCP sono broadcast e un router non le
inoltra: un dispositivo in VLAN 30 non raggiungerebbe mai
un server in VLAN 50.

Ho risolto con ip helper-address: il router intercetta il
broadcast, lo trasforma in unicast verso il server e scrive
nel campo giaddr l'indirizzo della propria
sottointerfaccia. Cosi' il server capisce da quale rete
arriva la richiesta e pesca dal pool giusto.

Avrei potuto mettere il DHCP sul router, che era piu'
semplice. Ho preferito il server perche' tutte le
assegnazioni si vedono in un posto solo, le prenotazioni
per indirizzo MAC si gestiscono senza toccare la
configurazione del router, e se domani i router diventano
due non devo duplicare niente.

Ho lasciato indirizzo statico dove il servizio deve stare
sempre allo stesso posto: server, apparati di rete,
telecamera e centralina.
```

## 12 — Il wireless ibrido

```
PERCHE' HO SCELTO UN WIRELESS IBRIDO

MyHome : LAP gestito da WLC-3504, WPA2-Enterprise/RADIUS
IOT    : access point autonomo, WPA2-PSK
GUEST  : access point autonomo, WPA2-PSK

MyHome e' l'unica rete su cui ci si muove: telefoni e
portatili passano dal giardino alla camera mentre sono
connessi. Roaming, gestione centralizzata di canali e
potenza, policy 802.1X uniforme sono i problemi che risolve
un controller, e per questo l'ho usato li'.

IOT e GUEST li ho lasciati su access point autonomi per una
ragione di disponibilita'. Un LAP che perde il WLC smette
di servire i client: mettendo la domotica dietro al
controller, un guasto del WLC mi spegnerebbe luci
automatiche, allarme antincendio e irrigazione. Un AP
autonomo tiene la configurazione a bordo e va avanti da
solo.

E' lo stesso principio con cui ho scritto la centralina
MCU: cio' che e' critico non dipende da un elemento
centrale.
```

## 12b — Enterprise e canali

```
PERCHE' ENTERPRISE SOLO SU MyHome

Con la PSK la chiave e' una sola e condivisa: per togliere
l'accesso a una persona dovrei cambiarla a tutti.

Con WPA2-Enterprise ho dato a ogni utente credenziali
proprie verificate dal RADIUS: revoco il singolo senza
toccare gli altri, e nei log vedo chi si e' collegato.

Su IoT e ospiti l'802.1X non era praticabile: buona parte
dei dispositivi non lo supporta, e per gli ospiti
servirebbe un'utenza per ogni persona che viene a cena. La'
la PSK va bene, perche' quelle due reti le ho gia' isolate
con le ACL e la chiave condivisa non espone nulla di
critico.

Come client RADIUS ho registrato il WLC, non il LAP: con
l'architettura lightweight e' il controller a parlare con
il server di autenticazione per tutti i suoi access point.

Ho assegnato i canali 1, 6 e 11, gli unici tre non
sovrapposti nella banda 2.4 GHz: con canali adiacenti gli
apparati si disturberebbero a vicenda.
```

## 13 — Perché il LAP è in VLAN 60

```
PERCHE' LA PORTA DEL LAP E' IN VLAN 60 E NON IN VLAN 20

Fra LAP e WLC c'e' un tunnel CAPWAP. Il traffico dei client
di MyHome non viene messo in VLAN 20 dal LAP: viene
incapsulato e portato fino al controller, ed e' il WLC a
immetterlo in VLAN 20 attraverso la propria interfaccia
dinamica.

Su quel cavo passa quindi solo CAPWAP, e ho messo la porta
nella VLAN 60 dell'infrastruttura wireless. La VLAN 20
arriva invece sulla porta del WLC, che ho configurato a
trunk.

Gli access point autonomi funzionano al contrario, in local
switching: mettono il frame direttamente sulla VLAN della
loro porta di accesso. Per questo AP-IOT sta su una porta
in VLAN 30 e AP-GUEST su una in VLAN 40.

Si vede provando: un client associato a MyHome prende un
indirizzo 192.168.20.x pur essendo l'access point attestato
su una porta in VLAN 60.

La VLAN 60 l'ho creata anche perche' con LAP e WLC sulla
stessa sottorete la scoperta del controller e' piu'
semplice, e perche' il piano di controllo del wireless non
e' la stessa cosa della gestione di switch e router.
```

## 14 — La centralina MCU

```
LA CENTRALINA - HO MESSO LA LOGICA A BORDO

Irriga solo se sono vere tutte e tre le condizioni:
  umidita' terreno < 30%   c'e' davvero bisogno
  luce ambiente    < 40%   non nelle ore calde
  almeno 6 ore dall'ultimo ciclo

Si ferma quando l'umidita' supera il 45%, non il 30% che
l'ha fatta partire.

Ho usato due soglie diverse perche' con una sola, appena il
valore tocca il 30%, il rele' si spegnerebbe, il valore
ricadrebbe sotto e si riaccenderebbe: decine di
commutazioni al minuto che bruciano il rele' e stressano
l'elettrovalvola.

E' anche il motivo per cui questa logica non potevo
scriverla nelle condizioni del registration server: quelle
sono booleane e senza memoria fra un'esecuzione e l'altra,
quindi non possono avere due soglie e uno stato.

L'ho resa fail-safe: valvola chiusa all'avvio, e lettura
fuori scala interpretata come sensore rotto, con chiusura
immediata. Meglio una pianta secca che un giardino
allagato.

Un attuatore comandato dal server si fermerebbe se cadesse
la rete. L'MCU continua a decidere anche scollegato e
pubblica lo stato quando la rete torna.

Ho verificato la logica su 9 scenari prima di scriverla.
```

## 15 — I limiti

```
I LIMITI DEL MIO PROGETTO

Il port forwarding espone comunque la porta 443 a chiunque
su Internet. In produzione userei una VPN: ci si collega
alla rete di casa e non si pubblica niente. Ho scelto il
port forwarding perche' e' cio' che chiede la traccia e
perche' Packet Tracer non offre una VPN client praticabile.

Le mie ACL sono stateless, come spiego nella nota 6. La
soluzione corretta sarebbe un firewall stateful.

Non ho previsto ridondanza: un router, un WLC, un LAP. Se
cade il WLC cade MyHome, mentre IOT e GUEST continuano - ed
e' proprio per questo che li ho lasciati su access point
autonomi. In un contesto reale metterei due WLC in coppia,
non rinuncerei al controller.

Il registration server e' un punto singolo di guasto per le
automazioni. Per questo ho messo la logica dell'irrigazione
a bordo dell'MCU.

L'ambiente di Packet Tracer non e' la fisica reale: le
velocita' di variazione servono a mostrare che le regole
scattano, non a dimensionare un impianto.
```

## 16 — Il collaudo

```
COME HO COLLAUDATO

Ho costruito e verificato per fasi, provando ogni livello
prima di salire al successivo: fisico, VLAN e trunk,
indirizzamento, DHCP, politica di traffico, wireless,
applicativo, accesso dall'esterno. Con dodici sottosistemi,
collaudare solo alla fine avrebbe significato non sapere
quale dei dodici era rotto.

Ho dato lo stesso peso alle prove che devono FALLIRE:

  PC di MyHome   ->  management        deve fallire
  ospite         ->  rete di casa      deve fallire
  HTTP dall'esterno                    deve fallire
  telecamera dall'esterno              deve fallire

Senza queste controprove, una rete "che funziona" potrebbe
essere semplicemente una rete piatta.

Per le automazioni ho fatto lo stesso: per ogni regola ho
provato anche il caso in cui non deve scattare, per esempio
il condizionatore con la finestra aperta.
```

---

## Ordine di lettura

Le note seguono il percorso del traffico, da Internet verso i dispositivi:
2 → 3 → 4 → 5 → 6 → 7 → 8 → 10 → 11 → 9 → 12 → 12b → 13 → 14.
La 1 apre, la 15 e la 16 chiudono.

Posate secondo la mappa, chi legge il `.pkt` da sinistra in basso trova già
quella sequenza.
