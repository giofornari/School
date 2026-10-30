/*
 * CENTRALINA GIARDINO - irrigazione automatica + telemetria energetica
 * MCU-PT, Packet Tracer 8.2.1 - linguaggio JavaScript
 *
 * COLLEGAMENTI FISICI (slot dell'MCU-PT)
 *   A0  analog IN   Soil Moisture / Water Level Sensor - umidita' terreno
 *   A1  analog IN   Photo Sensor                       - luce ambiente
 *   D0  digital OUT Rele' -> Lawn Sprinkler            - elettrovalvola
 *   D1  digital OUT RGB LED                            - stato centralina
 *
 * ATTENZIONE: i numeri di pin dipendono da DOVE hai infilato i componenti
 * nell'MCU. Aprilo in vista Physical, guarda l'ordine degli slot e correggi
 * le costanti qui sotto se non coincidono.
 *
 * LOGICA
 *   Irriga solo se TUTTE e tre sono vere:
 *     1. umidita' terreno < SOGLIA_SECCO       -> c'e' davvero bisogno
 *     2. luce ambiente   < SOGLIA_BUIO         -> non nelle ore calde
 *     3. sono passate almeno PAUSA_MIN_MS      -> niente cicli ravvicinati
 *   Si ferma quando l'umidita' supera SOGLIA_BAGNATO (isteresi).
 *
 * PERCHE' L'ISTERESI
 *   Se accendessi sotto il 30% e spegnessi sopra il 30%, appena il valore
 *   tocca la soglia il rele' commuterebbe decine di volte al minuto. Con due
 *   soglie diverse (30% accende, 45% spegne) il sistema resta stabile.
 *   E' anche il motivo per cui questa logica NON si puo' scrivere come
 *   condizione sul registration server: quelle sono booleane e senza memoria.
 */

// ---------- pin ----------
var PIN_UMIDITA = 0;   // A0
var PIN_LUCE    = 1;   // A1
var PIN_VALVOLA = 0;   // D0
var PIN_LED     = 1;   // D1

// ---------- soglie ----------
var SOGLIA_SECCO   = 30;   // % sotto cui il terreno e' secco  -> accende
var SOGLIA_BAGNATO = 45;   // % sopra cui e' bagnato           -> spegne
var SOGLIA_BUIO    = 40;   // % di luce sotto cui si puo' irrigare
var PAUSA_MIN_MS   = 6 * 60 * 60 * 1000;   // 6 ore fra due irrigazioni
var DURATA_MAX_MS  = 10 * 60 * 1000;       // 10 min: taglio di sicurezza

// ---------- stato ----------
var irrigazioneAttiva = false;
var inizioIrrigazione = 0;
var ultimaIrrigazione = -PAUSA_MIN_MS;   // cosi' la prima volta puo' partire
var guasto = false;

// L'MCU legge gli analogici come interi 0..1023: li riporto in percentuale.
function letturaPercento(pin) {
    var grezzo = analogRead(pin);
    return Math.round((grezzo / 1023) * 100);
}

// LED di stato: verde = ok, blu = sta irrigando, rosso = guasto
function stato(colore) {
    if (colore === "rosso")      { customWrite(PIN_LED, "255,0,0");   }
    else if (colore === "blu")   { customWrite(PIN_LED, "0,0,255");   }
    else                         { customWrite(PIN_LED, "0,255,0");   }
}

function apriValvola() {
    digitalWrite(PIN_VALVOLA, HIGH);
    irrigazioneAttiva = true;
    inizioIrrigazione = getTickCount();
    stato("blu");
    Serial.println("Irrigazione AVVIATA");
}

function chiudiValvola(motivo) {
    digitalWrite(PIN_VALVOLA, LOW);
    irrigazioneAttiva = false;
    ultimaIrrigazione = getTickCount();
    stato(guasto ? "rosso" : "verde");
    Serial.println("Irrigazione FERMATA - " + motivo);
}

function setup() {
    pinMode(PIN_UMIDITA, ANALOG);
    pinMode(PIN_LUCE,    ANALOG);
    pinMode(PIN_VALVOLA, OUTPUT);
    pinMode(PIN_LED,     OUTPUT);

    digitalWrite(PIN_VALVOLA, LOW);   // parte sempre chiusa: fail-safe
    stato("verde");

    // Registrazione sul registration server: da qui il cruscotto vede i dati
    IoEClient.setup({
        type: "Centralina Giardino",
        states: [
            { name: "Umidita terreno", type: "number", unit: "%" },
            { name: "Luce ambiente",   type: "number", unit: "%" },
            { name: "Irrigazione",     type: "bool" },
            { name: "Guasto",          type: "bool" }
        ]
    });

    Serial.println("Centralina giardino avviata");
}

function loop() {
    var umidita = letturaPercento(PIN_UMIDITA);
    var luce    = letturaPercento(PIN_LUCE);
    var adesso  = getTickCount();

    // --- diagnostica sensore ---
    // Un valore fuori scala significa sensore scollegato o in corto: in quel
    // caso NON irrigo. Meglio una pianta secca che un giardino allagato.
    guasto = (umidita < 0 || umidita > 100);
    if (guasto) {
        if (irrigazioneAttiva) { chiudiValvola("sensore guasto"); }
        stato("rosso");
        Serial.println("GUASTO: lettura umidita' fuori scala");
    }
    else if (irrigazioneAttiva) {
        // --- sono gia' in irrigazione: quando mi fermo? ---
        if (umidita >= SOGLIA_BAGNATO) {
            chiudiValvola("terreno bagnato (" + umidita + "%)");
        } else if (adesso - inizioIrrigazione > DURATA_MAX_MS) {
            // Se dopo 10 minuti l'umidita' non sale, o il sensore mente o
            // l'acqua non arriva. In entrambi i casi chiudo e segnalo.
            guasto = true;
            chiudiValvola("timeout: durata massima superata");
        }
    }
    else {
        // --- valvola chiusa: le tre condizioni per partire ---
        var terrenoSecco   = (umidita < SOGLIA_SECCO);
        var oraGiusta      = (luce < SOGLIA_BUIO);
        var pausaRispettata = (adesso - ultimaIrrigazione >= PAUSA_MIN_MS);

        if (terrenoSecco && oraGiusta && pausaRispettata) {
            apriValvola();
        }
    }

    // --- telemetria verso il cruscotto ---
    IoEClient.reportStates([umidita, luce, irrigazioneAttiva, guasto]);

    delay(1000);
}
