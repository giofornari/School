/**
 * Classe astratta che rappresenta un PC fisso.
 * Estende la classe PC aggiungendo il tipo di case.
 * 
 * @author giordii.dev
 */
public abstract class PCFisso extends PC {
    protected String tipoCase; // grande, medio, piccolo

    /**
     * Costruttore per un PC fisso.
     * 
     * @param tipoProcessore il tipo di processore
     * @param dimensioneRAM la dimensione della RAM in GB
     * @param dimensioneMemoriaMassa la dimensione della memoria di massa in GB
     * @param marca la marca del PC
     * @param modello il modello del PC
     * @param sistemaOperativo il sistema operativo installato
     * @param tipoCase il tipo di case (grande, medio, piccolo)
     */
    public PCFisso(String tipoProcessore, int dimensioneRAM, int dimensioneMemoriaMassa,
                   String marca, String modello, String sistemaOperativo, String tipoCase) {
        super(tipoProcessore, dimensioneRAM, dimensioneMemoriaMassa, marca, modello, sistemaOperativo);
        this.tipoCase = tipoCase;
    }

    public String getTipoCase() {
        return tipoCase;
    }

    @Override
    public String toString() {
        return super.toString() + String.format(", Case: %s", tipoCase);
    }
}
