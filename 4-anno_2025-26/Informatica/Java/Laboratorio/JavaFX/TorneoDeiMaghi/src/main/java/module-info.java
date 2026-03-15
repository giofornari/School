module com.example.torneodeimaghi {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.example.torneodeimaghi to javafx.fxml;
    exports com.example.torneodeimaghi;
}