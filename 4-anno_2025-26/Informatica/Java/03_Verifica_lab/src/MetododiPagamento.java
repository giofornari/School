
public abstract class MetododiPagamento {

    protected String id;
    protected double amt;

    public MetododiPagamento(String id) {
        this.id = id;
        this.amt = 0.0;
    }

    public void setImporto(double amt) {
        this.amt = amt;
    }

    public double getImporto() {
        return amt;
    }

    public String getIdentificativo() {
        return id;
    }

    public boolean autorizzaTransazione() {
        return amt > 0;
    }

    public abstract double calcolaCommissione();

    @Override
    public String toString() {
        var comm = calcolaCommissione();
        var tot = amt + comm;
        return String.format("ID: %s | Amt: %.2f | Comm: %.2f | Tot: %.2f", id, amt, comm, tot);
    }
}
