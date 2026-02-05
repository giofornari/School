module com.example.impiciatto {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.example.impiciatto to javafx.fxml;
    exports com.example.impiciatto;
}