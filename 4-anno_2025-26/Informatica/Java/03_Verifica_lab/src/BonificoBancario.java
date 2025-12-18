
public class BonificoBancario extends MetododiPagamento {

    private final String iban;

    public BonificoBancario(String id, String iban) {
        super(id);
        this.iban = iban;
    }

    public String getIbanBeneficiario() {
        return iban;
    }

    @Override
    public double calcolaCommissione() {
        return 2.50;
    }

    @Override
    public String toString() {
        return "BB [" + iban + "] " + super.toString();
    }
}
