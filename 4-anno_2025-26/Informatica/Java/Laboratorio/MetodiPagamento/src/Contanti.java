// Parte 5: nuovo metodo aggiunto
public class Contanti implements MetodoPagamento {
    
    @Override
    public boolean paga(double importo) {
        if (importo <= 0) {
            System.out.println("Pagamento fallito");
            return false;
        }
        System.out.println("Pagamento in Contanti: " + importo + "€");
        return true;
    }
}
