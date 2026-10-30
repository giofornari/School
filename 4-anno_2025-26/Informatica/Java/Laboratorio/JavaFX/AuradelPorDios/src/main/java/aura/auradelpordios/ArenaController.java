package aura.auradelpordios;

import aura.auradelpordios.arena.Arena;
import aura.auradelpordios.arena.Spell;
import aura.auradelpordios.arena.SpellType;
import aura.auradelpordios.arena.Wizard;
import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.geometry.Pos;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextArea;
import javafx.scene.image.ImageView;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class ArenaController {

    @FXML
    private BorderPane mainPane;

    @FXML
    private Label titleLabel;

    @FXML
    private HBox wizardsContainer;

    @FXML
    private TextArea battleLog;

    @FXML
    private Button nextTurnButton;

    @FXML
    private Button autoBattleButton;

    @FXML
    private Button auraInfinitaButton;

    private Arena arena;
    private Random random = new Random();
    private boolean auraInfinitaAttiva = false;

    @FXML
    public void initialize() {
        List<Wizard> wizards = new ArrayList<>();
        
        Wizard w1 = new Wizard("Merlino", "Il Boomer");
        w1.addSpell(new Spell("Siuuum di Fuoco", 15, 12, SpellType.ATTACCO));
        w1.addSpell(new Spell("Bevi Tachipirina", 10, 8, SpellType.CURA));
        w1.addSpell(new Spell("pop /bin/sh", 25, 20, SpellType.SHELL_PAYLOAD));
        
        Wizard w2 = new Wizard("Morgana", "La Cringe");
        w2.addSpell(new Spell("Dissing su TikTok", 12, 10, SpellType.ATTACCO));
        w2.addSpell(new Spell("Filtro Bellezza", 15, 10, SpellType.CURA));
        w2.addSpell(new Spell("rm -rf /", 30, 25, SpellType.SHELL_PAYLOAD));
        
        Wizard w3 = new Wizard("Gandalf", "Il Chad");
        w3.addSpell(new Spell("Fart Fulminante", 18, 15, SpellType.ATTACCO));
        w3.addSpell(new Spell("Sdrogo Curativo", 20, 15, SpellType.CURA));
        
        Wizard w4 = new Wizard("Smongolo", "L'Aura Master");
        w4.addSpell(new Spell("Schiaffo a Mano Aperta", 5, 5, SpellType.ATTACCO));
        w4.addSpell(new Spell("Kamehameha ma fatta male", 20, 30, SpellType.SHELL_PAYLOAD));
        
        wizards.add(w1);
        wizards.add(w2);
        wizards.add(w3);
        wizards.add(w4);

        arena = new Arena(wizards);
        
        updateUI();
        battleLog.appendText("🔥 BENVENUTI NELLA LOBBY DEI MEGA SMONGOLI 🔥\n");
        battleLog.appendText("AURA MAXIMA INIZIALIZZATA A LIVELLO: PEFFORZA\n\n");
    }

    private void updateUI() {
        wizardsContainer.getChildren().clear();
        
        String[] bgs = {"#ff00ff", "#00ff00", "#ffff00", "#00ffff", "#ff0000", "#0000ff"};
        
        for (Wizard w : arena.getWizards()) {
            VBox wizardBox = new VBox(5);
            wizardBox.setAlignment(Pos.CENTER);
            
            String bgColor = auraInfinitaAttiva ? bgs[random.nextInt(bgs.length)] : "#2a2a4e";
            wizardBox.setStyle("-fx-background-color: " + bgColor + "; -fx-padding: 10; -fx-border-color: #00ffcc; -fx-border-width: 5; -fx-border-radius: 15;");
            
            ImageView imageView = new ImageView();
            imageView.setFitHeight(100);
            imageView.setFitWidth(100);
            
            Label imgPlaceholder = new Label("FOTO BRUTTA\nQUI");
            imgPlaceholder.setStyle("-fx-background-color: #666666; -fx-text-fill: #ff00ff; -fx-font-family: 'Comic Sans MS'; -fx-min-width: 100; -fx-min-height: 100; -fx-alignment: center; -fx-text-alignment: center;");
            
            Label nameLabel = new Label(w.getNome() + "\n(" + w.getAlias() + ")");
            nameLabel.setStyle("-fx-text-fill: white; -fx-font-family: 'Comic Sans MS'; -fx-font-weight: bold; -fx-font-size: 16px; -fx-alignment: center; -fx-text-alignment: center;");
            if (auraInfinitaAttiva) nameLabel.setStyle("-fx-text-fill: black; -fx-font-family: 'Impact'; -fx-font-size: 20px;");
            
            Label hpLabel = new Label("HP: " + w.getHp() + " / " + w.getHpMax());
            hpLabel.setStyle(w.isAlive() ? "-fx-text-fill: #00ff00; -fx-font-weight: bold; -fx-font-size: 18px;" : "-fx-text-fill: red; -fx-font-weight: bold; -fx-font-size: 18px;");
            
            Label manaLabel = new Label("Mana: " + w.getMana() + " / " + w.getManaMax());
            manaLabel.setStyle("-fx-text-fill: #00ffff; -fx-font-weight: bold; -fx-font-size: 18px;");
            
            wizardBox.getChildren().addAll(imgPlaceholder, imageView, nameLabel, hpLabel, manaLabel);
            wizardsContainer.getChildren().add(wizardBox);
        }
        
        if (auraInfinitaAttiva) {
            mainPane.setStyle("-fx-background-color: " + bgs[random.nextInt(bgs.length)] + ";");
            titleLabel.setText("🔥🔥 AURA È OVER 9000!!! 🔥🔥");
        }
    }

    @FXML
    protected void onNextTurn() {
        if (arena.getWinner() != null) return;
        
        String log = arena.playTurn();
        battleLog.appendText(log + "\n");
        updateUI();
        
        checkWinner();
    }

    @FXML
    protected void onAutoBattle() {
        nextTurnButton.setDisable(true);
        autoBattleButton.setDisable(true);
        auraInfinitaButton.setDisable(true);
        
        new Thread(() -> {
            while (arena.getWinner() == null) {
                String log = arena.playTurn();
                Platform.runLater(() -> {
                    battleLog.appendText(log + "\n");
                    updateUI();
                });
                
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            Platform.runLater(() -> {
                battleLog.appendText("\n🏆 LA LOBBY È STATA CHIUSA! 🏆\n");
                checkWinner();
            });
        }).start();
    }
    
    @FXML
    protected void onAuraInfinita() {
        auraInfinitaAttiva = true;
        battleLog.appendText("\n🚨🚨🚨 ALLARME! AURA INFINITA ATTIVATA! 🚨🚨🚨\n");
        
        for (Wizard w : arena.getWizards()) {
            if (w.getNome().equals("Smongolo")) {
                w.heal(99999);
                w.rest(); w.rest(); w.rest(); w.rest(); w.rest(); // Fake max mana
                battleLog.appendText("💪 SMONGOLO ASSORBE L'ENERGIA DELL'UNIVERSO E DIVENTA UN DIO!!! 💪\n");
            }
        }
        
        auraInfinitaButton.setText("AURA INFINITA ON!!!");
        auraInfinitaButton.setStyle("-fx-background-color: black; -fx-text-fill: white; -fx-font-family: 'Impact'; -fx-font-size: 30px;");
        updateUI();
    }
    
    private void checkWinner() {
        if (arena.getWinner() != null) {
            nextTurnButton.setDisable(true);
            autoBattleButton.setDisable(true);
            auraInfinitaButton.setDisable(true);
        }
    }
}
