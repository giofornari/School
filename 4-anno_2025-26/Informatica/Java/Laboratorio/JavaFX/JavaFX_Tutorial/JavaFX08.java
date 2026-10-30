import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

// 8) TableView con oggetti personalizzati
public class JavaFX08 extends Application {

    public static class Persona {
        private String nome;
        private int eta;
        public Persona(String nome, int eta) { this.nome = nome; this.eta = eta; }
        public String getNome() { return nome; }
        public int getEta() { return eta; }
    }

    @Override
    public void start(Stage stage) {
        /* TableView con oggetti Persona, ogni riga è oggetto persona */
        TableView<Persona> table = new TableView<>();
        // Creazione colonne. Si inseriscono i titoli delle colonne Ogni colonna mapperà una proprietà dell'oggetto Persona
        TableColumn<Persona, String> colNome = new TableColumn<>("Nome");
        TableColumn<Persona, Integer> colEta = new TableColumn<>("Età");

        // Collegamento colonne alle proprietà dell'oggetto Persona
        // "nome" → chiama getNome() "eta" → chiama getEta()
        colNome.setCellValueFactory(new PropertyValueFactory<>("nome"));
        colEta.setCellValueFactory(new PropertyValueFactory<>("eta"));

        /* Aggiunta delle colonne alla tabella 
            causa warning: “possible heap pollution from parameterized vararg type” perché
            ⚠️ Attenzione: usando varargs (...) con tipi generici, potresti inserire nel heap un oggetto di tipo sbagliato senza che il compilatore se ne accorga.
        */
        table.getColumns().addAll(colNome, colEta);

        /* Inserimento dati nella tabella
            getItems(): è una ObservableList
            ogni elemento diventa una riga della tabella*/
        table.getItems().addAll(
            new Persona("Marco", 18),
            new Persona("Luca", 19),
            new Persona("Maria", 18)
        );

        VBox root = new VBox(10, table);
        stage.setScene(new Scene(root, 300, 250));
        stage.show();
    }

    public static void main(String[] args) { launch(); }
}
