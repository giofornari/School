module com.example.convertitorexml {
    requires javafx.controls;
    requires javafx.fxml;

    requires org.controlsfx.controls;

    opens com.example.convertitorexml to javafx.fxml;
    exports com.example.convertitorexml;
}