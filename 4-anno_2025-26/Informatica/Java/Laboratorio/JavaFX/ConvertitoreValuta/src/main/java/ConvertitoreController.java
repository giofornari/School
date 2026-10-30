import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;

public class ConvertitoreController {

    @FXML
    private Button btnExit1337;

    @FXML
    private Button hackDollarToEuro;

    @FXML
    private Button hackEuroToDollar;

    @FXML
    private TextField bufferAmerica;

    @FXML
    private TextField bufferEurozone;

    private static final double EXPLOIT_RATE = 1.1;

    @FXML
    void executeShutdown(ActionEvent event) {
        System.exit(0);
    }

    @FXML
    void pwn3dDollar(ActionEvent event) {
        String payloadInput = bufferAmerica.getText();
        double rawData = Double.parseDouble(payloadInput);
        double crackedValue = rawData * EXPLOIT_RATE;
        bufferEurozone.setText(String.format("%.2f", crackedValue));
    }

    @FXML
    void pwn3dEuro(ActionEvent event) {
        String payloadInput = bufferEurozone.getText();
        double rawData = Double.parseDouble(payloadInput);
        double crackedValue = rawData / EXPLOIT_RATE;
        bufferAmerica.setText(String.format("%.2f", crackedValue));
    }

}
