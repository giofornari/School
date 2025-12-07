// Palmare compatto
public class Palmare extends PCPortatile {
    private boolean bt;
    private String slotMem;

    public Palmare(String tipoProc, int ramGb, int memGb,
                   String marca, String modello, String sistOp,
                   double pesoKg, double altCm, double largCm, double profCm,
                   double diagPol, boolean wifi,
                   boolean bt, String slotMem) {
        super(tipoProc, ramGb, memGb, marca, modello, sistOp,
              pesoKg, altCm, largCm, profCm, diagPol, wifi);
        this.bt = bt;
        this.slotMem = slotMem;
    }

    public boolean hasBt() {
        return bt;
    }

    public String getSlotMem() {
        return slotMem;
    }

    @Override
    public String toString() {
        return "[Palmare] " + super.toString() +
               String.format(", Bluetooth: %s, Espansione: %s",
                           bt ? "Sì" : "No", slotMem);
    }
}
