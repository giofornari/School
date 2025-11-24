/**
 * Classe che rappresenta un Palmare.
 * 
 * @author giordii.dev
 */
public class Palmare extends PCPortatile {
    private boolean hasBluetooth;
    private String tipoEspansioneMemoria; // es. SD, mini-SD, micro-SD

    /**
     * Costruttore completo per un Palmare.
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
     * @param hasBluetooth presenza di interfaccia Bluetooth
     * @param tipoEspansioneMemoria tipo di espansione della memoria
     */
    public Palmare(String tipoProcessore, int dimensioneRAM, int dimensioneMemoriaMassa,
                   String marca, String modello, String sistemaOperativo,
                   double peso, double altezza, double larghezza, double profondita,
                   double dimensioneVideo, boolean hasWireless,
                   boolean hasBluetooth, String tipoEspansioneMemoria) {
        super(tipoProcessore, dimensioneRAM, dimensioneMemoriaMassa, marca, modello, sistemaOperativo,
              peso, altezza, larghezza, profondita, dimensioneVideo, hasWireless);
        this.hasBluetooth = hasBluetooth;
        this.tipoEspansioneMemoria = tipoEspansioneMemoria;
    }

    public boolean hasBluetooth() {
        return hasBluetooth;
    }

    public String getTipoEspansioneMemoria() {
        return tipoEspansioneMemoria;
    }

    @Override
    public String toString() {
        return "[Palmare] " + super.toString() + 
               String.format(", Bluetooth: %s, Espansione: %s", 
                           hasBluetooth ? "Sì" : "No", tipoEspansioneMemoria);
    }
}
