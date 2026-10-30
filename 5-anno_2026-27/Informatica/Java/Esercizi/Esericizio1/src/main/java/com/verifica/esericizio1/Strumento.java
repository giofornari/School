package com.verifica.esericizio1;

public abstract class Strumento {

    private String nome;
    private String marca;
    private double valore;

    public Strumento(String nome, String marca, double valore) {
        this.nome = nome;
        this.marca = marca;
        this.valore = valore;
    }

    public abstract double costoNoleggio(int giorni);

    public String info() {
        return "nome: " + nome + "\nmarca: " + marca + "\nvalore: " + valore + " €";
    }

    public String getNome() {
        return nome;
    }
    public String getMarca() {
        return marca;
    }
    public double getValore() {
        return valore;
    }
    public void setNome(String nome) {
        this.nome = nome;
    }
    public void setMarca(String marca) {
        this.marca = marca;
    }
    public void setValore(double valore) {
        this.valore = valore;
    }
}
