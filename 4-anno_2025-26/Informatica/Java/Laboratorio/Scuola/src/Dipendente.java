import java.time.LocalDate;

public abstract class Dipendente {
    protected String nome;
    protected char sesso;
    protected LocalDate birth;
    protected double base;

    
    public Dipendente(String nome, char sesso, LocalDate birth, double base) {
        this.nome = nome;
        this.sesso = sesso;
        this.birth = birth;
        this.base = base;
    }
    public String getNome() {
        return nome;
    }
    public void setNome(String nome) {
        this.nome = nome;
    }
    public char getSesso() {
        return sesso;
    }
    public void setSesso(char sesso) {
        this.sesso = sesso;
    }
    public LocalDate getBirth() {
        return birth;
    }
    public void setBirth(LocalDate birth) {
        this.birth = birth;
    }
    public double getBase() {
        return base;
    }
    public void setBase(double base) {
        this.base = base;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("Dipendente{");
        sb.append("nome=").append(nome);
        sb.append(", sesso=").append(sesso);
        sb.append(", birth=").append(birth);
        sb.append(", base=").append(base);
        sb.append('}');
        return sb.toString();
    }

    public abstract double calcolaStipendio();
}
