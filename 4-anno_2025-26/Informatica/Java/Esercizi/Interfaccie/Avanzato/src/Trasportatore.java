// Interfaccia per mezzi che possono trasportare persone
public interface Trasportatore {
    void carica(int persone);
    void scarica(int persone);
    int getCapacita();
}
