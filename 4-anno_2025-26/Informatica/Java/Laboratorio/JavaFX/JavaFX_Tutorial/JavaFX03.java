import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

// 3) TextField + Button + Label (Hello + Nome)
public class JavaFX03 extends Application{
    public void start(Stage stage) {
        TextField txt = new TextField();
        txt.setPromptText("Inserisci il tuo nome");
        Label lbl = new Label();
        Button btn = new Button("Saluta");

        btn.setOnAction(e -> lbl.setText("Ciao " + txt.getText() + "!"));

        // VBox con spaziatura di 10 pixel tra i nodi
        VBox root = new VBox(10, txt, btn, lbl);
        stage.setScene(new Scene(root, 300, 200));
        stage.show();
    }
    public static void main(String[] args) { launch(); }
}
