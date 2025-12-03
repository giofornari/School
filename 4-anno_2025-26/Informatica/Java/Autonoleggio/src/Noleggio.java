
import java.time.LocalDate;

/**
 * Classe che rappresenta un singolo contratto di noleggio. Gestisce le
 * informazioni del noleggio e calcola il costo finale.
 *
 * @author giordii.dev
 */
public class Noleggio {

    private final Veicolo veicolo;
    private final String nomeCliente;
    private final LocalDate dataInizio;
    private LocalDate dataFine;
    private double kmPercorsi;
    private double litriMancanti;
    private boolean concluso;

    /**
     * Costruttore per creare un nuovo noleggio
     *
     * @param veicolo il veicolo noleggiato
     * @param nomeCliente nome del cliente
     * @param dataInizio data di inizio del noleggio
     */
    public Noleggio(Veicolo veicolo, String nomeCliente, LocalDate dataInizio) {
        if (veicolo == null) {
            throw new IllegalArgumentException("Il veicolo non può essere null");
        }
        if (nomeCliente == null || nomeCliente.trim().isEmpty()) {
            throw new IllegalArgumentException("Il nome del cliente non può essere vuoto");
        }
        if (dataInizio == null) {
            throw new IllegalArgumentException("La data di inizio non può essere null");
        }

        this.veicolo = veicolo;
        this.nomeCliente = nomeCliente;
        this.dataInizio = dataInizio;
        this.dataFine = null;
        this.kmPercorsi = 0;
        this.litriMancanti = 0;
        this.concluso = false;
    }

    /**
     * Conclude il noleggio registrando i dati finali
     *
     * @param dataFine data di restituzione del veicolo
     * @param kmPercorsi km percorsi durante il noleggio
     * @param litriMancanti litri di carburante mancanti
     */
    public void concludiNoleggio(LocalDate dataFine, double kmPercorsi, double litriMancanti) {
        if (concluso) {
            throw new IllegalStateException("Il noleggio è già stato concluso");
        }
        if (dataFine == null) {
            throw new IllegalArgumentException("La data di fine non può essere null");
        }
        if (dataFine.isBefore(dataInizio)) {
            throw new IllegalArgumentException("La data di fine non può essere precedente alla data di inizio");
        }
        if (kmPercorsi < 0) {
            throw new IllegalArgumentException("I km percorsi non possono essere negativi");
        }
        if (litriMancanti < 0) {
            throw new IllegalArgumentException("I litri mancanti non possono essere negativi");
        }

        this.dataFine = dataFine;
        this.kmPercorsi = kmPercorsi;
        this.litriMancanti = litriMancanti;
        this.concluso = true;
    }

    /**
     * Calcola il numero di giorni di noleggio
     *
     * @return il numero di giorni di noleggio
     */
    public int calcolaGiorniNoleggio() {
        if (!concluso || dataFine == null) {
            throw new IllegalStateException("Il noleggio non è ancora stato concluso");
        }

        long giorni = java.time.temporal.ChronoUnit.DAYS.between(dataInizio, dataFine);
        // Se riconsegna lo stesso giorno, almeno 1 giorno
        return (int) Math.max(1, giorni);
    }

    /**
     * Calcola il costo totale del noleggio
     *
     * @return il costo totale in euro
     */
    public double calcolaCostoTotale() {
        if (!concluso) {
            throw new IllegalStateException("Il noleggio non è ancora stato concluso");
        }

        int giorni = calcolaGiorniNoleggio();
        return veicolo.calcolaCostoNoleggio(giorni, kmPercorsi, litriMancanti);
    }

    /**
     * Restituisce un dettaglio completo del costo con la scomposizione
     *
     * @return una stringa con il dettaglio dei costi
     */
    public String getDettaglioCosti() {
        if (!concluso) {
            return "Noleggio non ancora concluso";
        }

        int giorni = calcolaGiorniNoleggio();
        double totale = calcolaCostoTotale();

        StringBuilder sb = new StringBuilder();
        sb.append(String.format("Dettaglio costi per %s:\n", veicolo.getTarga()));
        sb.append(String.format("- Periodo: %s → %s (%d giorni)\n", dataInizio, dataFine, giorni));
        sb.append(String.format("- Km percorsi: %.2f km\n", kmPercorsi));
        sb.append(String.format("- Carburante mancante: %.2f litri\n", litriMancanti));
        sb.append(String.format("TOTALE: %.2f €", totale));

        return sb.toString();
    }

    // Getters
    public Veicolo getVeicolo() {
        return veicolo;
    }

    public String getNomeCliente() {
        return nomeCliente;
    }

    public LocalDate getDataInizio() {
        return dataInizio;
    }

    public LocalDate getDataFine() {
        return dataFine;
    }

    public double getKmPercorsi() {
        return kmPercorsi;
    }

    public double getLitriMancanti() {
        return litriMancanti;
    }

    public boolean isConcluso() {
        return concluso;
    }

    @Override
    public String toString() {
        if (!concluso) {
            return String.format("Noleggio ATTIVO - Cliente: %s | Veicolo: %s | Dal: %s",
                    nomeCliente, veicolo.getTarga(), dataInizio);
        } else {
            return String.format("Noleggio CONCLUSO - Cliente: %s | Veicolo: %s | %s → %s | Costo: %.2f €",
                    nomeCliente, veicolo.getTarga(), dataInizio, dataFine, calcolaCostoTotale());
        }
    }
}
