// Server rack / tower
public class Server extends PCFisso {
    private int numProc;
    private boolean raid;

    public Server(String tipoProc, int ramGb, int memGb,
                  String marca, String modello, String sistOp, String tipoCab,
                  int numProc, boolean raid) {
        super(tipoProc, ramGb, memGb, marca, modello, sistOp, tipoCab);
        if (numProc <= 0) {
            throw new IllegalArgumentException("numProc deve essere > 0");
        }
        this.numProc = numProc;
        this.raid = raid;
    }

    public int getNumProc() {
        return numProc;
    }

    public boolean hasRaid() {
        return raid;
    }

    @Override
    public String toString() {
        return "[Server] " + super.toString() +
               String.format(", Processori: %d, RAID: %s", numProc, raid ? "Sì" : "No");
    }
}
