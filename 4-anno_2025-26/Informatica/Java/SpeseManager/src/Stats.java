import java.util.List;
import java.util.ArrayList;

public class Stats {
    public String categoriaMediaPiuAlta(List<Spese> spese) {
        if (spese == null || spese.isEmpty()) return null;
        List<String> categorie = new ArrayList<>();
        for (Spese s : spese) {
            if (!categorie.contains(s.getCategory())) {
                categorie.add(s.getCategory());
            }
        }
        
        String maxCat = null;
        double maxAvg = Double.NEGATIVE_INFINITY;
        for (String cat : categorie) {
            double somma = 0;
            int count = 0;
            for (Spese s : spese) {
                if (cat.equals(s.getCategory())) {
                    somma += s.getMoneyyy();
                    count++;
                }
            }
            double avg = somma / count;
            if (avg > maxAvg) {
                maxAvg = avg;
                maxCat = cat;
            }
        }
        return maxCat;
    }

    public String categoriaMediaPiuBassa(List<Spese> spese) {
        if (spese == null || spese.isEmpty()) return null;
        List<String> categorie = new ArrayList<>();
        for (Spese s : spese) {
            if (!categorie.contains(s.getCategory())) {
                categorie.add(s.getCategory());
            }
        }
        String minCat = null;
        double minAvg = Double.POSITIVE_INFINITY;
        for (String cat : categorie) {
            double somma = 0;
            int count = 0;
            for (Spese s : spese) {
                if (cat.equals(s.getCategory())) {
                    somma += s.getMoneyyy();
                    count++;
                }
            }
            double avg = somma / count;
            if (avg < minAvg) {
                minAvg = avg;
                minCat = cat;
            }
        }
        return minCat;
    }
}
