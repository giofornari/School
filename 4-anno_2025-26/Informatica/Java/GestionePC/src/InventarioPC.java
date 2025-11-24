import java.util.ArrayList;
import java.util.List;

/**
 * Classe che gestisce un inventario di PC.
 * Fornisce funzionalità per aggiungere, rimuovere, cercare e analizzare i PC.
 * 
 * @author giordii.dev
 */
public class InventarioPC {
    private ArrayList<PC> inventario;

    /**
     * Costruttore che inizializza l'inventario vuoto.
     */
    public InventarioPC() {
        this.inventario = new ArrayList<>();
    }

    /**
     * Aggiunge un PC all'inventario.
     * 
     * @param pc il PC da aggiungere
     */
    public void aggiungiPC(PC pc) {
        inventario.add(pc);
    }

    /**
     * Rimuove un PC dall'inventario.
     * 
     * @param pc il PC da rimuovere
     * @return true se il PC è stato rimosso, false altrimenti
     */
    public boolean rimuoviPC(PC pc) {
        return inventario.remove(pc);
    }

    /**
     * Cerca tutti i PC di una determinata marca.
     * 
     * @param marca la marca da cercare
     * @return lista dei PC della marca specificata
     */
    public List<PC> cercaPerMarca(String marca) {
        List<PC> risultati = new ArrayList<>();
        for (PC pc : inventario) {
            if (pc.getMarca().equalsIgnoreCase(marca)) {
                risultati.add(pc);
            }
        }
        return risultati;
    }

    /**
     * Cerca tutti i PC con un determinato sistema operativo.
     * 
     * @param sistemaOperativo il sistema operativo da cercare
     * @return lista dei PC con il sistema operativo specificato
     */
    public List<PC> cercaPerSistemaOperativo(String sistemaOperativo) {
        List<PC> risultati = new ArrayList<>();
        for (PC pc : inventario) {
            if (pc.getSistemaOperativo().equalsIgnoreCase(sistemaOperativo)) {
                risultati.add(pc);
            }
        }
        return risultati;
    }

    /**
     * Trova il PC con la quantità massima di RAM.
     * 
     * @return il PC con più RAM, o null se l'inventario è vuoto
     */
    public PC trovaPCConPiuRAM() {
        if (inventario.isEmpty()) {
            return null;
        }
        PC pcConPiuRAM = inventario.get(0);
        for (PC pc : inventario) {
            if (pc.getDimensioneRAM() > pcConPiuRAM.getDimensioneRAM()) {
                pcConPiuRAM = pc;
            }
        }
        return pcConPiuRAM;
    }

    /**
     * Calcola la quantità media di RAM dei PC nell'inventario.
     * 
     * @return la media di RAM in GB, 0.0 se l'inventario è vuoto
     */
    public double calcolaMediaRAM() {
        if (inventario.isEmpty()) {
            return 0.0;
        }
        int sommaRAM = 0;
        for (PC pc : inventario) {
            sommaRAM += pc.getDimensioneRAM();
        }
        return (double) sommaRAM / inventario.size();
    }

    /**
     * Conta il numero di PC portatili con interfaccia WiFi.
     * 
     * @return il numero di portatili con WiFi
     */
    public int contaPortatiliConWifi() {
        int count = 0;
        for (PC pc : inventario) {
            if (pc instanceof PCPortatile) {
                PCPortatile portatile = (PCPortatile) pc;
                if (portatile.hasWireless()) {
                    count++;
                }
            }
        }
        return count;
    }

    /**
     * Conta il numero di server dotati di dischi RAID.
     * 
     * @return il numero di server con RAID
     */
    public int contaServerConRaid() {
        int count = 0;
        for (PC pc : inventario) {
            if (pc instanceof Server) {
                Server server = (Server) pc;
                if (server.hasRaid()) {
                    count++;
                }
            }
        }
        return count;
    }

    /**
     * Trova il notebook con peso minimo.
     * 
     * @return il notebook più leggero, o null se non ci sono notebook
     */
    public Notebook trovaNotebookPiuLeggero() {
        Notebook notebookPiuLeggero = null;
        for (PC pc : inventario) {
            if (pc instanceof Notebook) {
                Notebook notebook = (Notebook) pc;
                if (notebookPiuLeggero == null || 
                    notebook.getPeso() < notebookPiuLeggero.getPeso()) {
                    notebookPiuLeggero = notebook;
                }
            }
        }
        return notebookPiuLeggero;
    }

    /**
     * Cerca PC portatili che soddisfano criteri specifici.
     * 
     * @param pesoMassimo il peso massimo in kg
     * @param richiedeWifi se true, include solo portatili con WiFi
     * @return lista dei portatili che soddisfano i criteri
     */
    public List<PC> cercaPortatili(double pesoMassimo, boolean richiedeWifi) {
        List<PC> risultati = new ArrayList<>();
        for (PC pc : inventario) {
            if (pc instanceof PCPortatile) {
                PCPortatile portatile = (PCPortatile) pc;
                // Verifica il peso
                if (portatile.getPeso() <= pesoMassimo) {
                    // Verifica WiFi se richiesto
                    if (!richiedeWifi || portatile.hasWireless()) {
                        risultati.add(pc);
                    }
                }
            }
        }
        return risultati;
    }

    /**
     * Restituisce il numero di PC nell'inventario.
     * 
     * @return il numero di PC
     */
    public int size() {
        return inventario.size();
    }

    /**
     * Restituisce una rappresentazione testuale dell'inventario.
     * 
     * @return stringa con tutti i PC nell'inventario
     */
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("=== INVENTARIO PC ===\n");
        sb.append("Totale PC: ").append(inventario.size()).append("\n\n");
        for (int i = 0; i < inventario.size(); i++) {
            sb.append((i + 1)).append(". ").append(inventario.get(i).toString()).append("\n");
        }
        return sb.toString();
    }
}
