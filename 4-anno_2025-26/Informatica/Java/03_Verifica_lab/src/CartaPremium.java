
public class CartaPremium extends CartadiCredito {

    public CartaPremium(int id, String num, String exp) {
        super(id, num, exp);
    }

    @Override
    public double calcolaCommissione() {
        return imp * 0.015;
    }

    @Override
    public String toString() {
        double fee = calcolaCommissione();
        double tot = imp + fee;
        return String.format("CP [%s %s] ID: %s \n\t Importo: %.2f \n\t Commissione: %.2f \n\t Totale: %.2f\n\n",
                getNCarta(), getScadenza(), id, imp, fee, tot);
    }

}