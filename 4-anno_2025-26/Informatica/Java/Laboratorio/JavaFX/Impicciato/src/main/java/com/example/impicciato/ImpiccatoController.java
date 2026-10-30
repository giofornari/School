package com.example.impicciato;

import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.input.KeyEvent;

import java.io.InputStream;
import java.util.HashSet;
import java.util.Locale;
import java.util.Objects;
import java.util.Random;
import java.util.Set;

public class ImpiccatoController {

    @FXML
    private ImageView imgImpiccato;

    @FXML
    private Label lblParolaDaIndovinare;

    @FXML
    private Label lblLettereProvate;

    private final String[] parole = {"gatto", "cane", "elefante", "scimmia", "leone", "tigre"};
    private String parolaDaIndovinare;
    private StringBuilder parolaDaScoprire;
    private int tentativiFalliti;
    private static final int MAX_TENTATIVI = 10;
    private static final String IMAGE_BASE = "/images/";
    private final Set<Character> lettereProvate = new HashSet<>();

    @FXML
    public void initialize() {
        nuovaPartita();
        if (lblParolaDaIndovinare.getScene() != null) {
            var scene = lblParolaDaIndovinare.getScene();
            scene.setOnKeyTyped(this::keyEvent);
            if (scene.getRoot() != null) {
                scene.getRoot().setFocusTraversable(true);
                scene.getRoot().requestFocus();
            }
        }
        lblParolaDaIndovinare.sceneProperty().addListener((obs, oldS, newS) -> {
            if (newS != null) {
                newS.setOnKeyTyped(this::keyEvent);
                if (newS.getRoot() != null) {
                    newS.getRoot().setFocusTraversable(true);
                    newS.getRoot().requestFocus();
                }
            } else if (oldS != null) {
                oldS.setOnKeyTyped(null);
            }
            // reference obs so static analysis doesn't warn about unused parameter
            Objects.requireNonNull(obs);
        });
    }

    private void nuovaPartita() {
        Random random = new Random();
        parolaDaIndovinare = parole[random.nextInt(parole.length)];
        parolaDaScoprire = new StringBuilder("_ ".repeat(parolaDaIndovinare.length()));
        lblParolaDaIndovinare.setText(parolaDaScoprire.toString().trim());
        tentativiFalliti = 0;
        lettereProvate.clear();
        lblLettereProvate.setText("Lettere provate: ");
        aggiornaImmagine();
    }

    @FXML
    void keyEvent(KeyEvent event) {
        String txt = event.getCharacter();
        if (txt == null) return;
        txt = txt.toLowerCase(Locale.ROOT);
        if (txt.length() != 1 || !Character.isLetter(txt.charAt(0))) return;
        char ch = txt.charAt(0);
        if (lettereProvate.contains(ch)) return;
        lettereProvate.add(ch);
        lblLettereProvate.setText("Lettere provate: " + lettereProvate);
        if (parolaDaIndovinare.indexOf(ch) >= 0) {
            for (int i = 0; i < parolaDaIndovinare.length(); i++) {
                if (parolaDaIndovinare.charAt(i) == ch) {
                    parolaDaScoprire.setCharAt(i * 2, ch);
                }
            }
            lblParolaDaIndovinare.setText(parolaDaScoprire.toString().trim());
        } else {
            tentativiFalliti++;
            aggiornaImmagine();
        }
        controllaVittoriaOSconfitta();
    }

    private void aggiornaImmagine() {
        if (tentativiFalliti <= MAX_TENTATIVI) {
            String fileName = IMAGE_BASE + tentativiFalliti + ".png";
            try (InputStream is = getClass().getResourceAsStream(fileName)) {
                if (is == null) return;
                Image image = new Image(is);
                imgImpiccato.setImage(image);
            } catch (Exception ignored) {
            }
        }
    }

    private void controllaVittoriaOSconfitta() {
        if (parolaDaScoprire.indexOf("_") < 0) {
            lblParolaDaIndovinare.setText("HAI VINTO! La parola era: " + parolaDaIndovinare);
            disabilitaInput();
        }
        if (tentativiFalliti >= MAX_TENTATIVI) {
            lblParolaDaIndovinare.setText("HAI PERSO! La parola era: " + parolaDaIndovinare);
            disabilitaInput();
        }
    }

    private void disabilitaInput() {
        if (lblParolaDaIndovinare.getScene() != null) {
            lblParolaDaIndovinare.getScene().setOnKeyTyped(null);
        }
    }
}
