/**
 * Classe che rappresenta un PC Desktop.
 * 
 * @author giordii.dev
 */
public class Desktop extends PCFisso {
    private String tipoSchedaVideo;
    private String tipoSchedaAudio;

    /**
     * Costruttore completo per un Desktop.
     * 
     * @param tipoProcessore il tipo di processore
     * @param dimensioneRAM la dimensione della RAM in GB
     * @param dimensioneMemoriaMassa la dimensione della memoria di massa in GB
     * @param marca la marca del PC
     * @param modello il modello del PC
     * @param sistemaOperativo il sistema operativo installato
     * @param tipoCase il tipo di case
     * @param tipoSchedaVideo il tipo di scheda video
     * @param tipoSchedaAudio il tipo di scheda audio
     */
    public Desktop(String tipoProcessore, int dimensioneRAM, int dimensioneMemoriaMassa,
                   String marca, String modello, String sistemaOperativo, String tipoCase,
                   String tipoSchedaVideo, String tipoSchedaAudio) {
        super(tipoProcessore, dimensioneRAM, dimensioneMemoriaMassa, marca, modello, sistemaOperativo, tipoCase);
        this.tipoSchedaVideo = tipoSchedaVideo;
        this.tipoSchedaAudio = tipoSchedaAudio;
    }

    public String getTipoSchedaVideo() {
        return tipoSchedaVideo;
    }

    public String getTipoSchedaAudio() {
        return tipoSchedaAudio;
    }

    @Override
    public String toString() {
        return "[Desktop] " + super.toString() + 
               String.format(", Scheda Video: %s, Scheda Audio: %s", tipoSchedaVideo, tipoSchedaAudio);
    }
}
