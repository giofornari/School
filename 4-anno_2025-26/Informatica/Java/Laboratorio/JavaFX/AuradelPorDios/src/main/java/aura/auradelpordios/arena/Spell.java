package aura.auradelpordios.arena;

public class Spell {
    private String nome;
    private int costoMana;
    private int valoreBase;
    private SpellType tipo;

    public Spell(String nome, int costoMana, int valoreBase, SpellType tipo) {
        this.nome = nome;
        this.costoMana = costoMana;
        this.valoreBase = valoreBase;
        this.tipo = tipo;
    }

    public String getNome() {
        return nome;
    }

    public int getCostoMana() {
        return costoMana;
    }

    public int getValoreBase() {
        return valoreBase;
    }

    public SpellType getTipo() {
        return tipo;
    }
}
