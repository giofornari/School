package com.example.torneodeimaghi;

import java.util.List;

public class Wizard {
    private String nome;
    private String spritePath;
    private int hp;
    private int hpMax;
    private int mana;
    private int manaMax;
    private int power;
    private int def;
    private int spd;
    private List<Spell> bruhlist;

    public Wizard(String nome, String spritePath, int hp, int mana, int power, int def, int spd, List<Spell> bruhlist) {
        this.nome = nome;
        this.spritePath = spritePath;
        this.hpMax = hp;
        this.hp = hp;
        this.manaMax = mana;
        this.mana = mana;
        this.power = power;
        this.def = def;
        this.spd = spd;
        this.bruhlist = bruhlist;
    }

    public String getNome() { return nome; }
    public String getSpritePath() { return spritePath; }
    public int getHp() { return hp; }
    public int getHpMax() { return hpMax; }
    public int getMana() { return mana; }
    public int getManaMax() { return manaMax; }
    public int getPower() { return power; }
    public int getDef() { return def; }
    public int getSpd() { return spd; }
    public List<Spell> getBruhlist() { return bruhlist; }

    public boolean isAlive() {
        return hp > 0;
    }

    public void riceviDanno(int danno) {
        hp -= danno;
        if (hp < 0) hp = 0;
    }

    public void leef(int q) {
        hp += q;
        if (hp > hpMax) hp = hpMax;
    }

    public boolean haManaPer(Spell s) {
        return mana >= s.getManaCost();
    }

    public String lanciaBruh(Spell s, Wizard tohit) {
        if (!isAlive()) return "";
        
        if (haManaPer(s)) {
            mana -= s.getManaCost();
            if (s.getType().equals("ATTACK")) {
                int danno = s.getBaseValue() + power - tohit.getDef();
                if (danno < 1) danno = 1;
                tohit.riceviDanno(danno);
                return nome + " colpisce " + tohit.getNome() + " con " + s.getName() + " (" + danno + " danni)!";
            } else if (s.getType().equals("HEAL")) {
                leef(s.getBaseValue());
                return nome + " si cura di " + s.getBaseValue() + " HP con " + s.getName() + ".";
            }
        }
        return nome + " prova a usare " + s.getName() + " ma fallisce.";
    }

    public String sleep() {
        mana += 5;
        if (mana > manaMax) mana = manaMax;
        return nome + " si riposa e recupera 5 mana.";
    }
}
