package com.verifica.esericizio1;

public class Batteria extends Strumento {

    private int numeroPezzi;

    public Batteria(String nome, String marca, double valore, int numeroPezzi) {
        super(nome, marca, valore);
        this.numeroPezzi = numeroPezzi;
    }

    @Override
    public double costoNoleggio(int giorni) {
        double costo = getValore() * 0.02;
        costo = costo * giorni;
        if (numeroPezzi % 2 != 0) costo += 5;
        return costo;
    }

    @Override
    public String info() {
        return super.info() + "\ntiopo: Batteria\npieces: " + numeroPezzi;
    }

    public int getNumeroPezzi() { return numeroPezzi; }
    public void setNumeroPezzi(int numeroPezzi) { this.numeroPezzi = numeroPezzi; }
}
