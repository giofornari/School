import java.util.Arrays;
import java.util.List;

public class Main {
    public static final String RESET = "\u001B[0m";
    public static final String RED = "\u001B[31m";
    public static final String GREEN = "\u001B[32m";
    public static final String YELLOW = "\u001B[33m";
    public static final String CYAN = "\u001B[36m";

    public static void main(String[] args) throws Exception {
        System.out.println(RED + "Per Dio!" + RESET);
        Spese[] ricevute = {
            new Spese("Trasporto", "2025-10-24", 4.5, "Carta"),
            new Spese("Alimentari", 12.4, "Contanti"), // in nero
            new Spese("Bar", 7.0, "Contanti"), // uno sprits..
            new Spese("Viaggi", "2026-01-13", 340, "Bonifico") // neve 2026
        };

        List<Spese> listaSpese = Arrays.asList(ricevute);
        Stats stats = new Stats();

        double SpesaComplessiva = 0;
        for (Spese spesa : listaSpese)  {
            SpesaComplessiva += spesa.getMoneyyy();
        }
        System.out.println(GREEN + "Hai speso complessivamente: " + SpesaComplessiva + RESET);
        System.out.println(YELLOW + "La spesa media è " + (SpesaComplessiva / listaSpese.size()) + RESET);

        double maxSpesa = 0;
        double minSpesa = listaSpese.get(0).getMoneyyy();

        for (Spese spesa : listaSpese) {
            if (spesa.getMoneyyy() > maxSpesa) maxSpesa = spesa.getMoneyyy();
            if (spesa.getMoneyyy() < minSpesa) minSpesa = spesa.getMoneyyy();
        }

        System.out.println(CYAN + "La spesa max è " + maxSpesa + RESET);
        System.out.println(RED + "La spesa min è " + minSpesa + RESET);

        String categoriaMediaPiuAlta = stats.categoriaMediaPiuAlta(listaSpese);
        String categoriaMediaPiuBassa = stats.categoriaMediaPiuBassa(listaSpese);

        System.out.println(CYAN + "Categoria con media più alta: " + categoriaMediaPiuAlta + RESET);
        System.out.println(RED + "Categoria con media più bassa: " + categoriaMediaPiuBassa + RESET);
    }
    
}
