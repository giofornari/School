import java.time.LocalDate;

/**
 * @author giordii.dev
 */
public class Main {
    public static void main(String[] args) {
        System.out.println("=== SISTEMA GESTIONE BIBLIOTECA ===\n");
        
        // Creazione biblioteca
        Biblioteca biblioteca = new Biblioteca("Biblioteca Comunale");
        
        // Aggiunta libri
        Libro libro1 = new Libro(
            "Il Signore degli Anelli",
            LocalDate.of(1954, 7, 29),
            1216,
            "978-88-452-3232-8",
            "J.R.R. Tolkien"
        );
        
        Libro libro2 = new Libro(
            "1984",
            LocalDate.of(1949, 6, 8),
            328,
            "978-88-04-68012-1",
            "George Orwell"
        );
        
        Libro libro3 = new Libro(
            "Il Nome della Rosa",
            LocalDate.of(1980, 9, 1),
            503,
            "978-88-452-6647-7",
            "Umberto Eco"
        );
        
        Rivista rivista1 = new Rivista(
            "National Geographic Italia",
            LocalDate.of(2024, 11, 1),
            120,
            "Vol. 35, N. 11",
            "Mensile"
        );
        
        Rivista rivista2 = new Rivista(
            "Focus",
            LocalDate.of(2024, 10, 15),
            98,
            "N. 385",
            "Mensile"
        );
        
        Rivista rivista3 = new Rivista(
            "Le Scienze",
            LocalDate.of(2024, 11, 20),
            88,
            "N. 655",
            "Mensile"
        );
        
        biblioteca.aggiungiPubblicazione(libro1);
        biblioteca.aggiungiPubblicazione(rivista1);
        biblioteca.aggiungiPubblicazione(libro2);
        biblioteca.aggiungiPubblicazione(rivista2);
        biblioteca.aggiungiPubblicazione(libro3);
        biblioteca.aggiungiPubblicazione(rivista3);
        
        biblioteca.stampaCatalogo();
        
        System.out.println("--- TEST RICERCA PER NUMERO ---");
        Pubblicazione trovata = biblioteca.cercaPerNumero(3);
        if (trovata != null) {
            System.out.println("Trovata: " + trovata);
        }
        System.out.println();
        
        System.out.println("--- SOLO LIBRI ---");
        for (Libro l : biblioteca.getLibri()) {
            System.out.println(l);
        }
        System.out.println();
        
        System.out.println("--- SOLO RIVISTE ---");
        for (Rivista r : biblioteca.getRiviste()) {
            System.out.println(r);
        }
        System.out.println();
        
        System.out.println("--- TEST RIMOZIONE (numero progressivo 2) ---");
        biblioteca.rimuoviPubblicazione(2);
        biblioteca.stampaCatalogo();
        
        System.out.println("Totale pubblicazioni rimanenti: " + biblioteca.contaPubblicazioni());
    }
}
