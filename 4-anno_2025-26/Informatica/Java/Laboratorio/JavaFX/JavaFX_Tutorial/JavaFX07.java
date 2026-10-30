import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

// 7) Slider + ProgressBar (binding)
public class JavaFX07 extends Application {
    @Override
    public void start(Stage stage) {
        Slider slider = new Slider(0, 1, 0);
        ProgressBar bar = new ProgressBar(0);

        bar.progressProperty().bind(slider.valueProperty());

        VBox root = new VBox(10, slider, bar);
        stage.setScene(new Scene(root, 300, 150));
        stage.show();
    }
    public static void main(String[] args) { launch(); }
}