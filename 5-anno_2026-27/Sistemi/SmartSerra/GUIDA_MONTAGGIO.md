# SmartSerra: guida di montaggio in Packet Tracer 8.2

Ordine consigliato: dispositivi → moduli → cavi → router → servizi DC → Wi-Fi → IoT → test.
Tutti gli indirizzi sono in `documentazione.txt`, le config dei router in `config/`.

---

## 1. Dispositivi da piazzare

| Nome | Modello PT | Note |
|---|---|---|
| R-SEDE, R-SERRA, R-MAG | Router-PT | + 2 moduli **PT-ROUTER-NM-1CGE** negli slot 6 e 7 (vedi §2) |
| R-DC | Router-PT | + 3 moduli **PT-ROUTER-NM-1CGE** negli slot 6, 7 e 8 |
| R-ISP | Router-PT | + 1 modulo **PT-ROUTER-NM-1CGE** nello slot 6 |
| SW-UFFICI, SW-WLAN, SW-SERRA, SW-MAG, SW-DC | 2960-24TT | nessuna config necessaria (tutto in VLAN 1) |
| PC-UFF-1, PC-UFF-2 | PC-PT | DHCP |
| PC-MAG-1, PC-MAG-2 | PC-PT | DHCP |
| SRV-DHCP-DNS | Server-PT | 10.20.1.2 |
| SRV-IOT | Server-PT | 10.20.1.3 |
| WEB-ISP | Server-PT | 198.51.100.10 |
| WLC-SEDE | WLC-2504 (Wireless Devices) | mgmt 10.20.0.130 |
| LAP-1, LAP-2 | LAP-PT | + alimentatore (vedi §6) |
| LAPTOP-WIFI | Laptop-PT | scheda WPC300N |
| SMARTPHONE-WIFI | Smartphone-PT | Wi-Fi integrato |
| AP-SERRA | AccessPoint-PT | autonomo |
| Temperature Monitor, Furnace, Window, Ceiling Fan | Home (End Devices → Home) | Wi-Fi verso AP-SERRA |
| SBC-SERRA | Components → Boards → SBC Board | |
| Photo Sensor, Potentiometer | Components → Sensors | |
| Servo, LED | Components → Actuators | |

## 2. Moduli Gigabit sui Router-PT

Il Router-PT di default ha in rame solo **FastEthernet0/0** e **FastEthernet1/0** (le altre porte sono seriali e in fibra). Le LAN usano queste porte; i collegamenti tra router vanno in Gigabit su moduli aggiunti:

Router → **Physical** → spegni l'interruttore → trascina **PT-ROUTER-NM-1CGE** negli slot vuoti 6 e 7 (su R-DC anche nell'8; su R-ISP solo nel 6) → riaccendi.
Il modulo nello slot N diventa `GigabitEthernetN/0`: quindi Gi6/0, Gi7/0, Gi8/0.

> Se metti un modulo in uno slot diverso, il nome cambia (es. Gi9/0). Controlla con `show ip interface brief` e adatta i file in `config/`.

## 3. Cavi

| Da | A | Cavo |
|---|---|---|
| R-SEDE Gi6/0 | R-SERRA Gi7/0 | **Copper Cross-Over** (router ↔ router) — dorsale L1 |
| R-SERRA Gi6/0 | R-DC Gi7/0 | Copper Cross-Over — L2 |
| R-DC Gi6/0 | R-MAG Gi7/0 | Copper Cross-Over — L3 |
| R-MAG Gi6/0 | R-SEDE Gi7/0 | Copper Cross-Over — L4 |
| R-DC Gi8/0 | R-ISP Gi6/0 | Copper Cross-Over — WAN |
| R-ISP Fa0/0 | WEB-ISP Fa0 | Copper Cross-Over (router ↔ server) |
| R-SEDE Fa0/0 | SW-UFFICI Fa0/24 | Copper Straight |
| R-SEDE Fa1/0 | SW-WLAN Fa0/24 | Copper Straight |
| R-SERRA Fa0/0 | SW-SERRA Fa0/24 | Copper Straight |
| R-MAG Fa0/0 | SW-MAG Fa0/24 | Copper Straight |
| R-DC Fa0/0 | SW-DC Fa0/24 | Copper Straight |
| PC, server, WLC, LAP, AP-SERRA | switch della propria LAN (porte Fa0/1, Fa0/2…) | Copper Straight |

> Convenzione: su ogni router dell'anello Gi6/0 va verso il router successivo in senso orario (SEDE→SERRA→DC→MAG→SEDE), Gi7/0 arriva dal precedente. Niente clock rate: è Ethernet, non seriale.

## 4. Router

Per ogni router: CLI → rispondi `no` al dialog iniziale → incolla il file `config/R-xxx.txt` corrispondente.
Controllo veloce: `show ip interface brief` (tutto up/up) e `show ip route` (le floating AD 10 NON devono comparire finché l'anello è integro).

## 5. Data Center e ISP

**SRV-DHCP-DNS** (Desktop → IP Configuration): 10.20.1.2 / 255.255.255.240, GW 10.20.1.1, DNS 10.20.1.2

- Services → **DHCP** → On. Crea i 4 pool (Add) con i valori della tabella 6.1 della documentazione. Il campo *WLC Address* solo nel pool WLAN = 10.20.0.130. Lascia stare `serverPool`.
- Services → **DNS** → On. Aggiungi i record A: `www.smartserra.local → 198.51.100.10`, `iot.smartserra.local → 10.20.1.3`.

**SRV-IOT**: 10.20.1.3 / 255.255.255.240, GW 10.20.1.1, DNS 10.20.1.2

- Services → **IoT** → On.
- Da PC-UFF-1 → Web Browser → `http://10.20.1.3` → **Sign up now** → utente `serra`, password `Serra2026`.

**WEB-ISP**: 198.51.100.10 / 255.255.255.0, GW 198.51.100.1, DNS 10.20.1.2

- Services → **HTTP** → On → edit `index.html`, ad esempio:
  ```html
  <html><body><h1>SmartSerra</h1><p>Sito ospitato presso il provider (R-ISP).</p></body></html>
  ```

**PC uffici e magazzino**: Desktop → IP Configuration → **DHCP**. Devono prendere 10.20.0.10+ (uffici) e 10.20.0.226+ (magazzino).

## 6. Wi-Fi Sede (WLC + 2 LAP)

1. **LAP-1 e LAP-2** → Physical → trascina **ACCESS_POINT_POWER_ADAPTER** nella porta di alimentazione. Collegali a SW-WLAN.
2. **WLC-SEDE** → Config → Management: IP 10.20.0.130, mask 255.255.255.192, gateway 10.20.0.129, DNS 10.20.1.2.
3. Da PC-UFF-1 → Web Browser → `http://10.20.0.130` → crea l'account admin (es. `admin` / `Cisco123`).
4. Nel wizard: System name `WLC-SEDE`, management già compilato, rete wireless **SmartSerra-Sede**, sicurezza **WPA2 Personal**, passphrase `SedeSerra2026` → Apply. Poi rientra con `https://10.20.0.130`.
5. Controlla in **WLANs**: WLAN *Enabled*, Interface = **management**, Security → Layer 2 = **WPA+WPA2**, WPA2 Policy + AES, Auth Key Mgmt = **PSK**.
6. **Controller → Interfaces → management → Primary DHCP Server = 10.20.1.2** → Apply.
7. Aspetta che i LAP si associno (la spia diventa verde; in **Wireless → All APs** compaiono LAP-1 e LAP-2). Se non succede, fai un ping a 10.20.0.130 da un PC e attendi.
8. **LAPTOP-WIFI** → Physical → spegni → togli la scheda di rete cablata → metti **WPC300N** → riaccendi. Config → Wireless0: SSID `SmartSerra-Sede`, WPA2-PSK, `SedeSerra2026`, IP DHCP. Stessa cosa sullo smartphone.
   Deve prendere un IP 10.20.0.131-190.

> Bug noto PT 8.2.x: se un client non si associa, salva il .pkt e riaprilo.

## 7. Wi-Fi Serra e dispositivi IoT

**AP-SERRA** → Config → Port 1: SSID `SmartSerra-IoT`, Channel 6, **WPA2-PSK**, pass phrase `IoTSerra2026`, Encryption AES.

Per **Temperature Monitor, Furnace, Window, Ceiling Fan**:
1. Advanced → I/O Config → Network Adapter = **PT-IOT-NM-1W** (Wi-Fi).
2. Config → Wireless0: SSID `SmartSerra-IoT`, WPA2-PSK, `IoTSerra2026`, IP **DHCP** (riceve 10.20.0.194+).
3. Config → Settings → IoT Server = **Remote Server**: 10.20.1.3, utente `serra`, password `Serra2026` → **Connect** (il pulsante diventa *Refresh*).

**Regole**: Web Browser → `http://iot.smartserra.local` → login → **Conditions** → **Add**, una regola per riga della tabella §9 della documentazione.
Per le regole con AND aggiungi una seconda condizione nello stesso editor e scegli **AND**.
Se manca l'operatore `<=` usa `< 31.1`.

> Bug noto PT 8.2.x: dopo OK la regola a volte non compare nella lista. Prima salva e riapri il .pkt. Se ancora non compare, il workaround segnalato sul forum Cisco è copiare e incollare SRV-IOT, cancellare l'originale e lavorare sulla copia (stesso IP; poi *Refresh* sui dispositivi).

**Test**: Environment (**Shift+E**) → contenitore dove stanno i dispositivi → Edit → modifica **Ambient Temperature** (es. 14 °C, 22 °C, 29 °C, 33 °C) e guarda gli attuatori. Il Furnace scalda l'ambiente, quindi lo vedrai spegnersi da solo sopra 19 °C. Tieni i dispositivi in un contenitore piccolo (una stanza), così la temperatura cambia velocemente.

## 8. SBC illuminazione

1. Collega con **IoT Custom Cable**: Photo Sensor → **A0**, Potentiometer → **A1**, Servo → **D0**, LED → **D1** della SBC.
2. SBC → **Programming** → New → nome `Illuminazione`, template **Empty - Python** → Create → apri `main.py` → incolla `iot/sbc_illuminazione.py` → **Run**.
3. Test: **ALT + click e trascina** sul potenziometro per cambiare la luce desiderata; per la luce misurata cambia **Visible Light** dall'Environment (Shift+E). La console mostra ogni cambio di stato.

Prima di cablare, passa il mouse sulle porte della SBC e controlla che ci siano A0-A3 (nella 8.2 dovrebbero esserci). Se la tua versione non le ha, usa un **MCU Board**: il codice è identico, perché l'API `gpio` è la stessa.
Se il servo gira al contrario o troppo poco, cambia `ANGOLO_APERTA` e `ANGOLO_CHIUSA` in cima al programma. Per vedere i valori accettati: Servo → Advanced → Programming.

## 9. Checklist di consegna

- [ ] Tutti i PC prendono l'IP via DHCP (uffici, magazzino, Wi-Fi, IoT)
- [ ] Ping tra tutte le LAN + server + WEB-ISP
- [ ] Browser → `http://www.smartserra.local` apre il sito dell'ISP
- [ ] `shutdown` su R-SERRA Gi6/0 (L2) → `show ip route` su R-SERRA e R-DC mostra le rotte `[10/0]` → ping ancora OK
- [ ] `no shutdown` e ripeti con L1 → osserva il loop (Simulation mode) → è quello spiegato nel §5.3 della documentazione
- [ ] I 4 dispositivi IoT risultano registrati e le 6 regole sono attive
- [ ] La SBC reagisce a potenziometro e luce
- [ ] (facoltativo) Note nel .pkt (tasto **N**, Place Note) con il riassunto VLSM e le SSID
- [ ] Salva come `SmartSerra.pkt` e consegna insieme a `documentazione.txt`
