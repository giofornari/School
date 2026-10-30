package com.verifica.esericizio1;

public class Tastiera extends Strumento {

    private int numeroTasti;

    public Tastiera(String nome, String marca, double valore, int numeroTasti) {
        super(nome, marca, valore);
        this.numeroTasti = numeroTasti;
    }

    @Override
    public String info() {
        return super.info() + "\ntiopo: Tastiera\ntasti: " + numeroTasti;
    }
    @Override
    public double costoNoleggio(int giorni) {
        double costo = getValore() * 0.015;
        if (numeroTasti < 61) {
            costo *= 0.70;
        }
        costo = costo * giorni;
        return costo;
    }

    public int getNumeroTasti() {
        return numeroTasti;
    }
    public void setNumeroTasti(int numeroTasti) {
        this.numeroTasti = numeroTasti;
    }
}
