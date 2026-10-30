"""
CENTRALINA GIARDINO - irrigazione automatica + telemetria energetica
MCU-PT, Packet Tracer 8.2.1 - linguaggio Python

Versione equivalente a centralina.js: si carica UNA delle due, non entrambe.
La logica e le soglie sono identiche; cambia solo la sintassi.

COLLEGAMENTI FISICI (slot dell'MCU-PT)
    A0  analog IN   Soil Moisture / Water Level Sensor - umidita' terreno
    A1  analog IN   Photo Sensor                       - luce ambiente
    D0  digital OUT Rele' -> Lawn Sprinkler            - elettrovalvola
    D1  digital OUT RGB LED                            - stato centralina

ATTENZIONE: i numeri di pin dipendono da DOVE hai infilato i componenti
nell'MCU. Aprilo in vista Physical, guarda l'ordine degli slot e correggi le
costanti se non coincidono.

LOGICA
    Irriga solo se TUTTE e tre sono vere:
      1. umidita' terreno < SOGLIA_SECCO   -> c'e' davvero bisogno
      2. luce ambiente   < SOGLIA_BUIO     -> non nelle ore calde
      3. passate almeno PAUSA_MIN_MS       -> niente cicli ravvicinati
    Si ferma quando l'umidita' supera SOGLIA_BAGNATO (isteresi).

PERCHE' L'ISTERESI
    Accendere sotto il 30% e spegnere sopra il 30% farebbe commutare il rele'
    decine di volte al minuto attorno alla soglia. Due soglie diverse (30%
    accende, 45% spegne) rendono il sistema stabile. E' anche il motivo per
    cui questa logica non si puo' scrivere come condizione sul registration
    server: quelle sono booleane e senza memoria fra un'esecuzione e l'altra.
"""
from gpio import *
from time import *
from ioeclient import IoEClient

# ---------- pin ----------
PIN_UMIDITA = 0     # A0
PIN_LUCE = 1        # A1
PIN_VALVOLA = 0     # D0
PIN_LED = 1         # D1

# ---------- soglie ----------
SOGLIA_SECCO = 30           # % sotto cui il terreno e' secco  -> accende
SOGLIA_BAGNATO = 45         # % sopra cui e' bagnato           -> spegne
SOGLIA_BUIO = 40            # % di luce sotto cui si puo' irrigare
PAUSA_MIN_S = 6 * 60 * 60   # 6 ore fra due irrigazioni
DURATA_MAX_S = 10 * 60      # 10 min: taglio di sicurezza

# ---------- stato ----------
irrigazione_attiva = False
inizio_irrigazione = 0
ultima_irrigazione = -PAUSA_MIN_S   # cosi' la prima volta puo' partire
guasto = False


def letturaPercento(pin):
    """L'MCU legge gli analogici come interi 0..1023: li riporto in %."""
    return int(round(analogRead(pin) / 1023.0 * 100))


def stato(colore):
    """LED: verde = ok, blu = sta irrigando, rosso = guasto."""
    colori = {"rosso": "255,0,0", "blu": "0,0,255", "verde": "0,255,0"}
    customWrite(PIN_LED, colori.get(colore, colori["verde"]))


def apri_valvola(adesso):
    global irrigazione_attiva, inizio_irrigazione
    digitalWrite(PIN_VALVOLA, HIGH)
    irrigazione_attiva = True
    inizio_irrigazione = adesso
    stato("blu")
    print("Irrigazione AVVIATA")


def chiudi_valvola(adesso, motivo):
    global irrigazione_attiva, ultima_irrigazione
    digitalWrite(PIN_VALVOLA, LOW)
    irrigazione_attiva = False
    ultima_irrigazione = adesso
    stato("rosso" if guasto else "verde")
    print("Irrigazione FERMATA - " + motivo)


def setup():
    pinMode(PIN_UMIDITA, ANALOG)
    pinMode(PIN_LUCE, ANALOG)
    pinMode(PIN_VALVOLA, OUTPUT)
    pinMode(PIN_LED, OUTPUT)

    digitalWrite(PIN_VALVOLA, LOW)      # parte sempre chiusa: fail-safe
    stato("verde")

    # Registrazione sul registration server: da qui il cruscotto vede i dati
    IoEClient.setup({
        "type": "Centralina Giardino",
        "states": [
            {"name": "Umidita terreno", "type": "number", "unit": "%"},
            {"name": "Luce ambiente", "type": "number", "unit": "%"},
            {"name": "Irrigazione", "type": "bool"},
            {"name": "Guasto", "type": "bool"},
        ],
    })
    print("Centralina giardino avviata")


def loop():
    global guasto

    umidita = letturaPercento(PIN_UMIDITA)
    luce = letturaPercento(PIN_LUCE)
    adesso = time()

    # --- diagnostica sensore ---
    # Valore fuori scala = sensore scollegato o in corto: NON irrigo.
    # Meglio una pianta secca che un giardino allagato.
    guasto = not (0 <= umidita <= 100)

    if guasto:
        if irrigazione_attiva:
            chiudi_valvola(adesso, "sensore guasto")
        stato("rosso")
        print("GUASTO: lettura umidita' fuori scala")

    elif irrigazione_attiva:
        # --- gia' in irrigazione: quando mi fermo? ---
        if umidita >= SOGLIA_BAGNATO:
            chiudi_valvola(adesso, "terreno bagnato (%d%%)" % umidita)
        elif adesso - inizio_irrigazione > DURATA_MAX_S:
            # Se dopo 10 minuti l'umidita' non sale, o il sensore mente o
            # l'acqua non arriva. In entrambi i casi chiudo e segnalo.
            guasto = True
            chiudi_valvola(adesso, "timeout: durata massima superata")

    else:
        # --- valvola chiusa: le tre condizioni per partire ---
        terreno_secco = umidita < SOGLIA_SECCO
        ora_giusta = luce < SOGLIA_BUIO
        pausa_rispettata = (adesso - ultima_irrigazione) >= PAUSA_MIN_S

        if terreno_secco and ora_giusta and pausa_rispettata:
            apri_valvola(adesso)

    # --- telemetria verso il cruscotto ---
    IoEClient.reportStates([umidita, luce, irrigazione_attiva, guasto])

    delay(1000)


def main():
    setup()
    while True:
        loop()


if __name__ == "__main__":
    main()
