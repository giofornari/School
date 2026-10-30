package com.verifica.esericizio1;

import javafx.fxml.FXML;
import javafx.scene.control.*;

import java.util.ArrayList;

public class HelloController {

    @FXML
    private TextField txtnome, txtmarca, txtvalore, txttipo, txtnumm, txtggiorni;
    @FXML
    private Label lblnumm, lblerror;
    @FXML
    private TextArea txaoffer, txacarrello;

    private ArrayList<Strumento> lista = new ArrayList<>();
    private Strumento ultimo = null;

    @FXML
    public void initialize() {
        txttipo.focusedProperty().addListener((obs, old, newVal) -> {
            if (!newVal) updeitaCampo();
        });
    }

    private void updeitaCampo() {
        String t = txttipo.getText().trim().toLowerCase();
        if (t.equals("chitarra")) lblnumm.setText("N. Corde:");
        else if (t.equals("tastiera")) lblnumm.setText("N. Tasti:");
        else if (t.equals("batteria")) lblnumm.setText("N. Pezzi:");
        else if (t.equals("violino")) lblnumm.setText("Età (anni):");
        else lblnumm.setText("Campo:");
    }

    @FXML
    private void onGo() {
        String nome = txtnome.getText().trim();
        String marca = txtmarca.getText().trim();
        String valStr = txtvalore.getText().trim();
        String tipo = txttipo.getText().trim();
        String nummStr = txtnumm.getText().trim();

        double val;
        int campo;
        val = Double.parseDouble(valStr);
        campo = Integer.parseInt(nummStr);

        Strumento s;
        if (tipo.equalsIgnoreCase("Chitarra")) {
            s = new Chitarra(nome, marca, val, campo);
        }else if (tipo.equalsIgnoreCase("Tastiera")) {
            s = new Tastiera(nome, marca, val, campo);
        } else if (tipo.equalsIgnoreCase("Batteria")) {
            s = new Batteria(nome, marca, val, campo);
        } else if (tipo.equalsIgnoreCase("Violino")) {
            s = new Violino(nome, marca, val, campo);
        } else return;

        lista.add(s);
        ultimo = s;
        updeitaElenco();
        txacarrello.setText(s.info());
        lblerror.setText("fatto. aggiunto.");
    }

    @FXML
    private void onDimmi() {
        int gg;
        gg = Integer.parseInt(txtggiorni.getText().trim());
        double costo = ultimo.costoNoleggio(gg);
        txacarrello.setText(ultimo.info() + "\n\npricezo (" + gg + " giorni): " + costo + " €");
        lblerror.setText("costo trovato.");
        lblerror.setStyle("-fx-text-fill: green;");

    }

    private void updeitaElenco() {
        StringBuilder sb = new StringBuilder();
        for (Strumento s : lista) {
            sb.append(s.getNome()).append(" · ")
              .append(s.getClass().getSimpleName()).append(" · ")
              .append(s.getValore()).append(" €\n");
        }
        txaoffer.setText(sb.toString());
    }
}
