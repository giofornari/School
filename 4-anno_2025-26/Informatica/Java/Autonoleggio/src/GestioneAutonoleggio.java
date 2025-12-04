
import java.time.LocalDate;
import java.util.ArrayList;

/**
 * Classe che gestisce la flotta di veicoli e i noleggi di una catena di
 * autonoleggio. Permette di aggiungere veicoli, cercare veicoli disponibili,
 * avviare e concludere noleggi.
 *
 * @author giordii.dev
 */
public class GestioneAutonoleggio {

    private final String nomeAzienda;
    private final ArrayList<Veicolo> flotta;
    private final ArrayList<Noleggio> noleggi;

    /**
     * Costruttore della classe GestioneAutonoleggio
     *
     * @param nomeAzienda nome della catena di autonoleggio
     */
    public GestioneAutonoleggio(String nomeAzienda) {
        if (nomeAzienda == null || nomeAzienda.trim().isEmpty()) {
            throw new IllegalArgumentException("nome azienda != null");
        }

        this.nomeAzienda = nomeAzienda;
        this.flotta = new ArrayList<>();  // inizia vuota
        this.noleggi = new ArrayList<>();  // nessun noleggio ancora
    }

    /**
     * Aggiunge un veicolo alla flotta
     *
     * @param veicolo il veicolo da aggiungere
     */
    public void aggiungiVeicolo(Veicolo veicolo) {
        if (veicolo == null) {
            throw new IllegalArgumentException("veicolo != null");
        }

        // controllo che la targa non sia già nel sistema
        for (Veicolo v : flotta) {
            if (v.getTarga().equals(veicolo.getTarga())) {
                throw new IllegalArgumentException("targa " + veicolo.getTarga() + " gia presente");
            }
        }

        flotta.add(veicolo);  // aggiunto alla flotta
    }

    /**
     * Cerca un veicolo per numero di matricola
     *
     * @param numeroMatricola numero identificativo del veicolo
     * @return il veicolo trovato o null se non presente
     */
    public Veicolo cercaVeicolo(int numeroMatricola) {
        for (Veicolo v : flotta) {
            if (v.getNumeroMatricola() == numeroMatricola) {
                return v;  // trovato!
            }
        }
        return null;  // non esiste
    }

    /**
     * Cerca un veicolo per targa
     *
     * @param targa targa del veicolo
     * @return il veicolo trovato o null se non presente
     */
    public Veicolo cercaVeicoloPerTarga(String targa) {
        if (targa == null) {
            return null;  // targa invalida
        }

        for (Veicolo v : flotta) {
            if (v.getTarga().equalsIgnoreCase(targa)) {
                return v;  // match!
            }
        }
        return null;  // nessun veicolo con questa targa
    }

    /**
     * Verifica se un veicolo è disponibile per il noleggio
     *
     * @param veicolo il veicolo da verificare
     * @return true se il veicolo è disponibile, false se è in noleggio attivo
     */
    public boolean isVeicoloDisponibile(Veicolo veicolo) {
        for (Noleggio n : noleggi) {
            if (!n.isConcluso() && n.getVeicolo().equals(veicolo)) {
                return false;  // in giro con qualcuno
            }
        }
        return true;  // parcheggiato e pronto
    }

    /**
     * Avvia un nuovo noleggio
     *
     * @param numeroMatricola numero di matricola del veicolo da noleggiare
     * @param nomeCliente nome del cliente
     * @param dataInizio data di inizio del noleggio
     * @return il noleggio creato
     */
    public Noleggio avviaNoleggio(int numeroMatricola, String nomeCliente, LocalDate dataInizio) {
        Veicolo veicolo = cercaVeicolo(numeroMatricola);

        if (veicolo == null) {
            throw new IllegalArgumentException("veicolo " + numeroMatricola + " non trovato");
        }

        if (!isVeicoloDisponibile(veicolo)) {
            throw new IllegalStateException("veicolo " + veicolo.getTarga() + " gia in noleggio");
        }

        Noleggio noleggio = new Noleggio(veicolo, nomeCliente, dataInizio);
        noleggi.add(noleggio);  // registrato nel sistema

        return noleggio;
    }

    /**
     * Restituisce la lista dei veicoli disponibili
     *
     * @return lista di veicoli disponibili
     */
    public ArrayList<Veicolo> getVeicoliDisponibili() {
        ArrayList<Veicolo> disponibili = new ArrayList<>();

        for (Veicolo v : flotta) {
            if (isVeicoloDisponibile(v)) {
                disponibili.add(v);  // libero e pronto
            }
        }

        return disponibili;
    }

    /**
     * Restituisce la lista dei noleggi attivi
     *
     * @return lista di noleggi attivi
     */
    public ArrayList<Noleggio> getNoleggiAttivi() {
        ArrayList<Noleggio> attivi = new ArrayList<>();

        for (Noleggio n : noleggi) {
            if (!n.isConcluso()) {
                attivi.add(n);  // ancora in giro
            }
        }

        return attivi;
    }

    /**
     * Restituisce la lista dei noleggi conclusi
     *
     * @return lista di noleggi conclusi
     */
    public ArrayList<Noleggio> getNoleggiConclusi() {
        ArrayList<Noleggio> conclusi = new ArrayList<>();

        for (Noleggio n : noleggi) {
            if (n.isConcluso()) {
                conclusi.add(n);  // già restituiti
            }
        }

        return conclusi;
    }

    /**
     * Restituisce solo le autovetture della flotta
     *
     * @return lista di autovetture
     */
    public ArrayList<Autovettura> getAutovetture() {
        ArrayList<Autovettura> autovetture = new ArrayList<>();

        for (Veicolo v : flotta) {
            if (v instanceof Autovettura) {
                autovetture.add((Autovettura) v);  // cast sicuro dopo instanceof
            }
        }

        return autovetture;
    }

    /**
     * Restituisce solo i furgoni della flotta
     *
     * @return lista di furgoni
     */
    public ArrayList<Furgone> getFurgoni() {
        ArrayList<Furgone> furgoni = new ArrayList<>();

        for (Veicolo v : flotta) {
            if (v instanceof Furgone) {
                furgoni.add((Furgone) v);  // downcast sicuro
            }
        }

        return furgoni;
    }

    /**
     * Stampa l'intera flotta di veicoli
     */
    public void stampaFlotta() {
        System.out.println("\n=== FLOTTA " + nomeAzienda.toUpperCase() + " ===");
        System.out.println("Totale veicoli: " + flotta.size());
        System.out.println();

        if (flotta.isEmpty()) {
            System.out.println("Nessun veicolo nella flotta.");  // ancora da comprare
        } else {
            for (Veicolo v : flotta) {
                String stato = isVeicoloDisponibile(v) ? "[DISPONIBILE]" : "[IN NOLEGGIO]";
                System.out.println(stato + " " + v);
            }
        }
        System.out.println("================================\n");
    }

    /**
     * Stampa tutti i noleggi attivi
     */
    public void stampaNoleggiAttivi() {
        System.out.println("\n=== NOLEGGI ATTIVI ===");
        ArrayList<Noleggio> attivi = getNoleggiAttivi();

        if (attivi.isEmpty()) {
            System.out.println("Nessun noleggio attivo.");
        } else {
            for (Noleggio n : attivi) {
                System.out.println(n);
            }
        }
        System.out.println("======================\n");
    }

    /**
     * Stampa lo storico dei noleggi conclusi
     */
    public void stampaStoricoNoleggi() {
        System.out.println("\n=== STORICO NOLEGGI CONCLUSI ===");
        ArrayList<Noleggio> conclusi = getNoleggiConclusi();

        if (conclusi.isEmpty()) {
            System.out.println("Nessun noleggio concluso.");
        } else {
            for (Noleggio n : conclusi) {
                System.out.println(n);
            }
        }
        System.out.println("================================\n");
    }

    public String getNomeAzienda() {
        return nomeAzienda;
    }

    public int contaVeicoli() {
        return flotta.size();
    }

    public int contaNoleggi() {
        return noleggi.size();
    }
}
