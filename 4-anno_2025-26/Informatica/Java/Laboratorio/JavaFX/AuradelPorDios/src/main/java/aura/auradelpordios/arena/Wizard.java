package aura.auradelpordios.arena;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Wizard {
    private String nome;
    private String alias;
    private int hp, hpMax;
    private int mana, manaMax;
    private int potenzaMagica;
    private int difesa;
    private int velocita;
    private List<Spell> spellBook;

    private static final Random random = new Random();

    public Wizard(String nome, String alias) {
        this.nome = nome;
        this.alias = alias;
        
        // Assegnazione valori iniziali
        this.hpMax = random.nextInt(21) + 40; // 40-60
        this.hp = this.hpMax;
        
        this.manaMax = random.nextInt(21) + 20; // 20-40
        this.mana = this.manaMax;
        
        this.potenzaMagica = random.nextInt(6) + 5; // 5-10
        this.difesa = random.nextInt(6) + 3; // 3-8
        this.velocita = random.nextInt(10) + 1; // 1-10
        
        this.spellBook = new ArrayList<>();
    }

    public void addSpell(Spell spell) {
        this.spellBook.add(spell);
    }

    public String getNome() { return nome; }
    public String getAlias() { return alias; }
    public int getHp() { return hp; }
    public int getHpMax() { return hpMax; }
    public int getMana() { return mana; }
    public int getManaMax() { return manaMax; }
    public int getPotenzaMagica() { return potenzaMagica; }
    public int getDifesa() { return difesa; }
    public int getVelocita() { return velocita; }
    public List<Spell> getSpellBook() { return spellBook; }

    public boolean isAlive() {
        return hp > 0;
    }

    public void takeDamage(int danno) {
        this.hp -= danno;
        if (this.hp < 0) {
            this.hp = 0;
        }
    }

    public void heal(int quantita) {
        this.hp += quantita;
        if (this.hp > this.hpMax) {
            this.hp = this.hpMax;
        }
    }

    public boolean canCast(Spell s) {
        return this.mana >= s.getCostoMana();
    }

    public String cast(Spell s, Wizard target) {
        if (!isAlive()) return this.nome + " è morto e non può lanciare incantesimi.";
        if (!canCast(s)) return this.nome + " non ha abbastanza mana per lanciare " + s.getNome();

        this.mana -= s.getCostoMana();

        if (s.getTipo() == SpellType.ATTACCO || s.getTipo() == SpellType.SHELL_PAYLOAD) {
            int danno = s.getValoreBase() + this.potenzaMagica - target.getDifesa();
            if (danno < 1) danno = 1;
            
            if (s.getTipo() == SpellType.SHELL_PAYLOAD) {
                // SHELL_PAYLOAD ignores some defense or does extra fixed damage
                danno += 10;
            }

            target.takeDamage(danno);
            String result = this.nome + " lancia " + s.getNome() + " contro " + target.getNome() + " causando " + danno + " danni!";
            if (!target.isAlive()) {
                result += " " + target.getNome() + " è stato sconfitto!";
            }
            return result;
        } else if (s.getTipo() == SpellType.CURA) {
            int cura = s.getValoreBase() + (this.potenzaMagica / 2);
            this.heal(cura);
            return this.nome + " lancia " + s.getNome() + " e si cura di " + cura + " HP!";
        }
        
        return "";
    }

    public String rest() {
        if (!isAlive()) return this.nome + " è morto.";
        this.mana += 5;
        if (this.mana > this.manaMax) {
            this.mana = this.manaMax;
        }
        return this.nome + " riposa e recupera 5 mana.";
    }
}
