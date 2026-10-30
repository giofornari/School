package aura.auradelpordios.arena;

import java.util.List;
import java.util.Random;

public class AIController {
    private static final Random random = new Random();

    public static String takeAction(Wizard self, List<Wizard> aliveWizards) {
        if (!self.isAlive()) return "";

        // Trova bersagli possibili (tutti tranne se stesso)
        List<Wizard> targets = aliveWizards.stream()
                .filter(w -> w != self && w.isAlive())
                .toList();

        if (targets.isEmpty()) return self.getNome() + " non ha bersagli!";

        Wizard target = targets.get(random.nextInt(targets.size()));

        // Controlla se ha "pop /bin/sh" e abbastanza mana
        Spell shellPayload = null;
        Spell healSpell = null;
        Spell attackSpell = null;

        for (Spell s : self.getSpellBook()) {
            if (s.getTipo() == SpellType.SHELL_PAYLOAD && self.canCast(s)) {
                shellPayload = s;
            } else if (s.getTipo() == SpellType.CURA && self.canCast(s)) {
                if (healSpell == null || s.getValoreBase() > healSpell.getValoreBase()) {
                    healSpell = s;
                }
            } else if (s.getTipo() == SpellType.ATTACCO && self.canCast(s)) {
                if (attackSpell == null || s.getValoreBase() > attackSpell.getValoreBase()) {
                    attackSpell = s;
                }
            }
        }

        // Logica AI
        if (shellPayload != null && random.nextDouble() > 0.3) {
            return self.cast(shellPayload, target);
        }

        if (self.getHp() < (self.getHpMax() * 0.3) && healSpell != null) {
            return self.cast(healSpell, self);
        }

        if (attackSpell != null) {
            return self.cast(attackSpell, target);
        }

        return self.rest();
    }
}
