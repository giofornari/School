
/**
 * Classe astratta che rappresenta un veicolo generico di autonoleggio.
 * Contiene le informazioni comuni a tutti i veicoli e definisce il metodo astratto
 * per il calcolo del costo del noleggio.
 *
 * @author giordii.dev
 */
public abstract class Veicolo {

    private final String targa;
    private final int numeroMatricola;
    private final String marca;
    private final String modello;
    private final int cilindrata;
    private final int annoAcquisto;
    private final double capacitaSerbatoio;

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
    protected Veicolo(String targa, int numeroMatricola, String marca, String modello,
            int cilindrata, int annoAcquisto, double capacitaSerbatoio) {
        if (targa == null || targa.trim().isEmpty()) {
            throw new IllegalArgumentException("La targa non può essere vuota");
        }
        if (numeroMatricola <= 0) {
            throw new IllegalArgumentException("Il numero di matricola deve essere > 0");
        }
        if (marca == null || marca.trim().isEmpty()) {
            throw new IllegalArgumentException("La marca non può essere vuota");
        }
        if (modello == null || modello.trim().isEmpty()) {
            throw new IllegalArgumentException("Il modello non può essere vuoto");
        }
        if (cilindrata <= 0) {
            throw new IllegalArgumentException("La cilindrata deve essere > 0");
        }
        if (annoAcquisto <= 0) {
            throw new IllegalArgumentException("L'anno di acquisto deve essere > 0");
        }
        if (capacitaSerbatoio <= 0) {
            throw new IllegalArgumentException("La capacità del serbatoio deve essere > 0");
        }

        this.targa = targa;
        this.numeroMatricola = numeroMatricola;
        this.marca = marca;
        this.modello = modello;
        this.cilindrata = cilindrata;
        this.annoAcquisto = annoAcquisto;
        this.capacitaSerbatoio = capacitaSerbatoio;
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
        return numeroMatricola;
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
        return annoAcquisto;
    }

    public double getCapacitaSerbatoio() {
        return capacitaSerbatoio;
    }

    @Override
    public String toString() {
        return String.format("Matricola: %d | Targa: %s | %s %s (%dcc) | Anno: %d | Serbatoio: %.1fL",
                numeroMatricola, targa, marca, modello, cilindrata, annoAcquisto, capacitaSerbatoio);
    }
}
