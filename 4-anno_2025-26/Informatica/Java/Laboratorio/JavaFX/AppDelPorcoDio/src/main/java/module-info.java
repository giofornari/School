module aura.appdelporcodio {
    requires javafx.controls;
    requires javafx.fxml;


    opens aura.appdelporcodio to javafx.fxml;
    exports aura.appdelporcodio;
}