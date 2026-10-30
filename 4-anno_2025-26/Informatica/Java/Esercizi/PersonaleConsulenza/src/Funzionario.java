public class Funzionario extends Personale {
    public Funzionario(String codice, String cognome, String nome, int annoAssunzione) {
        super(codice, cognome, nome, annoAssunzione);
    }

    @Override
    public double getCostoOrario(int annoCorrente) {
        int anniServizio = getAnniServizio(annoCorrente);
        if (anniServizio < 10) {
            return 75.0; // Junior
        } else {
            return 85.0; // Senior
        }
    }

    @Override
    public String toString() {
        return super.toString() + " - Funzionario";
    }
}
