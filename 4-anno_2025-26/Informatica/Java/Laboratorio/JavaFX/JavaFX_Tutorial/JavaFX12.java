import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class JavaFX12 extends Application {

    @Override
    public void start(Stage stage) throws Exception {
        Parent root = FXMLLoader.load(getClass().getResource("main-view.fxml"));
        stage.setTitle("FXML Demo");
        stage.setScene(new Scene(root, 420, 220));
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}
