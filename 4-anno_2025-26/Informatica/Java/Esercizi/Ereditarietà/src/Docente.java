class Docente extends Persona {
    private String materia;
    private double salario;

    public Docente() {
    }

    public Docente(String codiceFiscale, String nome, String cognome,
                   String materia, double salario) {
        super(codiceFiscale, nome, cognome);
        this.materia = materia;
        this.salario = salario;
    }

    public String getMateria() {
        return materia;
    }

    public void setMateria(String materia) {
        this.materia = materia;
    }

    public double getSalario() {
        return salario;
    }

    public void setSalario(double salario) {
        this.salario = salario;
    }

    @Override
    public String toString() {
        return "Docente{" +
                "codiceFiscale='" + getCodiceFiscale() + '\'' +
                ", nome='" + getNome() + '\'' +
                ", cognome='" + getCognome() + '\'' +
                ", materia='" + materia + '\'' +
                ", salario=" + salario +
                '}';
    }
}
