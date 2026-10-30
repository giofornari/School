import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.stage.Stage;

//1) Finestra con Label (base)
public class JavaFX01 extends Application {
    @Override
    public void start(Stage stage) {
        Label lbl = new Label("Hello JavaFX!");
        stage.setScene(new Scene(lbl, 300, 100));
        stage.show();
    }
    public static void main(String[] args) { launch(); }
}
