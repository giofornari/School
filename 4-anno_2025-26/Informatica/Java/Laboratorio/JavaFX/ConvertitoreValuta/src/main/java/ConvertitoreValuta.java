
import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.GridPane;
import javafx.stage.Stage;

/*
 * Convertitore Euro/Dollari
 * 
 * Ho scelto GridPane perche mi permette di mettere i controlli
 * in una griglia (tipo tabella), cosi posso avere le label a sinistra
 * e i campi di input a destra. E' comodo per fare i form.
 */
public class ConvertitoreValuta extends Application {

    // tasso di cambio (ho preso quello attuale da google)
    private final double TASSO = 1.08;

    @Override
    public void start(Stage stage) {

        GridPane grid = new GridPane();
        grid.setHgap(10);   // spazio orizzontale tra colonne
        grid.setVgap(10);   // spazio verticale tra righe
        grid.setPadding(new Insets(20));  // margine esterno

        // creo i controlli
        Label lblImporto = new Label("Importo:");
        TextField txtImporto = new TextField();
        txtImporto.setPromptText("es. 100");

        Label lblDirezione = new Label("Converti:");

        // radiobutton per scegliere la direzione
        RadioButton rbEurUsd = new RadioButton("Euro -> Dollari");
        RadioButton rbUsdEur = new RadioButton("Dollari -> Euro");

        // il togglegroup serve per far si che solo uno sia selezionato
        ToggleGroup gruppo = new ToggleGroup();
        rbEurUsd.setToggleGroup(gruppo);
        rbUsdEur.setToggleGroup(gruppo);
        rbEurUsd.setSelected(true);

        Button btnConverti = new Button("Converti");

        Label lblRisultato = new Label("Risultato:");
        Label lblOutput = new Label("---");

        // posiziono tutto nella griglia (colonna, riga)
        grid.add(lblImporto, 0, 0);
        grid.add(txtImporto, 1, 0);

        grid.add(lblDirezione, 0, 1);
        grid.add(rbEurUsd, 1, 1);
        grid.add(rbUsdEur, 1, 2);

        grid.add(btnConverti, 1, 3);

        grid.add(lblRisultato, 0, 4);
        grid.add(lblOutput, 1, 4);

        // quando clicco il pulsante
        btnConverti.setOnAction(e -> {
            try {
                double importo = Double.parseDouble(txtImporto.getText());
                double risultato;
                String valuta;

                if (rbEurUsd.isSelected()) {
                    // euro -> dollari
                    risultato = importo * TASSO;
                    valuta = "$";
                } else {
                    // dollari -> euro
                    risultato = importo / TASSO;
                    valuta = "€";
                }

                lblOutput.setText(String.format("%.2f %s", risultato, valuta));

            } catch (NumberFormatException ex) {
                lblOutput.setText("Inserisci un numero valido!");
            }
        });

        Scene scene = new Scene(grid, 320, 200);
        stage.setTitle("Convertitore Euro/Dollari");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}
