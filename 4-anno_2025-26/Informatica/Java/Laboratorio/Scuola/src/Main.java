
import java.time.LocalDate;

public class Main {

    public static void main(String[] args) {
        System.out.println("=== GESTIONE DIPENDENTI SCUOLA ===");
        System.out.println();

        // Creazione docenti
        Docente docente1 = new Docente("Mario Rossi", 'M', LocalDate.of(1980, 3, 15), 18, 1800.00);
        Docente docente2 = new Docente("Laura Bianchi", 'F', LocalDate.of(1985, 7, 22), 25, 2100.00);

        // Creazione impiegati
        Impiegato impiegato1 = new Impiegato("Giuseppe Verdi", 'M', LocalDate.of(1990, 11, 5), 3, 1400.00);
        Impiegato impiegato2 = new Impiegato("Anna Neri", 'F', LocalDate.of(1988, 2, 18), 5, 1600.00);

        // Creazione impiegati con straordinari
        ImpiegatoStraordinario impStraord1 = new ImpiegatoStraordinario("Carlo Ferrari", 'M',
                LocalDate.of(1992, 6, 10), 4, 1500.00, 20);
        ImpiegatoStraordinario impStraord2 = new ImpiegatoStraordinario("Giulia Russo", 'F',
                LocalDate.of(1995, 9, 25), 2, 1300.00, 15);

        // Test metodi docenti
        System.out.println("--- DOCENTI ---");
        System.out.println(docente1);
        System.out.println("Stipendio effettivo: €" + docente1.calcolaStipendio());
        System.out.println("Nome: " + docente1.getNome());
        System.out.println("Sesso: " + docente1.getSesso());
        System.out.println("Data di nascita: " + docente1.getBirth());
        System.out.println("Ore docenza: " + docente1.getNOreDocenza());
        System.out.println("Stipendio base: €" + docente1.getBase());
        System.out.println();

        System.out.println(docente2);
        System.out.println("Stipendio effettivo: €" + docente2.calcolaStipendio());
        System.out.println();

        // Test metodi impiegati
        System.out.println("--- IMPIEGATI ---");
        System.out.println(impiegato1);
        System.out.println("Stipendio effettivo: €" + impiegato1.calcolaStipendio());
        System.out.println("Livello: " + impiegato1.getLivello());
        System.out.println();

        System.out.println(impiegato2);
        System.out.println("Stipendio effettivo: €" + impiegato2.calcolaStipendio());
        System.out.println();

        // Test metodi impiegati con straordinari
        System.out.println("--- IMPIEGATI CON STRAORDINARI ---");
        System.out.println(impStraord1);
        System.out.println("Stipendio effettivo: €" + impStraord1.calcolaStipendio());
        System.out.println("Ore straordinario: " + impStraord1.getOreStraordinario());
        System.out.println("Retribuzione oraria: €" + ImpiegatoStraordinario.getRetribuzioneOraria());
        System.out.println();

        System.out.println(impStraord2);
        System.out.println("Stipendio effettivo: €" + impStraord2.calcolaStipendio());
        System.out.println();

        // Test setter
        System.out.println("--- TEST MODIFICHE ---");
        docente1.setNOreDocenza(20);
        System.out.println("Ore docenza aggiornate per " + docente1.getNome() + ": " + docente1.getNOreDocenza());

        impStraord1.setOreStraordinario(25);
        System.out.println("Ore straordinario aggiornate per " + impStraord1.getNome() + ": " + impStraord1.getOreStraordinario());
        System.out.println("Nuovo stipendio effettivo: €" + impStraord1.calcolaStipendio());
    }
}
