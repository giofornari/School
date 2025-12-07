
public class Test {

    public static void main(String[] args) {
        Villa villa = new Villa(8, 240.0, "Via delle Rose 10", "Roma",
                3, 120.0, true);

        Appartamento appartamento = new Appartamento(4, 90.0, "Corso Garibaldi 25", "Milano",
                5, true, 2);

        Villa sameVilla = new Villa(8, 240.0, "Via delle Rose 10", "Roma",
                3, 120.0, true);

        System.out.println("\n" + villa.toString());

        System.out.println("\n" + appartamento.toString());

        System.out.printf("\nLa villa e la villa gemella sono %s%n\n", villa.equals(sameVilla) ? "uguali" : "diverse");
        System.out.printf("La villa e l'appartamento sono %s%n\n", villa.equals(appartamento) ? "uguali" : "diversi");
    }
}
