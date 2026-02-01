public abstract class Personale {
    private String codice;
    private String cognome;
    private String nome;
    private int annoAssunzione;

    public Personale(String codice, String cognome, String nome, int annoAssunzione) {
        this.codice = codice;
        this.cognome = cognome;
        this.nome = nome;
        this.annoAssunzione = annoAssunzione;
    }

    public String getCodice() {
        return codice;
    }

    public String getCognome() {
        return cognome;
    }

    public String getNome() {
        return nome;
    }

    public int getAnnoAssunzione() {
        return annoAssunzione;
    }

    public int getAnniServizio(int annoCorrente) {
        return annoCorrente - annoAssunzione;
    }

    // Metodo astratto per calcolare il costo orario
    public abstract double getCostoOrario(int annoCorrente);

    @Override
    public String toString() {
        return codice + " - " + cognome + " " + nome + " (assunto nel " + annoAssunzione + ")";
    }
}
