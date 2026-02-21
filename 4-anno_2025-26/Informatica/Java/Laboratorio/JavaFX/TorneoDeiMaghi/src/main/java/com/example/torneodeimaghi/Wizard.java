package com.example.torneodeimaghi;

import java.util.List;

public class Wizard {
    private String name;
    private String alias;
    private int hp;
    private int hpMax;
    private int mana;
    private int manaMax;
    private int magicPower;
    private int defense;
    private int speed;
    private List<Spell> spellBook;

    public Wizard(String name, String alias, int hp, int mana, int magicPower, int defense, int speed, List<Spell> spellBook) {
        this.name = name;
        this.alias = alias;
        this.hp = hp;
        this.hpMax = hp;
        this.mana = mana;
        this.manaMax = mana;
        this.magicPower = magicPower;
        this.defense = defense;
        this.speed = speed;
        this.spellBook = spellBook;
    }

    public String getName() {
        return name;
    }

    public String getAlias() {
        return alias;
    }

    public int getHp() {
        return hp;
    }

    public int getHpMax() {
        return hpMax;
    }

    public int getMana() {
        return mana;
    }

    public int getManaMax() {
        return manaMax;
    }

    public int getMagicPower() {
        return magicPower;
    }

    public int getDefense() {
        return defense;
    }

    public int getSpeed() {
        return speed;
    }

    public List<Spell> getSpellBook() {
        return spellBook;
    }

    public boolean isAlive() {
        return this.hp > 0;
    }

    public void takeDamage(int damage) {
        this.hp -= damage;
        if (this.hp < 0) {
            this.hp = 0;
        }
    }

    public void heal(int amount) {
        this.hp += amount;
        if (this.hp > this.hpMax) {
            this.hp = this.hpMax;
        }
    }

    public boolean canCast(Spell s) {
        return this.mana >= s.getManaCost();
    }

    public void cast(Spell s, Wizard target) {
        if (isAlive() && canCast(s)) {
            this.mana -= s.getManaCost();
            if ("ATTACK".equals(s.getType())) {
                int damage = s.getBaseValue() + this.magicPower - target.getDefense();
                if (damage < 1) {
                    damage = 1;
                }
                target.takeDamage(damage);
                System.out.println(this.name + " attacks " + target.getName() + " with " + s.getName() + " for " + damage + " damage!");
            } else if ("HEAL".equals(s.getType())) {
                this.heal(s.getBaseValue());
                System.out.println(this.name + " heals for " + s.getBaseValue() + " HP.");
            }
        }
    }

    public void rest() {
        this.mana += 5;
        if (this.mana > this.manaMax) {
            this.mana = this.manaMax;
        }
        System.out.println(this.name + " rests and recovers 5 mana.");
    }

    @Override
    public String toString() {
        return name + " (" + alias + ") - HP: " + hp + "/" + hpMax + ", Mana: " + mana + "/" + manaMax;
    }
}
