import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.GridPane;
import javafx.stage.Stage;

public class GridPaneDemo extends Application {

    @Override
    public void start(Stage stage) {

        GridPane grid = new GridPane();

        // spaziatura tra celle
        grid.setHgap(10);
        grid.setVgap(10);

        // margine interno
        grid.setPadding(new Insets(15));

        // === NODI ===
        Label lblNome = new Label("Nome:");
        TextField txtNome = new TextField();

        Label lblCognome = new Label("Cognome:");
        TextField txtCognome = new TextField();

        Label lblClasse = new Label("Classe:");
        ComboBox<String> cmbClasse = new ComboBox<>();
        cmbClasse.getItems().addAll("3Ainf", "4Ainf", "5Ainf");

        Button btnOk = new Button("OK");
        Button btnAnnulla = new Button("Annulla");

        // === POSIZIONAMENTO (colonna, riga) ===
        grid.add(lblNome,     0, 0);
        grid.add(txtNome,     1, 0);

        grid.add(lblCognome,  0, 1);
        grid.add(txtCognome,  1, 1);

        grid.add(lblClasse,   0, 2);
        grid.add(cmbClasse,   1, 2);

        grid.add(btnOk,       0, 3);
        grid.add(btnAnnulla,  1, 3);

        // allineamento pulsanti
        GridPane.setHalignment(btnOk, Pos.CENTER_LEFT.getHpos());
        GridPane.setHalignment(btnAnnulla, Pos.CENTER_RIGHT.getHpos());

        Scene scene = new Scene(grid, 320, 220);
        stage.setTitle("Esempio GridPane");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}
