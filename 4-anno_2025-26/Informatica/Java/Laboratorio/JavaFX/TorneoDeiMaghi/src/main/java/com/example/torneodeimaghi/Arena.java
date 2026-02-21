package com.example.torneodeimaghi;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Random;
import java.util.stream.Collectors;

public class Arena {
    private List<Wizard> wizards;
    private Random random = new Random();
    private int turn = 0;

    public Arena(List<Wizard> wizards) {
        this.wizards = wizards;
    }

    public void playMatch() {
        while (getAliveWizards().size() > 1) {
            playTurn();
        }
        System.out.println("\n" + getWinner().getName() + " is the winner!");
    }

    public void playTurn() {
        turn++;
        System.out.println("\n----- Turn " + turn + " -----");
        List<Wizard> aliveWizards = getAliveWizards();
        aliveWizards.sort(Comparator.comparingInt(Wizard::getSpeed).reversed());

        for (Wizard currentWizard : aliveWizards) {
            if (currentWizard.isAlive()) {
                System.out.println("\nIt's " + currentWizard.getName() + "'s turn. " + currentWizard);
                // AI Logic
                List<Wizard> possibleTargets = getAliveWizards().stream()
                        .filter(w -> !w.equals(currentWizard))
                        .collect(Collectors.toList());

                if (possibleTargets.isEmpty()) {
                    break;
                }

                // Simple AI: If HP is low, heal. Otherwise, attack a random target.
                if (currentWizard.getHp() < currentWizard.getHpMax() * 0.3 && currentWizard.canCast(getHealSpell(currentWizard))) {
                    currentWizard.cast(getHealSpell(currentWizard), currentWizard);
                } else if (currentWizard.canCast(getAttackSpell(currentWizard))) {
                    Wizard target = possibleTargets.get(random.nextInt(possibleTargets.size()));
                    currentWizard.cast(getAttackSpell(currentWizard), target);
                } else {
                    currentWizard.rest();
                }
            }
        }
    }

    private Spell getAttackSpell(Wizard wizard) {
        return wizard.getSpellBook().stream().filter(s -> "ATTACK".equals(s.getType())).findFirst().orElse(null);
    }

    private Spell getHealSpell(Wizard wizard) {
        return wizard.getSpellBook().stream().filter(s -> "HEAL".equals(s.getType())).findFirst().orElse(null);
    }

    public List<Wizard> getAliveWizards() {
        return wizards.stream().filter(Wizard::isAlive).collect(Collectors.toList());
    }

    public Wizard getWinner() {
        return getAliveWizards().get(0);
    }
}
