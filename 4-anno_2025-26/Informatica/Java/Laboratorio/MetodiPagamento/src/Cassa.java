import java.util.ArrayList;

public class Cassa {

    public static void main(String[] args) {
        
        // Parte 4: variabile MetodoPagamento + polimorfismo
        MetodoPagamento pagamento;

        pagamento = new CartaDiCredito();
        pagamento.paga(50.0);

        pagamento = new PayPal();
        pagamento.paga(30.0);

        pagamento = new BuonoRegalo();
        pagamento.paga(20.0);

        // Parte 5: nuovo metodo
        pagamento = new Contanti();
        pagamento.paga(15.0);

        // Parte 5: fallimento pagamento
        pagamento.paga(-5.0);

        // Parte 5: lista pagamenti
        ArrayList<MetodoPagamento> lista = new ArrayList<>();
        lista.add(new CartaDiCredito());
        lista.add(new PayPal());
        lista.add(new BuonoRegalo());
        lista.add(new Contanti());

        for (MetodoPagamento m : lista) {
            m.paga(10.0);
        }
    }
}
