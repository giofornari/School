
/**
 * Classe che rappresenta un furgone.
 * Estende la classe Veicolo aggiungendo la capacità di carico.
 *
 * Tariffa noleggio:
 * - 70 euro al giorno
 * - 1 euro ogni 30 km percorsi dopo i primi 100 km gratuiti
 * - 2 euro per ogni litro di carburante mancante
 *
 * @author giordii.dev
 */
public class Furgone extends Veicolo {

    private final double capCarico;

    // Costanti per il calcolo del costo
    private static final double COSTO_AL_GIORNO = 70.0;
    private static final double KM_GRATUITI = 100.0;
    private static final double KM_PER_EURO = 30.0;
    private static final double COSTO_LITRO_MANCANTE = 2.0;

    /**
     * Costruttore della classe Furgone
     *
     * @param targa targa del veicolo
     * @param numeroMatricola numero identificativo del veicolo
     * @param marca marca del veicolo
     * @param modello modello del veicolo
     * @param cilindrata cilindrata in cc
     * @param annoAcquisto anno di acquisto del veicolo
     * @param capacitaSerbatoio capacità del serbatoio in litri
     * @param capacitaCarico capacità di carico del furgone in kg
     */
    public Furgone(String targa, int numMatr, String marca, String modello,
            int cilindrata, int annoAcq, double capSerbatoio, double capCarico) {
        super(targa, numMatr, marca, modello, cilindrata, annoAcq, capSerbatoio);

        if (capCarico <= 0) {
            throw new IllegalArgumentException("capacita carico > 0");
        }

        this.capCarico = capCarico;
    }

    /**
     * Calcola il costo del noleggio per un furgone. Formula: (70 * giorni) +
     * ((kmPercorsi - 100) / 30) + (litriMancanti * 2) I primi 100 km sono
     * gratuiti
     *
     * @param giorni numero di giorni di noleggio
     * @param kmPercorsi chilometri percorsi durante il noleggio
     * @param litriMancanti litri di carburante mancanti al momento della
     * restituzione
     * @return l'importo totale del noleggio in euro
     */
    @Override
    public double calcolaCostoNoleggio(int giorni, double kmPercorsi, double litriMancanti) {
        if (giorni <= 0) {
            throw new IllegalArgumentException("giorni > 0");
        }
        if (kmPercorsi < 0) {
            throw new IllegalArgumentException("km >= 0");
        }
        if (litriMancanti < 0) {
            throw new IllegalArgumentException("litri mancanti >= 0");
        }
        if (litriMancanti > getCapacitaSerbatoio()) {
            throw new IllegalArgumentException("litri mancanti <= capacita serbatoio");
        }

        double costoGiorni = COSTO_AL_GIORNO * giorni;

        // Calcolo costo km: i primi 100 km sono gratuiti
        double kmOltreFranchigia = Math.max(0, kmPercorsi - KM_GRATUITI);
        double costoKm = kmOltreFranchigia / KM_PER_EURO;

        double costoCarburante = litriMancanti * COSTO_LITRO_MANCANTE;

        return costoGiorni + costoKm + costoCarburante;
    }

    public double getCapacitaCarico() {
        return capCarico;
    }

    @Override
    public String toString() {
        return "FURGONE: " + super.toString()
                + String.format(" | Carico: %.0fkg", capCarico);
    }
}
