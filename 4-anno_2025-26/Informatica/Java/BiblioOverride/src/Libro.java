import java.time.LocalDate;

/**
 * @author giordii.dev
 */
public class Libro extends Pubblicazione {
    private final String isbn;
    private final String autore;
    
    // Durata standard del prestito per i libri: 30 giorni
    private static final int DURATA_PRESTITO_GIORNI = 30;
    
    public Libro(String titolo, LocalDate dataPubblicazione, int numeroPagine, 
                 String isbn, String autore) {
        super(titolo, dataPubblicazione, numeroPagine);
        
        if (isbn == null || isbn.trim().isEmpty()) {
            throw new IllegalArgumentException("L'ISBN non può essere vuoto");
        }
        if (autore == null || autore.trim().isEmpty()) {
            throw new IllegalArgumentException("L'autore non può essere vuoto");
        }
        
        this.isbn = isbn;
        this.autore = autore;
    }
    
    /**
     * Override: i libri possono essere prestati per 30 giorni
     */
    @Override
    public LocalDate calcolaDataRestituzione(LocalDate dataInizio) {
        if (dataInizio == null) {
            throw new IllegalArgumentException("La data di inizio non può essere null");
        }
        return dataInizio.plusDays(DURATA_PRESTITO_GIORNI);
    }
    
    public String getIsbn() {
        return isbn;
    }
    
    public String getAutore() {
        return autore;
    }
    
    public static int getDurataPrestitoGiorni() {
        return DURATA_PRESTITO_GIORNI;
    }
    
    @Override
    public String toString() {
        return "LIBRO: " + super.toString() + 
               String.format(" | ISBN: %s | Autore: %s", isbn, autore);
    }
}
