import javafx.application.Application;
import javafx.beans.property.IntegerProperty;
import javafx.beans.property.SimpleIntegerProperty;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

// 4) Contatore con Binding
public class JavaFX04 extends Application{
    @Override
    public void start(Stage stage) {
        IntegerProperty count = new SimpleIntegerProperty(0);

        Label lbl = new Label();
        lbl.textProperty().bind(count.asString());

        Button btn = new Button("Aumenta");
        btn.setOnAction(e -> count.set(count.get() + 1));

        VBox root = new VBox(10, lbl, btn);
        stage.setScene(new Scene(root, 200, 150));
        stage.show();
    }
    public static void main(String[] args) { launch(); }
}
