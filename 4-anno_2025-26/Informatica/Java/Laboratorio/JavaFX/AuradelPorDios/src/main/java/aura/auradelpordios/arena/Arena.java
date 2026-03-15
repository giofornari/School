package aura.auradelpordios.arena;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

public class Arena {
    private List<Wizard> wizards;
    private int turno;

    public Arena(List<Wizard> wizards) {
        this.wizards = new ArrayList<>(wizards);
        this.turno = 1;
    }

    public List<Wizard> getAliveWizards() {
        return wizards.stream()
                .filter(Wizard::isAlive)
                .collect(Collectors.toList());
    }

    public Wizard getWinner() {
        List<Wizard> alive = getAliveWizards();
        if (alive.size() == 1) {
            return alive.get(0);
        }
        return null;
    }
    
    public List<Wizard> getWizards() {
        return this.wizards;
    }

    public String playTurn() {
        if (getWinner() != null) {
            return "La battaglia è già finita. Il vincitore è " + getWinner().getNome() + "!";
        }

        StringBuilder log = new StringBuilder();
        log.append("--- TURNO ").append(turno).append(" ---\n");

        List<Wizard> aliveWizards = getAliveWizards();
        // Ordina per velocità decrescente
        aliveWizards.sort(Comparator.comparingInt(Wizard::getVelocita).reversed());

        for (Wizard w : aliveWizards) {
            if (w.isAlive() && getWinner() == null) {
                String actionLog = AIController.takeAction(w, getAliveWizards());
                log.append(actionLog).append("\n");
            }
        }

        turno++;
        
        Wizard winner = getWinner();
        if (winner != null) {
            log.append("\n!!! ").append(winner.getNome()).append(" TRIONFA E DOMINA L'ARENA CON UN'AURA IMMENSA !!!\n");
        }

        return log.toString();
    }
}
