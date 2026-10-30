public abstract class Personale {
    private final String codice;
    private final String cognome;
    private final String nome;
    private final int annoAssunzione;

    public Personale(String codice, String cognome, String nome, int annoAssunzione) {
        this.codice = codice;
        this.cognome = cognome;
        this.nome = nome;
        this.annoAssunzione = annoAssunzione;
    }

    public String getCodice() {
        return this.codice;
    }

    public String getCognome() {
        return this.cognome;
    }

    public String getNome() {
        return this.nome;
    }

    public int getAnnoAssunzione() {
        return this.annoAssunzione;
    }

    public int getAnniServizio(int annoCorrente) {
        return annoCorrente - this.annoAssunzione;
    }

    // Metodo astratto per calcolare il costo orario
    public abstract double getCostoOrario(int annoCorrente);

    @Override
    public String toString() {
        return this.codice + " - " + this.cognome + " " + this.nome + " (assunto nel " + this.annoAssunzione + ")";
    }
}
