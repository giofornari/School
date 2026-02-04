package com.example.convertitorexml;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;

public class ConvertitoreController {

    // Exchange rate (approximation - 1 EUR = 1.08 USD as of 2026)
    private static final double EUR_TO_USD = 1.08;
    private static final double USD_TO_EUR = 1 / EUR_TO_USD;

    @FXML
    private Button btnChiudi;

    @FXML
    private Button btnDollari;

    @FXML
    private Button btnEuro;

    @FXML
    private TextField tfDollari;

    @FXML
    private TextField tfEuro;

    
    @FXML
    void btnChiudiEvent(ActionEvent event) {
        System.exit(0);
    }

    @FXML
    void btnDollariEvent(ActionEvent event) {
        try {
            String dollarText = tfDollari.getText().trim();
            if (dollarText.isEmpty()) {
                showError("Input Error", "Please enter an amount in dollars.");
                return;
            }

            double dollars = Double.parseDouble(dollarText);
            if (dollars < 0) {
                showError("Input Error", "Amount cannot be negative.");
                return;
            }

            double euros = dollars * USD_TO_EUR;
            tfEuro.setText(String.format("%.2f", euros));

        } catch (NumberFormatException e) {
            showError("Input Error", "Please enter a valid number.");
        }
    }

    @FXML
    void btnEuroEvent(ActionEvent event) {
        try {
            String euroText = tfEuro.getText().trim();
            if (euroText.isEmpty()) {
                showError("Input Error", "Please enter an amount in euros.");
                return;
            }

            double euros = Double.parseDouble(euroText);
            if (euros < 0) {
                showError("Input Error", "Amount cannot be negative.");
                return;
            }

            double dollars = euros * EUR_TO_USD;
            tfDollari.setText(String.format("%.2f", dollars));

        } catch (NumberFormatException e) {
            showError("Input Error", "Please enter a valid number.");
        }
    }

    private void showError(String title, String message) {
        Alert alert = new Alert(Alert.AlertType.ERROR);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }
}
