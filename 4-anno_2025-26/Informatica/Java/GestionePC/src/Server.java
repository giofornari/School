/**
 * Classe che rappresenta un Server.
 * 
 * @author giordii.dev
 */
public class Server extends PCFisso {
    private int numeroProcessori;
    private boolean hasRaid;

    /**
     * Costruttore completo per un Server.
     * 
     * @param tipoProcessore il tipo di processore
     * @param dimensioneRAM la dimensione della RAM in GB
     * @param dimensioneMemoriaMassa la dimensione della memoria di massa in GB
     * @param marca la marca del PC
     * @param modello il modello del PC
     * @param sistemaOperativo il sistema operativo installato
     * @param tipoCase il tipo di case
     * @param numeroProcessori il numero di processori
     * @param hasRaid presenza di dischi RAID
     */
    public Server(String tipoProcessore, int dimensioneRAM, int dimensioneMemoriaMassa,
                  String marca, String modello, String sistemaOperativo, String tipoCase,
                  int numeroProcessori, boolean hasRaid) {
        super(tipoProcessore, dimensioneRAM, dimensioneMemoriaMassa, marca, modello, sistemaOperativo, tipoCase);
        if (numeroProcessori <= 0) {
            throw new IllegalArgumentException("numeroProcessori deve essere > 0");
        }
        this.numeroProcessori = numeroProcessori;
        this.hasRaid = hasRaid;
    }

    public int getNumeroProcessori() {
        return numeroProcessori;
    }

    public boolean hasRaid() {
        return hasRaid;
    }

    @Override
    public String toString() {
        return "[Server] " + super.toString() + 
               String.format(", Processori: %d, RAID: %s", numeroProcessori, hasRaid ? "Sì" : "No");
    }
}
