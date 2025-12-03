import java.time.LocalDate;

/**
 * @author giordii.dev
 */
public abstract class Pubblicazione {
    private static int contatore = 1;
    
    private final int numeroProgressivo;
    private final String titolo;
    private final LocalDate dataPubblicazione;
    private final int numeroPagine;
    
    private boolean inPrestito;
    private LocalDate dataInizioPrestitoAttuale;
    private String utentePrestito;
    
    public Pubblicazione(String titolo, LocalDate dataPubblicazione, int numeroPagine) {
        if (titolo == null || titolo.trim().isEmpty()) {
            throw new IllegalArgumentException("Il titolo non può essere vuoto");
        }
        if (dataPubblicazione == null) {
            throw new IllegalArgumentException("La data di pubblicazione non può essere null");
        }
        if (numeroPagine <= 0) {
            throw new IllegalArgumentException("Il numero di pagine deve essere > 0");
        }
        
        this.numeroProgressivo = contatore++;
        this.titolo = titolo;
        this.dataPubblicazione = dataPubblicazione;
        this.numeroPagine = numeroPagine;
        this.inPrestito = false;
        this.dataInizioPrestitoAttuale = null;
        this.utentePrestito = null;
    }
    
    /**
     * Metodo astratto da implementare nelle sottoclassi per definire
     * il calcolo della data di restituzione specifica per ogni tipo di pubblicazione
     */
    public abstract LocalDate calcolaDataRestituzione(LocalDate dataInizio);
    
    public void prestito(String utente, LocalDate dataInizio) {
        if (inPrestito) {
            throw new IllegalStateException("La pubblicazione è già in prestito");
        }
        if (utente == null || utente.trim().isEmpty()) {
            throw new IllegalArgumentException("Il nome dell'utente non può essere vuoto");
        }
        if (dataInizio == null) {
            throw new IllegalArgumentException("La data di inizio prestito non può essere null");
        }
        
        this.inPrestito = true;
        this.dataInizioPrestitoAttuale = dataInizio;
        this.utentePrestito = utente;
    }
    
    public void restituzione() {
        if (!inPrestito) {
            throw new IllegalStateException("La pubblicazione non è in prestito");
        }
        
        this.inPrestito = false;
        this.dataInizioPrestitoAttuale = null;
        this.utentePrestito = null;
    }
    
    public boolean isInPrestito() {
        return inPrestito;
    }
    
    public LocalDate getDataInizioPrestitoAttuale() {
        return dataInizioPrestitoAttuale;
    }
    
    public String getUtentePrestito() {
        return utentePrestito;
    }
    
    public LocalDate getDataRestituzioneAttesa() {
        if (!inPrestito) {
            return null;
        }
        return calcolaDataRestituzione(dataInizioPrestitoAttuale);
    }
    
    public int getNumeroProgressivo() {
        return numeroProgressivo;
    }
    
    public String getTitolo() {
        return titolo;
    }
    
    public LocalDate getDataPubblicazione() {
        return dataPubblicazione;
    }
    
    public int getNumeroPagine() {
        return numeroPagine;
    }
    
    @Override
    public String toString() {
        String base = String.format("[#%d] %s - %s - %d pagine", 
            numeroProgressivo, titolo, dataPubblicazione, numeroPagine);
        
        if (inPrestito) {
            base += String.format(" | IN PRESTITO a %s (dal %s, rientro previsto: %s)",
                utentePrestito, dataInizioPrestitoAttuale, getDataRestituzioneAttesa());
        } else {
            base += " | DISPONIBILE";
        }
        
        return base;
    }
}
