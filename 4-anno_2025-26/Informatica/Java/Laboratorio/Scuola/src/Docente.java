
import java.time.LocalDate;

public class Docente extends Dipendente {

    private int nOreDocenza;

    public Docente(String nome, char sesso, LocalDate birth, int nOreDocenza, double base) {
        super(nome, sesso, birth, base);
        this.nOreDocenza = nOreDocenza;
    }

    public int getNOreDocenza() {
        return nOreDocenza;
    }

    public void setNOreDocenza(int nOreDocenza) {
        this.nOreDocenza = nOreDocenza;
    }

    @Override
    public String toString() {
        return "Docente{" + "nome='" + nome + "', sesso=" + sesso
                + ", dataNascita=" + birth + ", oreDocenza=" + nOreDocenza
                + ", stipendioBase=" + base + "}";
    }

    @Override
    public double calcolaStipendio() {
        return base;
    }
}
