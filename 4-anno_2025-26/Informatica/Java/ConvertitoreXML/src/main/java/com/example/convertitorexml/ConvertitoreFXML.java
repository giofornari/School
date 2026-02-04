package com.example.convertitorexml;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class ConvertitoreFXML extends Application {

    @Override
    public void start(Stage stage) throws Exception {
        Parent root = FXMLLoader.load(getClass().getResource("Convertitore.fxml"));
        stage.setTitle("Convertitore di Valuta");
        stage.setScene(new Scene(root, 450, 200));
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}
