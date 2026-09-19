package com.verifica.esericizio1;

/**
 * costo noleggio è dichiarato astratto perchè dipende strettamente dal tipo di strumento che si vuole noleggiare.
 * ogni sottoclasse deve quindi definire la logica di costo noleggio, propria per ogni tipo di strumento.
 * per info() non deve essere cosi perchè le informazioni su uno strumento generale possono e dovrebbero esistere. inoltre, in questo modo per ogni strumento possiamo ereditare i campi standard da fornire allo strumento e limitarci all'aggiunta dei attrb specifici per il tipo di strumento definito nella sottoclasse.
 */

public class Violino extends Strumento {

    private int eta;

    public Violino(String nome, String marca, double valore, int eta) {
        super(nome, marca, valore);
        this.eta = eta;
    }

    @Override
    public double costoNoleggio(int giorni) {
        double costo = getValore() * 0.018;
        costo = costo * giorni;
        if (eta > 84) costo *= 1.50;
        return costo;
    }

    @Override
    public String info() {
        return super.info() + "\ntipo: Violino\netà: " + eta + " yirs";
    }

    public int getEta() {
        return eta;
    }
    public void setEta(int eta) {
        this.eta = eta;
    }
}
