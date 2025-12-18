
public class CartaPremium extends CartadiCredito {

    public CartaPremium(String id, String num, String exp) {
        super(id, num, exp);
    }

    @Override
    public double calcolaCommissione() {
        return amt * 0.015;
    }

    @Override
    public String toString() {
        var comm = calcolaCommissione();
        var tot = amt + comm;
        return String.format("CP [%s %s] ID: %s | Amt: %.2f | Comm: %.2f | Tot: %.2f",
                getNumeroCarta(), getDataScadenza(), id, amt, comm, tot);
    }
}
