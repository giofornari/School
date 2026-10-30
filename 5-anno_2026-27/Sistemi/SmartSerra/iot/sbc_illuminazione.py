# =====================================================================
# SmartSerra - Controllo dell'illuminazione della serra
# Scheda: SBC-PT (Packet Tracer)  -  Programming > New > "Empty - Python"
#
# Collegamenti (IoT Custom Cable):
#   A0  <- Photo Sensor     (luce misurata, 0..1023)
#   A1  <- Potentiometer    (luce desiderata, 0..1023)  ALT+click e trascina per regolarlo
#   D0  -> Servo            (tenda: 0 = aperta, 90 = chiusa)
#   D1  -> LED              (lampada: intensita' 0..1023)
#
# Logica (regolazione proporzionale semplice):
#   errore = luce misurata - luce desiderata
#   errore >  BANDA  -> troppa luce: se la lampada e' accesa la spengo,
#                       altrimenti chiudo la tenda in proporzione all'eccesso
#   errore < -BANDA  -> poca luce: se la tenda e' chiusa la riapro,
#                       se e' aperta accendo la lampada in proporzione alla carenza
#   |errore| <= BANDA -> luce corretta: tenda e lampada restano come sono
# =====================================================================
from gpio import *
from time import *

# ---- collegamenti ----
SENSORE_LUCE = A0
POTENZIOMETRO = A1
TENDA = 0      # D0
LAMPADA = 1    # D1

# ---- parametri di regolazione ----
BANDA = 50          # tolleranza (+/- 50 su 1023, circa 5%): "luce corretta"
SCALA = 512         # eccesso/carenza che porta l'attuatore al 100%
ANGOLO_APERTA = 0   # posizione del servo con tenda aperta
ANGOLO_CHIUSA = 90  # posizione del servo con tenda chiusa
LED_MAX = 1023      # valore analogWrite con lampada al massimo
PERIODO_MS = 500    # ciclo di controllo


def limita(valore, minimo, massimo):
    return max(minimo, min(massimo, valore))


def proporzionale(scostamento):
    # percentuale 0..100 proporzionale allo scostamento (100% da SCALA in su)
    return limita((scostamento * 100) // SCALA, 0, 100)


def imposta_tenda(chiusura):
    angolo = ANGOLO_APERTA + ((ANGOLO_CHIUSA - ANGOLO_APERTA) * chiusura) // 100
    customWrite(TENDA, angolo)


def imposta_lampada(intensita):
    analogWrite(LAMPADA, (LED_MAX * intensita) // 100)


def main():
    pinMode(TENDA, OUT)
    pinMode(LAMPADA, OUT)

    chiusura = 0    # % di chiusura della tenda (0 = tutta aperta)
    intensita = 0   # % di intensita' della lampada (0 = spenta)
    imposta_tenda(chiusura)
    imposta_lampada(intensita)
    stato_precedente = None

    while True:
        luce = analogRead(SENSORE_LUCE)
        desiderata = analogRead(POTENZIOMETRO)
        errore = luce - desiderata

        if errore > BANDA:
            # TROPPA LUCE
            if intensita > 0:
                intensita = 0                      # prima tolgo la luce artificiale
            else:
                chiusura = proporzionale(errore)   # piu' eccesso -> piu' chiusura
            azione = "troppa luce"
        elif errore < -BANDA:
            # POCA LUCE
            if chiusura > 0:
                chiusura = 0                       # prima recupero la luce naturale
            else:
                intensita = proporzionale(-errore) # piu' carenza -> piu' intensita'
            azione = "poca luce"
        else:
            # LUCE CORRETTA: nessuna modifica
            azione = "luce corretta"

        imposta_tenda(chiusura)
        imposta_lampada(intensita)

        stato = (azione, chiusura, intensita)
        if stato != stato_precedente:
            print("luce=%d desiderata=%d errore=%d -> %s | tenda chiusa %d%% | lampada %d%%"
                  % (luce, desiderata, errore, azione, chiusura, intensita))
            stato_precedente = stato

        delay(PERIODO_MS)


if __name__ == "__main__":
    main()
