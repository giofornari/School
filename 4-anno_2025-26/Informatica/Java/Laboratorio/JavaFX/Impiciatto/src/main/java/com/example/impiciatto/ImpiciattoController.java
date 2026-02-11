package com.example.impiciatto;

import javafx.fxml.FXML;
import javafx.scene.control.Label;

public class ImpiciattoController {
    @FXML
    private Label welcomeText;

    @FXML
    protected void onHelloButtonClick() {
        welcomeText.setText("Welcome to JavaFX Application!");
    }
}
