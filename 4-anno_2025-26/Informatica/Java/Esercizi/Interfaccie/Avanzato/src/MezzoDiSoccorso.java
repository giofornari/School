// Mezzo di soccorso che pu\u00f2 volare, navigare, trasportare persone
// Implementa 4 interfacce diverse
public class MezzoDiSoccorso implements Volante, Navigabile, Trasportatore, Motorizzato {
    private String nome;
    private int capacita;
    private int personeABordo;
    private boolean motore;
    
    public MezzoDiSoccorso(String nome, int capacita) {
        this.nome = nome;
        this.capacita = capacita;
        this.personeABordo = 0;
        this.motore = false;
    }
    
    // Metodi di Volante
    @Override
    public void vola() {
        System.out.println(nome + " decolla e vola");
    }
    
    @Override
    public void atterra() {
        System.out.println(nome + " atterra");
    }
    
    // Metodi di Navigabile
    @Override
    public void naviga() {
        System.out.println(nome + " naviga sull'acqua");
    }
    
    @Override
    public void attracca() {
        System.out.println(nome + " attracca al porto");
    }
    
    // Metodi di Trasportatore
    @Override
    public void carica(int persone) {
        if (personeABordo + persone <= capacita) {
            personeABordo += persone;
            System.out.println("Caricate " + persone + " persone. Totale: " + personeABordo);
        } else {
            System.out.println("Capacita massima raggiunta");
        }
    }
    
    @Override
    public void scarica(int persone) {
        if (persone <= personeABordo) {
            personeABordo -= persone;
            System.out.println("Scaricate " + persone + " persone. Rimangono: " + personeABordo);
        } else {
            System.out.println("Non ci sono cosi tante persone a bordo");
        }
    }
    
    @Override
    public int getCapacita() {
        return capacita;
    }
    
    // Metodi di Motorizzato
    @Override
    public void accendiMotore() {
        motore = true;
        System.out.println("Motore di " + nome + " acceso");
    }
    
    @Override
    public void spegniMotore() {
        motore = false;
        System.out.println("Motore di " + nome + " spento");
    }
    
    @Override
    public boolean motoreAcceso() {
        return motore;
    }
    
    public String getNome() {
        return nome;
    }
}
