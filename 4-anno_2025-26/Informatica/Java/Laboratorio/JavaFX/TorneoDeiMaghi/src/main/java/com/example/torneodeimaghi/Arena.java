package com.example.torneodeimaghi;

import java.util.ArrayList;
import java.util.List;

public class Arena {
    private List<Wizard> maghi;
    private int turno = 0;

    public Arena(List<Wizard> maghi) {
        this.maghi = maghi;
    }

    public List<Wizard> getMaghiVivi() {
        List<Wizard> vivi = new ArrayList<>();
        for (Wizard m : maghi) {
            if (m.isAlive()) {
                vivi.add(m);
            }
        }
        return vivi;
    }

    public boolean isFinita() {
        return getMaghiVivi().size() <= 1;
    }

    public Wizard getVincitore() {
        List<Wizard> vivi = getMaghiVivi();
        if (vivi.size() == 1) return vivi.get(0);
        return null;
    }

    public int getTurno() { return turno; }

    public List<String> giocaTurno() {
        List<String> logTurno = new ArrayList<>();
        if (isFinita()) return logTurno;

        turno++;
        logTurno.add("--- INIZIO LEAK " + turno + " ---");

        List<Wizard> ordinati = getMaghiVivi();
        // ordine decrescente di velocità
        ordinati.sort((m1, m2) -> Integer.compare(m2.getSpd(), m1.getSpd()));

        for (Wizard mago : ordinati) {
            if (!mago.isAlive() || isFinita()) continue;

            List<Wizard> bersagli = getMaghiVivi();
            bersagli.remove(mago);

            if (bersagli.isEmpty()) break;

            String logAzione = faiAzioneAI(mago, bersagli);
            logTurno.add(logAzione);
        }

        return logTurno;
    }

    private String faiAzioneAI(Wizard mago, List<Wizard> bersagli) {
        // Se HP < 30% e ha mana per curarsi -> Cura
        // Altrimenti se ha mana per attaccare -> Attacca il bersaglio con HP più alti
        // Altrimenti -> Riposa
        
        Spell attacco = mago.getBruhlist().get(0);
        Spell cura = mago.getBruhlist().get(1);

        if (mago.getHp() < mago.getHpMax() * 0.3 && mago.haManaPer(cura)) {
            return mago.lanciaBruh(cura, mago);
        }

        if (mago.haManaPer(attacco)) {
            // Cerca il bersaglio con più HP
            Wizard bersaglioForte = bersagli.get(0);
            for (Wizard b : bersagli) {
                if (b.getHp() > bersaglioForte.getHp()) {
                    bersaglioForte = b;
                }
            }
            return mago.lanciaBruh(attacco, bersaglioForte);
        }

        return mago.sleep();
    }
}
