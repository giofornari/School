# Aggiornamenti — solo le differenze da applicare

Se hai già costruito il `.pkt` fino alla Fase 5/6, **non rifare niente**. Qui ci
sono solo i comandi da aggiungere, in ordine, per allineare quello che hai già
alle ultime due modifiche del progetto.

Tempo stimato: **10 minuti** per il Delta A, **25 minuti** per il Delta B.

---

## Cosa NON è cambiato

Prima di tutto, la parte rassicurante. Restano **identici e da non toccare**:

- tutte le VLAN 10, 20, 30, 40, 50 e 99 e i loro indirizzi;
- le sottointerfacce `Gi0/1.10/.20/.30/.40/.50` di R-HOME;
- il **NAT** (`access-list 100`) e il **port forwarding** su 443 e 8443;
- le ACL `MGMT-IN`, `MYHOME-IN`, `IOT-IN`, `OSPITI-IN`, `SERVIZI-IN`;
- la rotta di default e tutta la configurazione di `R-ISP`;
- i cinque server, il DNS, il web domotico, il registration server;
- tutti i dispositivi IoT, l'MCU e le regole di automazione;
- SSH, port-security, PortFast, BPDU Guard.

Le uniche cose toccate sono: **una VLAN in più**, **due porte dello switch**,
**una sottointerfaccia**, **un pool DHCP**, **una riga sul RADIUS**.

---

# Delta A — catena verso Internet (nuvola + modem)

## Ti serve?

Guarda il collegamento fra `R-ISP` e `R-HOME`. Se c'è **un cavo diretto** fra i
due router, ti serve. Se in mezzo hai già una nuvola e un modem DSL, salta al
Delta B.

## Cosa cambia e perché

Una casa non si collega al router dell'operatore con un cavo di rete: fra i due
ci sono la rete di accesso dell'operatore (il **DSLAM**) e il **modem** installato
dal cliente. Nuvola e modem sono trasparenti al livello 3 — non hanno IP, non
instradano — quindi **nessuna configurazione IP cambia**: `R-ISP` e `R-HOME`
restano direttamente connessi sulla stessa `203.0.113.0/30`.

## Passi

1. **Cancella il cavo** fra `R-ISP` Gi0/1 e `R-HOME` Gi0/0.

2. Trascina una **Cloud-PT** vuota, rinominala `CLOUD-ISP`. In vista
   **Physical** spegnila, inserisci **PT-CLOUD-NM-1CFE** (Ethernet) e
   **PT-CLOUD-NM-1AM** (modem RJ-11), riaccendila.

3. Trascina un **DSL-Modem-PT**, rinominalo `MODEM-DSL`. Nessuna configurazione.

4. Ricabla:

   | Da | A | Cavo |
   |---|---|---|
   | `R-ISP` Gi0/1 | `CLOUD-ISP` Ethernet0 | **Cross-Over** |
   | `CLOUD-ISP` Modem0 | `MODEM-DSL` Port 0 | **Phone** |
   | `MODEM-DSL` Port 1 | `R-HOME` Gi0/0 | **Straight-Through** |

5. `CLOUD-ISP → Config → CONNECTIONS → DSL`: scegli `Modem0` e `Ethernet0`,
   premi **Add**.

6. *(facoltativo, solo cosmetico)* aggiorna le description:

```
enable
configure terminal
interface GigabitEthernet0/0
 description --> MODEM-DSL --> CLOUD-ISP --> R-ISP
exit
end
write memory
```

## Verifica

Da `R-HOME`: `ping 203.0.113.1` → deve rispondere come prima.

Se non risponde **e i link sono verdi**, manca il passo 5: la Cloud-PT inoltra
solo sulle coppie di porte che le mappi.

---

# Delta B — wireless ibrido (WLC + LAP per MyHome)

## Cosa cambia e perché

`MyHome` passa da un AP autonomo a un **LAP gestito da un WLC-3504**. `IOT` e
`GUEST` **restano identici** sui loro AP autonomi: non li toccare.

Il motivo: `MyHome` è l'unica rete su cui si fa roaming e serve una policy 802.1X
uniforme. `IOT` e `GUEST` restano autonomi perché **devono funzionare anche se il
WLC cade** — con la domotica dietro al controller, un guasto spegnerebbe luci,
antincendio e irrigazione.

Serve una **VLAN 60** nuova per l'infrastruttura wireless: se LAP e WLC stanno
sulla stessa sottorete, il LAP trova il controller in broadcast e non serve
configurare l'opzione 43 del DHCP.

## B1 — SW-HOME: VLAN 60 e due porte

```
enable
configure terminal
!
vlan 60
 name WIRELESS
exit
!
! il trunk verso il router deve trasportare anche la 60.
! ATTENZIONE: usa "add", altrimenti sostituisci tutta la lista.
interface GigabitEthernet0/1
 switchport trunk allowed vlan add 60
exit
!
! Fa0/1 passa da VLAN 20 a VLAN 60: su quel cavo ora passa solo CAPWAP,
! non traffico dei client. E' il controller a immetterli in VLAN 20.
interface FastEthernet0/1
 description --> LAP-MYHOME (CAPWAP verso il WLC)
 switchport mode access
 switchport access vlan 60
exit
!
! Gi0/2 era spenta: diventa il trunk verso il controller.
! Native VLAN 60 perche' il management del WLC deve essere UNTAGGED.
interface GigabitEthernet0/2
 description --> WLC-HOME (trunk: mgmt untagged + VLAN client)
 switchport mode trunk
 switchport trunk native vlan 60
 switchport trunk allowed vlan 20,60
 no shutdown
exit
!
end
write memory
```

## B2 — R-HOME: sottointerfaccia e ACL

```
enable
configure terminal
!
interface GigabitEthernet0/1.60
 description VLAN 60 - WIRELESS (WLC + LAP, solo CAPWAP)
 encapsulation dot1Q 60
 ip address 192.168.60.1 255.255.255.0
 ip helper-address 192.168.50.12
exit
!
ip access-list extended WIRELESS-IN
 permit udp any any eq 67
 permit ip any 192.168.50.0 0.0.0.255
 permit ip any 192.168.60.0 0.0.0.255
 permit tcp any any established
 permit icmp any any echo-reply
 deny   ip any any
exit
!
interface GigabitEthernet0/1.60
 ip access-group WIRELESS-IN in
exit
!
end
write memory
```

> Nota: `Gi0/1.60` **non** ha `ip nat inside`, ed è voluto. L'infrastruttura
> wireless non deve uscire su Internet, quindi resta anche fuori dalla
> `access-list 100` del NAT, che non va toccata.

## B3 — Server DHCP: un pool in più

`SRV-DHCP` (192.168.50.12) → `Services → DHCP` → **Add**:

| Campo | Valore |
|---|---|
| Pool Name | `VLAN60-WIRELESS` |
| Default Gateway | `192.168.60.1` |
| DNS Server | `192.168.50.53` |
| Start IP Address | `192.168.60.100` |
| Subnet Mask | `255.255.255.0` |
| Maximum Users | `20` |
| **WLC Address** | **`192.168.60.2`** ← indispensabile, vedi sotto |

Gli altri tre pool restano com'erano.

> ### ⚠️ Il campo **WLC Address** è quello che fa il join
>
> È la traduzione che Packet Tracer dà all'**opzione 43 del DHCP**. Senza, il LAP
> prende regolarmente il suo indirizzo — `192.168.60.101` — ma **non sa dove sia
> il controller**, e resta in *CAPWAP not connected* all'infinito.
>
> Sembra un dettaglio e invece è il 90% dei casi in cui «il LAP non si registra»:
> il sintomo è ingannevole perché la rete funziona, il DHCP funziona, e sembra
> tutto a posto.
>
> Dopo aver compilato il campo, **spegni e riaccendi il LAP** (interruttore in
> vista *Physical*): deve rifare il DHCP per ricevere l'opzione.

## B4 — Server RADIUS: cambia il client

`SRV-RADIUS` (192.168.50.13) → `Services → AAA` → **Network Configuration**:

- **cancella** la riga del vecchio AP (`192.168.10.3`);
- **aggiungi**: Client Name `WLC-HOME`, Client IP `192.168.60.2`,
  Secret `RadiusCasa2026`, Server Type `Radius`.

Le utenze in **User Setup** (`giordi`, `famiglia1`, `famiglia2`) restano
identiche.

> Il client RADIUS è il **controller**, non il LAP: con l'architettura
> lightweight è il WLC a parlare col server di autenticazione per conto di tutti
> i suoi access point. Se domani aggiungi un secondo LAP, il RADIUS non si tocca.

## B5 — Apparati: togli l'AP, metti WLC e LAP

1. **Cancella** `AP-MYHOME` se l'avevi già piazzato su `Fa0/1`.
   (Non toccare `AP-IOT` su `Fa0/2` né `AP-GUEST` su `Fa0/3`.)

2. Aggiungi un **WLC-3504** (`Network Devices → Wireless Devices`), rinominalo
   `WLC-HOME`. Collega `GigabitEthernet1` a `SW-HOME` **Gi0/2**, **cross-over**.

3. Aggiungi un **LAP-PT**, rinominalo `LAP-MYHOME`. Collega `Ethernet0` a
   `SW-HOME` **Fa0/1**, cavo **dritto**. Mettilo graficamente nel corridoio.

4. Configura il WLC — **`https://192.168.60.2`** da PC-ADMIN, oppure tab **GUI**.
   Utente `admin`, password `CasaAdmin2026`.

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

   **Controller → Interfaces → New**

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
   | Layer 2 Security | **WPA2 Enterprise (802.1X)** |
   | AAA Server | `192.168.50.13`, porta 1812, secret `RadiusCasa2026` |

5. Il **LAP non va configurato**: prende l'indirizzo dal DHCP, trova il WLC in
   broadcast e scarica tutto via CAPWAP.

## Verifica del Delta B

| # | Cosa | Atteso |
|---|---|---|
| 1 | `show vlan brief` su SW-HOME | compare la VLAN 60; `Fa0/1` è in VLAN 60 |
| 2 | `show interfaces trunk` su SW-HOME | `Gi0/2` in trunk, **native 60**, allowed 20 e 60 |
| 3 | `show ip interface brief` su R-HOME | `Gi0/1.60` in `up/up` con `192.168.60.1` |
| 4 | Da PC-ADMIN: `ping 192.168.60.2` | risponde, e la GUI del WLC si apre |
| 5 | GUI del WLC → **Wireless → Access Points** | dopo ~1 minuto il LAP compare *associated* |
| 6 | Portatile su `MyHome` (utente `giordi`) | si associa e prende un IP **`192.168.20.1xx`** |

Il test 6 è quello che conta: il LAP è attaccato a una porta in **VLAN 60**, ma
il client prende un indirizzo di **VLAN 20**. È la prova che lo *switching
centralizzato* funziona — il traffico è stato tunnelato fino al WLC ed è il
controller ad averlo immesso nella VLAN giusta.

## Se qualcosa non torna

| Sintomo | Causa |
|---|---|
| **«Server Reset Connection» aprendo la GUI** | Hai usato `http://`. Il WLC serve **solo HTTPS**: scrivi `https://192.168.60.2` |
| GUI irraggiungibile anche in HTTPS dopo il salvataggio | Il WLC si riavvia: aspetta ~1 minuto, poi **cancella e ricollega il cavo** WLC↔switch (baco noto di PT) |
| GUI irraggiungibile e il management non è untagged | `VLAN Identifier` deve essere **0** e la native del trunk `Gi0/2` deve essere **60**: se non coincidono, perdi l'accesso al WLC |
| Il LAP non compare sul WLC | `Fa0/1` è rimasta in access VLAN 20 invece che 60 |
| Idem | Il management del WLC è taggato: dev'essere **VLAN Identifier 0** |
| Idem | Il LAP non ha preso l'indirizzo: manca `ip helper-address` su `Gi0/1.60` o il pool `VLAN60-WIRELESS` |
| Il client `MyHome` prende `192.168.60.x` | La WLAN non è mappata sull'interfaccia dinamica `vlan20-myhome` |
| L'autenticazione fallisce | Secret RADIUS diverso, o il client sul server AAA è rimasto il vecchio AP |
| Non pingi più il WLC dopo B1 | `switchport trunk allowed vlan` senza `add`: hai sostituito la lista invece di aggiungere |

## Piano B, se il WLC non collabora

Il WLC in Packet Tracer è permaloso. Se dopo mezz'ora il LAP non si registra,
**torna indietro in due minuti**: cancella WLC e LAP, rimetti un
`AccessPoint-PT` chiamato `AP-MYHOME` su `Fa0/1`, riporta la porta in
`switchport access vlan 20`, SSID `MyHome` con WPA2 Enterprise verso
`192.168.50.13`, e sul RADIUS rimetti il client `192.168.10.3`.

VLAN 60, sottointerfaccia e pool DHCP puoi lasciarli: non danno fastidio.

Poi dichiaralo in relazione. Una limitazione del simulatore dichiarata vale più
di un `.pkt` che non funziona.

---

## Riepilogo delle modifiche ai documenti

| Documento | Cosa è cambiato |
|---|---|
| `configurazioni_cli.md` | Nuova §0 (nuvola, modem, cablaggio, IP statico vs PPPoE); §2.1 e §2.3 con `Gi0/1.60` e `WIRELESS-IN`; §3 con VLAN 60 e le due porte; §4 riscritta in 4.1 WLC / 4.2 LAP / 4.3 AP autonomi; §5.3 pool DHCP; §5.4 client RADIUS |
| `relazione_progettuale.md` | §2 catena di accesso e IP statico; §3 VLAN 60; §4 riscritta: architettura ibrida, switching centralizzato vs locale, perché la VLAN 60; §8 e §9 aggiornate |
| `guida_costruzione_pkt.md` | Fase 1 riscritta con nuvola e modem; Fase 6 spezzata in 6a–6d; troubleshooting ampliato |
| `planimetria.svg` / `.png` | Modem nel locale tecnico, WLC nel rack, LAP nel corridoio, catena ISP nell'area operatore |

---

# Appendice — «Il LAP ha l'indirizzo ma resta *CAPWAP not connected*»

Sintomo: il LAP prende regolarmente `192.168.60.101` dal DHCP, tutti i link sono
verdi, ma non compare mai in **Wireless → Access Points** sul WLC.

Se il LAP ha l'indirizzo, allora **DHCP, `ip helper-address`, il pool e la VLAN
della porta funzionano già**. Il problema è solo la **scoperta** del controller:
il LAP ha un indirizzo ma non sa a chi bussare.

Un access point lightweight cerca il controller in tre modi, in quest'ordine:
broadcast sulla propria sottorete, DNS (`CISCO-CAPWAP-CONTROLLER.dominio`), e
**opzione 43 del DHCP**. In Packet Tracer il broadcast è inaffidabile: la strada
buona è l'opzione 43.

## Fix 1 — il campo *WLC Address* nel pool DHCP (prova questo per primo)

`SRV-DHCP` → `Services → DHCP` → pool `VLAN60-WIRELESS` → campo
**WLC Address** = `192.168.60.2` → **Save**.

È la versione semplificata dell'opzione 43 che Packet Tracer mette a
disposizione sul Server-PT.

Poi **spegni e riaccendi il LAP** dalla vista *Physical*: deve rifare il DHCP per
ricevere l'opzione. Aspetta un minuto.

## Diagnosi — se il campo non c'è o non basta

Prima di cambiare strategia, verifica che LAP e WLC si vedano davvero a
**livello 2**. Metti un PC di prova su una porta libera dello switch:

```
enable
configure terminal
interface FastEthernet0/20
 switchport mode access
 switchport access vlan 60
 no shutdown
exit
end
```

Dai al PC l'indirizzo statico `192.168.60.50/24` e prova `ping 192.168.60.2`.

| Esito | Significato |
|---|---|
| **Risponde** | LAP e WLC sono adiacenti a livello 2: il problema è solo la scoperta → passa al Fix 2 |
| **Non risponde** | Il management del WLC **non è sulla VLAN 60**: `VLAN Identifier` dev'essere `0` e la native del trunk `Gi0/2` dev'essere `60`. Ricontrolla quelli prima di andare avanti |

Finito il test, rimetti `Fa0/20` in VLAN 99 e `shutdown`.

## Fix 2 — opzione 43 servita dal router

Se il campo *WLC Address* non c'è o non basta, sposta il pool della VLAN 60 dal
server al router.

```
enable
configure terminal
!
! il router non puo' fare da server DHCP e da relay sulla stessa interfaccia:
! il relay ha la precedenza, quindi va tolto.
interface GigabitEthernet0/1.60
 no ip helper-address 192.168.50.12
exit
!
ip dhcp excluded-address 192.168.60.1 192.168.60.99
!
ip dhcp pool VLAN60-WIRELESS
 network 192.168.60.0 255.255.255.0
 default-router 192.168.60.1
 dns-server 192.168.50.53
 option 43 ip 192.168.60.2
exit
!
end
write memory
```

Poi spegni e riaccendi il LAP.

### `option 43 ip` in Packet Tracer, `option 43 hex` su IOS vero

Attenzione a non copiare la sintassi dai tutorial per apparati reali: sono
diverse, ed è una differenza che vale la pena conoscere.

Su un **IOS reale** l'opzione 43 verso un WLC si scrive in esadecimale, perché
il contenuto è un **TLV** — tipo, lunghezza, valore:

```
option 43 hex f104c0a83c02
```

| Pezzo | Valore | Significato |
|---|---|---|
| `f1` | 241 | Sotto-tipo Cisco «lista di controller WLC» |
| `04` | 4 | Lunghezza in byte: un indirizzo IPv4 |
| `c0a83c02` | 192.168.60.2 | L'indirizzo, un ottetto per byte |

In **Packet Tracer** quella forma non esiste: il `?` dopo `option 43` offre solo
`ip`. Il simulatore costruisce il TLV per conto suo, quindi si scrive
direttamente l'indirizzo:

```
option 43 ip 192.168.60.2
```

Saper spiegare che PT nasconde l'incapsulamento TLV mentre l'IOS reale te lo fa
scrivere a mano è un buon dettaglio da orale.

## Se ancora non parte

1. Aspetta davvero: in Packet Tracer il join può richiedere **1–2 minuti**.
2. Spegni e riaccendi **prima il WLC, poi il LAP**, in quest'ordine.
3. Cancella e ricollega il cavo del LAP: baco noto del simulatore.
4. Se dopo mezz'ora sei ancora fermo, applica il **piano B** più sopra: AP
   autonomo in VLAN 20. Non vale la pena bruciare una serata su un limite del
   simulatore.
