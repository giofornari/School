public class Tecnico extends Personale {
    public enum Area {
        INFORMATICA_TELECOMUNICAZIONI,
        ELETTRONICA_AUTOMAZIONE
    }

    private final Area area;
    private final boolean interno;

    public Tecnico(String codice, String cognome, String nome, int annoAssunzione, Area area, boolean interno) {
        super(codice, cognome, nome, annoAssunzione);
        this.area = area;
        this.interno = interno;
    }

    @Override
    public double getCostoOrario(int annoCorrente) {
        if (!this.interno) {
            return 0; // Solo tecnici interni hanno costo orario
        }

        double costoBase;
        if (this.area == Area.INFORMATICA_TELECOMUNICAZIONI) {
            costoBase = 50.0;
        } else {
            costoBase = 60.0;
        }

        int anniServizio = getAnniServizio(annoCorrente);
        return costoBase - anniServizio;
    }

    @Override
    public String toString() {
        String areaStr = (this.area == Area.INFORMATICA_TELECOMUNICAZIONI) ? "Informatica/Telecomunicazioni" : "Elettronica/Automazione";
        String tipoStr = this.interno ? "interno" : "esterno";
        return super.toString() + " - Tecnico " + areaStr + " (" + tipoStr + ")";
    }
}
