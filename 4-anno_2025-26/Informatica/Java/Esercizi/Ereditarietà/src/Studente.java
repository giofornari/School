class Studente extends Persona {
    private String matricola;
    private String universita;

    public Studente() {
    }

    public Studente(String codiceFiscale, String nome, String cognome,
                    String matricola, String universita) {
        super(codiceFiscale, nome, cognome);
        this.matricola = matricola;
        this.universita = universita;
    }

    public String getMatricola() {
        return matricola;
    }

    public void setMatricola(String matricola) {
        this.matricola = matricola;
    }

    public String getUniversita() {
        return universita;
    }

    public void setUniversita(String universita) {
        this.universita = universita;
    }

    @Override
    public String toString() {
        return "Studente{" +
                "codiceFiscale='" + getCodiceFiscale() + '\'' +
                ", nome='" + getNome() + '\'' +
                ", cognome='" + getCognome() + '\'' +
                ", matricola='" + matricola + '\'' +
                ", universita='" + universita + '\'' +
                '}';
    }
}
