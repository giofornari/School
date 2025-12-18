
import java.util.ArrayList;

public class Transazioni {

    private final ArrayList<Utente> usr;

    public Transazioni() {
        this.usr = new ArrayList<>();
    }

    public void aggiungiUtente(Utente u) {
        usr.add(u);
    }

    public void rimuoviUtente(Utente u) {
        usr.remove(u);
    }

    public void effettuaPagamentoPerTutti(double amt) {
        usr.forEach(u -> u.effettuaPagamento(amt, null));
    }

    public void mostraUtenti() {
        usr.forEach(u -> {
            var mp = u.getMetodoPagamentoPreferito();
            System.out.println(u + " | " + (mp != null ? mp.getClass().getSimpleName() : "None"));
        });
    }
}
