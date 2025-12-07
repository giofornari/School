
import java.time.LocalDate;

public class ImpiegatoStraordinario extends Impiegato {

    private int oreStraordinario;
    private static double retribuzioneOraria = 15.0;

    public ImpiegatoStraordinario(String nome, char sesso, LocalDate birth, int livello,
            double base, int oreStraordinario) {
        super(nome, sesso, birth, livello, base);
        this.oreStraordinario = oreStraordinario;
    }

    public int getOreStraordinario() {
        return oreStraordinario;
    }

    public void setOreStraordinario(int oreStraordinario) {
        this.oreStraordinario = oreStraordinario;
    }

    public static double getRetribuzioneOraria() {
        return retribuzioneOraria;
    }

    public static void setRetribuzioneOraria(double retribuzioneOraria) {
        ImpiegatoStraordinario.retribuzioneOraria = retribuzioneOraria;
    }

    @Override
    public String toString() {
        return "ImpiegatoStraordinario{" + "nome='" + nome + "', sesso=" + sesso
                + ", dataNascita=" + birth + ", livello=" + getLivello()
                + ", stipendioBase=" + base + ", oreStraordinario=" + oreStraordinario
                + ", retribuzioneOraria=" + retribuzioneOraria + "}";
    }

    @Override
    public double calcolaStipendio() {
        return base + (oreStraordinario * retribuzioneOraria);
    }
}
