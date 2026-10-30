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
        return String.format("[#%d] %s - %s - %d pagine", 
            numeroProgressivo, titolo, dataPubblicazione, numeroPagine);
    }
}
