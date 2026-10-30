import java.time.LocalDate;
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        LibreriaMusicale lb = new LibreriaMusicale("Smart Shuffle");
        lb.aggiungiBrano(new Brano("AD MAIORA", "Artie 5ive", "Trap", 196, LocalDate.of(2024, 12, 13)));
        lb.aggiungiBrano(new Brano("Milano Testarossa", "Artie 5ive", "Trap", 206, LocalDate.of(2024, 7, 19)));
        lb.aggiungiBrano(new Brano("PULL UP", "Mambolosco", "Trap", 180, LocalDate.of(2024, 7, 5)));
        lb.aggiungiBrano(new Brano("Connessioni", "Mambolosco", "Trap", 179, LocalDate.of(2024, 10, 3)));
        lb.aggiungiBrano(new Brano("Ballas 2", "Diss Gacha", "Trap", 132, LocalDate.of(2025, 1, 31)));
        lb.aggiungiBrano(new Brano("OUTFIT CHECK", "Diss Gacha", "Trap", 129, LocalDate.of(2025, 6, 4)));

        ArrayList<Brano> brani = lb.getBrani();
        for (Brano b : brani) {
            int listndTimes;
            if (b.getArtista().equals("Artie 5ive")) {
                listndTimes = 3;
            } else if (b.getArtista().equals("Mambolosco")) {
                listndTimes = 4;
            } else if (b.getArtista().equals("Diss Gacha")) {
                listndTimes = 5;
            } else {
                listndTimes = 2;
            }
            for (int i = 0; i < listndTimes; i++) {
                b.incrementaAscolti();
            }
        }

        ArrayList<String> artisti = new ArrayList<>();

        ArrayList<Integer> tot = new ArrayList<>();
        for (Brano b : brani) {
            String art = b.getArtista();
            boolean exist = false;
            for (int i = 0; i < artisti.size(); i++) {
                if (artisti.get(i).equalsIgnoreCase(art)) {
                    tot.set(i, tot.get(i) + 1);
                    exist = true;
                    break;
                }
            }
            if (!exist) {
                artisti.add(art);
                tot.add(1);
            }
        }

        boolean sorted = false;
        while (!sorted) {
            sorted = true;
            for (int i = 0; i < tot.size() - 1; i++) {
                if (tot.get(i) < tot.get(i + 1)) {
                    int cntTmp = tot.get(i);
                    tot.set(i, tot.get(i + 1));
                    tot.set(i + 1, cntTmp);
                    String artTmp = artisti.get(i);
                    artisti.set(i, artisti.get(i + 1));
                    artisti.set(i + 1, artTmp);
                    sorted = false;
                }
            }
        }

        System.out.println("\nTop artisti per numero di brani:");
        for (int i = 0; i < artisti.size(); i++) {
            System.out.println(" - " + artisti.get(i) + ": " + tot.get(i));
        }
        String genere = "Trap";
        int maxSec = 600;
        ArrayList<Brano> pl = lb.shuffleConSeed(genere, maxSec);
        System.out.println("\nPlaylist " + genere + " shuffle (max " + maxSec + " sec):");
        for (Brano b : pl) {
            System.out.println(" - " + b);
        }
    }
}
