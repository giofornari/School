import java.time.LocalDate;
import java.util.ArrayList;

/**
 * Gestione biblioteca con prestiti di libri e riviste
 * @author giordii.dev
 */
public class Biblioteca {
    private final String nome;  // nome della biblioteca
    private final ArrayList<Pubblicazione> pubbl;  // catalogo completo con libri e riviste
    
    /**
     * Crea una nuova biblioteca
     * @param nome il nome della biblioteca
     */
    public Biblioteca(String nome) {
        if (nome == null || nome.trim().isEmpty()) {
            throw new IllegalArgumentException("nome != null");
        }
        this.nome = nome;
        this.pubbl = new ArrayList<>();  // inizia vuoto, si riempie dopo
    }
    
    /**
     * Aggiunge una pubblicazione al catalogo
     * @param p la pubblicazione da aggiungere
     */
    public void aggiungiPubblicazione(Pubblicazione p) {
        if (p == null) {
            throw new IllegalArgumentException("pubblicazione != null");
        }
        pubbl.add(p);  // aggiungi al catalogo
    }
    
    /**
     * Rimuove una pubblicazione dal catalogo
     * @param numeroProgressivo l'ID della pubblicazione
     */
    public void rimuoviPubblicazione(int numeroProgressivo) {
        pubbl.removeIf(p -> p.getNumeroProgressivo() == numeroProgressivo);
        // usa lambda per rimozione efficiente, java 8+
    }
    
    /**
     * Cerca una pubblicazione per numero progressivo
     * @param numeroProgressivo l'ID univoco
     * @return la pubblicazione trovata o null
     */
    public Pubblicazione cercaPerNumero(int numeroProgressivo) {
        for (Pubblicazione p : pubbl) {
            if (p.getNumeroProgressivo() == numeroProgressivo) {
                return p;  // trovata!
            }
        }
        return null;  // non esiste nel catalogo
    }
    
    /**
     * Effettua il prestito di una pubblicazione
     * @param numeroProgressivo ID della pubblicazione
     * @param utente nome dell'utente
     * @param dataInizio data inizio prestito
     */
    public void effettuaPrestito(int numeroProgressivo, String utente, LocalDate dataInizio) {
        Pubblicazione p = cercaPerNumero(numeroProgressivo);
        if (p == null) {
            throw new IllegalArgumentException("Pubblicazione non trovata");
        }
        p.prestito(utente, dataInizio);  // delega alla pubblicazione
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
        for (Pubblicazione p : pubbl) {
            if (p.isInPrestito()) {
                inPrestito.add(p);  // fuori in giro da qualche parte
            }
        }
        return inPrestito;
    }
    
    public ArrayList<Pubblicazione> getPubblicazioniDisponibili() {
        ArrayList<Pubblicazione> disponibili = new ArrayList<>();
        for (Pubblicazione p : pubbl) {
            if (!p.isInPrestito()) {
                disponibili.add(p);  // sullo scaffale pronte
            }
        }
        return disponibili;
    }
    
    /**
     * Filtra solo i libri dal catalogo
     * @return lista dei libri
     */
    public ArrayList<Libro> getLibri() {
        ArrayList<Libro> libri = new ArrayList<>();
        for (Pubblicazione p : pubbl) {
            if (p instanceof Libro) {
                libri.add((Libro) p);  // cast sicuro dopo instanceof check
            }
        }
        return libri;
    }
    
    /**
     * Filtra solo le riviste dal catalogo
     * @return lista delle riviste
     */
    public ArrayList<Rivista> getRiviste() {
        ArrayList<Rivista> riviste = new ArrayList<>();
        for (Pubblicazione p : pubbl) {
            if (p instanceof Rivista) {
                riviste.add((Rivista) p);  // downcast sicuro, instanceof garantisce
            }
        }
        return riviste;
    }
    
    public int contaPubblicazioni() {
        return pubbl.size();
    }
    
    public void stampaCatalogo() {
        System.out.println("\n=== CATALOGO BIBLIOTECA: " + nome + " ===");
        System.out.println("Totale pubblicazioni: " + pubbl.size());
        System.out.println();
        
        if (pubbl.isEmpty()) {
            System.out.println("Nessuna pubblicazione presente.");  // scaffali vuoti...
        } else {
            for (Pubblicazione p : pubbl) {
                System.out.println(p);
            }
        }
        System.out.println("==========================================");
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
