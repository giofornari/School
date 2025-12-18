
public class CartadiCredito extends MetododiPagamento {

    private final String num;
    private final String exp;

    public CartadiCredito(int id, String num, String exp) {
        super(id);
        this.num = num;
        this.exp = exp;
    }

    public String getNCarta() {
        return num;
    }

    public String getScadenza() {
        return exp;
    }

    @Override
    public double calcolaCommissione() {
        return imp * 0.02;
    }

    @Override
    public String toString() {
        return "CC [" + num + " " + exp + "] " + super.toString();
    }
}
