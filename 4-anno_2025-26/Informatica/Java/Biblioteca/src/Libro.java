import java.time.LocalDate;

/**
 * @author giordii.dev
 */
public class Libro extends Pubblicazione {
    private final String isbn;
    private final String autore;
    
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
    
    public String getIsbn() {
        return isbn;
    }
    
    public String getAutore() {
        return autore;
    }
    
    @Override
    public String toString() {
        return "LIBRO: " + super.toString() + 
               String.format(" | ISBN: %s | Autore: %s", isbn, autore);
    }
}
