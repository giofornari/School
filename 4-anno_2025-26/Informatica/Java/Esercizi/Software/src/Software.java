class Programma {
    private String denominazione;
    private String produttore;
    private String versione;
    private String sistemaOperativo;
    private int anno;

    public Programma(String denominazione, String produttore, String versione, String sistemaOperativo, int anno) {
        this.denominazione = denominazione;
        this.produttore = produttore;
        this.versione = versione;
        this.sistemaOperativo = sistemaOperativo;
        this.anno = anno;
    }

    public String getDenominazione() {
        return denominazione;
    }

    public String getProduttore() {
        return produttore;
    }

    public String getVersione() {
        return versione;
    }

    public String getSistemaOperativo() {
        return sistemaOperativo;
    }

    public int getAnno() {
        return anno;
    }

    public void setDenominazione(String denominazione) {
        this.denominazione = denominazione;
    }

    public void setProduttore(String produttore) {
        this.produttore = produttore;
    }

    public void setVersione(String versione) {
        this.versione = versione;
    }

    public void setSistemaOperativo(String sistemaOperativo) {
        this.sistemaOperativo = sistemaOperativo;
    }

    public void setAnno(int anno) {
        this.anno = anno;
    }

    @Override
    public String toString() {
        return "Programma{" +
                "denominazione='" + denominazione + '\'' +
                ", produttore='" + produttore + '\'' +
                ", versione='" + versione + '\'' +
                ", sistemaOperativo='" + sistemaOperativo + '\'' +
                ", anno=" + anno +
                '}';
    }
}

class Contenitore {
    private final Programma[] programmi;
    private final int maxSize;

    public Contenitore(int N) {
        this.maxSize = N;
        this.programmi = new Programma[N];
    }

    public Programma getProgramma(int posizione) {
        if (posizione >= 0 && posizione < maxSize) {
            return programmi[posizione];
        }
        return null;
    }

    public void setProgramma(Programma programma, int posizione) {
        if (posizione >= 0 && posizione < maxSize) {
            programmi[posizione] = programma;
        }
    }

    public void killProgramma(int posizione) {
        if (posizione >= 0 && posizione < maxSize) {
            programmi[posizione] = null;
        }
    }

    public int getN() {
        int count = 0;
        for (Programma p : programmi) {
            if (p != null) {
                count++;
            }
        }
        return count;
    }

    public int cercaProgrammaPerDenominazione(String denominazione) {
        for (int i = 0; i < maxSize; i++) {
            if (programmi[i] != null && programmi[i].getDenominazione().equals(denominazione)) {
                return i;
            }
        }
        return -1;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("Contenitore programmi:\n");
        for (int i = 0; i < maxSize; i++) {
            if (programmi[i] != null) {
                sb.append("- ").append(programmi[i].getDenominazione()).append("\n");
            }
        }
        return sb.toString();
    }

    public int confrontaContenitore(Contenitore altroContenitore) {
        int programmiInComune = 0;
        for (int i = 0; i < maxSize; i++) {
            if (programmi[i] != null) {
                String denominazione = programmi[i].getDenominazione();
                if (altroContenitore.cercaProgrammaPerDenominazione(denominazione) != -1) {
                    programmiInComune++;
                }
            }
        }
        return programmiInComune;
    }
}

public class Software {
    public static void main(String[] args) {
        Contenitore contenitore1 = new Contenitore(5);
        Programma p1 = new Programma("ZeroCool", "HackLab", "v1.0.0", "Linux", 2024);
        Programma p2 = new Programma("AcidBurn", "CyberWorks", "v3.7", "Linux", 2024);
        Programma p3 = new Programma("CrashOverride", "NullSector", "v13.37", "Linux", 2024);

        contenitore1.setProgramma(p1, 0);
        contenitore1.setProgramma(p2, 1);
        contenitore1.setProgramma(p3, 2);
        
        System.out.println("Numero programmi: " + contenitore1.getN());
        System.out.println(contenitore1.toString());
        
        int pos = contenitore1.cercaProgrammaPerDenominazione("CrashOverride");
        System.out.println("Posizione CrashOverride: " + pos);
        
        Contenitore contenitore2 = new Contenitore(3);
        contenitore2.setProgramma(p1, 0);
        contenitore2.setProgramma(p3, 1);
        
        int comuni = contenitore1.confrontaContenitore(contenitore2);
        System.out.println("Programmi in comune: " + comuni);
    }
}
