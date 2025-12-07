import java.util.ArrayList;
import java.util.List;

// Gestione semplice dell'inventario PC
public class InventarioPC {
    private ArrayList<PC> pcs;

    public InventarioPC() {
        this.pcs = new ArrayList<>();
    }

    public void aggiungiPC(PC pc) {
        pcs.add(pc);
    }

    public boolean rimuoviPC(PC pc) {
        return pcs.remove(pc);
    }

    public List<PC> cercaPerMarca(String marca) {
        List<PC> match = new ArrayList<>();
        for (PC pc : pcs) {
            if (pc.getMarca().equalsIgnoreCase(marca)) {
                match.add(pc);
            }
        }
        return match;
    }

    public List<PC> cercaPerSistemaOperativo(String sistOp) {
        List<PC> match = new ArrayList<>();
        for (PC pc : pcs) {
            if (pc.getSistOp().equalsIgnoreCase(sistOp)) {
                match.add(pc);
            }
        }
        return match;
    }

    public PC trovaPCConPiuRAM() {
        if (pcs.isEmpty()) {
            return null;
        }
        PC pcTop = pcs.get(0);
        for (PC pc : pcs) {
            if (pc.getRamGb() > pcTop.getRamGb()) {
                pcTop = pc;
            }
        }
        return pcTop;
    }

    public double calcolaMediaRAM() {
        if (pcs.isEmpty()) {
            return 0.0;
        }
        int sumRam = 0;
        for (PC pc : pcs) {
            sumRam += pc.getRamGb();
        }
        return (double) sumRam / pcs.size();
    }

    public int contaPortatiliConWifi() {
        int cnt = 0;
        for (PC pc : pcs) {
            if (pc instanceof PCPortatile) {
                PCPortatile portatile = (PCPortatile) pc;
                if (portatile.hasWifi()) {
                    cnt++;
                }
            }
        }
        return cnt;
    }

    public int contaServerConRaid() {
        int cnt = 0;
        for (PC pc : pcs) {
            if (pc instanceof Server) {
                Server server = (Server) pc;
                if (server.hasRaid()) {
                    cnt++;
                }
            }
        }
        return cnt;
    }

    public Notebook trovaNotebookPiuLeggero() {
        Notebook leggero = null;
        for (PC pc : pcs) {
            if (pc instanceof Notebook) {
                Notebook nb = (Notebook) pc;
                if (leggero == null || nb.getPesoKg() < leggero.getPesoKg()) {
                    leggero = nb;
                }
            }
        }
        return leggero;
    }

    public List<PC> cercaPortatili(double pesoMax, boolean richiedeWifi) {
        List<PC> match = new ArrayList<>();
        for (PC pc : pcs) {
            if (pc instanceof PCPortatile) {
                PCPortatile portatile = (PCPortatile) pc;
                if (portatile.getPesoKg() <= pesoMax) {
                    if (!richiedeWifi || portatile.hasWifi()) {
                        match.add(pc);
                    }
                }
            }
        }
        return match;
    }

    public int size() {
        return pcs.size();
    }

    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("=== INVENTARIO PC ===\n");
        sb.append("Totale PC: ").append(pcs.size()).append("\n\n");
        for (int i = 0; i < pcs.size(); i++) {
            sb.append((i + 1)).append(". ").append(pcs.get(i).toString()).append("\n");
        }
        return sb.toString();
    }
}
