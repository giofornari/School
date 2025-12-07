import java.util.ArrayList;

// Gestione composizione treno
public class Treno {
    private final String nome;
    private final ArrayList<Vagone> vagoni;

    public Treno(String nome) {
        if (nome == null || nome.trim().isEmpty()) {
            throw new IllegalArgumentException("nome non vuoto");
        }
        this.nome = nome;
        this.vagoni = new ArrayList<>();
    }

    public void addVag(Vagone vagone) {
        if (vagone == null) {
            throw new NullPointerException("vagone != null");
        }
        vagoni.add(vagone);
    }

    public double totPeso() {
        double pesoTotale = 0.0;
        for (Vagone vagone : vagoni) {
            pesoTotale += vagone.totPeso();
        }
        return pesoTotale;
    }

    public int numVag() {
        return vagoni.size();
    }

    public int numVagPass() {
        int count = 0;
        for (Vagone vagone : vagoni) {
            if (vagone instanceof VagonePasseggeri) {
                count++;
            }
        }
        return count;
    }

    public int numVagMerci() {
        int count = 0;
        for (Vagone vagone : vagoni) {
            if (vagone instanceof VagoneMerci) {
                count++;
            }
        }
        return count;
    }

    public int getPassTot() {
        int capacita = 0;
        for (Vagone vagone : vagoni) {
            if (vagone instanceof VagonePasseggeri) {
                capacita += ((VagonePasseggeri) vagone).getTotSeats();
            }
        }
        return capacita;
    }

    public int getPassOcc() {
        int occupati = 0;
        for (Vagone vagone : vagoni) {
            if (vagone instanceof VagonePasseggeri) {
                occupati += ((VagonePasseggeri) vagone).getOccSeats();
            }
        }
        return occupati;
    }

    public ArrayList<Vagone> getVagoni() {
        return new ArrayList<>(vagoni);
    }

    public String getNome() {
        return nome;
    }

    @Override
    public String toString() {
        return String.format("Treno '%s' - Vagoni: %d (Passeggeri: %d, Merci: %d), Peso complessivo: %.2f kg",
                nome, numVag(), numVagPass(), 
                numVagMerci(), totPeso());
    }
}
