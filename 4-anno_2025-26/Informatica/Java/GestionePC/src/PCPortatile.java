/**
 * Classe astratta che rappresenta un PC portatile.
 * Estende la classe PC aggiungendo peso, dimensioni fisiche, dimensione del video e wireless.
 * 
 * @author giordii.dev
 */
public abstract class PCPortatile extends PC {
    protected double peso; // in kg
    protected double altezza; // in cm
    protected double larghezza; // in cm
    protected double profondita; // in cm
    protected double dimensioneVideo; // in pollici
    protected boolean hasWireless;

    /**
     * Costruttore per un PC portatile.
     * 
     * @param tipoProcessore il tipo di processore
     * @param dimensioneRAM la dimensione della RAM in GB
     * @param dimensioneMemoriaMassa la dimensione della memoria di massa in GB
     * @param marca la marca del PC
     * @param modello il modello del PC
     * @param sistemaOperativo il sistema operativo installato
     * @param peso il peso in kg
     * @param altezza l'altezza in cm
     * @param larghezza la larghezza in cm
     * @param profondita la profondità in cm
     * @param dimensioneVideo la dimensione del video in pollici
     * @param hasWireless presenza di interfaccia wireless
     */
    public PCPortatile(String tipoProcessore, int dimensioneRAM, int dimensioneMemoriaMassa,
                       String marca, String modello, String sistemaOperativo,
                       double peso, double altezza, double larghezza, double profondita,
                       double dimensioneVideo, boolean hasWireless) {
        super(tipoProcessore, dimensioneRAM, dimensioneMemoriaMassa, marca, modello, sistemaOperativo);
        if (peso <= 0) {
            throw new IllegalArgumentException("peso deve essere > 0");
        }
        if (dimensioneVideo <= 0) {
            throw new IllegalArgumentException("dimensioneVideo deve essere > 0");
        }
        this.peso = peso;
        this.altezza = altezza;
        this.larghezza = larghezza;
        this.profondita = profondita;
        this.dimensioneVideo = dimensioneVideo;
        this.hasWireless = hasWireless;
    }

    public double getPeso() {
        return peso;
    }

    public double getAltezza() {
        return altezza;
    }

    public double getLarghezza() {
        return larghezza;
    }

    public double getProfondita() {
        return profondita;
    }

    public double getDimensioneVideo() {
        return dimensioneVideo;
    }

    public boolean hasWireless() {
        return hasWireless;
    }

    @Override
    public String toString() {
        return super.toString() + 
               String.format(", Peso: %.2fkg, Dimensioni: %.1fx%.1fx%.1fcm, Video: %.1f\", WiFi: %s",
                           peso, altezza, larghezza, profondita, dimensioneVideo, hasWireless ? "Sì" : "No");
    }
}
