public class TestOrario {
    public static void main(String[] args) {
        Orario orario1 = new Orario(23, 59, 59);
        
        System.out.println("now: " + orario1.mostra());
        orario1.tic();
        System.out.println("after un tic: " + orario1.mostra());
        
        orario1.aggiungiMinuti(125);
        System.out.println("after 125 minutes: " + orario1.mostra());
        
        Orario orario2 = new Orario(10, 30, 45);
        
        if (orario1.ugualeA(orario2)) {
            System.out.println("same time");
        } else {
            System.out.println("you need a resync.");
        }
    }
}
