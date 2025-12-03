import java.time.LocalDate;

/**
 * @author giordii.dev
 */
public class Rivista extends Pubblicazione {
    private final String numeroVolume;
    private final String periodicita;
    
    // Durata standard del prestito per le riviste: 7 giorni
    private static final int DURATA_PRESTITO_GIORNI = 7;
    
    public Rivista(String titolo, LocalDate dataPubblicazione, int numeroPagine,
                   String numeroVolume, String periodicita) {
        super(titolo, dataPubblicazione, numeroPagine);
        
        if (numeroVolume == null || numeroVolume.trim().isEmpty()) {
            throw new IllegalArgumentException("Il numero/volume non può essere vuoto");
        }
        if (periodicita == null || periodicita.trim().isEmpty()) {
            throw new IllegalArgumentException("La periodicità non può essere vuota");
        }
        
        this.numeroVolume = numeroVolume;
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
        return numeroVolume;
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
               String.format(" | N/Vol: %s | Periodicità: %s", numeroVolume, periodicita);
    }
}
