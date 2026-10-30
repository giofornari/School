import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;

public class MainController {

    @FXML private TextField txtNome;
    @FXML private Label lblMessaggio;

    @FXML
    private void onSaluta(ActionEvent event) {
        String nome = txtNome.getText().trim();
        if (nome.isEmpty()) {
            lblMessaggio.setText("Inserisci un nome 🙂");
        } else {
            lblMessaggio.setText("Ciao " + nome + "!");
        }
    }
}

