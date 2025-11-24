/**
 * Classe astratta che rappresenta un PC generico.
 * Contiene gli attributi comuni a tutti i tipi di PC.
 * 
 * @author giordii.dev
 */
public abstract class PC {
    protected String tipoProcessore;
    protected int dimensioneRAM; // in GB
    protected int dimensioneMemoriaMassa; // in GB
    protected String marca;
    protected String modello;
    protected String sistemaOperativo;

    /**
     * Costruttore completo per un PC.
     * 
     * @param tipoProcessore il tipo di processore
     * @param dimensioneRAM la dimensione della RAM in GB
     * @param dimensioneMemoriaMassa la dimensione della memoria di massa in GB
     * @param marca la marca del PC
     * @param modello il modello del PC
     * @param sistemaOperativo il sistema operativo installato
     */
    public PC(String tipoProcessore, int dimensioneRAM, int dimensioneMemoriaMassa,
              String marca, String modello, String sistemaOperativo) {
        if (dimensioneRAM <= 0) {
            throw new IllegalArgumentException("dimensioneRAM deve essere > 0");
        }
        if (dimensioneMemoriaMassa <= 0) {
            throw new IllegalArgumentException("dimensioneMemoriaMassa deve essere > 0");
        }
        this.tipoProcessore = tipoProcessore;
        this.dimensioneRAM = dimensioneRAM;
        this.dimensioneMemoriaMassa = dimensioneMemoriaMassa;
        this.marca = marca;
        this.modello = modello;
        this.sistemaOperativo = sistemaOperativo;
    }

    // Getter methods
    public String getTipoProcessore() {
        return tipoProcessore;
    }

    public int getDimensioneRAM() {
        return dimensioneRAM;
    }

    public int getDimensioneMemoriaMassa() {
        return dimensioneMemoriaMassa;
    }

    public String getMarca() {
        return marca;
    }

    public String getModello() {
        return modello;
    }

    public String getSistemaOperativo() {
        return sistemaOperativo;
    }

    @Override
    public String toString() {
        return String.format("Marca: %s, Modello: %s, CPU: %s, RAM: %dGB, Memoria: %dGB, OS: %s",
                marca, modello, tipoProcessore, dimensioneRAM, dimensioneMemoriaMassa, sistemaOperativo);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        PC pc = (PC) o;
        return marca.equals(pc.marca) && modello.equals(pc.modello);
    }
}
