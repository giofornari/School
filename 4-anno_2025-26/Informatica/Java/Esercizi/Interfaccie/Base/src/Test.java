public class Test {
    public static void main(String[] args) {
        System.out.println("ESERCIZIO BASE - Interfacce Multiple\n");
        
        // Creo un veicolo anfibio
        VeicoloAnfibio veicolo = new VeicoloAnfibio("Duck Boat");
        
        // Uso normale
        System.out.println("Uso diretto:");
        veicolo.vola();
        veicolo.nuota();
        System.out.println();
        
        // Uso come interfaccia Volante
        System.out.println("Uso come Volante:");
        Volante obj1 = veicolo;
        obj1.vola();
        System.out.println();
        
        // Uso come interfaccia Nuotante
        System.out.println("Uso come Nuotante:");
        Nuotante obj2 = veicolo;
        obj2.nuota();
        System.out.println();
        
        // Verifica
        System.out.println("Verifica:");
        System.out.println(veicolo.getNome() + " implementa Volante? " + (veicolo instanceof Volante));
        System.out.println(veicolo.getNome() + " implementa Nuotante? " + (veicolo instanceof Nuotante));
    }
}
