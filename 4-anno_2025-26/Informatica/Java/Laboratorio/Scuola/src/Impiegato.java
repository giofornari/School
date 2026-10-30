
import java.time.LocalDate;

public class Impiegato extends Dipendente {

    private int livello;

    public Impiegato(String nome, char sesso, LocalDate birth, int livello, double base) {
        super(nome, sesso, birth, base);
        this.livello = livello;
    }

    public int getLivello() {
        return livello;
    }

    public void setLivello(int livello) {
        this.livello = livello;
    }

    @Override
    public String toString() {
        return "Impiegato{" + "nome='" + nome + "', sesso=" + sesso
                + ", dataNascita=" + birth + ", livello=" + livello
                + ", stipendioBase=" + base + "}";
    }

    @Override
    public double calcolaStipendio() {
        return base;
    }
}
