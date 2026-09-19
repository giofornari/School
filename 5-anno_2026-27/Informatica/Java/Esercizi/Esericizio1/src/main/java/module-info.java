module com.verifica.esericizio1 {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.verifica.esericizio1 to javafx.fxml;
    exports com.verifica.esericizio1;
}