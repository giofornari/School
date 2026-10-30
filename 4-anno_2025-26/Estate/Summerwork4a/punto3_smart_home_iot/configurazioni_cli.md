# Configurazioni complete

Tutto quello che va incollato o impostato, apparato per apparato.
Le motivazioni delle scelte stanno in [`relazione_progettuale.md`](relazione_progettuale.md).

## Piano indirizzi — riepilogo

| Rete | VLAN | Gateway | Assegnazione | Chi |
|---|---|---|---|---|
| 198.51.100.0/24 | — | .1 (R-ISP) | statica | LAN dell'ISP: web pubblico .10, DNS pubblico .53, PC esterno .20 |
| 203.0.113.0/30 | — | — | statica | Link R-ISP (.1) ↔ R-HOME (.2) |
| 192.168.10.0/24 | 10 | .1 | statica | Management: switch .2, PC admin .100 |
| 192.168.20.0/24 | 20 | .1 | DHCP .100–.199 | PC e laptop di famiglia. Interfaccia dinamica del WLC: .5 |
| 192.168.30.0/24 | 30 | .1 | DHCP .100–.199 + statici | IoT. Webcam .20, MCU .30 |
| 192.168.40.0/24 | 40 | .1 | DHCP .100–.150 | Ospiti |
| 192.168.50.0/24 | 50 | .1 | statica | IoT srv .10, web .11, DHCP .12, RADIUS .13, DNS .53 |
| 192.168.60.0/24 | 60 | .1 | WLC statico, LAP in DHCP | Infrastruttura wireless: WLC .2, LAP .100+ |
| — | 99 | — | — | Native VLAN dei trunk e porte spente |

---

# 0. La catena verso Internet

Una casa **non** si collega al router dell'operatore con un cavo di rete. La
catena reale, dal centrale fino alla presa di casa, è questa:

```
[R-ISP]──cross──[CLOUD-ISP]┈┈doppino┈┈[MODEM-DSL]──dritto──[R-HOME]──trunk──[SW-HOME]
 router          rete di               modem CPE            router di        switch
 del provider    accesso (DSLAM)       (bridge)             casa (NAT)       VLAN
   ↑ centrale        ↑ centrale           ↑ casa               ↑ casa          ↑ casa
```

| Apparato | Che cos'è davvero | Ha un IP? |
|---|---|---|
| `R-ISP` | Il router di terminazione del provider | Sì, `203.0.113.1/30` |
| `CLOUD-ISP` | La rete di accesso dell'operatore: il **DSLAM** che raccoglie i doppini del quartiere | No, è un apparato di livello 2 |
| `MODEM-DSL` | Il modem in casa tua, in **bridge**: converte il doppino in Ethernet e basta | No, è trasparente |
| `R-HOME` | Il router di casa: NAT, DHCP relay, ACL, inter-VLAN | Sì, `203.0.113.2/30` |
| `SW-HOME` | Lo switch di distribuzione | Sì, solo per gestione: `192.168.10.2` |

**Il punto che conta.** Nuvola e modem sono **trasparenti al livello 3**: non
hanno indirizzo IP e non instradano niente. Sono un cavo lungo che passa per la
centrale. È per questo che `R-ISP` e `R-HOME` restano sulla **stessa** rete
`203.0.113.0/30` pur essendo a chilometri di distanza, e infatti il piano di
indirizzamento, il NAT e il port forwarding non cambiano di una riga rispetto a
un collegamento diretto.

## 0.1 Configurazione della nuvola

È l'unico dei due che va configurato, ed è il passaggio che quasi tutti
dimenticano.

1. Trascina una **Cloud-PT** vuota, rinominala `CLOUD-ISP`.
2. Vista **Physical**: spegni l'apparato con l'interruttore.
3. Inserisci due moduli:
   - **PT-CLOUD-NM-1CFE** → porta `Ethernet0`, verso `R-ISP`
   - **PT-CLOUD-NM-1AM** → porta `Modem0`, verso il modem di casa
4. Riaccendi.
5. Tab **Config → CONNECTIONS → DSL**: nei due menu scegli `Modem0` e
   `Ethernet0`, premi **Add**. La coppia deve comparire nell'elenco.

**Perché serve.** La Cloud-PT non è uno switch: non impara i MAC e non inoltra a
broadcast. Inoltra **solo** sulle coppie di porte che le mappi esplicitamente.
Senza quella riga il pacchetto entra dal doppino e viene scartato, e il sintomo
è che `R-HOME` non pinga `R-ISP` pur avendo tutti i link verdi. È esattamente lo
stesso meccanismo del punto 4 della consegna.

## 0.2 Il modem

**Nessuna configurazione.** `DSL-Modem-PT` è un bridge trasparente: `Port 0` è
l'RJ-11 verso il doppino, `Port 1` è l'Ethernet verso il router di casa.

## 0.3 Cablaggio della catena

| Collegamento | Cavo |
|---|---|
| `R-ISP` Gi0/1 → `CLOUD-ISP` Ethernet0 | Copper **Cross-Over** |
| `CLOUD-ISP` Modem0 → `MODEM-DSL` Port 0 | **Phone** (RJ-11, tratteggiato) |
| `MODEM-DSL` Port 1 → `R-HOME` Gi0/0 | Copper **Straight-Through** |
| `R-HOME` Gi0/1 → `SW-HOME` Gi0/1 | Copper **Cross-Over** |

La regola: fra due apparati dello stesso tipo serve l'incrociato, fra tipi
diversi il dritto. La Cloud-PT si comporta come un apparato terminale, quindi
verso un router vuole il cross-over; il modem si comporta come uno switch,
quindi verso il router vuole il dritto.

## 0.4 Perché un IP pubblico statico e non PPPoE

Una linea domestica di consumo assegna un indirizzo pubblico **dinamico**, di
solito via PPPoE o DHCP. Qui ho scelto una linea con **IP statico**
(`203.0.113.2/30`), e la ragione è tecnica, non di comodità.

Il requisito 7 della traccia chiede il **monitoraggio da Internet**. Il port
forwarding pubblica un servizio su un indirizzo: se quell'indirizzo cambia a
ogni riconnessione, da fuori non sai più dove chiamare. Le soluzioni sono due:
un servizio di **DNS dinamico** che aggiorna il record ogni volta che l'IP
cambia, oppure un **IP statico**. Per un sistema che comanda serrature e
telecamere, il secondo è la scelta corretta — ed è quello che si sottoscrive
davvero quando si vuole raggiungere casa da remoto in modo affidabile.

Nota per l'orale: PPPoE sarebbe più realistico per una linea consumer, ma in
Packet Tracer la sua configurazione è limitata e fragile, e comunque non
cambierebbe nulla di quello che c'è a valle del modem.

---

# 1. R-ISP — router del provider

Modello: ISR 2911.

```
enable
configure terminal
hostname R-ISP
no ip domain-lookup
!
banner motd #Router ISP - accesso riservato#
!
interface GigabitEthernet0/0
 description --> LAN ISP (web pubblico, DNS pubblico, client esterni)
 ip address 198.51.100.1 255.255.255.0
 no shutdown
exit
!
interface GigabitEthernet0/1
 description --> CLOUD-ISP (rete di accesso, doppino del cliente)
 ip address 203.0.113.1 255.255.255.252
 no shutdown
exit
!
! Nessuna rotta statica: entrambe le reti sono direttamente connesse.
! La nuvola e il modem sono trasparenti al livello 3, quindi R-HOME e' un
! vicino direttamente connesso su 203.0.113.0/30 anche se fisicamente
! ci sono in mezzo il DSLAM e il doppino.
! Gli indirizzi privati di casa non sono e non devono essere instradabili
! su Internet: e' il NAT su R-HOME a farli sparire.
!
line console 0
 password cisco
 login
exit
enable secret cisco
service password-encryption
!
end
write memory
```

---

# 2. R-HOME — router di casa

Modello: ISR 2911. È il pezzo centrale: inter-VLAN routing, DHCP relay, ACL, NAT.

## 2.1 Base e interfacce

```
enable
configure terminal
hostname R-HOME
no ip domain-lookup
ip domain-name casa.lan
!
! ---------- WAN: verso il modem, e da li' al DSLAM e all'ISP ----------
interface GigabitEthernet0/0
 description --> MODEM-DSL --> CLOUD-ISP --> R-ISP
 ip address 203.0.113.2 255.255.255.252
 ip nat outside
 no shutdown
exit
!
! ---------- LAN: trunk verso lo switch ----------
interface GigabitEthernet0/1
 description --> SW-HOME (trunk 802.1Q)
 no ip address
 no shutdown
exit
!
interface GigabitEthernet0/1.10
 description VLAN 10 - MANAGEMENT
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
 ip nat inside
exit
!
interface GigabitEthernet0/1.20
 description VLAN 20 - MYHOME
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
 ip helper-address 192.168.50.12
 ip nat inside
exit
!
interface GigabitEthernet0/1.30
 description VLAN 30 - IOT
 encapsulation dot1Q 30
 ip address 192.168.30.1 255.255.255.0
 ip helper-address 192.168.50.12
 ip nat inside
exit
!
interface GigabitEthernet0/1.40
 description VLAN 40 - OSPITI
 encapsulation dot1Q 40
 ip address 192.168.40.1 255.255.255.0
 ip helper-address 192.168.50.12
 ip nat inside
exit
!
interface GigabitEthernet0/1.50
 description VLAN 50 - SERVIZI
 encapsulation dot1Q 50
 ip address 192.168.50.1 255.255.255.0
 ip nat inside
exit
!
interface GigabitEthernet0/1.60
 description VLAN 60 - WIRELESS (WLC + LAP, solo CAPWAP)
 encapsulation dot1Q 60
 ip address 192.168.60.1 255.255.255.0
 ip helper-address 192.168.50.12
exit
!
interface GigabitEthernet0/1.99
 description VLAN 99 - native, non instradata
 encapsulation dot1Q 99 native
exit
!
ip route 0.0.0.0 0.0.0.0 203.0.113.1
```

> `ip helper-address` non c'è su VLAN 10 e 50 perché lì gli indirizzi sono
> tutti statici: un server o uno switch che prende l'indirizzo dal DHCP è una
> pessima idea, perché se il DHCP cambia idea il servizio diventa irraggiungibile.

## 2.2 NAT

```
! Chi puo' uscire su Internet. VLAN 10 e VLAN 30 NON sono nell'elenco:
! il management non deve essere raggiungibile da fuori e gli IoT non devono
! poter chiamare casa loro.
access-list 100 remark --- Sorgenti autorizzate al NAT ---
access-list 100 permit ip 192.168.20.0 0.0.0.255 any
access-list 100 permit ip 192.168.40.0 0.0.0.255 any
access-list 100 permit ip 192.168.50.0 0.0.0.255 any
!
ip nat inside source list 100 interface GigabitEthernet0/0 overload
!
! Port forwarding: pubblica i due servizi raggiungibili da Internet.
! Solo HTTPS: su HTTP le credenziali viaggerebbero in chiaro.
ip nat inside source static tcp 192.168.50.11 443 203.0.113.2 443
ip nat inside source static tcp 192.168.50.10 443 203.0.113.2 8443
```

## 2.3 ACL fra VLAN

Le ACL si applicano **in ingresso** su ogni sottointerfaccia, cioè filtrano il
traffico che *esce* da quella VLAN.

```
! ---------- VLAN 10 MANAGEMENT: arriva ovunque, non esce su Internet ----------
ip access-list extended MGMT-IN
 permit ip any 192.168.0.0 0.0.255.255
 deny   ip any any
exit
!
! ---------- VLAN 20 MYHOME: tutto tranne management e ospiti ----------
ip access-list extended MYHOME-IN
 permit tcp any any established
 permit icmp any any echo-reply
 deny   ip any 192.168.10.0 0.0.0.255
 deny   ip any 192.168.40.0 0.0.0.255
 permit ip any any
exit
!
! ---------- VLAN 30 IOT: solo i servizi, niente Internet, niente MyHome ----------
ip access-list extended IOT-IN
 permit udp any any eq 67
 permit ip any host 192.168.50.10
 permit ip any host 192.168.50.11
 permit udp any host 192.168.50.53 eq 53
 permit tcp any any established
 permit icmp any any echo-reply
 permit ip any 192.168.30.0 0.0.0.255
 deny   ip any any
exit
!
! ---------- VLAN 40 OSPITI: solo DNS/DHCP e Internet ----------
ip access-list extended OSPITI-IN
 permit udp any any eq 67
 permit udp any host 192.168.50.53 eq 53
 permit tcp any host 192.168.50.53 eq 53
 deny   ip any 192.168.0.0 0.0.255.255
 permit ip any any
exit
!
! ---------- VLAN 50 SERVIZI ----------
ip access-list extended SERVIZI-IN
 permit tcp any any established
 permit icmp any any echo-reply
 permit udp any eq 53 any
 permit udp any eq 67 any
 permit ip any 192.168.30.0 0.0.0.255
 deny   ip any 192.168.10.0 0.0.0.255
 deny   ip any 192.168.20.0 0.0.0.255
 deny   ip any 192.168.40.0 0.0.0.255
 permit ip any any
exit
!
! ---------- VLAN 60 WIRELESS: solo verso i servizi e verso se stessa ----------
ip access-list extended WIRELESS-IN
 permit udp any any eq 67
 permit ip any 192.168.50.0 0.0.0.255
 permit ip any 192.168.60.0 0.0.0.255
 permit tcp any any established
 permit icmp any any echo-reply
 deny   ip any any
exit
!
interface GigabitEthernet0/1.10
 ip access-group MGMT-IN in
exit
interface GigabitEthernet0/1.20
 ip access-group MYHOME-IN in
exit
interface GigabitEthernet0/1.30
 ip access-group IOT-IN in
exit
interface GigabitEthernet0/1.40
 ip access-group OSPITI-IN in
exit
interface GigabitEthernet0/1.50
 ip access-group SERVIZI-IN in
exit
interface GigabitEthernet0/1.60
 ip access-group WIRELESS-IN in
exit
```

> ### Perché ci sono `established` ed `echo-reply`
>
> Le ACL di Cisco sono **stateless**: guardano un pacchetto alla volta e non
> sanno che fa parte di una conversazione già aperta. Se blocco «da VLAN 50
> verso VLAN 20», blocco anche le **risposte** del server alle richieste che
> arrivano da MyHome, e il cruscotto smette di caricare.
>
> `permit tcp any any established` lascia passare i segmenti TCP che hanno i
> flag ACK o RST, cioè quelli che appartengono a una connessione già stabilita:
> un pacchetto di apertura (solo SYN) non passa. `permit icmp any any echo-reply`
> fa lo stesso per le risposte al ping, così i test funzionano.
>
> È una soluzione approssimata: un attaccante può fabbricare un pacchetto con
> l'ACK già alzato. La soluzione vera è un **firewall stateful**, che tiene una
> tabella delle connessioni aperte — su IOS sarebbe CBAC (`ip inspect`) o la
> Zone-Based Firewall. Saperlo dire è metà del voto su questa parte.

## 2.4 Accesso sicuro agli apparati

```
username admin secret CasaAdmin2026
enable secret CasaEnable2026
service password-encryption
!
crypto key generate rsa general-keys modulus 1024
!
ip ssh version 2
line vty 0 4
 transport input ssh
 login local
 exec-timeout 5 0
exit
line console 0
 login local
 exec-timeout 5 0
exit
!
end
write memory
```

> SSH e non Telnet: Telnet manda la password in chiaro. Su una rete dove
> esiste una VLAN ospiti, mandare la password di amministrazione in chiaro
> significa regalarla a chiunque riesca a mettersi in ascolto.

---

# 3. SW-HOME — switch di distribuzione

Modello: Catalyst 2960 (24 FastEthernet + 2 GigabitEthernet).

## 3.1 VLAN e trunk

```
enable
configure terminal
hostname SW-HOME
no ip domain-lookup
!
vlan 10
 name MANAGEMENT
vlan 20
 name MYHOME
vlan 30
 name IOT
vlan 40
 name OSPITI
vlan 50
 name SERVIZI
vlan 60
 name WIRELESS
vlan 99
 name NATIVE-UNUSED
exit
!
! ---------- trunk verso il router ----------
interface GigabitEthernet0/1
 description --> R-HOME
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,30,40,50,60,99
 no shutdown
exit
```

> `switchport trunk allowed vlan` elenca solo le VLAN che servono davvero: se
> un domani qualcuno crea la VLAN 60 per sbaglio, sul trunk non passa.
> `native vlan 99` toglie il punto d'appoggio all'attacco di VLAN hopping con
> doppio tag.

## 3.2 Porte di accesso

```
! ---------- LAP gestito dal controller ----------
! Attenzione: la porta del LAP sta in VLAN 60, NON in VLAN 20.
! Su quel cavo passa solo CAPWAP: e' il WLC a immettere i client
! di MyHome nella VLAN 20, attraverso la propria interfaccia dinamica.
interface FastEthernet0/1
 description --> LAP-MYHOME (CAPWAP verso il WLC)
 switchport mode access
 switchport access vlan 60
exit
!
! ---------- Access Point autonomi ----------
interface FastEthernet0/2
 description --> AP-IOT
 switchport mode access
 switchport access vlan 30
exit
interface FastEthernet0/3
 description --> AP-GUEST
 switchport mode access
 switchport access vlan 40
exit
!
! ---------- Server, VLAN 50 ----------
interface range FastEthernet0/4-8
 description --> Server (IoT, web, DHCP, RADIUS, DNS)
 switchport mode access
 switchport access vlan 50
exit
!
! ---------- PC di famiglia, VLAN 20 ----------
interface range FastEthernet0/9-12
 description --> PC famiglia
 switchport mode access
 switchport access vlan 20
exit
!
! ---------- IoT cablati, VLAN 30 ----------
interface range FastEthernet0/13-18
 description --> IoT cablati (webcam, serratura, sprinkler, sirena...)
 switchport mode access
 switchport access vlan 30
exit
!
! ---------- Postazione di amministrazione, VLAN 10 ----------
interface FastEthernet0/19
 description --> PC amministrazione
 switchport mode access
 switchport access vlan 10
exit
!
! ---------- Porte inutilizzate: spente e parcheggiate ----------
interface range FastEthernet0/20-24
 description --> NON UTILIZZATA
 switchport mode access
 switchport access vlan 99
 shutdown
exit
!
! ---------- Wireless LAN Controller ----------
! Trunk con native VLAN 60: l'interfaccia di management del WLC deve
! essere UNTAGGED, altrimenti i LAP non si registrano. E' l'unica
! eccezione alla native 99 di tutti gli altri trunk, ed e' voluta.
interface GigabitEthernet0/2
 description --> WLC-HOME (trunk: mgmt untagged + VLAN client)
 switchport mode trunk
 switchport trunk native vlan 60
 switchport trunk allowed vlan 20,60
 no shutdown
exit
```

## 3.3 Sicurezza di porta e STP

```
! PortFast su tutte le porte di accesso: un PC o un IoT non genera topologia,
! quindi non ha senso fargli aspettare i 30 secondi di listening/learning.
! BPDU Guard spegne la porta se invece arriva una BPDU: significa che qualcuno
! ha attaccato uno switch dove non doveva.
interface range FastEthernet0/1-19
 spanning-tree portfast
 spanning-tree bpduguard enable
exit
!
! Port-security sulle porte IoT: un solo MAC per porta, imparato al volo e
! salvato in configurazione. Se qualcuno stacca la telecamera e attacca un
! portatile, la porta si spegne.
interface range FastEthernet0/13-18
 switchport port-security
 switchport port-security maximum 1
 switchport port-security mac-address sticky
 switchport port-security violation shutdown
exit
```

## 3.4 Gestione

```
interface vlan 10
 description Gestione dello switch
 ip address 192.168.10.2 255.255.255.0
 no shutdown
exit
ip default-gateway 192.168.10.1
!
ip domain-name casa.lan
username admin secret CasaAdmin2026
enable secret CasaEnable2026
service password-encryption
crypto key generate rsa general-keys modulus 1024
ip ssh version 2
line vty 0 4
 transport input ssh
 login local
exit
!
end
write memory
```

---

# 4. Wireless — architettura ibrida

`MyHome` gira su un **LAP gestito da un WLC**; `IOT` e `GUEST` su due **AP
autonomi**. Le motivazioni stanno in [`relazione_progettuale.md`](relazione_progettuale.md) §4.

## 4.1 WLC-HOME — Wireless LAN Controller

Modello: **WLC-3504** (`Network Devices → Wireless Devices`).
Porta `GigabitEthernet1` → `SW-HOME` Gi0/2, cavo **cross-over**.

Prima configurazione: apri il WLC, tab **GUI**, oppure da un browser di
PC-ADMIN vai su **`https://192.168.60.2`**. Utente `admin`, password
`CasaAdmin2026`.

> ### ⚠️ La GUI del WLC va aperta in **HTTPS**, non in HTTP
>
> `http://192.168.60.2` restituisce **«Server Reset Connection»**. Non è un
> guasto: il WLC serve la propria interfaccia web **solo in HTTPS** e non fa il
> redirect da HTTP, quindi la connessione viene resettata invece che rediretta.
>
> Scrivi per esteso **`https://192.168.60.2`**.
>
> Se anche in HTTPS non risponde, in ordine:
> 1. dopo il salvataggio il WLC **si riavvia**: aspetta un minuto buono;
> 2. **cancella e ricollega il cavo** fra WLC e switch — è un baco noto di
>    Packet Tracer dopo il riavvio del controller;
> 3. controlla che il management sia **untagged** (`VLAN Identifier 0`) e che la
>    native VLAN del trunk `Gi0/2` sia la **60**: se il management finisce su una
>    VLAN diversa dalla native del trunk, il WLC diventa irraggiungibile.


**Controller → Interfaces → management**

| Campo | Valore |
|---|---|
| IP Address | `192.168.60.2` |
| Netmask | `255.255.255.0` |
| Gateway | `192.168.60.1` |
| **VLAN Identifier** | **0 (untagged)** |
| Port Number | 1 |

> Il `0` non è una svista. L'interfaccia di management deve viaggiare **untagged**
> sulla native VLAN del trunk — che infatti su quella porta è la 60. Un management
> taggato è la causa numero uno per cui i LAP non si registrano mai.

**Controller → Interfaces → New** — interfaccia dinamica per i client:

| Campo | Valore |
|---|---|
| Interface Name | `vlan20-myhome` |
| VLAN Identifier | `20` |
| IP Address | `192.168.20.5` |
| Netmask | `255.255.255.0` |
| Gateway | `192.168.20.1` |
| Port Number | 1 |

**WLANs → Create New**

| Campo | Valore |
|---|---|
| Profile Name / SSID | `MyHome` |
| Status | Enabled |
| Interface | `vlan20-myhome` |
| Security → Layer 2 | **WPA2 Enterprise (802.1X)** |
| Security → AAA Servers | `192.168.50.13`, porta 1812, secret `RadiusCasa2026` |

## 4.2 LAP-MYHOME — access point lightweight

Modello: **LAP-PT**. Porta `Ethernet0` → `SW-HOME` Fa0/1 (access VLAN 60),
cavo **straight-through**.

**Nessuna configurazione manuale.** Il LAP prende l'indirizzo dal DHCP nel pool
`VLAN60-WIRELESS`, trova il WLC con una richiesta broadcast — sono sulla stessa
sottorete — costruisce il tunnel **CAPWAP** e scarica da lì SSID, sicurezza,
canale e potenza.

**Dove metterlo fisicamente:** a soffitto nel corridoio, che è baricentrico.
Con il controller, la posizione conta più della configurazione: quella la
riceve.

> Se dopo un minuto il LAP non compare in **Wireless → Access Points** sul WLC,
> i sospetti in ordine sono tre: la porta dello switch non è in access VLAN 60;
> il management del WLC è taggato invece che untagged; il LAP non ha preso
> l'indirizzo perché manca `ip helper-address` su `Gi0/1.60`.

## 4.3 AP autonomi — IOT e GUEST

Due `AccessPoint-PT`. Su ciascuno: **Config → Port 1 (Wireless)**.

| Parametro | AP-IOT | AP-GUEST |
|---|---|---|
| SSID | `IOT` | `GUEST` |
| Canale | 6 | 11 |
| Authentication | WPA2-PSK | WPA2-PSK |
| Pass Phrase | `IoT-Casa-2026!` | `Ospiti-2026!` |
| Encryption | AES | AES |
| Porta dello switch | Fa0/2, access **VLAN 30** | Fa0/3, access **VLAN 40** |

Questi due fanno **local switching**: mettono il frame direttamente sulla VLAN
della loro porta di accesso. È il contrario del LAP, il cui traffico viene
tunnelato fino al WLC ed è il controller a immetterlo in VLAN 20. Per questo la
porta del LAP sta in VLAN 60 e queste due no.

**Canali 1, 6, 11**: sono gli unici tre non sovrapposti nella banda 2.4 GHz.
Il canale 1 è riservato al LAP (glielo assegna il WLC), 6 e 11 ai due AP
autonomi. Metterli vicini — 1, 2, 3 — li farebbe interferire fra loro, con un
calo di prestazioni che non si spiega guardando la configurazione IP.

> Se nel menu **Authentication** del tuo Packet Tracer compare anche **WPA3**,
> usalo e scrivilo in relazione. Se non c'è, WPA2 soddisfa già il requisito
> «WPA2/WPA3». Guarda il menu prima di scriverlo.

---

# 5. Server — configurazione via GUI

Tutti in VLAN 50, indirizzi statici, gateway `192.168.50.1`, DNS `192.168.50.53`.

## 5.1 SRV-IOT — 192.168.50.10

`Services → IoT` → **On**. Poi da un PC della VLAN 20 apri
`https://192.168.50.10`, crea l'utenza di amministrazione e registra i
dispositivi. Le 10 condizioni di automazione stanno in
[`dispositivi_e_automazioni.md`](dispositivi_e_automazioni.md) §4.

## 5.2 SRV-WEB — 192.168.50.11

`Services → HTTP` → HTTP **On**, HTTPS **On**. È il cruscotto domotico,
l'unico servizio pubblicato su Internet (porta 443).

## 5.3 SRV-DHCP — 192.168.50.12

`Services → DHCP` → **On**. Tre pool, uno per VLAN servita:

| Pool | Default Gateway | DNS | Start IP | Subnet Mask | Max Users |
|---|---|---|---|---|---|
| `VLAN20-MYHOME` | 192.168.20.1 | 192.168.50.53 | 192.168.20.100 | 255.255.255.0 | 100 |
| `VLAN30-IOT` | 192.168.30.1 | 192.168.50.53 | 192.168.30.100 | 255.255.255.0 | 100 |
| `VLAN40-OSPITI` | 192.168.40.1 | 192.168.50.53 | 192.168.40.100 | 255.255.255.0 | 51 |
| `VLAN60-WIRELESS` | 192.168.60.1 | 192.168.50.53 | 192.168.60.100 | 255.255.255.0 | 20 |

Sul pool `VLAN60-WIRELESS` compila anche il campo **WLC Address** con
**`192.168.60.2`**: è l'**opzione 43 del DHCP**, cioè il modo in cui il LAP
scopre dove sta il controller. Senza, il LAP prende l'indirizzo ma resta in
*CAPWAP not connected*.

Il server riconosce da quale VLAN arriva la richiesta grazie al campo *giaddr*
scritto dal router quando fa il relay: è questo che gli fa scegliere il pool
giusto. Senza `ip helper-address` sulle sottointerfacce, nessuno di questi pool
verrebbe mai usato, perché le richieste DHCP sono broadcast e i broadcast non
attraversano un router.

## 5.4 SRV-RADIUS — 192.168.50.13

`Services → AAA` → **On**, `Service Type: RADIUS`.

**Network Configuration** (i client sono gli AP, non gli utenti):

| Client Name | Client IP | Secret | Server Type |
|---|---|---|---|
| WLC-HOME | 192.168.60.2 | `RadiusCasa2026` | Radius |

Il client RADIUS è il **controller**, non il LAP. Con l'architettura lightweight
è il WLC a parlare con il server di autenticazione per conto di tutti i suoi
access point: se domani ne aggiungi un secondo, il RADIUS non va toccato.

**User Setup** (le persone autorizzate su `MyHome`):

| Username | Password |
|---|---|
| `giordi` | `Password2026!` |
| `famiglia1` | `Password2026!` |
| `famiglia2` | `Password2026!` |

Ogni utente ha credenziali proprie: revocare l'accesso a una persona significa
cancellare una riga, non cambiare la chiave a tutta la casa.

## 5.5 SRV-DNS — 192.168.50.53

`Services → DNS` → **On**.

| Nome | Tipo | Indirizzo |
|---|---|---|
| `casa.lan` | A | 192.168.50.11 |
| `iot.casa.lan` | A | 192.168.50.10 |
| `cam.casa.lan` | A | 192.168.30.20 |
| `energia.casa.lan` | A | 192.168.30.30 |
| `www.esempio.it` | A | 198.51.100.10 |

L'ultimo record risolve il sito pubblico. In alternativa si imposta il
**DNS forwarding** verso `198.51.100.53`, che è più realistico: il DNS interno
risolve i nomi di casa e gira all'esterno tutto il resto.

## 5.6 Lato ISP

| Dispositivo | Indirizzo | Servizio |
|---|---|---|
| SRV-WEB-PUBBLICO | 198.51.100.10 | HTTP + HTTPS, gateway 198.51.100.1 |
| SRV-DNS-PUBBLICO | 198.51.100.53 | DNS, record `www.esempio.it → 198.51.100.10` |
| PC-FUORICASA | 198.51.100.20 | Il PC con cui provi il monitoraggio da Internet |

---

# 6. Riepilogo credenziali

Da mettere in relazione, così il prof può entrare e provare.

| Cosa | Utente | Password |
|---|---|---|
| Router e switch — SSH / console | `admin` | `CasaAdmin2026` |
| WLC — interfaccia web | `admin` | `CasaAdmin2026` |
| Router e switch — enable | — | `CasaEnable2026` |
| Wi-Fi `MyHome` (RADIUS) | `giordi` | `Password2026!` |
| Wi-Fi `IOT` (PSK) | — | `IoT-Casa-2026!` |
| Wi-Fi `GUEST` (PSK) | — | `Ospiti-2026!` |
| Registration server IoT | `admin` | da impostare al primo accesso |
| RADIUS shared secret | — | `RadiusCasa2026` |

In una casa vera queste password sarebbero tutte diverse e lunghe: qui sono
mnemoniche perché il progetto deve essere ispezionabile da chi lo corregge.
Vale la pena scriverlo, invece di far pensare che sia una svista.
