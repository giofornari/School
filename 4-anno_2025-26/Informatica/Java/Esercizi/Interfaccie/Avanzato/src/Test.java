import java.util.ArrayList;

public class Test {
    public static void main(String[] args) {
        System.out.println("ESERCIZIO AVANZATO - Interfacce e Polimorfismo\n");
        
        // Creo alcuni mezzi di soccorso
        MezzoDiSoccorso elicottero = new MezzoDiSoccorso("Elicottero-1", 6);
        MezzoDiSoccorso motovedetta = new MezzoDiSoccorso("Motovedetta-2", 10);
        
        System.out.println("--- Uso come Motorizzato ---");
        elicottero.accendiMotore();
        System.out.println("Motore acceso? " + elicottero.motoreAcceso());
        System.out.println();
        
        System.out.println("--- Uso come Trasportatore ---");
        elicottero.carica(4);
        System.out.println("Capacita massima: " + elicottero.getCapacita());
        System.out.println();
        
        System.out.println("--- Uso come Volante ---");
        Volante mezzo1 = elicottero;
        mezzo1.vola();
        mezzo1.atterra();
        System.out.println();
        
        System.out.println("--- Uso come Navigabile ---");
        motovedetta.accendiMotore();
        Navigabile mezzo2 = motovedetta;
        mezzo2.naviga();
        mezzo2.attracca();
        System.out.println();
        
        System.out.println("--- Lista di mezzi Motorizzati ---");
        ArrayList<Motorizzato> flotta = new ArrayList<>();
        flotta.add(elicottero);
        flotta.add(motovedetta);
        
        System.out.println("Accendo tutti i motori:");
        for (Motorizzato m : flotta) {
            if (!m.motoreAcceso()) {
                m.accendiMotore();
            }
        }
        System.out.println();
        
        System.out.println("--- Verifica implementazioni ---");
        System.out.println(elicottero.getNome() + " implementa Volante? " + (elicottero instanceof Volante));
        System.out.println(elicottero.getNome() + " implementa Navigabile? " + (elicottero instanceof Navigabile));
        System.out.println(elicottero.getNome() + " implementa Trasportatore? " + (elicottero instanceof Trasportatore));
        System.out.println(elicottero.getNome() + " implementa Motorizzato? " + (elicottero instanceof Motorizzato));
    }
}
