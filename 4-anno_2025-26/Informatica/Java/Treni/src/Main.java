public class Main {
    public static void main(String[] args) {
        System.out.println("=== SISTEMA DI GESTIONE TRENI ===\n");
        
        // Creazione treno
        Treno trenoRegionale = new Treno("Regionale Express 1234");
        System.out.println("Treno creato: " + trenoRegionale.getNome());
        System.out.println();
        
        // Vagoni passeggeri
        System.out.println("--- Aggiunta Vagoni Passeggeri ---");
        
        VagonePasseggeri vp1 = new VagonePasseggeri(
            "VP-001", 45000, "Alstom", 2015, 1, 60, 45
        );
        trenoRegionale.addVag(vp1);
        System.out.println("Aggiunto: " + vp1.toString());
        
        VagonePasseggeri vp2 = new VagonePasseggeri(
            "VP-002", 42000, "Bombardier", 2018, 1, 64, 58
        );
        trenoRegionale.addVag(vp2);
        System.out.println("Aggiunto: " + vp2.toString());
        
        VagonePasseggeri vp3 = new VagonePasseggeri(
            "VP-003", 40000, "Siemens", 2020, 2, 80, 72
        );
        trenoRegionale.addVag(vp3);
        System.out.println("Aggiunto: " + vp3.toString());
        
        VagonePasseggeri vp4 = new VagonePasseggeri(
            "VP-004", 41000, "Alstom", 2019, 2, 80, 65
        );
        trenoRegionale.addVag(vp4);
        System.out.println("Aggiunto: " + vp4.toString());
        
        System.out.println();
        
        // Vagoni merci
        System.out.println("--- Aggiunta Vagoni Merci ---");
        
        VagoneMerci vm1 = new VagoneMerci(
            "VM-101", 28000, "Greenbrier", 2016, 120.0, 50000, 42000
        );
        trenoRegionale.addVag(vm1);
        System.out.println("Aggiunto: " + vm1.toString());
        
        VagoneMerci vm2 = new VagoneMerci(
            "VM-102", 30000, "FreightCar", 2017, 140.0, 60000, 55000
        );
        trenoRegionale.addVag(vm2);
        System.out.println("Aggiunto: " + vm2.toString());
        
        VagoneMerci vm3 = new VagoneMerci(
            "VM-103", 26000, "Greenbrier", 2021, 100.0, 45000, 38000
        );
        trenoRegionale.addVag(vm3);
        System.out.println("Aggiunto: " + vm3.toString());
        
        System.out.println();
        System.out.println("=".repeat(80));
        System.out.println();
        
        // Riepilogo composizione
        System.out.println("--- RIEPILOGO COMPOSIZIONE TRENO ---");
        System.out.println(trenoRegionale.toString());
        System.out.println();
        
        // Statistiche
        System.out.println("--- STATISTICHE DETTAGLIATE ---");
        System.out.println("Numero totale di vagoni: " + trenoRegionale.numVag());
        System.out.println("  - Vagoni passeggeri: " + trenoRegionale.numVagPass());
        System.out.println("  - Vagoni merci: " + trenoRegionale.numVagMerci());
        System.out.println();
        
        System.out.println("Capacità passeggeri:");
        System.out.println("  - Posti totali disponibili: " + trenoRegionale.getPassTot());
        System.out.println("  - Posti attualmente occupati: " + trenoRegionale.getPassOcc());
        System.out.println("  - Posti liberi: " + 
            (trenoRegionale.getPassTot() - trenoRegionale.getPassOcc()));
        System.out.println();
        
        System.out.println(String.format("Peso complessivo del treno (escluse motrici): %.2f kg (%.2f tonnellate)",
            trenoRegionale.totPeso(), 
            trenoRegionale.totPeso() / 1000));
        System.out.println();
        
        // Test modifica peso medio
        System.out.println("--- TEST MODIFICA PESO MEDIO OCCUPANTE ---");
        System.out.println("Peso medio occupante attuale: " + VagonePasseggeri.avgPeso + " kg");
        System.out.println("Peso complessivo attuale: " + 
            String.format("%.2f kg", trenoRegionale.totPeso()));
        
        VagonePasseggeri.avgPeso = 70.0;
        System.out.println("\nPeso medio occupante modificato a: " + VagonePasseggeri.avgPeso + " kg");
        System.out.println("Nuovo peso complessivo: " + 
            String.format("%.2f kg", trenoRegionale.totPeso()));
        System.out.println("Differenza: " + 
            String.format("%.2f kg", (70.0 - 65.0) * trenoRegionale.getPassOcc()));
        System.out.println();
        
        // Elenco completo vagoni
        System.out.println("=".repeat(80));
        System.out.println("--- ELENCO COMPLETO VAGONI ---");
        int numero = 1;
        for (Vagone vagone : trenoRegionale.getVagoni()) {
            System.out.println(numero + ". " + vagone.toString());
            numero++;
        }
        
        System.out.println();
        System.out.println("=== FINE PROGRAMMA ===");
    }
}
