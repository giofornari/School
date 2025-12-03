
/**
 * Classe che rappresenta un'autovettura.
 * Estende la classe Veicolo aggiungendo il numero di posti.
 *
 * Tariffa noleggio:
 * - 50 euro al giorno
 * - 1 euro ogni 25 km percorsi
 * - 2 euro per ogni litro di carburante mancante
 *
 * @author giordii.dev
 */
public class Autovettura extends Veicolo {

    private final int numeroPosti;

    // Costanti per il calcolo del costo
    private static final double COSTO_AL_GIORNO = 50.0;
    private static final double KM_PER_EURO = 25.0;
    private static final double COSTO_LITRO_MANCANTE = 2.0;

    /**
     * Costruttore della classe Autovettura
     *
     * @param targa targa del veicolo
     * @param numeroMatricola numero identificativo del veicolo
     * @param marca marca del veicolo
     * @param modello modello del veicolo
     * @param cilindrata cilindrata in cc
     * @param annoAcquisto anno di acquisto del veicolo
     * @param capacitaSerbatoio capacità del serbatoio in litri
     * @param numeroPosti numero di posti dell'autovettura
     */
    public Autovettura(String targa, int numeroMatricola, String marca, String modello,
            int cilindrata, int annoAcquisto, double capacitaSerbatoio, int numeroPosti) {
        super(targa, numeroMatricola, marca, modello, cilindrata, annoAcquisto, capacitaSerbatoio);

        if (numeroPosti <= 0) {
            throw new IllegalArgumentException("Il numero di posti deve essere > 0");
        }

        this.numeroPosti = numeroPosti;
    }

    /**
     * Calcola il costo del noleggio per un'autovettura. Formula: (50 * giorni)
     * + (kmPercorsi / 25) + (litriMancanti * 2)
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
            throw new IllegalArgumentException("Il numero di giorni deve essere > 0");
        }
        if (kmPercorsi < 0) {
            throw new IllegalArgumentException("I km percorsi non possono essere negativi");
        }
        if (litriMancanti < 0) {
            throw new IllegalArgumentException("I litri mancanti non possono essere negativi");
        }
        if (litriMancanti > getCapacitaSerbatoio()) {
            throw new IllegalArgumentException("I litri mancanti non possono superare la capacità del serbatoio");
        }

        double costoGiorni = COSTO_AL_GIORNO * giorni;
        double costoKm = (kmPercorsi / KM_PER_EURO);
        double costoCarburante = litriMancanti * COSTO_LITRO_MANCANTE;

        return costoGiorni + costoKm + costoCarburante;
    }

    public int getNumeroPosti() {
        return numeroPosti;
    }

    @Override
    public String toString() {
        return "AUTOVETTURA: " + super.toString()
                + String.format(" | Posti: %d", numeroPosti);
    }
}
