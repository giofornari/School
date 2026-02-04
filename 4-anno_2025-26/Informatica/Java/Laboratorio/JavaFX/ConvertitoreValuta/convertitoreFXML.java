import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class convertitoreFXML extends Application {

    @Override
    public void start(Stage terminal) throws Exception {
        Parent rootAccess = FXMLLoader.load(getClass().getResource("Convertitore.fxml"));
        terminal.setTitle("CryptoConverter v1.337");
        terminal.setScene(new Scene(rootAccess, 550, 320));
        terminal.show();
    }

    public static void main(String[] args) {
        Application.launch(convertitoreFXML.class, args);
    }
}
