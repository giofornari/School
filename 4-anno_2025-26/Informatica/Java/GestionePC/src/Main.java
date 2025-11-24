import java.util.List;

// Entry point test inventario
public class Main {
    public static void main(String[] args) {
        System.out.println("=== SISTEMA DI GESTIONE INVENTARIO PC ===\n");

        InventarioPC inv = new InventarioPC();

        // desktop
        Desktop desk1 = new Desktop(
            "Intel Core i7-13700K", 32, 1000,
            "Dell", "Optiplex 7090", "Windows 11 Pro",
            "grande", "NVIDIA RTX 4070", "Realtek ALC897"
        );
        Desktop desk2 = new Desktop(
            "AMD Ryzen 9 5950X", 64, 2000,
            "HP", "EliteDesk 800 G9", "Windows 11 Pro",
            "medio", "AMD Radeon RX 7600", "Realtek ALC1220"
        );

        // server
        Server srv1 = new Server(
            "Intel Xeon Gold 6330", 128, 4000,
            "Dell", "PowerEdge R750", "Ubuntu Server 22.04",
            "grande", 2, true
        );
        Server srv2 = new Server(
            "AMD EPYC 7763", 256, 8000,
            "HPE", "ProLiant DL385 Gen10", "Red Hat Enterprise Linux 9",
            "grande", 4, true
        );
        Server srv3 = new Server(
            "Intel Xeon E-2386G", 64, 2000,
            "Lenovo", "ThinkSystem SR250", "Windows Server 2022",
            "medio", 1, false
        );

        // notebook
        Notebook nb1 = new Notebook(
            "Intel Core i5-1235U", 16, 512,
            "Lenovo", "ThinkPad X1 Carbon Gen 10", "Windows 11 Pro",
            1.12, 2.2, 31.5, 21.7, 14.0, true,
            true, 2.1
        );
        Notebook nb2 = new Notebook(
            "Apple M2 Pro", 32, 1000,
            "Apple", "MacBook Pro 16", "macOS Ventura",
            2.15, 2.49, 35.57, 24.81, 16.2, true,
            true, 1.0
        );
        Notebook nb3 = new Notebook(
            "AMD Ryzen 7 6800U", 16, 512,
            "ASUS", "Zenbook S 13", "Windows 11 Home",
            1.0, 1.69, 29.67, 21.04, 13.3, true,
            false, 0
        );

        // palmari
        Palmare palm1 = new Palmare(
            "Qualcomm Snapdragon 8 Gen 2", 8, 256,
            "Samsung", "Galaxy Tab S9", "Android 13",
            0.498, 0.57, 16.54, 25.45, 11.0, true,
            true, "microSD"
        );
        Palmare palm2 = new Palmare(
            "Apple A15 Bionic", 4, 128,
            "Apple", "iPad Mini 6", "iPadOS 16",
            0.293, 0.63, 13.48, 19.53, 8.3, true,
            true, "none"
        );

        System.out.println("Aggiunta PC all'inventario...\n");
        inv.aggiungiPC(desk1);
        inv.aggiungiPC(desk2);
        inv.aggiungiPC(srv1);
        inv.aggiungiPC(srv2);
        inv.aggiungiPC(srv3);
        inv.aggiungiPC(nb1);
        inv.aggiungiPC(nb2);
        inv.aggiungiPC(nb3);
        inv.aggiungiPC(palm1);
        inv.aggiungiPC(palm2);

        System.out.println(inv);

        System.out.println("\n=== TEST: PC CON PIÙ RAM ===");
        PC pcMaxRam = inv.trovaPCConPiuRAM();
        if (pcMaxRam != null) {
            System.out.println(pcMaxRam);
        }

        System.out.println("\n=== TEST: MEDIA RAM ===");
        double mediaRam = inv.calcolaMediaRAM();
        System.out.printf("Media RAM: %.2f GB\n", mediaRam);

        System.out.println("\n=== TEST: PORTATILI CON WiFi ===");
        int portWifi = inv.contaPortatiliConWifi();
        System.out.println("Numero di portatili con WiFi: " + portWifi);

        System.out.println("\n=== TEST: SERVER CON RAID ===");
        int srvRaid = inv.contaServerConRaid();
        System.out.println("Numero di server con RAID: " + srvRaid);

        System.out.println("\n=== TEST: NOTEBOOK PIÙ LEGGERO ===");
        Notebook nbLeggero = inv.trovaNotebookPiuLeggero();
        if (nbLeggero != null) {
            System.out.println(nbLeggero);
        }

        System.out.println("\n=== TEST: RICERCA PER MARCA (Dell) ===");
        List<PC> pcDell = inv.cercaPerMarca("Dell");
        System.out.println("PC Dell trovati: " + pcDell.size());
        for (PC pc : pcDell) {
            System.out.println("  - " + pc);
        }

        System.out.println("\n=== TEST: RICERCA PER SISTEMA OPERATIVO (Windows 11 Pro) ===");
        List<PC> pcWin11 = inv.cercaPerSistemaOperativo("Windows 11 Pro");
        System.out.println("PC con Windows 11 Pro trovati: " + pcWin11.size());
        for (PC pc : pcWin11) {
            System.out.println("  - " + pc);
        }

        System.out.println("\n=== TEST: RICERCA PORTATILI (peso <= 1.5kg, con WiFi) ===");
        List<PC> portLeggeri = inv.cercaPortatili(1.5, true);
        System.out.println("Portatili trovati: " + portLeggeri.size());
        for (PC pc : portLeggeri) {
            System.out.println("  - " + pc);
        }

        System.out.println("\n=== TEST: RICERCA PORTATILI (peso <= 2.5kg, senza filtro WiFi) ===");
        List<PC> portMedi = inv.cercaPortatili(2.5, false);
        System.out.println("Portatili trovati: " + portMedi.size());
        for (PC pc : portMedi) {
            System.out.println("  - " + pc);
        }

        System.out.println("\n=== TEST: RIMOZIONE PC ===");
        System.out.println("Rimozione del palmare Samsung...");
        boolean okRemove = inv.rimuoviPC(palm1);
        System.out.println("Rimozione riuscita: " + (okRemove ? "Sì" : "No"));
        System.out.println("Nuova dimensione inventario: " + inv.size());

        System.out.println("\n=== TEST: RICERCA PER MARCA (Apple) ===");
        List<PC> pcApple = inv.cercaPerMarca("Apple");
        System.out.println("PC Apple trovati: " + pcApple.size());
        for (PC pc : pcApple) {
            System.out.println("  - " + pc);
        }

        System.out.println("\n=== FINE TEST ===");
    }
}
