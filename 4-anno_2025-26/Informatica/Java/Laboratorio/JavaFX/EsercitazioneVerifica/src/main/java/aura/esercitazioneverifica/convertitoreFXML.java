package aura.esercitazioneverifica;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class convertitoreFXML extends Application {

    @Override
    public void start(Stage stage) throws Exception {
        // Ensure the FXML is loaded from the correct resource path
        var resource = getClass().getResource("/aura/esercitazioneverifica/hello-view.fxml");
        Parent root = FXMLLoader.load(resource);
        stage.setTitle("FXML Demo");
        stage.setScene(new Scene(root, 420, 220));
        stage.show();
    }
    static void main() {
        launch();
    }
}
