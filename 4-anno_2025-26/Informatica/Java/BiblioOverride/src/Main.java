import java.time.LocalDate;

/**
 * @author giordii.dev
 */
public class Main {
    public static void main(String[] args) {
        System.out.println("=== SISTEMA GESTIONE BIBLIOTECA CON PRESTITI ===\n");
        
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
        
        System.out.println("--- INFORMAZIONI DURATE PRESTITI ---");
        System.out.println("Durata prestito libri: " + Libro.getDurataPrestitoGiorni() + " giorni");
        System.out.println("Durata prestito riviste: " + Rivista.getDurataPrestitoGiorni() + " giorni");
        System.out.println();
        
        // Test prestiti
        System.out.println("--- TEST PRESTITI ---");
        LocalDate oggi = LocalDate.of(2024, 12, 1);
        
        System.out.println("\nPrestito libro #1 a Mario Rossi dal " + oggi);
        biblioteca.effettuaPrestito(1, "Mario Rossi", oggi);
        
        System.out.println("Prestito rivista #2 a Luigi Verdi dal " + oggi);
        biblioteca.effettuaPrestito(2, "Luigi Verdi", oggi);
        
        System.out.println("Prestito libro #3 a Anna Bianchi dal " + oggi);
        biblioteca.effettuaPrestito(3, "Anna Bianchi", oggi);
        
        System.out.println("Prestito rivista #4 a Carlo Neri dal " + oggi);
        biblioteca.effettuaPrestito(4, "Carlo Neri", oggi);
        
        biblioteca.stampaPrestiti();
        
        System.out.println("--- CATALOGO AGGIORNATO ---");
        biblioteca.stampaCatalogo();
        
        System.out.println("--- PUBBLICAZIONI DISPONIBILI ---");
        for (Pubblicazione p : biblioteca.getPubblicazioniDisponibili()) {
            System.out.println(p);
        }
        System.out.println();
        
        System.out.println("--- TEST RESTITUZIONE ---");
        System.out.println("Restituzione libro #1");
        biblioteca.effettuaRestituzione(1);
        
        System.out.println("Restituzione rivista #2");
        biblioteca.effettuaRestituzione(2);
        System.out.println();
        
        biblioteca.stampaPrestiti();
        
        System.out.println("--- VERIFICA OVERRIDE CALCOLO DATA ---");
        Libro libroTest = new Libro("Test Libro", LocalDate.now(), 100, "123-456", "Autore Test");
        Rivista rivistaTest = new Rivista("Test Rivista", LocalDate.now(), 50, "N.1", "Settimanale");
        
        LocalDate dataTest = LocalDate.of(2024, 12, 1);
        System.out.println("Data inizio prestito: " + dataTest);
        System.out.println("Libro - Data restituzione (30 giorni): " + libroTest.calcolaDataRestituzione(dataTest));
        System.out.println("Rivista - Data restituzione (7 giorni): " + rivistaTest.calcolaDataRestituzione(dataTest));
        System.out.println();
        
        System.out.println("--- STATISTICHE FINALI ---");
        System.out.println("Totale pubblicazioni: " + biblioteca.contaPubblicazioni());
        System.out.println("Pubblicazioni in prestito: " + biblioteca.getPubblicazioniInPrestito().size());
        System.out.println("Pubblicazioni disponibili: " + biblioteca.getPubblicazioniDisponibili().size());
        System.out.println("Totale libri: " + biblioteca.getLibri().size());
        System.out.println("Totale riviste: " + biblioteca.getRiviste().size());
    }
}
