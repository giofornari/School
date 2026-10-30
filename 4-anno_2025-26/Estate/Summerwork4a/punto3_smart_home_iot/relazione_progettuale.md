# Progetto CPT — Domotica e IoT
## Relazione progettuale

Villa unifamiliare su un piano. Rete segmentata in sei VLAN, tre reti wireless su
architettura ibrida, 21 dispositivi IoT, accesso e monitoraggio da Internet,
sottosistema di automazione su microcontrollore.

Questo documento non descrive *come* si costruisce la rete — quello sta in
[`guida_costruzione_pkt.md`](guida_costruzione_pkt.md) e
[`configurazioni_cli.md`](configurazioni_cli.md). Descrive **perché** è fatta
così: per ogni scelta, il vincolo che l'ha imposta, l'alternativa scartata e la
ragione dello scarto.

---

## 1. Criteri di progetto

Prima di posare un apparato ho fissato cinque criteri. Tutte le decisioni che
seguono discendono da questi, e dove due criteri sono entrati in conflitto l'ho
scritto.

| # | Criterio | Conseguenza operativa |
|---|---|---|
| 1 | **La domotica non deve dipendere da un elemento centrale** | Ciò che è critico tiene la logica a bordo: rete IoT su AP autonomi, irrigazione su microcontrollore |
| 2 | **Un dispositivo IoT compromesso non deve poter fare danni** | VLAN IoT senza uscita su Internet e senza accesso alla rete di famiglia |
| 3 | **Esporre il minimo indispensabile verso l'esterno** | Un solo servizio pubblicato, solo in HTTPS, telecamera non raggiungibile da fuori |
| 4 | **Ogni scelta dev'essere difendibile, non solo funzionante** | Dove esisteva un'alternativa più semplice ma peggiore, è documentata e scartata |
| 5 | **Dichiarare i limiti invece di nasconderli** | §12 elenca ciò che il progetto non copre e perché |

Il criterio 1 e il criterio 2 sono in tensione: isolare gli IoT li rende più
sicuri ma anche più dipendenti dal server locale. La composizione dei due è nel
§6 e nel §10.

---

## 2. L'abitazione

Villa unifamiliare su un piano, con garage annesso, giardino esposto a sud e
cantina al piano interrato.

**Ambienti:** ingresso, cucina, bagno con lavanderia, camera matrimoniale, un
corridoio di distribuzione che attraversa tutta la casa, soggiorno, studio,
camera singola, locale tecnico.

| Locale | Contenuto | Motivazione della collocazione |
|---|---|---|
| **Locale tecnico** | rack: modem, router, switch, WLC, i due AP autonomi, i cinque server | Baricentrico: tratte in rame corte verso tutti gli ambienti e copertura wireless da un punto solo. Chiuso a chiave, quindi le porte fisiche non sono raggiungibili dagli ospiti |
| **Corridoio** | LAP a soffitto | Con un access point gestito la posizione conta più della configurazione: quella la riceve dal controller |
| **Cantina** | batteria di accumulo, contatore | La batteria è pesante e vuole un ambiente fresco; il contatore sta dove entra la linea elettrica. Collegamento in fibra al rack |
| **Giardino** | pannello solare, sensore di luce, irrigazione, centralina MCU | Esposizione sud: è ciò che rende sensato il fotovoltaico |
| **Garage** | nessun apparato di rete | Volutamente fuori dalla rete domotica |

**Perché il locale tecnico è al centro e non in garage o in cantina.** Sono i due
posti dove in una casa reale finisce quasi sempre il router, ed è quasi sempre un
errore: sono i punti più periferici, quindi le tratte si allungano e il segnale
Wi-Fi deve attraversare più muri. Un locale baricentrico risolve entrambi i
problemi con una scelta sola.

**Perché la fibra fra cantina e piano abitabile.** Il percorso reale è di 25–30 m
in un cavedio condiviso con i cavi di potenza. Il rame in quelle condizioni
raccoglie disturbi elettromagnetici e, soprattutto, crea un percorso conduttivo
fra due quadri elettrici diversi. La fibra è immune ai disturbi e disaccoppia
elettricamente i due punti.

Planimetria annotata in [`planimetria.svg`](planimetria.svg). Lo schema **non è
in scala**: la dimensione di ogni locale è proporzionata al numero di apparati
che ospita. È una pianta funzionale, non un progetto edilizio, e va detto invece
di lasciarlo dedurre.

---

## 3. Architettura di rete

```
                        ── CENTRALE DELL'OPERATORE ──
   [ Web pubblico ]      [ DNS pubblico ]      [ PC "sono fuori casa" ]
    198.51.100.10         198.51.100.53           198.51.100.20
            └──────────────┬──────┴───────────────────┘
                           │ 198.51.100.0/24
                    [ R-ISP ] 203.0.113.1/30
                           │
                   [ CLOUD-ISP ]  rete di accesso / DSLAM — nessun IP
                           ┊ doppino telefonico
  ═════════════════════════┊═══ CONFINE DI PROPRIETÀ ═══════════════════
                   [ MODEM-DSL ]  bridge trasparente — nessun IP
                           │
                    [ R-HOME ] 203.0.113.2/30 — NAT, DHCP relay, ACL
                           │ trunk 802.1Q
                    [ SW-HOME ]
     ┌──────┬──────┬──────┬──────┬──────┬──────┐
   VLAN10 VLAN20 VLAN30 VLAN40 VLAN50 VLAN60
   Mgmt   MyHome  IoT   Ospiti Servizi Wireless
                                        WLC+LAP
```

### 3.1 La catena di accesso

Un errore ricorrente nei progetti scolastici è collegare il router di casa
direttamente a quello dell'operatore con un cavo di rete. In una casa reale non
esiste: fra i due ci sono la rete di accesso dell'operatore e il modem installato
presso il cliente.

| Apparato | Funzione reale | Dove | Livello 3 |
|---|---|---|---|
| `R-ISP` | Router di terminazione del provider | Centrale | Sì |
| `CLOUD-ISP` | **DSLAM**: raccoglie i doppini del quartiere | Centrale | No |
| `MODEM-DSL` | Modem del cliente, in **bridge** | Locale tecnico | No |
| `R-HOME` | Router di casa: NAT, relay, ACL, inter-VLAN | Locale tecnico | Sì |

**La conseguenza che dimostra di aver capito il modello a livelli.** Nuvola e
modem sono trasparenti al livello 3: non hanno indirizzo, non instradano, non
decrementano il TTL. Per il routing sono un cavo lungo che passa dalla centrale.
Per questo `R-ISP` e `R-HOME` restano **direttamente connessi sulla stessa
`203.0.113.0/30`** pur essendo a chilometri di distanza — ed è lo stesso motivo
per cui il modem di casa non compare mai in un `tracert`.

Il piano di indirizzamento, il NAT, le rotte e il port forwarding **non cambiano
di una riga** rispetto a un collegamento diretto: cambia solo il percorso fisico.

La nuvola richiede configurazione esplicita (`Config → DSL`, mappatura
`Modem0 ↔ Ethernet0`): il Cloud-PT non è uno switch, non impara i MAC e inoltra
**solo** sulle coppie di porte programmate. Senza quella riga il collegamento non
passa pur avendo tutti i link verdi.

### 3.2 Router-on-a-stick

Un solo collegamento fisico router–switch, portato a trunk 802.1Q, con una
sottointerfaccia per VLAN.

**Alternativa scartata:** un cavo per VLAN. Servirebbero sei cavi e sei porte su
un router che ne ha due. **Alternativa migliore in altro contesto:** uno switch
multilayer con interfacce SVI, che instrada in hardware invece che in software.
Ha senso dove il traffico inter-VLAN è pesante; in una casa quel traffico è
qualche Mb/s di telecamera e telemetria, quindi il collo di bottiglia del link
condiviso resta teorico.

### 3.3 Indirizzo pubblico statico, non PPPoE

Una linea consumer assegna un indirizzo pubblico dinamico. Qui è statico, e la
ragione è il requisito di monitoraggio da Internet: **il port forwarding pubblica
un servizio su un indirizzo**, e se quell'indirizzo cambia a ogni riconnessione
da fuori non si sa più dove chiamare. Le alternative sono due: un servizio di
**DNS dinamico** che aggiorna il record a ogni cambio, oppure un **IP statico**.
Per un sistema che comanda serrature e telecamere il secondo è più solido, e in
una linea reale è ciò che si sottoscrive proprio per questo motivo.

PPPoE sarebbe più realistico per una linea domestica ma non cambierebbe nulla a
valle del modem, e in Packet Tracer è fragile.

Gli indirizzi pubblici sono quelli riservati alla documentazione dalla **RFC
5737** (`198.51.100.0/24` e `203.0.113.0/24`): non appartengono a nessuno, quindi
il progetto non usa indirizzi altrui.

---

## 4. Indirizzamento

| Rete | VLAN | Gateway | Assegnazione | Contenuto |
|---|---|---|---|---|
| 198.51.100.0/24 | — | .1 | statica | LAN dell'operatore |
| 203.0.113.0/30 | — | — | statica | Link ISP ↔ casa |
| 192.168.10.0/24 | 10 | .1 | statica | Management: switch .2, PC admin .100 |
| 192.168.20.0/24 | 20 | .1 | DHCP .100–.199 | PC e portatili di famiglia; interfaccia dinamica del WLC .5 |
| 192.168.30.0/24 | 30 | .1 | DHCP + statici | IoT; webcam .20, MCU .30 |
| 192.168.40.0/24 | 40 | .1 | DHCP .100–.150 | Ospiti |
| 192.168.50.0/24 | 50 | .1 | statica | I cinque server |
| 192.168.60.0/24 | 60 | .1 | WLC statico, LAP DHCP | Infrastruttura wireless |
| — | 99 | — | — | Native VLAN dei trunk, nessuna porta |

**Criterio.** Indirizzo statico dove il servizio deve essere sempre allo stesso
posto (server, apparati di rete, telecamera, centralina); DHCP dove i dispositivi
cambiano nel tempo. Un server che prende l'indirizzo dal DHCP è una pessima idea:
se il DHCP cambia idea, il servizio diventa irraggiungibile e nessuno capisce
perché.

**Perché una /30 sul link con l'ISP.** Due host utili su quattro indirizzi: è il
minimo che serve a un collegamento punto-punto e non spreca spazio pubblico, che
è una risorsa scarsa e a pagamento. Le reti interne restano /24 perché lì lo
spazio privato è abbondante e la leggibilità vale più dell'ottimizzazione.

---

## 5. Segmentazione: le VLAN

La traccia chiede almeno quattro VLAN. Ne ho usate sei più una inutilizzata, e
ogni aggiunta ha una ragione.

### 5.1 Perché una VLAN dedicata ai server (50)

I server sono l'unica cosa a cui devono accedere **tutte** le altre VLAN: gli IoT
ci registrano lo stato, i PC aprono il cruscotto, il controller wireless
interroga il RADIUS, e il web domotico è esposto verso Internet.

Lasciandoli dentro MyHome, per far parlare gli IoT con il registration server
bisognerebbe aprire un varco dalla VLAN meno affidabile della casa verso quella
che contiene i PC personali — cioè esattamente ciò che la segmentazione dovrebbe
impedire. Isolandoli la regola diventa netta: **tutti raggiungono la VLAN 50
sulle porte dei servizi, nessuno raggiunge le altre VLAN.**

È il ragionamento di una DMZ aziendale applicato in piccolo.

### 5.2 Perché una VLAN dedicata all'infrastruttura wireless (60)

Due motivi, uno funzionale e uno di principio.

**Funzionale:** se LAP e interfaccia di management del controller stanno sulla
stessa sottorete, il LAP può trovare il WLC senza dipendere da meccanismi di
scoperta più fragili. Meno pezzi, meno cose che si rompono.

**Di principio:** il piano di controllo del wireless non è la stessa cosa della
gestione di switch e router. Tenerlo separato significa che chi amministra gli
apparati non transita sulla stessa sottorete su cui viaggia CAPWAP.

### 5.3 Perché la native VLAN è la 99

Di default la native VLAN di un trunk è la 1, e i frame della native viaggiano
**senza tag**. Un attaccante su una porta di accesso in VLAN 1 può iniettare un
frame con un tag 802.1Q già dentro: lo switch toglie il tag della native e
inoltra il frame nella VLAN indicata dal tag interno. È il **VLAN hopping con
doppio tag**. Spostare la native su una VLAN senza porte assegnate toglie il
punto di appoggio all'attacco.

**Eccezione dichiarata:** la porta del WLC è l'unico trunk con native 60, perché
l'interfaccia di management del controller dev'essere untagged. È una deroga
consapevole, circoscritta a una porta, verso un apparato dell'infrastruttura.

### 5.4 Politica di traffico

| Da → a | 10 | 20 | 30 | 40 | 50 | 60 | Internet |
|---|---|---|---|---|---|---|---|
| **10 Mgmt** | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✖ |
| **20 MyHome** | ✖ | ✔ | ✔ | ✖ | ✔ | ✖ | ✔ |
| **30 IoT** | ✖ | ✖ | ✔ | ✖ | solo servizi | ✖ | ✖ |
| **40 Ospiti** | ✖ | ✖ | ✖ | ✔ | solo DNS/DHCP | ✖ | ✔ |
| **50 Servizi** | ✖ | ✖ | ✔ | ✖ | ✔ | ✖ | ✔ |
| **60 Wireless** | ✖ | ✖ | ✖ | ✖ | solo servizi | ✔ | ✖ |

Le quattro righe che contano:

**Gli IoT non escono su Internet e non entrano in MyHome.** È la scelta di
sicurezza più importante del progetto. I dispositivi domotici commerciali sono il
punto debole di una casa: firmware non aggiornati, credenziali di default,
servizi esposti. Confinandoli in una VLAN che parla solo con il registration
server, anche un dispositivo compromesso non ha strada verso i PC di famiglia e
non può essere arruolato in una botnet, perché non raggiunge Internet. Le
automazioni continuano a funzionare, perché avvengono tutte fra VLAN 30 e 50.

**Gli ospiti non vedono niente.** L'ACL nega tutto ciò che è diretto a
`192.168.0.0/16` tranne DNS e DHCP, e permette il resto. Un ospite naviga e
basta: non trova né la telecamera né i PC.

**Il management non esce.** La VLAN 10 raggiunge tutto ma non ha rotta verso
Internet: se le credenziali di uno switch trapelano, non sono usabili da fuori.

**L'infrastruttura wireless parla solo con i servizi.** Al controller serve il
RADIUS, non Internet.

### 5.5 Il limite delle ACL, dichiarato

Nelle configurazioni compaiono `permit tcp any any established` e
`permit icmp any any echo-reply`. Non sono riempitivo: le ACL di Cisco sono
**stateless**, guardano un pacchetto alla volta e non sanno che fa parte di una
conversazione già aperta. Bloccando «da VLAN 50 verso VLAN 20» si bloccano anche
le **risposte** del server alle richieste dei PC, e il cruscotto smette di
caricare.

`established` lascia passare i segmenti TCP con i flag ACK o RST — quelli di una
connessione già stabilita — mentre un pacchetto di apertura con il solo SYN non
passa.

**È una soluzione approssimata e va detto:** un attaccante può fabbricare un
pacchetto con l'ACK già alzato. La soluzione corretta è un **firewall stateful**
che mantenga una tabella delle connessioni aperte — su IOS sarebbe CBAC
(`ip inspect`) o la Zone-Based Firewall. Non l'ho usata perché aggiunge
complessità sproporzionata a una rete domestica e perché il concetto da
dimostrare qui è la segmentazione, non il filtraggio applicativo.

---

## 6. Wireless: architettura ibrida

Tre reti realizzate con **due tecnologie diverse**, scelte in base a cosa deve
fare ciascuna.

| SSID | VLAN | Apparato | Autenticazione |
|---|---|---|---|
| `MyHome` | 20 | **LAP** gestito da **WLC-3504** | WPA2 Enterprise (802.1X) verso RADIUS |
| `IOT` | 30 | AP autonomo | WPA2-PSK |
| `GUEST` | 40 | AP autonomo | WPA2-PSK, chiave a rotazione |

### 6.1 Perché il controller solo sulla rete principale

**`MyHome` è l'unica rete su cui ci si muove.** Telefoni e portatili passano dal
giardino alla camera mentre sono connessi. Roaming fra access point, gestione
centralizzata di canali e potenza, policy 802.1X uniforme: sono esattamente i
problemi che un controller risolve. E aggiungendo un secondo LAP, questo scarica
la configurazione da solo.

**`IOT` e `GUEST` restano autonomi per disponibilità.** Un LAP che perde il WLC
smette di servire i client. Mettendo la rete IoT dietro al controller, un guasto
del WLC fermerebbe la domotica: niente luci automatiche, niente allarme
antincendio, niente irrigazione. Un AP autonomo tiene la configurazione a bordo e
continua da solo.

**È il criterio 1 del §1 applicato al wireless**, ed è lo stesso principio per
cui la centralina dell'irrigazione ha la logica sul microcontrollore e non sul
server: ciò che è critico non dipende da un elemento centrale.

Due ragioni minori ma vere: la rete ospiti è statica e a SSID singolo, non
guadagna nulla dalla gestione centralizzata; e tenerla su una scatola separata
significa che, se quell'AP viene compromesso, non fa parte dell'infrastruttura
gestita.

**In un contesto diverso la scelta si ribalta.** In una scuola o in un albergo
passerebbe tutto dal controller, ospiti compresi: con decine di AP la
configurazione uno per uno è ingestibile, e la ridondanza si ottiene con due WLC
in coppia invece che rinunciando al controller.

### 6.2 Switching centralizzato contro switching locale

È il punto tecnico che non si deduce guardando lo schema.

Fra LAP e WLC si stabilisce un tunnel **CAPWAP**. Il traffico dei client `MyHome`
non viene messo sulla VLAN 20 dal LAP: viene **incapsulato e portato fino al
controller**, ed è il WLC a immetterlo nella VLAN 20 attraverso la propria
interfaccia dinamica.

Conseguenza: **la porta di switch del LAP non sta in VLAN 20, sta in VLAN 60**,
perché su quel cavo passa solo CAPWAP. La VLAN 20 arriva invece sulla porta del
WLC, configurata a trunk. Gli AP autonomi funzionano al contrario — *local
switching*: mettono il frame direttamente sulla VLAN della loro porta di accesso.

Il collaudo lo dimostra: un client associato a `MyHome` prende un indirizzo di
VLAN 20 pur essendo l'access point attestato su una porta in VLAN 60.

### 6.3 Perché Enterprise solo su MyHome

Con **WPA2-PSK** la chiave è una sola e condivisa: chi la conosce entra, e per
revocare l'accesso a una persona bisogna cambiarla a tutti. Con **WPA2-Enterprise**
ogni utente ha credenziali proprie verificate dal RADIUS: si revoca il singolo
utente senza toccare gli altri, e nei log si vede *chi* si è collegato.

Sui dispositivi IoT l'Enterprise è impraticabile — buona parte non supporta
802.1X — e sugli ospiti sarebbe una scocciatura: servirebbe un'utenza per ogni
persona che viene a cena. Lì la PSK è corretta, con la premessa che quelle due
reti sono già isolate dalle ACL, quindi la chiave condivisa non espone nulla di
critico.

Il client RADIUS è il **controller**, non il LAP: con l'architettura lightweight
è il WLC a parlare con il server di autenticazione per conto di tutti i suoi
access point.

**Canali 1, 6, 11**: gli unici tre non sovrapposti nella banda 2.4 GHz.
Assegnarne di adiacenti farebbe interferire gli apparati fra loro, con un calo di
prestazioni che non si spiega guardando la configurazione IP.

---

## 7. Servizi di rete

| Servizio | Indirizzo | Nota progettuale |
|---|---|---|
| Registration server IoT | 192.168.50.10 | Registra i 21 dispositivi e ospita le regole |
| Web server domotico | 192.168.50.11 | Unico servizio pubblicato su Internet |
| Server DHCP | 192.168.50.12 | Centralizzato, vedi sotto |
| Server RADIUS (AAA) | 192.168.50.13 | Autenticazione 802.1X per `MyHome` |
| Server DNS | 192.168.50.53 | Zona interna `casa.lan`, forward verso l'esterno |
| Telecamera IP | 192.168.30.20 | Statico, non pubblicata |
| Monitoraggio energetico | 192.168.30.30 | MCU, vedi §9 |

### 7.1 DHCP centralizzato e `ip helper-address`

Il DHCP sta su un server dedicato in VLAN 50, non sul router. Le richieste DHCP
sono **broadcast**, e un router non inoltra i broadcast: senza accorgimenti un
dispositivo in VLAN 30 non raggiungerebbe mai un server in VLAN 50.

`ip helper-address` risolve: il router intercetta il broadcast, lo trasforma in
unicast verso il server e ci scrive dentro l'indirizzo della propria
sottointerfaccia nel campo *giaddr*, così il server capisce da quale rete arriva
la richiesta e sceglie il pool giusto.

**Alternativa scartata: il DHCP sul router**, che sarebbe più semplice. Con un
server unico si vedono tutte le assegnazioni in un posto solo, si gestiscono le
prenotazioni per MAC senza toccare la configurazione del router, e se un domani i
router diventassero due la configurazione non andrebbe duplicata.

### 7.2 DNS interno

| Nome | Indirizzo |
|---|---|
| `casa.lan` | 192.168.50.11 |
| `iot.casa.lan` | 192.168.50.10 |
| `cam.casa.lan` | 192.168.30.20 |
| `energia.casa.lan` | 192.168.30.30 |

Il DNS interno inoltra all'esterno ciò che non sa risolvere. Esiste per due
ragioni pratiche: nessuno ricorda gli indirizzi IP, e se un servizio cambia
indirizzo si aggiorna un record invece di riconfigurare tutti i client.

---

## 8. Accesso da Internet

**Uscita.** NAT overload (PAT) su `R-HOME`: le VLAN autorizzate escono con
l'unico indirizzo pubblico, distinte per numero di porta. VLAN 10, 30 e 60 sono
**deliberatamente escluse** dalla lista del NAT: management, IoT e infrastruttura
wireless non hanno motivo di uscire, e ciò che non è nella lista non esce.

**Ingresso.** Il NAT dinamico non basta, perché le sessioni le apre chi sta
dentro. Per raggiungere il cruscotto da fuori serve un **NAT statico con
traduzione di porta**:

| Dall'esterno | Verso | Servizio |
|---|---|---|
| `203.0.113.2:443` | `192.168.50.11:443` | Cruscotto domotico |
| `203.0.113.2:8443` | `192.168.50.10:443` | Registration server IoT |

Due decisioni da motivare, perché riguardano *cosa non* si espone.

**Solo HTTPS.** Su HTTP le credenziali viaggiano in chiaro e chiunque sia sul
percorso può leggerle. Pubblicare la porta 80 di un sistema che comanda serrature
e telecamere sarebbe un errore grave.

**La telecamera non è pubblicata.** Si raggiunge solo passando dal cruscotto
autenticato. Le telecamere IP esposte su Internet sono una delle cause più
frequenti di violazione della privacy domestica — esistono motori di ricerca che
le indicizzano. Un solo punto d'ingresso, autenticato e cifrato, è molto più
difendibile di cinque servizi esposti.

**Instradamento.** `R-HOME` ha una sola uscita, quindi gli basta una rotta di
default. `R-ISP` raggiunge la rete di casa perché il link è direttamente
connesso: nuvola e modem non contano, sono trasparenti al livello 3. Gli
indirizzi privati interni non sono e non devono essere instradabili su Internet —
è il NAT a farli sparire.

---

## 9. Sistema IoT

21 dispositivi su tre categorie: **Home** (15), **Power Grid** (3),
**Industrial/esterni** (3). Elenco completo con funzione, vantaggio e modalità di
collegamento in [`dispositivi_e_automazioni.md`](dispositivi_e_automazioni.md).

**10 regole di automazione**, di cui **4 con più condizioni in AND**. Sono queste
ultime a soddisfare davvero il requisito «il comportamento si adatta allo stato
degli input»: una regola a condizione singola è poco più di un interruttore.

Tre esempi che mostrano il criterio con cui sono scritte:

| Regola | Logica | Perché così |
|---|---|---|
| `LuceIngresso-ON` | Movimento **AND** luce ambiente < 30 % | La seconda condizione impedisce che la luce si accenda di giorno |
| `Caldo-Condizionatore` | Temperatura ≥ 27 °C **AND** finestra chiusa | Il condizionatore non parte a raffreddare la strada |
| `Antincendio` | Fumo > 30 % | Un sensore, quattro attuatori: sirena, sprinkler, apertura finestra per lo sfogo dei fumi, annuncio vocale |

Il collaudo prevede per ognuna anche la **controprova** — stessa temperatura ma
finestra aperta, stesso movimento ma di giorno — perché è la controprova a
dimostrare che la regola guarda davvero entrambe le condizioni.

### 9.1 Monitoraggio energetico

```
[Solar Panel] ══> [Power Meter] ══> [Battery] ══> carichi domotici
                        │
              lettura analogica
                        ▼
                   [MCU-PT] ──rete──> registration server
```

Il Power Meter mostra il valore a schermo ma non lo pubblica in rete: è l'MCU a
leggerlo e a renderlo disponibile al cruscotto. È il motivo per cui i due
sottosistemi sono progettati insieme e non separatamente.

---

## 10. Il sottosistema a microcontrollore

Un **MCU-PT** in giardino gestisce irrigazione e telemetria energetica con
componenti discreti: sensore di umidità del terreno e fotoresistore su ingressi
analogici, relè verso l'elettrovalvola e LED RGB di stato su uscite digitali.

**La logica irriga solo se tutte e tre le condizioni sono vere:** terreno sotto
il 30 %, luce ambiente sotto il 40 %, e almeno sei ore dall'ultima irrigazione.
Ogni condizione risolve un problema diverso — l'umidità è il motivo per irrigare,
la luce bassa evita l'evaporazione nelle ore calde, il tempo minimo evita che un
sensore sporco faccia partire il ciclo in continuazione.

### 10.1 L'isteresi

Il ciclo si ferma quando l'umidità supera il **45 %**, non il 30 % che l'ha fatto
partire. Senza questo scarto, appena l'umidità tocca la soglia il relè si
spegnerebbe, il valore ricadrebbe sotto e si riaccenderebbe: decine di
commutazioni al minuto, che bruciano il relè e stressano l'elettrovalvola.

**È anche la ragione per cui questa logica non può stare sul registration
server:** le condizioni del server sono booleane e senza memoria fra
un'esecuzione e l'altra, quindi non possono implementare due soglie e uno stato.

### 10.2 Perché un microcontrollore e non un attuatore preconfezionato

Un attuatore comandato dal server esegue e basta: se la rete cade, si ferma.
L'MCU contiene la logica a bordo e continua a decidere anche scollegato,
pubblicando lo stato quando la rete torna. È la differenza fra **controllo
centralizzato** ed **edge computing**, ed è il motivo per cui nell'automazione
reale la logica critica non sta mai solo nel cloud.

La logica è stata verificata su **9 scenari** prima di scriverla nel simulatore:
avvio corretto, blocco di giorno, blocco a terreno bagnato, isteresi, assenza di
commutazioni ripetute su valori oscillanti attorno alla soglia, rispetto della
pausa di sei ore, ripartenza dopo la pausa, timeout di sicurezza, sensore fuori
scala. Tutti superati.

Il comportamento in caso di guasto è **fail-safe**: valvola chiusa all'avvio, e
lettura fuori scala interpretata come sensore rotto con chiusura immediata.
Meglio una pianta secca che un giardino allagato.

---

## 11. Quadro di sicurezza

| Misura | Minaccia contrastata |
|---|---|
| VLAN IoT senza Internet né accesso a MyHome | Dispositivo IoT compromesso usato come testa di ponte o arruolato in botnet |
| VLAN ospiti isolata da tutto il privato | Ospite curioso o dispositivo infetto portato in casa |
| Native VLAN 99 senza porte assegnate | VLAN hopping con doppio tag |
| Porte inutilizzate spente e parcheggiate in VLAN 99 | Chi collega un portatile a una presa libera |
| `port-security` sulle porte IoT | Sostituzione fisica di un dispositivo con un portatile |
| WPA2-Enterprise su MyHome | Chiave condivisa che circola fra troppe persone |
| Solo HTTPS pubblicato | Credenziali in chiaro sul percorso |
| Telecamera non esposta | Telecamere indicizzate dai motori di ricerca |
| VLAN di management senza rotta verso Internet | Credenziali degli apparati usate dall'esterno |
| VLAN 60 separata per il wireless | Piano di controllo degli AP fuori dalla sottorete di gestione |
| SSH al posto di Telnet | Password di amministrazione in chiaro sulla rete |
| Locale tecnico chiuso a chiave | Accesso fisico alle porte del rack |

L'ultima riga non è un dettaglio: **tutte le misure sopra si aggirano con
l'accesso fisico**, e una rete che protegge il livello 2 lasciando il rack aperto
in corridoio ha un modello di minaccia incoerente.

---

## 12. Limiti dichiarati

Vale più dichiararli che farseli trovare.

**Il port forwarding espone comunque una superficie.** La porta 443 pubblica
risponde a chiunque su Internet. In una casa reale la soluzione migliore è una
**VPN**: ci si collega alla rete di casa e da lì si raggiunge il cruscotto, senza
pubblicare niente. Ho usato il port forwarding perché è ciò che chiede la traccia
e perché Packet Tracer non offre una VPN client praticabile: è un compromesso
didattico, non la scelta che farei in produzione.

**Le ACL sono stateless.** Vedi §5.5. La soluzione corretta è un firewall
stateful.

**Nessuna ridondanza.** Un solo router, un solo controller, un solo LAP. Se cade
il router cade tutto; se cade il WLC cade `MyHome` — mentre `IOT` e `GUEST`
continuano, ed è precisamente per questo che sono su AP autonomi. In un contesto
reale la ridondanza si ottiene con due WLC in coppia e due uplink, non
rinunciando al controller.

**Il registration server è un punto singolo di guasto per le automazioni.** Se è
spento, le regole non scattano. È il motivo per cui il sottosistema di
irrigazione tiene la propria logica a bordo.

**L'ambiente di Packet Tracer non è la fisica reale.** Le velocità di variazione
di temperatura, fumo e livello dell'acqua sono quelle del simulatore: servono a
dimostrare che le regole scattano, non a dimensionare un impianto.

**Verificato e non verificato.** La logica della centralina è stata provata su 9
scenari. La disponibilità in Packet Tracer 8.2.1 dei dispositivi usati è stata
controllata. Il supporto **WPA3** non è documentato con certezza nella versione
in uso: il progetto adotta WPA2, che soddisfa il requisito, e passerebbe a WPA3
dove disponibile. La registrazione **LAP → WLC** è la parte più fragile del
simulatore: il collaudo la spezza in quattro test separati proprio per isolarne
il punto di rottura.

---

## 13. Collaudo

Il progetto è stato costruito e verificato per fasi, testando ogni livello prima
di salire al successivo. Non è pedanteria: con dodici sottosistemi, collaudare
solo alla fine significa non sapere quale dei dodici è rotto.

| Livello | Verifica |
|---|---|
| Fisico | Link attivi su tutta la catena, cavi corretti per tipo di apparato |
| Collegamento | VLAN presenti, trunk attivi con la native attesa |
| Rete | Sottointerfacce `up`, ping fra VLAN adiacenti, NAT nelle traduzioni |
| DHCP | Ogni VLAN riceve indirizzo, gateway e DNS dal pool giusto |
| Politica | **Controprove**: il PC di MyHome *non* raggiunge il management, l'ospite *non* vede la casa |
| Wireless | Client su `MyHome` che riceve un indirizzo di VLAN 20 pur essendo l'AP su una porta in VLAN 60 |
| Applicativo | Registrazione dei 21 dispositivi, 10 regole con relative controprove |
| Esterno | Cruscotto raggiungibile da fuori in HTTPS; HTTP e telecamera **volutamente** irraggiungibili |

**Le verifiche che devono fallire valgono quanto quelle che devono riuscire.**
Un ping che non passa perché una ACL lo blocca è la dimostrazione che la
segmentazione funziona; senza controprove, una rete «che funziona» potrebbe
semplicemente essere una rete piatta.

---

## 14. Sintesi delle decisioni

| Decisione | Alternativa scartata | Ragione dello scarto |
|---|---|---|
| Catena ISP → DSLAM → modem → router | Cavo diretto fra i due router | Non esiste in una casa reale; la catena mostra la trasparenza al livello 3 |
| IP pubblico statico | PPPoE / IP dinamico | Il port forwarding ha bisogno di un indirizzo stabile |
| Router-on-a-stick | Un cavo per VLAN | Sei cavi su un router con due porte |
| VLAN 50 dedicata ai server | Server dentro MyHome | Aprirebbe un varco dagli IoT verso i PC personali |
| VLAN 60 dedicata al wireless | Infrastruttura wireless in VLAN 10 | Separa il piano di controllo degli AP dalla gestione degli apparati |
| Native VLAN 99 | Native VLAN 1 di default | Toglie il punto d'appoggio al VLAN hopping |
| DHCP su server + `helper-address` | DHCP sul router | Assegnazioni e prenotazioni gestite in un posto solo |
| WLC + LAP su `MyHome` | AP autonomo | È l'unica rete con roaming e policy 802.1X uniforme |
| AP autonomi su `IOT` e `GUEST` | Tutto dietro al controller | Un guasto del WLC fermerebbe la domotica |
| WPA2-Enterprise su `MyHome` | PSK ovunque | Revoca del singolo utente e tracciabilità degli accessi |
| IoT senza uscita su Internet | IoT con accesso pieno | Un dispositivo compromesso non raggiunge né la famiglia né l'esterno |
| Solo HTTPS pubblicato | HTTP + HTTPS | Credenziali in chiaro su un sistema che comanda serrature |
| Telecamera non pubblicata | Port forwarding sulla webcam | Le telecamere esposte sono indicizzate dai motori di ricerca |
| Logica di irrigazione su MCU | Condizioni sul registration server | Servono isteresi e memoria di stato, che le condizioni non hanno |
| Isteresi 30 % / 45 % | Soglia singola al 30 % | Decine di commutazioni al minuto attorno al valore critico |

---

## 15. Copertura dei requisiti

| # | Requisito della traccia | Realizzazione |
|---|---|---|
| 1 | Planimetria con ambienti, esterni, locali tecnici, posizione apparati | 9 ambienti, giardino, garage, locale tecnico, cantina; 21 dispositivi numerati |
| 2 | Server web pubblico, router ISP, router di casa | Catena `R-ISP → CLOUD-ISP → MODEM-DSL → R-HOME`, indirizzi RFC 5737 |
| 3 | ≥10 dispositivi IoT, ≥3 categorie, comportamento reattivo | 21 dispositivi, 3 categorie, 10 regole di cui 4 multi-condizione |
| 3+ | *Extra*: microcontrollore e componenti elettronici | MCU con 2 ingressi analogici e 2 uscite digitali, codice in JS e Python |
| 4 | VLAN 10/20/30/40 | Le quattro richieste + VLAN 50 Servizi + VLAN 60 Wireless + VLAN 99 native, tutte motivate |
| 5 | Tre SSID con autenticazione differenziata | Architettura ibrida WLC+LAP / AP autonomi, Enterprise + PSK |
| 6 | Web domotico, IoT server, DNS, DHCP, telecamera IP, monitoraggio energetico | 5 server in VLAN 50, webcam statica, Power Meter con telemetria via MCU |
| 7 | Instradamento verso Internet e monitoraggio da Internet | Rotta di default, NAT overload, port forwarding su 443 e 8443 |

---

## Documenti di riferimento

| File | Contenuto |
|---|---|
| [`planimetria.svg`](planimetria.svg) | Pianta annotata con la posizione di tutti gli apparati |
| [`dispositivi_e_automazioni.md`](dispositivi_e_automazioni.md) | I 21 dispositivi e le 10 regole, in dettaglio |
| [`configurazioni_cli.md`](configurazioni_cli.md) | Configurazioni complete di ogni apparato |
| [`guida_costruzione_pkt.md`](guida_costruzione_pkt.md) | Procedura di costruzione e collaudo |
| [`mcu/`](mcu/) | Codice della centralina, JavaScript e Python |
