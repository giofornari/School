import java.time.LocalDate;

/**
 * Classe astratta per pubblicazioni (libri e riviste)
 * @author giordii.dev
 */
public abstract class Pubblicazione {
    private static int contatore = 1;  // auto-increment per ID univoco
    
    private final int numProgressivo;  // ID generato automaticamente
    private final String titolo;
    private final LocalDate dataPubbl;  // quando è uscita
    private final int numPagine;  // spessore del mattone
    
    // stato del prestito
    private boolean inPrestito;  // true se qualcuno se l'è presa
    private LocalDate dataInizioPrestitoAttuale;  // quando è stata prestata
    private String utentePrestito;  // chi l'ha in questo momento
    
    public Pubblicazione(String titolo, LocalDate dataPubbl, int numPagine) {
        if (titolo == null || titolo.trim().isEmpty()) {
            throw new IllegalArgumentException("titolo != null");
        }
        if (dataPubbl == null) {
            throw new IllegalArgumentException("data pubblicazione != null");
        }
        if (numPagine <= 0) {
            throw new IllegalArgumentException("numero pagine > 0");
        }
        
        this.numProgressivo = contatore++;
        this.titolo = titolo;
        this.dataPubbl = dataPubbl;
        this.numPagine = numPagine;
        this.inPrestito = false;  // inizialmente disponibile
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
        return numProgressivo;
    }
    
    public String getTitolo() {
        return titolo;
    }
    
    public LocalDate getDataPubblicazione() {
        return dataPubbl;
    }
    
    public int getNumeroPagine() {
        return numPagine;
    }
    
    @Override
    public String toString() {
        String base = String.format("[#%d] %s - %s - %d pagine", 
            numProgressivo, titolo, dataPubbl, numPagine);
        
        if (inPrestito) {
            base += String.format(" | IN PRESTITO a %s (dal %s, rientro previsto: %s)",
                utentePrestito, dataInizioPrestitoAttuale, getDataRestituzioneAttesa());
        } else {
            base += " | DISPONIBILE";  // sullo scaffale pronta per essere presa
        }
        
        return base;
    }
}
