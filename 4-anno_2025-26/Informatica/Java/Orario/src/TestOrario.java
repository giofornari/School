public class TestOrario {
    public static void main(String[] args) {
        // Crea un oggetto Orario con valore iniziale 23:59:59
        Orario orario1 = new Orario(23, 59, 59);
        
        // Visualizza l'orario con mostra()
        System.out.println("Orario iniziale: " + orario1.mostra());
        
        // Chiama tic() e mostra il nuovo orario (dovrebbe diventare 00:00:00)
        orario1.tic();
        System.out.println("Dopo un tic: " + orario1.mostra());
        
        // Aggiunge 125 minuti e mostra il risultato
        orario1.aggiungiMinuti(125);
        System.out.println("Dopo 125 minuti: " + orario1.mostra());
        
        // Crea un secondo oggetto Orario e verifica se i due orari sono uguali
        Orario orario2 = new Orario(10, 30, 45);
        
        if (orario1.ugualeA(orario2)) {
            System.out.println("Gli orari sono uguali.");
        } else {
            System.out.println("Gli orari sono diversi.");
        }
    }
}
