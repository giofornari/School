# Costruzione in Packet Tracer — passo passo

Ordine ragionato: ogni fase si testa prima di passare alla successiva. Costruire
tutto e poi cercare l'errore alla fine è il modo più lento di finire.

Tempo indicativo: 3–4 ore, di cui circa metà per i dispositivi IoT.

---

## Fase 0 — Preparazione

Crea un file nuovo e salvalo subito come `SmartHome_Cognome.pkt`. **Salva a ogni
fine fase**: Packet Tracer non ha annulla illimitato e perdere due ore di
configurazione IoT è un'esperienza che non vuoi fare.

Attiva la griglia (`Options → Preferences → Show Grid`) e disattiva
`Auto Cable Connection`: i cavi automatici in una rete con VLAN sono una
sorgente di errori difficili da vedere.

---

## Fase 1 — La catena verso Internet

Questa è la parte che rende la rete credibile: una casa non si attacca al router
dell'operatore con un cavo di rete. La catena è
**R-ISP → nuvola → modem → router di casa → switch**.

1. Trascina due **ISR 2911** (`Network Devices → Routers → 2911`).
   Rinominali `R-ISP` e `R-HOME`.
2. Trascina una **Cloud-PT** vuota (`Network Devices → WAN Emulation → Cloud-PT`),
   rinominala `CLOUD-ISP`. In vista **Physical** spegnila, inserisci
   **PT-CLOUD-NM-1CFE** (porta Ethernet) e **PT-CLOUD-NM-1AM** (porta modem
   RJ-11), riaccendila.
3. Trascina un **DSL-Modem-PT** (`Network Devices → WAN Emulation`), rinominalo
   `MODEM-DSL`. Non richiede nessuna configurazione.
4. Cabla la catena:

   | Da | A | Cavo |
   |---|---|---|
   | `R-ISP` Gi0/1 | `CLOUD-ISP` Ethernet0 | Cross-Over |
   | `CLOUD-ISP` Modem0 | `MODEM-DSL` Port 0 | **Phone** |
   | `MODEM-DSL` Port 1 | `R-HOME` Gi0/0 | Straight-Through |

5. **Configura la nuvola**: `CLOUD-ISP → Config → CONNECTIONS → DSL`, scegli
   `Modem0` e `Ethernet0`, premi **Add**.
6. Incolla le configurazioni di [`configurazioni_cli.md`](configurazioni_cli.md)
   §1 e §2.1.

**Test 1** — da R-HOME: `ping 203.0.113.1`. Deve rispondere.

> Se non risponde **e i link sono tutti verdi**, nel 90% dei casi manca la
> mappatura `Modem0 ↔ Ethernet0` nella nuvola. La Cloud-PT non è uno switch:
> inoltra solo sulle coppie di porte che le programmi. È lo stesso meccanismo
> del punto 4 della consegna.
>
> Se invece un link è rosso, è il cavo: cross-over verso la nuvola, dritto dal
> modem al router.

**Perché R-ISP e R-HOME sono sulla stessa /30** anche se fisicamente ci sono in
mezzo il DSLAM e il doppino: nuvola e modem sono **trasparenti al livello 3**,
non hanno indirizzo IP e non instradano. Sono un cavo lungo che passa per la
centrale. È la stessa ragione per cui il modem di casa tua non compare in un
`tracert`.

---

## Fase 2 — Lato ISP

1. Uno **switch 2960** (`SW-ISP`) collegato a `Gi0/0` di R-ISP.
2. Tre dispositivi su quello switch: `SRV-WEB-PUBBLICO`, `SRV-DNS-PUBBLICO`,
   `PC-FUORICASA`. Indirizzi in §5.6, gateway `198.51.100.1`.
3. Sul server web attiva `Services → HTTP` e modifica `index.html` con qualcosa
   di riconoscibile ("Sito pubblico di prova").

**Test 2** — da `PC-FUORICASA`: `ping 198.51.100.10`, poi apri il browser su
`http://198.51.100.10`. Deve caricare la pagina.

---

## Fase 3 — Switch di casa e VLAN

1. Uno **switch 2960** (`SW-HOME`), collegato con **cross-over** da `Gi0/1` a
   `Gi0/1` di R-HOME.
2. Incolla §3 per intero, **tranne** la parte port-security (§3.3, secondo
   blocco): attivala solo alla fine, quando gli IoT sono già collegati,
   altrimenti impari il MAC sbagliato.
3. Incolla §2.2, §2.3, §2.4 su R-HOME.

**Test 3** — su SW-HOME: `show vlan brief` (devi vedere 10, 20, 30, 40, 50, 60, 99)
e `show interfaces trunk` (Gi0/1 native 99; Gi0/2 verso il WLC native **60**).
Su R-HOME: `show ip interface brief` — le sei sottointerfacce devono essere
`up/up`.

> Errore classico: il trunk resta `down`. Su un 2960 la porta va messa
> esplicitamente in `switchport mode trunk`; se hai lasciato `dynamic auto` su
> entrambi i lati, il trunk non si forma.

---

## Fase 4 — Server

1. Cinque **Server-PT** sulle porte `Fa0/4`–`Fa0/8`, indirizzi statici da §5.
2. Configura nell'ordine: **DNS**, **DHCP**, **RADIUS**, **HTTP**, **IoT**.
   Il DNS per primo perché tutti gli altri lo useranno.
3. Un **PC-ADMIN** su `Fa0/19` (VLAN 10), indirizzo statico `192.168.10.100`.

**Test 4** — da PC-ADMIN: `ping 192.168.50.10` e `ping 192.168.50.53`.
Poi `nslookup casa.lan` (sul PC: `Desktop → Command Prompt`): deve rispondere
`192.168.50.11`.

Se il ping verso i server funziona ma `nslookup` no, il problema è nella
configurazione DNS del client, non nella rete.

---

## Fase 5 — DHCP e verifica delle ACL

1. Collega un **PC-SOGGIORNO** su `Fa0/9` (VLAN 20), impostato su **DHCP**.

**Test 5a** — il PC deve ricevere un indirizzo `192.168.20.1xx`, gateway
`192.168.20.1`, DNS `192.168.50.53`. Se resta su `169.254.x.x` significa che
manca `ip helper-address` sulla sottointerfaccia, oppure il pool sul server ha
il gateway sbagliato.

**Test 5b** — dallo stesso PC:

| Comando | Atteso | Perché |
|---|---|---|
| `ping 192.168.50.10` | ✅ risponde | MyHome può usare i servizi |
| `ping 192.168.10.2` | ❌ non risponde | MyHome non entra nel management |
| `ping 198.51.100.10` | ✅ risponde | MyHome esce su Internet (NAT) |

Se il terzo fallisce ma i primi due vanno, il problema è nel NAT: controlla
`show ip nat translations` su R-HOME mentre pinghi.

---

## Fase 6 — Wireless: controller, LAP e AP autonomi

**È la fase più delicata di tutto il progetto.** Fallo in questo ordine e testa
ogni pezzo, altrimenti alla fine non sai quale dei cinque elementi non funziona.

### 6a — I due AP autonomi (i più semplici, si fanno per primi)

1. Due **AccessPoint-PT** su `Fa0/2` e `Fa0/3`. Rinominali `AP-IOT` e `AP-GUEST`.
2. Configurali con la tabella §4.3: SSID, WPA2-PSK, canali 6 e 11.

**Test 6a** — un portatile con modulo `PT-LAPTOP-NM-1W` si associa a `GUEST`,
prende `192.168.40.1xx`, **naviga** (`ping 198.51.100.10` ✅) ma **non vede la
casa** (`ping 192.168.20.100` ❌).

Questa è la dimostrazione più efficace dell'isolamento: falla vedere al prof.

### 6b — Il controller

3. Un **WLC-3504** (`Network Devices → Wireless Devices`), rinominalo `WLC-HOME`.
   Collega `GigabitEthernet1` a `SW-HOME` **Gi0/2** con un **cross-over**.
4. Configura la porta dello switch come da §3.2: trunk, **native VLAN 60**,
   allowed 20 e 60.
5. Sul WLC (tab **GUI**, oppure browser da PC-ADMIN su `https://192.168.60.2`)
   imposta management, interfaccia dinamica e WLAN come da §4.1.

**Test 6b** — da PC-ADMIN: `ping 192.168.60.2` deve rispondere e la GUI del WLC
deve aprirsi su **`https://192.168.60.2`**.

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


### 6c — Il LAP

6. Un **LAP-PT**, rinominalo `LAP-MYHOME`. Collega `Ethernet0` a `SW-HOME`
   **Fa0/1** (access **VLAN 60**) con un cavo **dritto**.
7. Non configurare niente sul LAP: prende l'indirizzo dal DHCP, trova il WLC in
   broadcast e scarica la configurazione via CAPWAP.

**Test 6c** — dopo circa un minuto il LAP deve comparire in
**Wireless → Access Points** sulla GUI del WLC, in stato *associated*.

> Se non compare, i sospetti in ordine di probabilità:
> 1. la porta `Fa0/1` non è in **access VLAN 60** (magari è rimasta in VLAN 20);
> 2. il management del WLC è **taggato** invece che untagged;
> 3. il LAP non ha preso l'indirizzo: manca `ip helper-address` su `Gi0/1.60`,
>    oppure il pool `VLAN60-WIRELESS` non esiste sul server DHCP.

### 6d — Il client su MyHome

8. Un secondo portatile wireless: SSID `MyHome`, **WPA2 Enterprise**,
   utente `giordi`, password `Password2026!`.

**Test 6d** — deve associarsi e prendere un indirizzo `192.168.20.1xx`, cioè
**della VLAN 20**, anche se il LAP è fisicamente attaccato a una porta in
VLAN 60. È la prova che lo switching centralizzato funziona: il traffico è stato
tunnelato fino al WLC ed è il controller ad averlo immesso in VLAN 20.

Se il prof ti chiede una sola cosa sul wireless, mostragli questo.

> Se l'autenticazione fallisce, il 90% delle volte è il segreto condiviso RADIUS:
> deve essere **identico** nella WLAN del WLC e nella riga *Network Configuration*
> del server AAA. Attenzione: il client RADIUS ora è il **WLC** (`192.168.60.2`),
> non il LAP.

### Piano B, se il WLC non collabora

Il WLC in Packet Tracer è notoriamente permaloso. Se dopo mezz'ora il LAP non si
registra e la consegna incombe, **non buttare via il progetto**: sostituisci LAP
e WLC con un terzo `AccessPoint-PT` chiamato `AP-MYHOME` su `Fa0/1` in access
**VLAN 20**, con SSID `MyHome` e WPA2 Enterprise verso `192.168.50.13`. Sono due
minuti. Nella relazione dichiara la scelta e il motivo: una limitazione del
simulatore dichiarata vale più di un `.pkt` che non funziona.

---

## Fase 7 — Dispositivi IoT

Questa è la fase lunga. Conviene procedere per stanza, seguendo la
[planimetria](planimetria.svg), e registrare ogni dispositivo appena piazzato.

**Per ogni dispositivo IoT:**

1. Trascinalo dalla barra `End Devices → Home` (oppure `Smart City`,
   `Industrial`, `Power Grid`).
2. Rinominalo con un nome parlante: `Lampada-Soggiorno`, non `Light0`.
   Con 21 dispositivi, i nomi di default rendono le condizioni illeggibili.
3. **Config → Settings**:
   - `Display Name`: il nome della planimetria
   - `IoT Server`: **Remote Server**
   - `Server Address`: `192.168.50.10`
   - `User Name` / `Password`: le credenziali del registration server
4. Se è wireless: `Config → Wireless0` → SSID `IOT`, WPA2-PSK, `IoT-Casa-2026!`.
   Se è cablato: collegalo a una porta `Fa0/13`–`Fa0/18`.
5. Verifica che compaia nell'elenco del registration server prima di passare al
   successivo.

**Indirizzi statici** per i due dispositivi che devono essere raggiungibili per
nome: Webcam `192.168.30.20`, MCU `192.168.30.30`.

**Test 7** — apri `https://192.168.50.10` da PC-SOGGIORNO: devi vedere tutti i
dispositivi registrati, con lo stato aggiornato in tempo reale.

---

## Fase 8 — Sottosistema di alimentazione

Da `End Devices → Power Grid`:

1. `Solar Panel` in giardino, `Power Meter` e `Battery` in cantina.
2. Collegali con il **cavo di alimentazione** (Power), non con quello di rete:
   `Solar Panel → Power Meter → Battery`.
3. Verifica che il Power Meter mostri un valore diverso da zero. Se è a zero,
   alza la luce ambiente: `Environment` (l'icona in alto) → aumenta `Sunlight`.

---

## Fase 9 — Microcontrollore

1. `Components → Boards → MCU-PT` in giardino. Rinominalo `MCU-GIARDINO`.
2. In vista **Physical**, spegni l'MCU e inserisci negli slot:
   `Water Level Sensor` (o `Soil Moisture`), `Photo Sensor`, `Lawn Sprinkler`,
   `RGB LED`. Riaccendi.
3. **Annota l'ordine degli slot**: da lì dipendono i numeri di pin nel codice.
   Se non coincidono con quelli nei commenti, correggi le costanti in cima al
   file — è l'unico punto in cui il codice va adattato.
4. Wireless: SSID `IOT`, PSK, indirizzo statico `192.168.30.30`.
5. `Programming` → nuovo progetto → scegli il linguaggio → incolla
   [`mcu/centralina.js`](mcu/centralina.js) **oppure**
   [`mcu/centralina.py`](mcu/centralina.py) → `Run`.

**Test 9** — nella console dell'MCU deve comparire `Centralina giardino avviata`.
Poi, dal pannello `Environment`, abbassa `Water Level` sotto il 30 % e `Sunlight`
sotto il 40 %: il LED deve passare a blu e lo sprinkler deve partire. Rialza
l'umidità sopra il 45 %: si deve fermare.

> La logica è già stata verificata a tavolino su 9 scenari (isteresi, assenza di
> chattering, pausa di 6 ore, timeout, sensore guasto). Se in Packet Tracer si
> comporta diversamente, il problema sono i numeri di pin, non l'algoritmo.

---

## Fase 10 — Le condizioni di automazione

Da PC-SOGGIORNO apri `https://192.168.50.10`, entra e vai su
**Conditions → Add**. Inserisci le 10 regole di
[`dispositivi_e_automazioni.md`](dispositivi_e_automazioni.md) §4.

Due avvertenze:

Il pulsante **AND** sta sotto la prima riga di condizione. Se non lo premi
ottieni due regole separate invece di una regola con due condizioni — e le
quattro regole multi-condizione sono proprio quelle che dimostrano il requisito.

Aggiungi **una regola alla volta e provala subito** con il pannello
`Environment`. Inserirne dieci e poi capire quale non scatta è molto più lento.

**Test 10** — per ogni regola, forza la condizione dal pannello ambiente e
verifica l'attuatore:

| Regola | Come provarla | Cosa deve succedere |
|---|---|---|
| `LuceIngresso-ON` | Abbassa `Visible Light` sotto 30 %, poi clicca il Motion Detector | La lampada si accende |
| `LuceIngresso-ON` (controprova) | Alza la luce sopra 30 %, riclicca il sensore | La lampada **non** si accende |
| `Antincendio` | Alza `Smoke` sopra 30 % | Sirena, sprinkler, finestra aperta |
| `Allagamento` | Alza `Water Level` sopra 5 cm | Scarico e sirena |
| `Caldo-Condizionatore` | `Ambient Temperature` a 28 °C, finestra chiusa | AC + ventilatore al massimo |
| `Caldo-Condizionatore` (controprova) | Stessa temperatura, finestra **aperta** | AC **spento** |

Le due controprove valgono più delle prove: dimostrano che la regola guarda
davvero *entrambe* le condizioni.

---

## Fase 11 — Port forwarding e monitoraggio da Internet

È il requisito 7 e si prova per ultimo, perché ha bisogno che tutto il resto
funzioni.

**Test 11** — da `PC-FUORICASA` (198.51.100.20, che è *fuori* dalla rete di casa):

| Comando | Atteso |
|---|---|
| `https://203.0.113.2` | ✅ carica il cruscotto domotico |
| `https://203.0.113.2:8443` | ✅ carica il registration server IoT |
| `http://203.0.113.2` | ❌ non risponde (HTTP non è pubblicato: è voluto) |
| `ping 192.168.30.20` | ❌ non risponde (la telecamera non è esposta: è voluto) |

Su R-HOME, mentre provi: `show ip nat translations` deve mostrare le traduzioni
statiche e quelle dinamiche.

**Le due righe che falliscono sono parte del progetto, non un difetto.**
Scrivilo in relazione: dimostri di aver deciso *cosa non* esporre.

---

## Fase 12 — Chiusura

1. Ora attiva la **port-security** sulle porte IoT (§3.3, secondo blocco): i MAC
   corretti sono già stati imparati.
2. `write memory` su router e switch. Se non salvi, alla riapertura del file la
   configurazione c'è comunque, ma `show startup-config` sarà vuoto e il prof lo
   noterà.
3. Aggiungi in Packet Tracer delle **note testuali** (strumento `Place Note`)
   accanto a ogni gruppo di apparati, con VLAN e indirizzo. Un `.pkt` che si
   spiega da solo mentre lo si guarda vale punti sulla voce «organizzazione
   della rete».
4. Salva come `SmartHome_Cognome.pkt`.

---

## Riepilogo dei test

| # | Cosa verifica | Esito atteso |
|---|---|---|
| 1 | Catena R-ISP → nuvola → modem → R-HOME | ping ok attraverso il DSLAM |
| 2 | Web pubblico raggiungibile dalla LAN ISP | pagina caricata |
| 3 | VLAN e trunk | 6 VLAN, trunk up, 5 sottointerfacce up |
| 4 | Server e DNS | ping ok, `nslookup casa.lan` risolve |
| 5a | DHCP con relay | indirizzo del pool corretto |
| 5b | ACL da MyHome | servizi ✅, management ❌, Internet ✅ |
| 6a | AP autonomi e isolamento ospiti | guest naviga ma non vede la casa |
| 6b | WLC raggiungibile | GUI aperta su `192.168.60.2` |
| 6c | LAP registrato | compare in *Wireless → Access Points*, *associated* |
| 6d | Switching centralizzato | client su porta VLAN 60 che prende un IP **VLAN 20** |
| 7 | Registrazione IoT | 21 dispositivi nell'elenco |
| 8 | Catena di alimentazione | Power Meter con valore ≠ 0 |
| 9 | MCU | avvio, isteresi, LED di stato |
| 10 | Automazioni | 10 regole + 2 controprove |
| 11 | Port forwarding | 2 servizi raggiungibili, 2 volutamente no |

Se tutti passano, il progetto è completo rispetto ai sette requisiti della
traccia.

---

## Problemi frequenti

| Sintomo | Causa quasi certa |
|---|---|
| `R-HOME` non pinga `R-ISP` ma i link sono verdi | Manca la mappatura `Modem0 ↔ Ethernet0` nella nuvola: `CLOUD-ISP → Config → DSL → Add` |
| Link rosso verso la nuvola o il modem | Cavo sbagliato: **cross-over** router↔nuvola, **phone** nuvola↔modem, **dritto** modem↔router |
| Trunk `down` | Un lato in `dynamic auto`: metti `switchport mode trunk` esplicito |
| PC prende `169.254.x.x` | Manca `ip helper-address`, o il pool ha gateway sbagliato |
| Ping fra VLAN non va in **nessuna** direzione | Sottointerfaccia senza `encapsulation dot1Q <vlan>`, o VLAN non nella `allowed list` |
| Il cruscotto si apre ma resta vuoto | ACL: manca `permit tcp any any established` sul ritorno |
| WPA2 Enterprise non associa | Segreto RADIUS diverso fra WLC e server AAA, o client RADIUS sbagliato: dev'essere il **WLC** `192.168.60.2`, non il LAP |
| **«Server Reset Connection»** sulla GUI del WLC | Hai usato `http://`: il WLC serve **solo HTTPS**. Usa `https://192.168.60.2` |
| GUI del WLC muta dopo il salvataggio | Il controller si riavvia: aspetta ~1 min, poi cancella e ricollega il cavo WLC↔switch |
| Il LAP non compare sul WLC | Porta `Fa0/1` non in access VLAN 60, management del WLC taggato, o LAP senza indirizzo (`ip helper-address` su `Gi0/1.60`) |
| Il client `MyHome` prende un IP `192.168.60.x` | La WLAN sul WLC non è mappata sull'interfaccia dinamica `vlan20-myhome` |
| Dispositivo IoT non compare nell'elenco | `IoT Server` lasciato su *Home Gateway* invece di *Remote Server* |
| Il Power Meter legge zero | `Sunlight` a zero nel pannello Environment |
| Lo sprinkler dell'MCU non parte | Numeri di pin non corrispondenti agli slot fisici |
| Porta dello switch `err-disabled` | BPDU Guard o port-security scattata: `shutdown` + `no shutdown` per riattivarla |
