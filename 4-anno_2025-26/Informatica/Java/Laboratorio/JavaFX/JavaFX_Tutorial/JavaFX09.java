import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

// 9) Multi-finestra (aprire una seconda Stage)
public class JavaFX09 extends Application {
    @Override
    public void start(Stage stage) {
        Button open = new Button("Apri nuova finestra");

        open.setOnAction(e -> {
            Stage second = new Stage();
            second.setScene(new Scene(new VBox(new Button("Ciao!")), 200, 100));
            second.show();
        });

        stage.setScene(new Scene(new VBox(open), 300, 150));
        stage.show();
    }
    public static void main(String[] args) { launch(); }
}
