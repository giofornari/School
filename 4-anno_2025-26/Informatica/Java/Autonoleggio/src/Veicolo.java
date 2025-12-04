
/**
 * Classe astratta che rappresenta un veicolo generico di autonoleggio.
 * Contiene le informazioni comuni a tutti i veicoli e definisce il metodo astratto
 * per il calcolo del costo del noleggio.
 *
 * @author giordii.dev
 */
public abstract class Veicolo {

    private final String targa;
    private final int numMatr;
    private final String marca;
    private final String modello;
    private final int cilindrata;
    private final int annoAcq;
    private final double capSerbatoio;

    /**
     * Costruttore della classe Veicolo
     *
     * @param targa targa del veicolo
     * @param numeroMatricola numero identificativo del veicolo
     * @param marca marca del veicolo
     * @param modello modello del veicolo
     * @param cilindrata cilindrata in cc
     * @param annoAcquisto anno di acquisto del veicolo
     * @param capacitaSerbatoio capacità del serbatoio in litri
     */
    protected Veicolo(String targa, int numMatr, String marca, String modello,
            int cilindrata, int annoAcq, double capSerbatoio) {
        if (targa == null || targa.trim().isEmpty()) {
            throw new IllegalArgumentException("targa != null");
        }
        if (numMatr <= 0) {
            throw new IllegalArgumentException("numero matricola > 0");
        }
        if (marca == null || marca.trim().isEmpty()) {
            throw new IllegalArgumentException("marca != null");
        }
        if (modello == null || modello.trim().isEmpty()) {
            throw new IllegalArgumentException("modello != null");
        }
        if (cilindrata <= 0) {
            throw new IllegalArgumentException("cilindrata > 0");
        }
        if (annoAcq <= 0) {
            throw new IllegalArgumentException("anno acquisto > 0");
        }
        if (capSerbatoio <= 0) {
            throw new IllegalArgumentException("capacita serbatoio > 0");
        }

        this.targa = targa;
        this.numMatr = numMatr;
        this.marca = marca;
        this.modello = modello;
        this.cilindrata = cilindrata;
        this.annoAcq = annoAcq;
        this.capSerbatoio = capSerbatoio;
    }

    /**
     * Metodo astratto per calcolare il costo del noleggio. Ogni tipo di veicolo
     * implementa la propria logica di calcolo.
     *
     * @param giorni numero di giorni di noleggio
     * @param kmPercorsi chilometri percorsi durante il noleggio
     * @param litriMancanti litri di carburante mancanti al momento della
     * restituzione
     * @return l'importo totale del noleggio in euro
     */
    public abstract double calcolaCostoNoleggio(int giorni, double kmPercorsi, double litriMancanti);

    // Getters
    public String getTarga() {
        return targa;
    }

    public int getNumeroMatricola() {
        return numMatr;
    }

    public String getMarca() {
        return marca;
    }

    public String getModello() {
        return modello;
    }

    public int getCilindrata() {
        return cilindrata;
    }

    public int getAnnoAcquisto() {
        return annoAcq;
    }

    public double getCapacitaSerbatoio() {
        return capSerbatoio;
    }

    @Override
    public String toString() {
        return String.format("Matricola: %d | Targa: %s | %s %s (%dcc) | Anno: %d | Serbatoio: %.1fL",
                numMatr, targa, marca, modello, cilindrata, annoAcq, capSerbatoio);
    }
}
