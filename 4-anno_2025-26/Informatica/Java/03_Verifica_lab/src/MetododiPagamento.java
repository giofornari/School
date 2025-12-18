public abstract class MetododiPagamento {

    protected int id;
    protected double imp;

    public MetododiPagamento(int id) {
        this.id = id;
        this.imp = 0.0;
    }

    public void setImporto(double imp) {
        this.imp = imp;
    }

    public double getImporto() {
        return imp;
    }

    public int getId() {
        return id;
    }
    /**
     * se importo > 0 >> print ok
     * @return true se ok
     */
    public boolean autorizzaTransazione() {
        if (imp > 0) {
            System.out.println("OK per importo: " + imp);
            return true;
        }
        return false;
    }

    public abstract double calcolaCommissione();

    /**
     * print dei dettagli su pagamento
     * @return info su tranzxazione
     */
    @Override
    public String toString() {
        double fee = calcolaCommissione();
        double tot = imp + fee;
        return String.format("\n\tID: %s \n\t importo: %.2f \n\t commissioni: %.2f \n\t totale: %.2f\n\n", id, imp, fee, tot);
    }
}