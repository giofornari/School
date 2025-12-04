
import java.time.LocalDate;

/**
 * Classe Main per testare il sistema di gestione autonoleggio. Dimostra tutte
 * le funzionalità del sistema con esempi pratici.
 *
 * @author giordii.dev
 */
public class Main {

    public static void main(String[] args) {
        System.out.println("=== SISTEMA GESTIONE AUTONOLEGGIO ===\n");

        // autonoleggio italiano classico
        GestioneAutonoleggio autonoleggio = new GestioneAutonoleggio("RentCar Italia");

        System.out.println("--- CREAZIONE FLOTTA ---\n");

        // auto economiche per tutti
        Autovettura auto1 = new Autovettura(
                "AB123CD",
                1001,
                "Fiat",
                "Panda",  // la regina delle citycar italiane
                1200,
                2020,
                35.0,
                5
        );

        Autovettura auto2 = new Autovettura(
                "EF456GH",
                1002,
                "Volkswagen",
                "Golf",  // tedesca affidabile
                1600,
                2021,
                50.0,
                5
        );

        Autovettura auto3 = new Autovettura(
                "IJ789KL",
                1003,
                "BMW",
                "Serie 3",  // per chi vuole fare bella figura
                2000,
                2022,
                60.0,
                5
        );

        // furgoni per traslochi e corrieri
        Furgone furgone1 = new Furgone(
                "MN012OP",
                2001,
                "Fiat",
                "Ducato",  // il più venduto in Italia
                2300,
                2019,
                90.0,
                1200.0
        );

        Furgone furgone2 = new Furgone(
                "QR345ST",
                2002,
                "Mercedes",
                "Sprinter",  // il top di gamma
                2500,
                2021,
                100.0,
                1500.0
        );

        Furgone furgone3 = new Furgone(
                "UV678WX",
                2003,
                "Iveco",
                "Daily",  // marchio italiano, sempre affidabile
                3000,
                2020,
                80.0,
                1800.0
        );

        autonoleggio.aggiungiVeicolo(auto1);
        autonoleggio.aggiungiVeicolo(auto2);
        autonoleggio.aggiungiVeicolo(auto3);
        autonoleggio.aggiungiVeicolo(furgone1);
        autonoleggio.aggiungiVeicolo(furgone2);
        autonoleggio.aggiungiVeicolo(furgone3);

        System.out.println("Flotta creata con successo!");
        autonoleggio.stampaFlotta();

        System.out.println("--- STATISTICHE FLOTTA ---");
        System.out.println("Autovetture: " + autonoleggio.getAutovetture().size());
        System.out.println("Furgoni: " + autonoleggio.getFurgoni().size());
        System.out.println("Veicoli disponibili: " + autonoleggio.getVeicoliDisponibili().size());
        System.out.println();

        // Test noleggi
        System.out.println("--- AVVIO NOLEGGI ---\n");

        LocalDate oggi = LocalDate.of(2025, 12, 1);

        // weekend fuori con la Panda
        System.out.println("Cliente Mario Rossi noleggia Fiat Panda (1001)");
        Noleggio noleggio1 = autonoleggio.avviaNoleggio(1001, "Mario Rossi", oggi);
        System.out.println("✓ Noleggio avviato\n");

        // trasloco con il furgone
        System.out.println("Cliente Luigi Verdi noleggia Fiat Ducato (2001)");
        Noleggio noleggio2 = autonoleggio.avviaNoleggio(2001, "Luigi Verdi", oggi);
        System.out.println("✓ Noleggio avviato\n");

        // settimana di lusso con la BMW
        System.out.println("Cliente Anna Bianchi noleggia BMW Serie 3 (1003)");
        Noleggio noleggio3 = autonoleggio.avviaNoleggio(1003, "Anna Bianchi", oggi);
        System.out.println("✓ Noleggio avviato\n");

        autonoleggio.stampaNoleggiAttivi();

        System.out.println("--- VEICOLI ANCORA DISPONIBILI ---");
        for (Veicolo v : autonoleggio.getVeicoliDisponibili()) {
            System.out.println(v);
        }
        System.out.println();

        // Conclusione noleggi
        System.out.println("--- CONCLUSIONE NOLEGGI ---\n");

        // Mario torna dopo 3 giorni, ha fatto 200km
        System.out.println("Restituzione Fiat Panda da Mario Rossi");
        LocalDate dataFine1 = oggi.plusDays(3);
        noleggio1.concludiNoleggio(dataFine1, 200.0, 5.0);
        System.out.println(noleggio1.getDettaglioCosti());
        System.out.println();

        // Luigi ha fatto il trasloco, 250km totali
        System.out.println("Restituzione Fiat Ducato da Luigi Verdi");
        LocalDate dataFine2 = oggi.plusDays(5);
        noleggio2.concludiNoleggio(dataFine2, 250.0, 10.0);  // 150km oltre franchigia
        System.out.println(noleggio2.getDettaglioCosti());
        System.out.println();

        // Anna ha girato mezza Italia con la BMW
        System.out.println("Restituzione BMW Serie 3 da Anna Bianchi");
        LocalDate dataFine3 = oggi.plusDays(7);
        noleggio3.concludiNoleggio(dataFine3, 500.0, 15.0);
        System.out.println(noleggio3.getDettaglioCosti());
        System.out.println();

        autonoleggio.stampaStoricoNoleggi();

        // Test calcolo costi diretto
        System.out.println("--- TEST CALCOLO COSTI (metodo override) ---\n");

        System.out.println("AUTOVETTURA - Esempio: 5 giorni, 300 km, 8 litri mancanti");
        double costoAuto = auto2.calcolaCostoNoleggio(5, 300.0, 8.0);
        System.out.println("Costo autovettura:");
        System.out.println("  - Giorni: 5 * 50€ = 250€");
        System.out.println("  - Km: 300 / 25 = 12€");
        System.out.println("  - Carburante: 8 * 2€ = 16€");
        System.out.println("  TOTALE: " + String.format("%.2f", costoAuto) + " €");
        System.out.println();

        System.out.println("FURGONE - Esempio: 5 giorni, 250 km, 12 litri mancanti");
        double costoFurgone = furgone2.calcolaCostoNoleggio(5, 250.0, 12.0);
        System.out.println("Costo furgone:");
        System.out.println("  - Giorni: 5 * 70€ = 350€");
        System.out.println("  - Km: (250-100) / 30 = 5€");
        System.out.println("  - Carburante: 12 * 2€ = 24€");
        System.out.println("  TOTALE: " + String.format("%.2f", costoFurgone) + " €");
        System.out.println();

        // confronto prezzi per noleggio breve
        System.out.println("--- CONFRONTO TARIFFE (1 giorno, 50 km, 0 litri) ---");
        double autoBreve = auto1.calcolaCostoNoleggio(1, 50.0, 0.0);
        double furgoneBreve = furgone1.calcolaCostoNoleggio(1, 50.0, 0.0);
        System.out.println("Autovettura: " + String.format("%.2f", autoBreve) + " €");
        System.out.println("Furgone: " + String.format("%.2f", furgoneBreve) + " € (primi 100km gratis!)");
        System.out.println();

        // Statistiche finali
        System.out.println("--- STATISTICHE FINALI ---");
        System.out.println("Totale veicoli in flotta: " + autonoleggio.contaVeicoli());
        System.out.println("Totale noleggi effettuati: " + autonoleggio.contaNoleggi());
        System.out.println("Noleggi attivi: " + autonoleggio.getNoleggiAttivi().size());
        System.out.println("Noleggi conclusi: " + autonoleggio.getNoleggiConclusi().size());
        System.out.println("Veicoli disponibili: " + autonoleggio.getVeicoliDisponibili().size());

        // quanto abbiamo incassato oggi
        double fatturatoTotale = 0;
        for (Noleggio n : autonoleggio.getNoleggiConclusi()) {
            fatturatoTotale += n.calcolaCostoTotale();
        }
        System.out.println("Fatturato totale: " + String.format("%.2f", fatturatoTotale) + " €");  // soldi in cassa
    }
}
