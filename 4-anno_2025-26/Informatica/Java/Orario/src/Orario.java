public class Orario {
    private int ore;
    private int minuti;
    private int secondi;

    public Orario(int ore, int minuti, int secondi) {
        if (ore < 0 || ore >= 24 || minuti < 0 || minuti >= 60 || secondi < 0 || secondi >= 60) {
            this.ore = 0;
            this.minuti = 0;
            this.secondi = 0;
        } else {
            this.ore = ore;
            this.minuti = minuti;
            this.secondi = secondi;
        }
    }

    public Orario() {
        this.ore = 0;
        this.minuti = 0;
        this.secondi = 0;
    }
   
    public int getOre() { return ore; }
   
    public int getMinuti() { return minuti; }
   
    public int getSecondi() { return secondi; }
    
    public void tic() {
        this.secondi++;
        if (this.secondi >= 60) {
            this.secondi = 0;
            this.minuti++;
            if (this.minuti >= 60) {
                this.minuti = 0;
                this.ore++;
                if (this.ore >= 24) {
                    this.ore = 0;
                }
            }
        }
    }
    
    public void aggiungiMinuti(int m) {
        this.minuti += m;
        while (this.minuti >= 60) {
            this.minuti -= 60;
            this.ore++;
            if (this.ore >= 24) {
                this.ore -= 24;
            }
        }
    }

    public String mostra() {
        return ore + ":" + minuti + ":" + secondi;
    }
    
    public boolean ugualeA(Orario altro) {
        return this.ore == altro.ore && this.minuti == altro.minuti && this.secondi == altro.secondi;
    }
}
