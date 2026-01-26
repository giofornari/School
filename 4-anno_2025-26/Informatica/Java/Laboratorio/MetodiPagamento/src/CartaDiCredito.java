public class CartaDiCredito implements MetodoPagamento {
    
    @Override
    public boolean paga(double importo) {
        if (importo <= 0) {
            System.out.println("Pagamento fallito");
            return false;
        }
        System.out.println("Pagamento con Carta di Credito: " + importo + "€");
        return true;
    }
}
