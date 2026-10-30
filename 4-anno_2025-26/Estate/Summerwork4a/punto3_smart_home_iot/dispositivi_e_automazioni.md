# Dispositivi IoT e automazioni

21 dispositivi su tre categorie, 10 regole di automazione, un sottosistema a
microcontrollore. Il numero fra parentesi rimanda al marker sulla
[planimetria](planimetria.svg).

> La traccia chiede di documentare ogni sistema descrivendone **funzione,
> vantaggi e modalità di collegamento alla rete**: sono le tre colonne delle
> tabelle qui sotto.

---

## 1. Categoria Home — 15 dispositivi

Tutti in **VLAN 30 (IOT)**, `192.168.30.0/24`, registrati sul registration
server `192.168.50.10`.

| # | Dispositivo | Tipo | Funzione | Vantaggio | Collegamento |
|---|---|---|---|---|---|
| 1 | Smart Lamp | attuatore | Illuminazione soggiorno, accensione e intensità | Si spegne da sola quando non c'è nessuno: è la voce di consumo più facile da tagliare | Wireless, SSID `IOT`, DHCP |
| 2 | Ceiling Fan | attuatore | Ventilazione soggiorno, due velocità | Consuma circa un decimo del condizionatore: sopra i 24 °C si prova prima con il ventilatore | Wireless `IOT`, DHCP |
| 3 | Window | attuatore | Apertura motorizzata della finestra | Ricambio d'aria automatico; in caso di fumo diventa una via di sfogo | Wireless `IOT`, DHCP |
| 4 | Home Speaker | attuatore | Annunci vocali e allarmi sonori | Un allarme che si sente è più utile di una notifica che nessuno guarda | Wireless `IOT`, DHCP |
| 5 | Smoke Detector | **sensore** | Rileva il fumo in angolo cottura | Innesca la catena antincendio in automatico, senza attendere una persona | Wireless `IOT`, DHCP |
| 6 | Fire Sprinkler | attuatore | Erogazione acqua a soffitto in cucina | Interviene nei primi secondi, quando l'incendio è ancora circoscritto | Cablato al rack, VLAN 30 |
| 7 | Smart Door | attuatore | Serratura elettronica dell'ingresso | Si controlla se è chiusa da remoto e si può aprire senza chiavi | Cablato, VLAN 30, IP statico |
| 8 | Motion Detector | **sensore** | Presenza in ingresso e corridoio | Input per luci, telecamera e allarme: un solo sensore, tre usi | Wireless `IOT`, DHCP |
| 9 | **Webcam** | **sensore** | Telecamera IP dell'ingresso | Verifica visiva di cosa ha fatto scattare l'allarme | Cablato, VLAN 30, **IP statico 192.168.30.20** |
| 10 | Water Level Monitor | **sensore** | Livello acqua a pavimento in lavanderia | Un allagamento scoperto dopo ore costa quanto rifare un pavimento | Cablato, VLAN 30 |
| 11 | Drain Actuator | attuatore | Scarico rapido del pavimento | Agisce mentre l'allarme suona, non dopo | Cablato, VLAN 30 |
| 12 | Air Conditioner | attuatore | Climatizzazione camera matrimoniale | Si accende solo sopra soglia e solo se la finestra è chiusa | Cablato, VLAN 30 |
| 13 | Humiture Monitor | **sensore** | Temperatura e umidità in camera | Input per condizionatore, termosifone e ventilatore | Wireless `IOT`, DHCP |
| 14 | Furnace | attuatore | Riscaldamento camera singola / studio | Riscalda solo la stanza usata, non tutta la casa | Cablato, VLAN 30 |
| 15 | Siren | attuatore | Sirena di allarme, corridoio | Segnalazione acustica comune a incendio, allagamento e intrusione | Cablato, VLAN 30 |

**Sensori (input): 5** — 5, 8, 9, 10, 13.
**Attuatori (output): 10** — 1, 2, 3, 4, 6, 7, 11, 12, 14, 15.

---

## 2. Categoria Power Grid — 3 dispositivi

In Packet Tracer stanno sotto **End Devices → Power Grid**. Si collegano fra
loro con i **cavi di alimentazione**, non con cavi di rete: il pannello alimenta
il contatore, il contatore alimenta la batteria.

| # | Dispositivo | Funzione | Vantaggio | Collegamento |
|---|---|---|---|---|
| 16 | Solar Panel | Genera energia dalla luce del giardino esposto a sud | Alimenta i carichi domotici a costo zero nelle ore diurne | Cavo di alimentazione verso il Power Meter |
| 20 | Battery | Accumulo in cantina | Sposta l'energia prodotta di giorno sui consumi serali, quando la produzione è nulla | Alimentata dal Power Meter |
| 21 | **Power Meter** | Misura la potenza che transita fra pannello e batteria | È il **sistema di monitoraggio energetico** richiesto dalla traccia: senza misura non si può ottimizzare niente | Cavo di alimentazione in ingresso e in uscita; la telemetria arriva al server tramite l'MCU |

**Catena di alimentazione:**

```
[Solar Panel] ══ cavo alimentazione ══> [Power Meter] ══> [Battery] ══> carichi IoT
      (16)                                    (21)            (20)
                                               │
                                    lettura analogica
                                               ▼
                                          [MCU-PT] (19) ──rete──> registration server
```

Il Power Meter da solo mostra il valore a schermo ma non lo pubblica in rete: è
l'MCU a leggerlo e a renderlo disponibile al cruscotto. È il motivo per cui i
due sottosistemi sono progettati insieme.

### Collegare più batterie

I dispositivi Power Grid si collegano con l'**IoT Custom Cable**, non con un cavo
di rete, e ognuno ha pochissime porte: tipicamente un ingresso e un'uscita. Per
metterne più di una ci sono due strade.

**In cascata.** L'uscita della prima batteria entra nell'ingresso della seconda:

```
[Solar Panel] → [Power Meter] → [Battery 1] → [Battery 2] → carichi
```

È la più semplice e non richiede altri apparati. Controlla in vista **Physical**
quante porte ha davvero la tua Battery: se ne ha una sola, questa strada è chiusa.

**Rami separati.** Un pannello e un contatore per ogni batteria, in parallelo:

```
[Solar Panel 1] → [Power Meter 1] → [Battery 1]
[Solar Panel 2] → [Power Meter 2] → [Battery 2]
```

Più apparati, ma ogni ramo è misurato separatamente — e in un impianto vero è
proprio così che si fa quando si vuole sapere quanto rende ciascuna stringa di
pannelli.

### Cosa dire all'orale: serie o parallelo?

Attenzione, perché qui c'è la domanda-trappola. **Packet Tracer non simula né
tensione né corrente**: il suo modello di alimentazione è binario, un carico è
alimentato o non lo è. Quindi *dentro il simulatore* la differenza fra serie e
parallelo non esiste. Dirlo è un punto a favore, non una debolezza.

In un impianto reale invece:

| Collegamento | Tensione | Capacità (Ah) | Quando si usa |
|---|---|---|---|
| **Parallelo** | resta quella di una batteria | **si somma** | Si vuole più autonomia a parità di tensione. Se una si guasta, le altre continuano |
| **Serie** | **si somma** | resta quella di una batteria | L'inverter richiede una tensione più alta: quattro batterie da 12 V per farne una da 48 V |

In una casa con accumulo si usa quasi sempre il **parallelo**, o combinazioni
serie-parallelo per avere insieme la tensione richiesta dall'inverter e
l'autonomia voluta.

**Il vincolo che quasi nessuno cita:** le batterie in parallelo devono essere
**identiche** — stesso modello, stessa capacità, stesso stato di carica e
possibilmente stesso lotto. Se non lo sono, quella più carica si scarica dentro
quella più scarica invece di alimentare il carico, e a lungo andare le rovina
entrambe. È il motivo per cui non si aggiunge una batteria nuova a un banco
vecchio.

---

## 3. Categoria Industrial / esterni — 3 dispositivi

| # | Dispositivo | Funzione | Vantaggio | Collegamento |
|---|---|---|---|---|
| 17 | Photo Sensor | Misura la luce ambiente in giardino | Distingue giorno e notte meglio di un orologio: funziona anche con il cielo coperto e non va aggiornato con l'ora legale | Ingresso analogico dell'MCU |
| 18 | Lawn Sprinkler | Irrigazione del giardino | Il prato e le piante sopravvivono alle vacanze; irriga solo quando serve davvero | Uscita digitale dell'MCU (relè) |
| 19 | **MCU-PT** | Centralina: irrigazione + telemetria energetica | Logica a bordo, funziona anche se la rete o il server sono giù | Wireless `IOT`, **IP statico 192.168.30.30** |

---

## 4. Le 10 regole di automazione

Si scrivono nel registration server: si apre `https://192.168.50.10` da un PC
della VLAN 20, si entra con l'utenza di amministrazione e si va in
**Conditions → Add**.

| # | Nome | Condizione (input) | Azione (output) | Perché |
|---|---|---|---|---|
| 1 | `LuceIngresso-ON` | Motion Detector = On **AND** Photo Sensor < 30 % | Smart Lamp On, luminosità 80 % | Due condizioni insieme: la luce non si accende di giorno. È l'esempio da mostrare al prof per «comportamento che si adatta allo stato degli input» |
| 2 | `LuceIngresso-OFF` | Motion Detector = Off per 120 s | Smart Lamp Off | Il ritardo evita che la luce si spenga mentre sei fermo a togliere le scarpe |
| 3 | `Antincendio` | Smoke Detector > 30 % | Siren On, Fire Sprinkler On, Window Open, Speaker "Allarme fumo" | Un sensore, quattro attuatori: sfogo dei fumi, spegnimento, allarme sonoro |
| 4 | `Allagamento` | Water Level > 5 cm | Drain Actuator On, Siren On, Speaker "Allagamento lavanderia" | Interviene e avvisa insieme |
| 5 | `Allagamento-Stop` | Water Level < 1 cm | Drain Actuator Off, Siren Off | Rientro automatico: nessuno deve ricordarsi di chiudere lo scarico |
| 6 | `Caldo-Ventilatore` | Temperature > 24 °C **AND** < 27 °C | Ceiling Fan On (Low) | Si prova prima con il ventilatore: consuma molto meno |
| 7 | `Caldo-Condizionatore` | Temperature ≥ 27 °C **AND** Window = Closed | Air Conditioner On, Ceiling Fan On (High) | Il condizionatore parte solo se la finestra è chiusa: raffreddare la strada è inutile |
| 8 | `Freddo` | Temperature < 19 °C | Furnace On | Soglia di comfort minima |
| 9 | `Umidità` | Humidity > 70 % | Ceiling Fan On (High), Window Open | Contro la condensa e la muffa |
| 10 | `Intrusione` | Motion Detector = On **AND** Smart Door = Locked **AND** modalità "fuori casa" | Webcam On, Siren On, notifica al cruscotto | Movimento in casa con la porta chiusa e nessuno presente: qualcosa non torna |

Regole con **due o più condizioni**: 1, 6, 7, 10. Sono quelle che dimostrano
davvero il requisito, perché una regola a condizione singola è poco più di un
interruttore.

### Come si scrive una condizione in Packet Tracer

```
Name:      LuceIngresso-ON
Enabled:   ✔
Condition: Motion Detector  |  On   |  is   |  true
      AND  Photo Sensor     |  Level|  <    |  30
Action:    Set  Smart Lamp  |  Status  |  to  |  On
           Set  Smart Lamp  |  Level   |  to  |  80
```

Il pulsante `AND` sta sotto la prima riga di condizione: se non lo premi ottieni
due regole separate, non una regola con due condizioni. È l'errore più comune.

---

## 5. Il sottosistema a microcontrollore

**MCU-PT** in giardino, con quattro componenti discreti.

| Porta | Componente | Direzione | Cosa fa |
|---|---|---|---|
| `A0` (analog) | Soil Moisture / Water Level Sensor | input | Umidità del terreno nei vasi, 0–100 % |
| `A1` (analog) | Photo Sensor (17) | input | Luce ambiente, 0–100 % |
| `D0` (digital) | Relè → Lawn Sprinkler (18) | output | Apre l'elettrovalvola |
| `D1` (digital) | RGB LED | output | Stato: verde ok, blu irrigazione, rosso guasto |

### La logica

Irriga **solo** se tutte e tre sono vere: terreno sotto il 30 %, luce sotto il
40 % (mattina presto o sera), e non ha già irrigato nelle ultime sei ore.

Le tre condizioni servono a tre cose diverse. L'umidità è il motivo per irrigare.
La luce bassa evita di irrigare nelle ore calde, quando l'acqua evapora prima di
essere assorbita e le gocce sulle foglie fanno da lente. Il tempo minimo fra due
irrigazioni evita che un sensore sporco o bagnato faccia partire il ciclo in
continuazione.

### L'isteresi

Il ciclo si ferma quando l'umidità supera il **45 %**, non il 30 % che l'ha fatto
partire. Senza questo scarto, appena l'umidità tocca il 30 % il relè si
spegnerebbe, il valore ricadrebbe sotto e si riaccenderebbe: decine di
commutazioni al minuto, che bruciano il relè e stressano l'elettrovalvola.

**È il punto tecnico più forte del sottosistema**, e vale la pena saperlo
spiegare: è anche il motivo per cui questa logica non si può scrivere come
condizione sul registration server, che è booleana e senza memoria fra
un'esecuzione e l'altra.

Codice commentato in [`mcu/centralina.js`](mcu/centralina.js) e
[`mcu/centralina.py`](mcu/centralina.py) — due versioni equivalenti, si carica
quella che preferisci.

---

## 6. Riepilogo per la valutazione

| Requisito della traccia | Come è soddisfatto |
|---|---|
| Almeno 10 dispositivi IoT | **21** |
| Almeno 3 categorie | **3**: Home (15), Power Grid (3), Industrial/esterni (3) |
| Comportamento che si adatta agli input | 10 regole, di cui **4 con più condizioni** in AND |
| Documentare funzione, vantaggi, collegamento | Tabelle §1–§3 |
| Telecamera IP | Webcam (9), `192.168.30.20` |
| Sistema di monitoraggio energetico | Power Meter (21) + telemetria via MCU (19) |
| **Punteggio extra**: microcontrollore e componenti | MCU-PT con 2 ingressi analogici e 2 uscite digitali, codice in JS e Python |
