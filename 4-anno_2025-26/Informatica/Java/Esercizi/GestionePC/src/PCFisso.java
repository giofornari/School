// Base per PC fissi
public abstract class PCFisso extends PC {
    protected String tipoCab;

    public PCFisso(String tipoProc, int ramGb, int memGb,
                   String marca, String modello, String sistOp, String tipoCab) {
        super(tipoProc, ramGb, memGb, marca, modello, sistOp);
        this.tipoCab = tipoCab;
    }

    public String getTipoCab() {
        return tipoCab;
    }

    @Override
    public String toString() {
        return super.toString() + String.format(", Case: %s", tipoCab);
    }
}
