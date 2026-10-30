
import java.util.ArrayList;

public class Transazioni {
    // godo vsxcode che mi dice quando usare final
    private final ArrayList<Utente> user;

    public Transazioni() {
        this.user = new ArrayList<>();
    }

    public void aggiungiUtente(Utente u) {
        user.add(u);
    }

    public void rimuoviUtente(Utente u) {
        user.remove(u);
    }

    public void effettuaPagamentoPerTutti(double imp) {
        user.forEach(u -> u.effettuaPagamento(imp, null));
    }
    /**
     * funct per info su utenti
     */
    public void mostraUtenti() {
        user.forEach(u -> {
            MetododiPagamento mp = u.getPreferito();
            System.out.println(u + " >> " + (mp.getClass().getSimpleName()) + "\n"); // posso usare il nome dellla classe invece di fare una funzione apposta
        });
    }
}