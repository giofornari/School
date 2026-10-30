# Punto 3 — Progetto CPT: Domotica e IoT

Villa su un piano con garage e giardino, rete segmentata in 6 VLAN, 3 SSID su
architettura wireless ibrida (WLC + LAP e AP autonomi), 21 dispositivi IoT,
accesso e monitoraggio da Internet, sottosistema a microcontrollore.

## I file

| File | A cosa serve |
|---|---|
| **[`note_pkt.md`](note_pkt.md)** | **La documentazione da mettere dentro il `.pkt`**: 17 note già impaginate, con la mappa di dove posarle |
| [`Relazione_progettuale_CPT_Domotica_IoT.pdf`](Relazione_progettuale_CPT_Domotica_IoT.pdf) | Le stesse motivazioni in forma di relazione A4, se serve un documento a parte |
| [`relazione_progettuale.md`](relazione_progettuale.md) | Sorgente della relazione: si modifica qui, poi `python3 genera_pdf.py` |
| [`genera_pdf.py`](genera_pdf.py) | Rigenera il PDF dal Markdown |
| [`planimetria.svg`](planimetria.svg) · [`.png`](planimetria.png) | Pianta annotata con i 21 marker numerati e la legenda — va nella relazione |
| [`sfondo/`](sfondo/) | La stessa pianta **senza marker**, pronta da caricare come sfondo del `.pkt`, più lo script che rigenera tutte le varianti |
| [`dispositivi_e_automazioni.md`](dispositivi_e_automazioni.md) | I 21 dispositivi con funzione, vantaggi e collegamento; le 10 regole di automazione |
| [`configurazioni_cli.md`](configurazioni_cli.md) | Configurazioni complete di router, switch, AP e server |
| [`guida_costruzione_pkt.md`](guida_costruzione_pkt.md) | Le 12 fasi di costruzione in Packet Tracer, ognuna con il suo test |
| [`AGGIORNAMENTI.md`](AGGIORNAMENTI.md) | **Se hai già iniziato a costruire il `.pkt`**: solo i comandi delta da applicare, senza rifare niente |
| [`mcu/centralina.js`](mcu/centralina.js) · [`mcu/centralina.py`](mcu/centralina.py) | Codice della centralina a microcontrollore, due versioni equivalenti |

## Da consegnare

La traccia chiede **il file `.pkt`**. Questi documenti sono il progetto e la
relazione: il `.pkt` va costruito seguendo `guida_costruzione_pkt.md` — circa
3–4 ore, di cui metà per i dispositivi IoT.

## Copertura dei requisiti

| # | Requisito | Come è soddisfatto |
|---|---|---|
| 1 | Planimetria con stanze, esterni, locali tecnici, posizione apparati | `planimetria.svg`: 9 ambienti, giardino, garage, locale tecnico + cantina, 21 dispositivi numerati |
| 2 | Server web pubblico, router ISP, router di casa | Catena realistica `R-ISP → CLOUD-ISP (DSLAM) → MODEM-DSL → R-HOME → SW-HOME`, indirizzi pubblici RFC 5737 |
| 3 | ≥10 dispositivi IoT, ≥3 categorie, comportamento reattivo agli input | **21** dispositivi, **3** categorie, **10** regole di cui **4 multi-condizione** |
| 3+ | *Extra*: microcontrollore e componenti elettronici | `MCU-PT` con 2 ingressi analogici e 2 uscite digitali, codice in JS e Python |
| 4 | VLAN 10/20/30/40 | Le quattro richieste **+ VLAN 50 Servizi**, **VLAN 60 Wireless** e **VLAN 99** native inutilizzata, tutte motivate |
| 5 | Tre SSID con autenticazione differenziata | Architettura ibrida: `MyHome` su **LAP + WLC-3504** con WPA2-Enterprise/RADIUS, `IOT` e `GUEST` su **AP autonomi** con WPA2-PSK |
| 6 | Web domotico, IoT server, DNS, DHCP, telecamera IP, monitoraggio energetico | 5 server in VLAN 50 + Webcam `192.168.30.20` + Power Meter con telemetria via MCU |
| 7 | Instradamento per Internet e monitoraggio da Internet | Rotta di default + NAT overload + port forwarding su 443 e 8443 |

## I tre punti forti da citare all'orale

**La VLAN IoT non ha uscita su Internet.** È la scelta di sicurezza più
importante del progetto: un dispositivo domotico compromesso — firmware vecchio,
password di default — non raggiunge né i PC di famiglia né l'esterno, quindi non
può essere arruolato in una botnet. Le automazioni continuano a funzionare
perché avvengono tutte fra VLAN 30 e VLAN 50.

**Le ACL sono stateless, e si vede.** Nelle configurazioni compaiono
`permit tcp any any established` e `permit icmp any any echo-reply`: servono a
far tornare indietro le risposte, perché un'ACL guarda un pacchetto alla volta e
non sa che fa parte di una conversazione già aperta. La soluzione vera sarebbe
un firewall stateful (CBAC o Zone-Based Firewall). Saperlo dire vale metà del
voto su quella parte.

**Il wireless è ibrido, e non per caso.** `MyHome` gira su un LAP gestito dal
WLC perché è l'unica rete su cui si fa roaming e serve una policy 802.1X
uniforme. `IOT` e `GUEST` restano su AP autonomi perché **devono continuare a
funzionare se il controller cade**: con la domotica dietro al WLC, un guasto del
controller spegnerebbe luci, allarme antincendio e irrigazione. È lo stesso
principio per cui la centralina tiene la logica sul microcontrollore.
Conseguenza tecnica da citare: la porta di switch del LAP sta in **VLAN 60**, non
in VLAN 20, perché con CAPWAP è il controller a immettere i client nella loro
VLAN (*central switching*), mentre gli AP autonomi fanno *local switching*.

**L'isteresi della centralina.** Il ciclo di irrigazione parte sotto il 30 % di
umidità e si ferma sopra il 45 %, non sopra il 30 %. Con una soglia sola il relè
commuterebbe decine di volte al minuto attorno al valore critico. È anche il
motivo per cui quella logica non si può scrivere come condizione sul
registration server, che è booleana e senza memoria fra un'esecuzione e l'altra.

## Cosa è stato verificato e cosa no

**Verificato:** la logica della centralina, provata su 9 scenari (isteresi,
assenza di commutazioni ripetute, pausa minima fra due cicli, timeout di
sicurezza, sensore guasto) — tutti superati. La disponibilità in Packet Tracer
8.2.1 dei dispositivi usati, incluso il `Power Meter` sotto
`End Devices → Power Grid`, e del servizio AAA/RADIUS sul `Server-PT`.

**Non verificato in Packet Tracer:** la registrazione **LAP → WLC**. È la parte
notoriamente più permalosa del simulatore, per questo la guida la spezza in
quattro test separati (6a–6d) e prevede un piano B: sostituire LAP e WLC con un
terzo AP autonomo in VLAN 20 richiede due minuti, e una limitazione del
simulatore dichiarata in relazione vale più di un `.pkt` che non funziona.

**Non verificato:** il supporto **WPA3**. Nella documentazione di Packet Tracer
8.2 sono documentati con certezza WEP, WPA-PSK, WPA2-PSK e WPA/WPA2 Enterprise.
Guarda il menu `Authentication` del tuo AP: se WPA3 c'è, usalo e citalo;
altrimenti WPA2 soddisfa già il requisito «WPA2/WPA3». Non darlo per scontato
nella relazione senza averlo visto.
