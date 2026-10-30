import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

// 2) Pulsante che cambia il testo della Label
public class JavaFX02 extends Application {
    @Override
    public void start(Stage stage) {
        Label lbl = new Label("Premi il pulsante");
        Button btn = new Button("Cliccami");

        btn.setOnAction(e -> lbl.setText("Hai cliccato!"));

        // VBox con spaziatura di 10 pixel tra i nodi
        VBox root = new VBox(10, lbl, btn);
        stage.setScene(new Scene(root, 300, 150));
        stage.show();
    }
    public static void main(String[] args) { launch(); }
}
