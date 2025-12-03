import java.time.LocalDate;
import java.util.ArrayList;

/**
 * @author giordii.dev
 */
public class Biblioteca {
    private final String nome;
    private final ArrayList<Pubblicazione> pubblicazioni;
    
    public Biblioteca(String nome) {
        if (nome == null || nome.trim().isEmpty()) {
            throw new IllegalArgumentException("Il nome della biblioteca non può essere vuoto");
        }
        this.nome = nome;
        this.pubblicazioni = new ArrayList<>();
    }
    
    public void aggiungiPubblicazione(Pubblicazione p) {
        if (p == null) {
            throw new IllegalArgumentException("La pubblicazione non può essere null");
        }
        pubblicazioni.add(p);
    }
    
    public void rimuoviPubblicazione(int numeroProgressivo) {
        pubblicazioni.removeIf(p -> p.getNumeroProgressivo() == numeroProgressivo);
    }
    
    public Pubblicazione cercaPerNumero(int numeroProgressivo) {
        for (Pubblicazione p : pubblicazioni) {
            if (p.getNumeroProgressivo() == numeroProgressivo) {
                return p;
            }
        }
        return null;
    }
    
    public void effettuaPrestito(int numeroProgressivo, String utente, LocalDate dataInizio) {
        Pubblicazione p = cercaPerNumero(numeroProgressivo);
        if (p == null) {
            throw new IllegalArgumentException("Pubblicazione non trovata");
        }
        p.prestito(utente, dataInizio);
    }
    
    public void effettuaRestituzione(int numeroProgressivo) {
        Pubblicazione p = cercaPerNumero(numeroProgressivo);
        if (p == null) {
            throw new IllegalArgumentException("Pubblicazione non trovata");
        }
        p.restituzione();
    }
    
    public ArrayList<Pubblicazione> getPubblicazioniInPrestito() {
        ArrayList<Pubblicazione> inPrestito = new ArrayList<>();
        for (Pubblicazione p : pubblicazioni) {
            if (p.isInPrestito()) {
                inPrestito.add(p);
            }
        }
        return inPrestito;
    }
    
    public ArrayList<Pubblicazione> getPubblicazioniDisponibili() {
        ArrayList<Pubblicazione> disponibili = new ArrayList<>();
        for (Pubblicazione p : pubblicazioni) {
            if (!p.isInPrestito()) {
                disponibili.add(p);
            }
        }
        return disponibili;
    }
    
    public ArrayList<Libro> getLibri() {
        ArrayList<Libro> libri = new ArrayList<>();
        for (Pubblicazione p : pubblicazioni) {
            if (p instanceof Libro) {
                libri.add((Libro) p);
            }
        }
        return libri;
    }
    
    public ArrayList<Rivista> getRiviste() {
        ArrayList<Rivista> riviste = new ArrayList<>();
        for (Pubblicazione p : pubblicazioni) {
            if (p instanceof Rivista) {
                riviste.add((Rivista) p);
            }
        }
        return riviste;
    }
    
    public int contaPubblicazioni() {
        return pubblicazioni.size();
    }
    
    public void stampaCatalogo() {
        System.out.println("\n=== CATALOGO BIBLIOTECA: " + nome + " ===");
        System.out.println("Totale pubblicazioni: " + pubblicazioni.size());
        System.out.println();
        
        if (pubblicazioni.isEmpty()) {
            System.out.println("Nessuna pubblicazione presente.");
        } else {
            for (Pubblicazione p : pubblicazioni) {
                System.out.println(p);
            }
        }
        System.out.println("==========================================\n");
    }
    
    public void stampaPrestiti() {
        System.out.println("\n=== PUBBLICAZIONI IN PRESTITO ===");
        ArrayList<Pubblicazione> inPrestito = getPubblicazioniInPrestito();
        
        if (inPrestito.isEmpty()) {
            System.out.println("Nessuna pubblicazione in prestito.");
        } else {
            for (Pubblicazione p : inPrestito) {
                System.out.println(p);
            }
        }
        System.out.println("==================================\n");
    }
    
    public String getNome() {
        return nome;
    }
}
