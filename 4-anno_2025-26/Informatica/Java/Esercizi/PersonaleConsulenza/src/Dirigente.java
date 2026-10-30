public class Dirigente extends Personale {
    public Dirigente(String codice, String cognome, String nome, int annoAssunzione) {
        super(codice, cognome, nome, annoAssunzione);
    }

    @Override
    public double getCostoOrario(int annoCorrente) {
        return 100.0; // Sempre 100 €/ora
    }

    @Override
    public String toString() {
        return super.toString() + " - Dirigente";
    }
}
