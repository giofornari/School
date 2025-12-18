
public class Utente {

    private final String nome;
    private final int uid;
    private MetododiPagamento favol;

    public Utente(String nome, int uid) {
        this.nome = nome;
        this.uid = uid;
        this.favol = null;
    }

    public String getNome() {
        return nome;
    }

    public int getIdUser() {
        return uid;
    }

    public MetododiPagamento getPreferito() {
        return favol;
    }

    public void setMetodoPagamentoPreferito(MetododiPagamento mp) {
        this.favol = mp;
    }
    public void effettuaPagamento(double imp, MetododiPagamento mp) {
        MetododiPagamento m = mp;
        if (m == null) {
            return;
        }

        m.setImporto(imp);
        if (m.autorizzaTransazione()) {
            System.out.println(nome + " >> " + m);
        }
    }

    @Override
    public String toString() {
        return nome + " (ID:" + uid + ")";
    }
}