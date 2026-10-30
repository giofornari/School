package com.verifica.esericizio1;

public class Chitarra extends Strumento {

    private int numeroCorde;

    public Chitarra(String nome, String marca, double valore, int numeroCorde) {
        super(nome, marca, valore);
        this.numeroCorde = numeroCorde;
    }

    @Override
    public double costoNoleggio(int giorni) {
        double costo = getValore() * 0.01;
        costo = costo * giorni;
        if (numeroCorde != 6) {
            costo *= 1.20;
        }
        return costo;
    }

    @Override
    public String info() {
        return super.info() + "\ntiopo: Chitarra\ncorde: " + numeroCorde;
    }

    public int getNumeroCorde() {
        return numeroCorde;
    }
    public void setNumeroCorde(int numeroCorde) {
        this.numeroCorde = numeroCorde;
    }
}
