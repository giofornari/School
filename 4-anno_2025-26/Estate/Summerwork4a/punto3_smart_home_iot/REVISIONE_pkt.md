# Revisione di `Fornari-SmartHomeIoT1.pkt`

Analisi automatica del file salvato in XML (Packet Tracer 8.2.1.0118).
65 dispositivi, 44 collegamenti, 4 apparati di rete con configurazione IOS.

---

## Prima le cose che funzionano

Vale la pena dirle, perché sono la parte difficile ed è tutta a posto.

| Cosa | Stato |
|---|---|
| Catena `R-ISP → Cloud0 → DSL Modem0 → R-HOME` | ✅ esattamente come da progetto |
| NAT overload + port forwarding 443 e 8443 | ✅ presenti e corretti |
| Rotta di default verso `203.0.113.1` | ✅ |
| Sei sottointerfacce `Gi0/1.10/.20/.30/.40/.50/.60` + `.99` native | ✅ con `ip helper-address` dove serve |
| Trunk `Gi0/1`: native 99, allowed 10,20,30,40,50,60,99 | ✅ |
| Trunk `Gi0/2` verso il WLC: native 60, allowed 20,60 | ✅ |
| WLC: management `192.168.60.2` **+ interfaccia dinamica `192.168.20.5`** | ✅ create entrambe |
| **I due LAP hanno fatto il join** | ✅ lease `cisco-…-Gig0` su `.100` e `.109` — CAPWAP risolto |
| Pool DHCP VLAN 20/30/40/60, con **WLC Address** sul pool 60 | ✅ |
| Servizio AAA/RADIUS attivo | ✅ |
| HTTPS attivo su `IooT`, `-WEB`, `OUT-WEB` | ✅ |
| Registration server con **18 dispositivi registrati** e 5 regole attive | ✅ requisito «≥10 dispositivi» superato |

---

## 🔴 Bloccanti — rompono un requisito della traccia

### 1. Il lato ISP è su una sottorete sbagliata

| Dispositivo | Indirizzo attuale | Dovrebbe essere |
|---|---|---|
| `R-ISP` Gi0/0 | `198.51.100.1/24` | ✅ giusto |
| `OUT-WEB` | `192.51.100.10` | `198.51.100.10` |
| `OUT-DNS` | `192.51.100.53` | `198.51.100.53` |
| `PC0` | `192.51.100.20` | `198.51.100.20` |
| gateway dei tre | `192.51.100.1` | `198.51.100.1` |

**`192`.51.100 invece di `198`.51.100.** Un carattere, e i tre dispositivi
esterni non raggiungono il proprio router: sono su una rete che non esiste.

Conseguenza diretta: **il requisito 2** (server web pubblico raggiungibile) e il
**requisito 7** (monitoraggio da Internet) non sono dimostrabili. `PC-FUORICASA`
non può aprire `https://203.0.113.2`, che è il test finale del progetto.

Correggi i tre host, non il router: `198.51.100.0/24` è il blocco riservato alla
documentazione dalla RFC 5737, ed è quello giusto da citare in relazione.

### 2. I client Wi-Fi di casa finiscono in VLAN 60 invece che in VLAN 20

Tutti i dispositivi personali — `giordi's phone`, `archlinux`, `T10 di giulia`,
`PC-CASA`, `telefono di mamma`, `telefono di pelatons` — hanno **gateway
`192.168.60.1`**, e il pool VLAN 60 ha assegnato `.101`–`.110` a MAC che non
sono quelli dei LAP.

**Causa:** la WLAN sul WLC (profilo `main`) è mappata sull'interfaccia
**management** invece che sull'interfaccia dinamica `vlan20-myhome`, che pure
esiste ed è configurata correttamente su `192.168.20.5`.

**Perché è grave e non estetico.** La VLAN 60 esiste per isolare il piano di
controllo del wireless. Con i telefoni di famiglia dentro, quella separazione
non esiste più, e soprattutto **salta la dimostrazione dello switching
centralizzato** — che era il punto forte da mostrare al prof: *il LAP è su una
porta in VLAN 60 ma il client prende un indirizzo di VLAN 20*.

**Fix:** WLC → `WLANs` → profilo `main` → campo **Interface** → seleziona
`vlan20-myhome`. Poi disassocia e riassocia un client.

### 3. Nessuna ACL applicata: la segmentazione non c'è

Su `R-HOME` c'è **solo** `access-list 100` (quella del NAT). Mancano tutte e sei
le ACL di politica: `MGMT-IN`, `MYHOME-IN`, `IOT-IN`, `OSPITI-IN`, `SERVIZI-IN`,
`WIRELESS-IN`, e nessun `ip access-group` su nessuna sottointerfaccia.

Le VLAN esistono, quindi il **requisito 4** è formalmente soddisfatto. Ma il
traffico fra VLAN passa tutto: **l'ospite `Robby` in VLAN 40 può raggiungere i
PC di famiglia, i server e la telecamera.** Segmentare senza politica è come
mettere le porte in casa e lasciarle tutte aperte.

È anche il primo dei tre punti forti che avevi da raccontare all'orale — quello
sulla VLAN IoT senza uscita su Internet. Adesso non è vero.

Incolla la §2.3 di `configurazioni_cli.md`. Sono cinque minuti.

### 4. Manca tutta la categoria Power Grid

Nel file non c'è **nessun** `Solar Panel`, **nessuna** `Battery`, **nessun**
`Power Meter`. C'è solo un `Power Distribution Device0` che non è collegato a
niente.

Due requisiti a rischio:

- **Requisito 6** — «sistema di monitoraggio energetico»: non esiste.
- **Requisito 3** — «almeno 3 categorie differenti»: adesso i dispositivi sono
  quasi tutti categoria *Home* più qualche *Thing* custom. Difficile sostenere
  che siano tre.

È la lacuna che costa più punti in rapporto al tempo che serve per chiuderla:
tre dispositivi, due cavi di alimentazione, dieci minuti.

### 5. Lo switch non è raggiungibile per la gestione

`SW-HOME` ha `ip default-gateway 192.168.10.1` ma **nessuna `interface Vlan10`
con indirizzo IP**. Senza SVI lo switch non risponde a ping né a SSH, quindi la
VLAN 10 Management non gestisce niente e la configurazione SSH che hai messo è
inutilizzabile.

```
enable
configure terminal
interface Vlan10
 description Gestione dello switch
 ip address 192.168.10.2 255.255.255.0
 no shutdown
end
write memory
```

---

## 🟠 Importanti — da sistemare prima di consegnare

### 6. L'SSID si chiama `Vodafone-E69504958`

La rete principale non si chiama `MyHome` ma `Vodafone-E69504958`, e il profilo
WLAN si chiama `main`. In una relazione scolastica il nome del router di casa
sembra esattamente quello che è: un copia-incolla. Rinomina l'SSID in `MyHome` e
il profilo in `WLAN-MyHome`, oppure allinea la relazione — ma la prima è meglio.

### 7. Dodici dispositivi non sono in rete

Questi hanno indirizzo **APIPA `169.254.x.x`**, cioè hanno chiesto il DHCP e non
hanno ricevuto risposta:

`IoT2`, `IoT3`, `IoT2(1)`, `IoT2(2)`, `IoT2(3)`, `IoT2(4)`, `EXTRA`, `EXTRA2`,
`CLIMA`, `CLIMA2`, `CRITICAL`, `CRITICAL2`, più `iphone di Fonta`.

Sono tutti sull'SSID **`HomeGateway`**, che è il default di Packet Tracer, non su
`IOT`. Non essendo associati a `AP-IoT`, non raggiungono né il DHCP né il
registration server — e con loro non lo raggiunge tutto quello che ci è appeso
dietro (sirena, finestre, termostati, condizionatore).

Portali sull'SSID `IOT` con la PSK, oppure — se li usi solo come raggruppamento
logico — toglili, perché un dispositivo con APIPA in un progetto valutato sembra
un errore anche quando non lo è.

### 8. Una sola regola su cinque ha più condizioni

Le cinque regole sono attive e funzionano, ma la traccia chiede che *«il
comportamento di parte dei dispositivi si adatti allo stato dei dispositivi di
input»*, e una regola a condizione singola è poco più di un interruttore.

| Regola | Condizioni |
|---|---|
| `too hot` | 1 |
| `too humidity` | 1 |
| `uff ospiti fumatrici` | 1 |
| `bad trap` | 1 |
| `forse salviamo l'ambiente` | **2 in AND** ✅ |

Aggiungine due o tre con due condizioni in `AND` — per esempio *movimento
rilevato* **e** *luce ambiente sotto soglia* → accendi la luce. Sono quelle che
dimostrano davvero il requisito, e ne hai già gli ingressi in casa.

### 9. Manca la sicurezza di porta sullo switch

Nessuna `port-security`, nessun `spanning-tree portfast`, nessun `bpduguard`.
Erano la §3.3 di `configurazioni_cli.md` ed è la parte che rende difendibile la
voce «scelte di sicurezza» della relazione.

Le porte inutilizzate: `Fa0/21`–`Fa0/23` sono in VLAN 99 e spente ✅, ma
`Fa0/20` è ancora in VLAN 30 e accesa.

---

## 🟡 Pulizia — costa poco e il prof valuta «organizzazione»

| Cosa | Adesso | Meglio |
|---|---|---|
| Nomi dei server | `-DNS`, `-WEB`, `IooT` | `SRV-DNS`, `SRV-WEB`, `SRV-IOT` |
| Server pubblico | `OUT-WEB    www.itis.pr.it` (spazi multipli) | `SRV-WEB-PUBBLICO` |
| Switch lato ISP | dispositivo `Switch2`, hostname `Switch` | `SW-ISP` su entrambi |
| Switch di casa | dispositivo `main sw`, hostname `SW-HOME` | allinea il nome del dispositivo a `SW-HOME` |
| `Fa0/1` dello switch | ha un residuo `switchport trunk allowed vlan 2-9,11-29,…` | rimuovilo: è in access mode, quella riga non serve |
| Pool DHCP | `VLAN30`, `VLAN40` | `VLAN30-IOT`, `VLAN40-OSPITI`, come `VLAN20-MYHOME` |
| Dominio | router: `giordi.lan` — documenti: `casa.lan` | scegline uno e allinea i record del DNS interno |
| Interfacce dei router | senza `description` | aggiungile: si legge la topologia dal `show run` |
| `MCU0` | nessun IP statico | `192.168.30.30`, come da progetto |

---

## Verifica finale, in ordine

Quando hai chiuso i punti 1–5, in quest'ordine:

1. Da `PC0` (dopo la correzione dell'indirizzo): `ping 198.51.100.1` → deve rispondere.
2. Da `PC0`: `https://203.0.113.2` → deve aprire il cruscotto domotico.
   **È il test del requisito 7.**
3. Disassocia e riassocia un telefono su `MyHome`: deve prendere un indirizzo
   **`192.168.20.1xx`**. Se prende `192.168.60.x`, la WLAN è ancora mappata male.
4. Da `Robby` (ospite, VLAN 40): `ping 198.51.100.10` ✅ ma
   `ping 192.168.20.100` ❌. Se il secondo risponde, le ACL non sono attive.
5. Da `PC1` (VLAN 10): `ssh -l admin 192.168.10.2` → deve entrare nello switch.
6. Sul registration server: tutti i dispositivi presenti, nessuno con `169.254.x.x`.

---

## Bilancio

L'impianto è solido: la parte più difficile — catena di accesso, NAT, port
forwarding, sei VLAN, trunk, WLC con LAP registrati — funziona. Quello che manca
è **applicare le politiche e chiudere due buchi**, non rifare architettura.

In ordine di rapporto punti/tempo:

1. Correggere `192.51.100` → `198.51.100` — **2 minuti**, sblocca due requisiti.
2. Rimappare la WLAN su `vlan20-myhome` — **1 minuto**, sblocca la dimostrazione migliore del progetto.
3. Incollare le ACL della §2.3 — **5 minuti**, ripristina il punto forte n.1.
4. Aggiungere Solar Panel + Power Meter + Battery — **10 minuti**, chiude il requisito 6 e la terza categoria.
5. SVI di management sullo switch — **1 minuto**.

Venti minuti in tutto per passare da «funziona quasi» a «copre tutti e sette i
requisiti».
