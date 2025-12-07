// Vagone merci
public class VagoneMerci extends Vagone {
    private final double vol;
    private final double maxLoad;
    private double effLoad;

    public VagoneMerci(String id, double tara, String manufactor, 
                      int created, double vol, double maxLoad, 
                      double effLoad) {
        super(id, tara, manufactor, created);
        
        if (vol <= 0) {
            throw new IllegalArgumentException("volume carico > 0");
        }
        if (maxLoad <= 0) {
            throw new IllegalArgumentException("peso max carico > 0");
        }
        if (effLoad < 0) {
            throw new IllegalArgumentException("peso effettivo >= 0");
        }
        if (effLoad > maxLoad) {
            throw new IllegalArgumentException("effettivo <= massimo");
        }
        
        this.vol = vol;
        this.maxLoad = maxLoad;
        this.effLoad = effLoad;
    }

    @Override
    public double totPeso() {
        return tara + effLoad;
    }

    public double getVol() {
        return vol;
    }

    public double getMaxLoad() {
        return maxLoad;
    }

    public double getEffLoad() {
        return effLoad;
    }

    public void setEffLoad(double effLoad) {
        if (effLoad < 0) {
            throw new IllegalArgumentException("peso effettivo >= 0");
        }
        if (effLoad > maxLoad) {
            throw new IllegalArgumentException("effettivo <= massimo");
        }
        this.effLoad = effLoad;
    }

    @Override
    public String toString() {
        return String.format("VAGONE MERCI - %s, Volume: %.2f m³, Carico: %.2f/%.2f kg, Peso totale: %.2f kg",
                super.toString(), vol, effLoad, maxLoad, totPeso());
    }
}
