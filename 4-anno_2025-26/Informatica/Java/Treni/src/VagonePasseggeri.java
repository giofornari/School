// Vagone passeggeri
public class VagonePasseggeri extends Vagone {
    public static double avgPeso = 65.0;
    
    private final int classe;
    private final int totSeats;
    private int occSeats;

    public VagonePasseggeri(String id, double tara, String manufactor, 
                           int created, int classe, int totSeats, 
                           int occSeats) {
        super(id, tara, manufactor, created);
        
        if (classe < 1 || classe > 2) {
            throw new IllegalArgumentException("classe 1 o 2");
        }
        if (totSeats <= 0) {
            throw new IllegalArgumentException("posti disponibili > 0");
        }
        if (occSeats < 0) {
            throw new IllegalArgumentException("posti occupati >= 0");
        }
        if (occSeats > totSeats) {
            throw new IllegalArgumentException("occupati <= disponibili");
        }
        
        this.classe = classe;
        this.totSeats = totSeats;
        this.occSeats = occSeats;
    }

    @Override
    public double totPeso() {
        return tara + (occSeats * avgPeso);
    }

    public int getClasse() {
        return classe;
    }

    public int getTotSeats() {
        return totSeats;
    }

    public int getOccSeats() {
        return occSeats;
    }

    public void setOccSeats(int occSeats) {
        if (occSeats < 0) {
            throw new IllegalArgumentException("posti occupati >= 0");
        }
        if (occSeats > totSeats) {
            throw new IllegalArgumentException("occupati <= disponibili");
        }
        this.occSeats = occSeats;
    }

    @Override
    public String toString() {
        return String.format("VAGONE PASSEGGERI - %s, Classe: %d, Posti: %d/%d, Peso totale: %.2f kg",
                super.toString(), classe, occSeats, totSeats, totPeso());
    }
}
