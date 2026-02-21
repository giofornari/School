package com.example.torneodeimaghi;

public class Spell {
    private String name;
    private int manaCost;
    private int baseValue;
    private String type; // "ATTACK" or "HEAL"

    public Spell(String name, int manaCost, int baseValue, String type) {
        this.name = name;
        this.manaCost = manaCost;
        this.baseValue = baseValue;
        this.type = type;
    }

    public String getName() {
        return name;
    }

    public int getManaCost() {
        return manaCost;
    }

    public int getBaseValue() {
        return baseValue;
    }

    public String getType() {
        return type;
    }
}
