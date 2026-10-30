module aura.esercitazioneverifica {
    requires javafx.controls;
    requires javafx.fxml;

    requires org.kordamp.bootstrapfx.core;

    opens aura.esercitazioneverifica to javafx.fxml;
    exports aura.esercitazioneverifica;
}