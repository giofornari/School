/**
 * Classe che rappresenta un Notebook.
 * 
 * @author giordii.dev
 */
public class Notebook extends PCPortatile {
    private boolean hasWebcam;
    private double risoluzioneWebcam; // in megapixel (0 se non ha webcam)

    /**
     * Costruttore completo per un Notebook.
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
     * @param hasWebcam presenza di webcam
     * @param risoluzioneWebcam risoluzione della webcam in megapixel (0 se non ha webcam)
     */
    public Notebook(String tipoProcessore, int dimensioneRAM, int dimensioneMemoriaMassa,
                    String marca, String modello, String sistemaOperativo,
                    double peso, double altezza, double larghezza, double profondita,
                    double dimensioneVideo, boolean hasWireless,
                    boolean hasWebcam, double risoluzioneWebcam) {
        super(tipoProcessore, dimensioneRAM, dimensioneMemoriaMassa, marca, modello, sistemaOperativo,
              peso, altezza, larghezza, profondita, dimensioneVideo, hasWireless);
        this.hasWebcam = hasWebcam;
        this.risoluzioneWebcam = hasWebcam ? risoluzioneWebcam : 0;
    }

    public boolean hasWebcam() {
        return hasWebcam;
    }

    public double getRisoluzioneWebcam() {
        return risoluzioneWebcam;
    }

    @Override
    public String toString() {
        String webcamInfo = hasWebcam ? 
            String.format("Webcam: Sì (%.1fMP)", risoluzioneWebcam) : "Webcam: No";
        return "[Notebook] " + super.toString() + ", " + webcamInfo;
    }
}
