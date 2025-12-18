
public class Utente {

    private final String nm;
    private final int uid;
    private MetododiPagamento pref;

    public Utente(String nm, int uid) {
        this.nm = nm;
        this.uid = uid;
        this.pref = null;
    }

    public String getNome() {
        return nm;
    }

    public int getIdUtente() {
        return uid;
    }

    public MetododiPagamento getMetodoPagamentoPreferito() {
        return pref;
    }

    public void setMetodoPagamentoPreferito(MetododiPagamento mp) {
        this.pref = mp;
    }

    public void effettuaPagamento(double amt, MetododiPagamento mp) {
        var m = mp != null ? mp : pref;
        if (m == null) {
            return;
        }

        m.setImporto(amt);
        if (m.autorizzaTransazione()) {
            System.out.println(nm + " -> " + m);
        }
    }

    @Override
    public String toString() {
        return nm + " (ID:" + uid + ")";
    }
}
