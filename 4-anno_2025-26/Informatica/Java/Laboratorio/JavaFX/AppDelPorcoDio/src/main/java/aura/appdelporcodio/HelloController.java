package aura.appdelporcodio;

import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.scene.layout.VBox;

public class HelloController {
    // Login Screen Components
    @FXML
    private VBox welcome_screen;

    @FXML
    private TextField username;

    @FXML
    private PasswordField password;

    @FXML
    private CheckBox ai;

    @FXML
    private Button login;

    @FXML
    private Button home;

    @FXML
    private Button close;

    @FXML
    public void initialize() {
        // Add event handlers
        login.setOnAction(e -> onLoginButtonClick());
        close.setOnAction(e -> onCloseButtonClick());
        home.setOnAction(e -> onHomeButtonClick());
    }

    @FXML
    protected void onLoginButtonClick() {
        String user = username.getText().trim();
        String pass = password.getText().trim();
        boolean isAI = ai.isSelected();

        // Validation
        if (user.isEmpty() || pass.isEmpty()) {
            showError("Username e password sono obbligatori!");
            return;
        }

        if (!isAI) {
            showError("Devi confermare di non essere un AI agent!");
            return;
        }

        // Simple authentication (hardcoded for now)
        if (validateCredentials(user, pass)) {
            showSuccess("Login successful!");
            // Here you would load the home/main screen
            clearLoginForm();
        } else {
            showError("Username o password errati!");
        }
    }

    @FXML
    protected void onCloseButtonClick() {
        System.exit(0);
    }

    @FXML
    protected void onHomeButtonClick() {
        // Navigate to home screen (to be implemented)
        showInfo("Tornando alla home...");
    }

    private boolean validateCredentials(String user, String pass) {
        // Simple hardcoded credentials for demo
        return user.equals("admin") && pass.equals("password123");
    }

    private void showError(String message) {
        Alert alert = new Alert(Alert.AlertType.ERROR);
        alert.setTitle("Errore");
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }

    private void showSuccess(String message) {
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setTitle("Successo");
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }

    private void showInfo(String message) {
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setTitle("Info");
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }

    private void clearLoginForm() {
        username.clear();
        password.clear();
        ai.setSelected(false);
    }
}
