import java.time.LocalDate;
import java.util.List;

public class Main {

    public static void main(String[] args) {
        SpesaManager revolut = new SpesaManager();
        revolut.addSpesa(new Spese("Trasporto", LocalDate.of(2024, 5, 10), 12.80, "Carta")); // maledetto carnet 8 corse
        revolut.addSpesa(new Spese("Alimentari", LocalDate.of(2024, 5, 12), 42.30, "Contanti")); // in nero sotto casa...
        revolut.addSpesa(new Spese(7.50, "Bar", "Contanti")); // uno sprits...
        revolut.addSpesa(new Spese(120.00, "Tecnologia", "Bonifico")); // questa era una truffa

        stampaElenco(revolut.getSpese());
        stampaStatistiche(revolut);
    }

    private static void stampaElenco(List<Spese> spese) {
        System.out.println("Spese inserite:");
        for (int i = 0; i < spese.size(); i++) {
            Spese spesa = spese.get(i);
            System.out.printf(
                "%d) %s - %.2f (%s) | %s%n",
                i + 1,
                spesa.getCategory(),
                spesa.getAmount(),
                spesa.getPayMethod(),
                spesa.getDate() == null ? "data non disponibile" : spesa.getDate()
            );
        }
        System.out.println();
    }

    private static void stampaStatistiche(SpesaManager manager) {
        List<Spese> spese = manager.getSpese();
        double totale = 0;
        double max = Double.NEGATIVE_INFINITY;
        double min = Double.POSITIVE_INFINITY;

        for (Spese spesa : spese) {
            double importo = spesa.getAmount();
            totale += importo;
            max = Math.max(max, importo);
            min = Math.min(min, importo);
        }
        
        double media = spese.isEmpty() ? 0 : totale / spese.size();

        System.out.printf("Totale: %.2f%n", totale);
        System.out.printf("Media: %.2f%n", media);
        System.out.printf("Massimo: %.2f%n", max);
        System.out.printf("Minimo: %.2f%n", min);

        String categoriaTop = manager.calcolaCategoriaMaggiore();
        String metodoTop = manager.calcolaPayMethodMaggiore();

        double mediaCategoriaTop = categoriaTop.isEmpty() ? 0 : mediaPerCategoria(spese, categoriaTop);
        double totaleMetodoTop = metodoTop.isEmpty() ? 0 : totalePerMetodo(spese, metodoTop);

        System.out.println();
        System.out.printf("Categoria con media piu alta: %s (%.2f)%n", categoriaTop, mediaCategoriaTop);
        System.out.printf("Metodo con totale piu alto: %s (%.2f)%n", metodoTop, totaleMetodoTop);
    }

    private static double mediaPerCategoria(List<Spese> spese, String categoria) {
        double totale = 0;
        int count = 0;
        for (Spese spesa : spese) {
            if (spesa.getCategory().equals(categoria)) {
                totale += spesa.getAmount();
                count++;
            }
        }
        return count == 0 ? 0 : totale / count;
    }

    private static double totalePerMetodo(List<Spese> spese, String metodo) {
        double totale = 0;
        for (Spese spesa : spese) {
            if (spesa.getPayMethod().equals(metodo)) {
                totale += spesa.getAmount();
            }
        }
        return totale;
    }
}
