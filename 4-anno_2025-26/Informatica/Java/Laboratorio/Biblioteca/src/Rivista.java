import java.time.LocalDate;

/**
 * @author giordii.dev
 */
public class Rivista extends Pubblicazione {
    private final String numeroVolume;
    private final String periodicita;
    
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
    
    public String getNumeroVolume() {
        return numeroVolume;
    }
    
    public String getPeriodicita() {
        return periodicita;
    }
    
    @Override
    public String toString() {
        return "RIVISTA: " + super.toString() + 
               String.format(" | N/Vol: %s | Periodicità: %s", numeroVolume, periodicita);
    }
}
