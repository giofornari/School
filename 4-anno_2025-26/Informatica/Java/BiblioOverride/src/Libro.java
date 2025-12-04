import java.time.LocalDate;

/**
 * Libro con ISBN e autore, prestabile per 30 giorni
 * @author giordii.dev
 */
public class Libro extends Pubblicazione {
    private final String isbn;    // codice identificativo internazionale
    private final String autore;  // chi ha scritto questo capolavoro (o mattone)
    
    // Durata standard del prestito per i libri: 30 giorni
    private static final int DURATA_PRESTITO_GIORNI = 30;  // un mese pieno per leggerlo con calma
    
    public Libro(String titolo, LocalDate dataPubbl, int numPagine, 
                 String isbn, String autore) {
        super(titolo, dataPubbl, numPagine);
        
        if (isbn == null || isbn.trim().isEmpty()) {
            throw new IllegalArgumentException("isbn != null");
        }
        if (autore == null || autore.trim().isEmpty()) {
            throw new IllegalArgumentException("autore != null");
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
