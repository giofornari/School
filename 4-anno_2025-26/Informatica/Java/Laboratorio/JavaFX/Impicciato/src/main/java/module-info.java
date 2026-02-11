module com.example.impicciato {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.example.impicciato to javafx.fxml;
    exports com.example.impicciato;
}