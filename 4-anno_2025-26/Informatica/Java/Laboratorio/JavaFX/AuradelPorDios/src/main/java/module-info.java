module aura.auradelpordios {
    requires javafx.controls;
    requires javafx.fxml;


    opens aura.auradelpordios to javafx.fxml;
    exports aura.auradelpordios;
}