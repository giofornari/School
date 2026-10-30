package aura.esercitazioneverifica;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;

public class ConvertitoreController {

    @FXML
    private Button btn_chiudi;

    @FXML
    private Button btn_dollar;

    @FXML
    private Button btn_euro;

    @FXML
    private TextField txt_dollar;

    @FXML
    private TextField txt_euro;

    @FXML
    void btn_chiudiEvent(ActionEvent event) {
        System.exit(0);
    }

    @FXML
    void btn_dollarEvent(ActionEvent event) {
        double euro = Double.parseDouble(txt_dollar.getText());
        txt_euro.setText(String.format("%.2f", euro * 1.1));
    }

    @FXML
    void btn_euroEvent(ActionEvent event) {
        double dollar = Double.parseDouble(txt_euro.getText());
        txt_dollar.setText(String.format("%.2f", dollar / 1.1));
    }

}
