import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

// 5) ListView dinamica (aggiungi elemento)
public class JavaFX05 extends Application{
    @Override
    public void start(Stage stage) {
        // Creazione ObservableList per la ListView (diventa il contenitore dati)
        ObservableList<String> items = FXCollections.observableArrayList();
        // Creazione ListView (il componente visuale) con la ObservableList
        ListView<String> list = new ListView<>(items);
        TextField txt = new TextField();
        Button btn = new Button("Aggiungi");

        btn.setOnAction(e -> {
            if (!txt.getText().isEmpty()) {
                items.add(txt.getText());
                txt.clear();
            }
        });

        VBox root = new VBox(10, txt, btn, list);
        stage.setScene(new Scene(root, 300, 300));
        stage.show();
    }
    public static void main(String[] args) { launch(); }
}
