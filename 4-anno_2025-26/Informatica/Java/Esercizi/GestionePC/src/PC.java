// PC base astratto
public abstract class PC {
    protected String tipoProc;
    protected int ramGb;
    protected int memGb;
    protected String marca;
    protected String modello;
    protected String sistOp;

    public PC(String tipoProc, int ramGb, int memGb,
              String marca, String modello, String sistOp) {
        if (ramGb <= 0) {
            throw new IllegalArgumentException("ramGb deve essere > 0");
        }
        if (memGb <= 0) {
            throw new IllegalArgumentException("memGb deve essere > 0");
        }
        this.tipoProc = tipoProc;
        this.ramGb = ramGb;
        this.memGb = memGb;
        this.marca = marca;
        this.modello = modello;
        this.sistOp = sistOp;
    }

    public String getTipoProc() {
        return tipoProc;
    }

    public int getRamGb() {
        return ramGb;
    }

    public int getMemGb() {
        return memGb;
    }

    public String getMarca() {
        return marca;
    }

    public String getModello() {
        return modello;
    }

    public String getSistOp() {
        return sistOp;
    }

    @Override
    public String toString() {
        return String.format("Marca: %s, Modello: %s, CPU: %s, RAM: %dGB, Memoria: %dGB, OS: %s",
                marca, modello, tipoProc, ramGb, memGb, sistOp);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        PC pc = (PC) o;
        return marca.equals(pc.marca) && modello.equals(pc.modello);
    }
}
