
public class CartadiCredito extends MetododiPagamento {

    private final String num;
    private final String exp;

    public CartadiCredito(String id, String num, String exp) {
        super(id);
        this.num = num;
        this.exp = exp;
    }

    public String getNumeroCarta() {
        return num;
    }

    public String getDataScadenza() {
        return exp;
    }

    @Override
    public double calcolaCommissione() {
        return amt * 0.02;
    }

    @Override
    public String toString() {
        return "CC [" + num + " " + exp + "] " + super.toString();
    }
}
