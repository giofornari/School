import java.time.LocalDate;

/**
 * Rivista periodica, prestabile solo per 7 giorni
 * @author giordii.dev
 */
public class Rivista extends Pubblicazione {
    private final String numVol;  // numero/volume della rivista
    private final String periodicita;  // quanto spesso esce (settimanale, mensile...)
    
    // Durata standard del prestito per le riviste: 7 giorni
    private static final int DURATA_PRESTITO_GIORNI = 7;  // una settimana, si leggono veloci
    
    public Rivista(String titolo, LocalDate dataPubbl, int numPagine,
                   String numVol, String periodicita) {
        super(titolo, dataPubbl, numPagine);
        
        if (numVol == null || numVol.trim().isEmpty()) {
            throw new IllegalArgumentException("numero/volume != null");
        }
        if (periodicita == null || periodicita.trim().isEmpty()) {
            throw new IllegalArgumentException("periodicita != null");
        }
        
        this.numVol = numVol;
        this.periodicita = periodicita;
    }
    
    /**
     * Override: le riviste possono essere prestate per soli 7 giorni
     */
    @Override
    public LocalDate calcolaDataRestituzione(LocalDate dataInizio) {
        if (dataInizio == null) {
            throw new IllegalArgumentException("La data di inizio non può essere null");
        }
        return dataInizio.plusDays(DURATA_PRESTITO_GIORNI);
    }
    
    public String getNumeroVolume() {
        return numVol;
    }
    
    public String getPeriodicita() {
        return periodicita;
    }
    
    public static int getDurataPrestitoGiorni() {
        return DURATA_PRESTITO_GIORNI;
    }
    
    @Override
    public String toString() {
        return "RIVISTA: " + super.toString() + 
               String.format(" | N/Vol: %s | Periodicità: %s", numVol, periodicita);
    }
}
