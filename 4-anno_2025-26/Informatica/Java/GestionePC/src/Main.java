import java.util.List;

/**
 * Classe di test per il sistema di gestione PC.
 * Crea un inventario di esempio e testa tutte le funzionalità.
 * 
 * @author giordii.dev
 */
public class Main {
    public static void main(String[] args) {
        System.out.println("=== SISTEMA DI GESTIONE INVENTARIO PC ===\n");

        // Creazione dell'inventario
        InventarioPC inventario = new InventarioPC();

        // Creazione di PC Desktop
        Desktop desktop1 = new Desktop(
            "Intel Core i7-13700K", 32, 1000,
            "Dell", "Optiplex 7090", "Windows 11 Pro",
            "grande", "NVIDIA RTX 4070", "Realtek ALC897"
        );
        Desktop desktop2 = new Desktop(
            "AMD Ryzen 9 5950X", 64, 2000,
            "HP", "EliteDesk 800 G9", "Windows 11 Pro",
            "medio", "AMD Radeon RX 7600", "Realtek ALC1220"
        );

        // Creazione di Server
        Server server1 = new Server(
            "Intel Xeon Gold 6330", 128, 4000,
            "Dell", "PowerEdge R750", "Ubuntu Server 22.04",
            "grande", 2, true
        );
        Server server2 = new Server(
            "AMD EPYC 7763", 256, 8000,
            "HPE", "ProLiant DL385 Gen10", "Red Hat Enterprise Linux 9",
            "grande", 4, true
        );
        Server server3 = new Server(
            "Intel Xeon E-2386G", 64, 2000,
            "Lenovo", "ThinkSystem SR250", "Windows Server 2022",
            "medio", 1, false
        );

        // Creazione di Notebook
        Notebook notebook1 = new Notebook(
            "Intel Core i5-1235U", 16, 512,
            "Lenovo", "ThinkPad X1 Carbon Gen 10", "Windows 11 Pro",
            1.12, 2.2, 31.5, 21.7, 14.0, true,
            true, 2.1
        );
        Notebook notebook2 = new Notebook(
            "Apple M2 Pro", 32, 1000,
            "Apple", "MacBook Pro 16", "macOS Ventura",
            2.15, 2.49, 35.57, 24.81, 16.2, true,
            true, 1.0
        );
        Notebook notebook3 = new Notebook(
            "AMD Ryzen 7 6800U", 16, 512,
            "ASUS", "Zenbook S 13", "Windows 11 Home",
            1.0, 1.69, 29.67, 21.04, 13.3, true,
            false, 0
        );

        // Creazione di Palmari
        Palmare palmare1 = new Palmare(
            "Qualcomm Snapdragon 8 Gen 2", 8, 256,
            "Samsung", "Galaxy Tab S9", "Android 13",
            0.498, 0.57, 16.54, 25.45, 11.0, true,
            true, "microSD"
        );
        Palmare palmare2 = new Palmare(
            "Apple A15 Bionic", 4, 128,
            "Apple", "iPad Mini 6", "iPadOS 16",
            0.293, 0.63, 13.48, 19.53, 8.3, true,
            true, "none"
        );

        // Aggiunta dei PC all'inventario
        System.out.println("Aggiunta PC all'inventario...\n");
        inventario.aggiungiPC(desktop1);
        inventario.aggiungiPC(desktop2);
        inventario.aggiungiPC(server1);
        inventario.aggiungiPC(server2);
        inventario.aggiungiPC(server3);
        inventario.aggiungiPC(notebook1);
        inventario.aggiungiPC(notebook2);
        inventario.aggiungiPC(notebook3);
        inventario.aggiungiPC(palmare1);
        inventario.aggiungiPC(palmare2);

        // Stampa inventario completo
        System.out.println(inventario);

        // Test: PC con più RAM
        System.out.println("\n=== TEST: PC CON PIÙ RAM ===");
        PC pcConPiuRAM = inventario.trovaPCConPiuRAM();
        if (pcConPiuRAM != null) {
            System.out.println(pcConPiuRAM);
        }

        // Test: Media RAM
        System.out.println("\n=== TEST: MEDIA RAM ===");
        double mediaRAM = inventario.calcolaMediaRAM();
        System.out.printf("Media RAM: %.2f GB\n", mediaRAM);

        // Test: Conteggio portatili con WiFi
        System.out.println("\n=== TEST: PORTATILI CON WiFi ===");
        int portatiliConWifi = inventario.contaPortatiliConWifi();
        System.out.println("Numero di portatili con WiFi: " + portatiliConWifi);

        // Test: Conteggio server con RAID
        System.out.println("\n=== TEST: SERVER CON RAID ===");
        int serverConRaid = inventario.contaServerConRaid();
        System.out.println("Numero di server con RAID: " + serverConRaid);

        // Test: Notebook più leggero
        System.out.println("\n=== TEST: NOTEBOOK PIÙ LEGGERO ===");
        Notebook notebookLeggero = inventario.trovaNotebookPiuLeggero();
        if (notebookLeggero != null) {
            System.out.println(notebookLeggero);
        }

        // Test: Ricerca per marca
        System.out.println("\n=== TEST: RICERCA PER MARCA (Dell) ===");
        List<PC> pcDell = inventario.cercaPerMarca("Dell");
        System.out.println("PC Dell trovati: " + pcDell.size());
        for (PC pc : pcDell) {
            System.out.println("  - " + pc);
        }

        // Test: Ricerca per sistema operativo
        System.out.println("\n=== TEST: RICERCA PER SISTEMA OPERATIVO (Windows 11 Pro) ===");
        List<PC> pcWindows11 = inventario.cercaPerSistemaOperativo("Windows 11 Pro");
        System.out.println("PC con Windows 11 Pro trovati: " + pcWindows11.size());
        for (PC pc : pcWindows11) {
            System.out.println("  - " + pc);
        }

        // Test: Ricerca portatili con criteri multipli
        System.out.println("\n=== TEST: RICERCA PORTATILI (peso <= 1.5kg, con WiFi) ===");
        List<PC> portatiliLeggeri = inventario.cercaPortatili(1.5, true);
        System.out.println("Portatili trovati: " + portatiliLeggeri.size());
        for (PC pc : portatiliLeggeri) {
            System.out.println("  - " + pc);
        }

        // Test: Ricerca portatili senza filtro WiFi
        System.out.println("\n=== TEST: RICERCA PORTATILI (peso <= 2.5kg, senza filtro WiFi) ===");
        List<PC> portatiliMedi = inventario.cercaPortatili(2.5, false);
        System.out.println("Portatili trovati: " + portatiliMedi.size());
        for (PC pc : portatiliMedi) {
            System.out.println("  - " + pc);
        }

        // Test: Rimozione di un PC
        System.out.println("\n=== TEST: RIMOZIONE PC ===");
        System.out.println("Rimozione del palmare Samsung...");
        boolean rimosso = inventario.rimuoviPC(palmare1);
        System.out.println("Rimozione riuscita: " + (rimosso ? "Sì" : "No"));
        System.out.println("Nuova dimensione inventario: " + inventario.size());

        // Test: Ricerca per marca Apple
        System.out.println("\n=== TEST: RICERCA PER MARCA (Apple) ===");
        List<PC> pcApple = inventario.cercaPerMarca("Apple");
        System.out.println("PC Apple trovati: " + pcApple.size());
        for (PC pc : pcApple) {
            System.out.println("  - " + pc);
        }

        System.out.println("\n=== FINE TEST ===");
    }
}
