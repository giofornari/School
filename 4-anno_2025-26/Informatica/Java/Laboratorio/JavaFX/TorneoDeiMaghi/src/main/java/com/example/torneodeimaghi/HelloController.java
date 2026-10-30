package com.example.torneodeimaghi;

import javafx.fxml.FXML;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;

import java.util.ArrayList;
import java.util.List;

public class HelloController {

    @FXML
    private HBox arenaContainer;

    @FXML
    private Label logLabel;

    @FXML
    private Button nextTurnBtn;

    @FXML
    private Button resetBtn;

    private Arena arena;
    private List<Wizard> bruhlist;

    @FXML
    public void initialize() {
        initgame();
    }

    private void initgame() {
        bruhlist = new ArrayList<>();
        Spell attacco1 = new Spell("sixseven", 7, 10, "ATTACK");
        Spell cura1 = new Spell("spiridicchio", 5, 8, "HEAL");

        Spell attacco2 = new Spell("whhaaaaaat", 9, 12, "ATTACK");
        Spell cura2 = new Spell("vam0n0s", 7, 10, "HEAL");

        Spell attacco3 = new Spell("skibidibop", 8, 11, "ATTACK");
        Spell cura3 = new Spell("centralina_si-olè", 10, 15, "HEAL");

        // random-guy-1 (67.png)
        Wizard w1 = new Wizard("random-guy-1", "67.png", 50, 30, 8, 5, 7, 
                new ArrayList<>(List.of(attacco1, cura1)));
        
        // random-guy-2 (ngga.png)
        Wizard w2 = new Wizard("random-guy-2", "ngga.png", 45, 40, 9, 4, 9, 
                new ArrayList<>(List.of(attacco2, cura2)));

        // random-guy-3 (skbd.png)
        Wizard w3 = new Wizard("random-guy-3", "skbd.png", 60, 25, 6, 7, 4, 
                new ArrayList<>(List.of(attacco3, cura3)));

        bruhlist.add(w1);
        bruhlist.add(w2);
        bruhlist.add(w3);

        arena = new Arena(bruhlist);
        
        logLabel.setText("Brienvenidos nell'Aura Baura XP! Bruh sta per poppare /bin/sh.");
        nextTurnBtn.setDisable(false);
        
        aggiornaVistaMaghi();
    }

    @FXML
    void onNextTurn() {
        if (!arena.isFinita()) {
            List<String> logs = arena.giocaTurno();
            
            StringBuilder summary = new StringBuilder();
            for (String log : logs) {
                summary.append(log).append("\n");
            }
            logLabel.setText(summary.toString());
            
            aggiornaVistaMaghi();
            
            if (arena.isFinita()) {
                Wizard popper = arena.getVincitore();
                if (popper != null) {
                    logLabel.setText(logLabel.getText() + "\nIL VINCITORE E': " + popper.getNome() + "!");
                } else {
                    logLabel.setText(logLabel.getText() + "\nSPIRIDICCHIO! tutti sconfitti.");
                }
                nextTurnBtn.setDisable(true);
            }
        }
    }

    @FXML
    void onReset() {
        initgame();
    }

    private void aggiornaVistaMaghi() {
        arenaContainer.getChildren().clear();

        for (Wizard mago : bruhlist) {
            VBox card = new VBox(10);
            card.setAlignment(Pos.CENTER);
            card.setPadding(new Insets(10));
            card.setPrefWidth(200);

            if (mago.isAlive()) {
                card.setStyle("-fx-background-color: rgba(255, 255, 255, 0.8); -fx-background-radius: 10; -fx-border-color: #333; -fx-border-radius: 10; -fx-border-width: 2;");
            } else {
                card.setStyle("-fx-background-color: rgba(100, 100, 100, 0.8); -fx-background-radius: 10; -fx-border-color: #000; -fx-border-radius: 10; -fx-border-width: 2;");
            }

            ImageView imgView = new ImageView();
            imgView.setFitWidth(120);
            imgView.setFitHeight(120);
            imgView.setPreserveRatio(true);
            
            try {
                Image img = new Image(getClass().getResourceAsStream("/com/example/torneodeimaghi/imagess/" + mago.getSpritePath()));
                imgView.setImage(img);
            } catch (Exception e) {
                System.out.println("Immagine non trovata: " + mago.getSpritePath());
            }

            Label nomeLbl = new Label(mago.getNome());
            nomeLbl.setStyle("-fx-font-weight: bold; -fx-font-size: 16px;");

            Label hpLbl = new Label("HP: " + mago.getHp() + "/" + mago.getHpMax());
            Label manaLbl = new Label("Mana: " + mago.getMana() + "/" + mago.getManaMax());
            Label statLbl = new Label("Atk: " + mago.getPower() + " | Def: " + mago.getDef() + " | Vel: " + mago.getSpd());
            
            if (!mago.isAlive()) {
                Label mortoLbl = new Label("-100000000000-AURA");
                mortoLbl.setStyle("-fx-text-fill: red; -fx-font-weight: bold;");
                card.getChildren().addAll(nomeLbl, imgView, mortoLbl);
            } else {
                card.getChildren().addAll(nomeLbl, imgView, hpLbl, manaLbl, statLbl);
            }

            arenaContainer.getChildren().add(card);
        }
    }
}
