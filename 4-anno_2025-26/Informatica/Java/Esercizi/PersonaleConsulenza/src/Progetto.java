import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Progetto {
    private final String nomeProgetto;
    private final List<Personale> membri;
    private final Map<String, Integer> oreAssegnate; // Mappa codice -> ore di attività
    private final int annoCorrente;

    public Progetto(String nomeProgetto, int annoCorrente) {
        this.nomeProgetto = nomeProgetto;
        this.annoCorrente = annoCorrente;
        this.membri = new ArrayList<>();
        this.oreAssegnate = new HashMap<>();
    }

    // Aggiunge un membro al progetto con le ore previste
    public void aggiungiMembro(Personale membro, int ore) {
        this.membri.add(membro);
        this.oreAssegnate.put(membro.getCodice(), ore);
    }

    // Calcola il costo complessivo del progetto
    public double calcolaCostoComplessivo() {
        double costoTotale = 0.0;

        for (Personale membro : this.membri) {
            int ore = this.oreAssegnate.get(membro.getCodice());
            double costoOrario = membro.getCostoOrario(this.annoCorrente);
            double costoMembro = ore * costoOrario;
            costoTotale += costoMembro;
        }

        return costoTotale;
    }

    // Restituisce i dettagli del costo per ogni membro
    public void stampaDettagliCosti() {
        System.out.println("Progetto: " + this.nomeProgetto);
        System.out.println("Anno: " + this.annoCorrente);
        System.out.println();

        double costoTotale = 0.0;

        for (Personale membro : this.membri) {
            int ore = this.oreAssegnate.get(membro.getCodice());
            double costoOrario = membro.getCostoOrario(this.annoCorrente);
            double costoMembro = ore * costoOrario;

            System.out.println(membro);
            System.out.println("Ore: " + ore);
            System.out.println("Costo orario: " + costoOrario);
            System.out.println("Costo: " + costoMembro);
            System.out.println();

            costoTotale += costoMembro;
        }

        System.out.println("COSTO TOTALE: " + costoTotale);
    }

    public String getNomeProgetto() {
        return this.nomeProgetto;
    }

    public List<Personale> getMembri() {
        return new ArrayList<>(this.membri);
    }
}
