public class Main {
    static void main() {
        Progetto progetto = new Progetto("Progetto Test", 2026);

        progetto.aggiungiMembro(new Dirigente("D001", "Rossi", "Mario", 2010), 50);
        progetto.aggiungiMembro(new Funzionario("F001", "Bianchi", "Luigi", 2020), 100);
        progetto.aggiungiMembro(new Tecnico("T001", "Verdi", "Anna", 2018, Tecnico.Area.INFORMATICA_TELECOMUNICAZIONI, true), 150);

        progetto.stampaDettagliCosti();
    }
}
