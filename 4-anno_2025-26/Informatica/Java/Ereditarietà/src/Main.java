public class Main {
    public static void main(String[] args) {
        Studente studente = new Studente("RSSMRA80A01H501U", "Mario", "Rossi",
                "S12345", "Universita degli Studi");
        Docente docente = new Docente("BNCLRA70B41H501K", "Laura", "Bianchi",
                "Programmazione", 2800.00);

        System.out.println(studente);
        System.out.println(docente);
    }
}
