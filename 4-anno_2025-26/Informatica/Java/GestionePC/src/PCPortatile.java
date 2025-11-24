// Base per portatili
public abstract class PCPortatile extends PC {
    protected double pesoKg;
    protected double altCm;
    protected double largCm;
    protected double profCm;
    protected double diagPol;
    protected boolean wifi;

    public PCPortatile(String tipoProc, int ramGb, int memGb,
                       String marca, String modello, String sistOp,
                       double pesoKg, double altCm, double largCm, double profCm,
                       double diagPol, boolean wifi) {
        super(tipoProc, ramGb, memGb, marca, modello, sistOp);
        if (pesoKg <= 0) {
            throw new IllegalArgumentException("pesoKg deve essere > 0");
        }
        if (diagPol <= 0) {
            throw new IllegalArgumentException("diagPol deve essere > 0");
        }
        this.pesoKg = pesoKg;
        this.altCm = altCm;
        this.largCm = largCm;
        this.profCm = profCm;
        this.diagPol = diagPol;
        this.wifi = wifi;
    }

    public double getPesoKg() {
        return pesoKg;
    }

    public double getAltCm() {
        return altCm;
    }

    public double getLargCm() {
        return largCm;
    }

    public double getProfCm() {
        return profCm;
    }

    public double getDiagPol() {
        return diagPol;
    }

    public boolean hasWifi() {
        return wifi;
    }

    @Override
    public String toString() {
        return super.toString() +
               String.format(", Peso: %.2fkg, Dimensioni: %.1fx%.1fx%.1fcm, Video: %.1f\", WiFi: %s",
                           pesoKg, altCm, largCm, profCm, diagPol, wifi ? "Sì" : "No");
    }
}
