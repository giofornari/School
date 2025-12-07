public class Cd {
    // attributi
    private String titolo;
    private String autore;
    private int numBrani;
    private double durata;

    // costruttore
    public Cd(String titolo, String autore, int numBrani, double durata) {
        this.titolo = titolo;
        this.autore = autore;
        this.numBrani = numBrani;
        this.durata = durata;
    }

    // metodi
    public String toString() {
        return "\nTitolo: " + titolo + "\nAutore: " + autore + "\nNumero brani: " + numBrani + "\nDurata: " + durata + " minuti";
    }
    public int compareDurata(double durata) {
        if (this.durata > durata) {
            return 1;
        } else if (this.durata < durata) {
            return -1;
        } else {
            return 0;
        }
    }

    // getter
    public String getTitolo() {
        return titolo;
    }
    
    public String getAutore() {
        return autore;
    }
    
    public int getNumBrani() {
        return numBrani;
    }
    public double getDurata() {
        return durata;
    }
    
    // setter
    public void setTitolo(String titolo) {
        this.titolo = titolo;
    }
    public void setAutore(String autore) {
        this.autore = autore;
    }
    public void setNumBrani(int numBrani) {
        this.numBrani = numBrani;
    }
    public void setDurata(double durata) {
        this.durata = durata;
    }
    

    // main
    public static void main(String[] args) {
        Cd cd1 = new Cd("LA BELLAVITA", "Artie 5ive", 18, 54.00);
        Cd cd2 = new Cd("Milano Demons", "Shiva", 20, 59.30);
        Cd cd3 = new Cd("La Divina Commedia", "Tedua", 17, 53.50);

        System.out.println("\n------------------------------"+cd1.toString()+"\n------------------------------\n");
        System.out.println("\n------------------------------"+cd2.toString()+"\n------------------------------\n");
        System.out.println("\n------------------------------"+cd3.toString()+"\n------------------------------\n");

        Cd longestCd = cd1;
        if (cd2.compareDurata(longestCd.durata) > 0) {
            longestCd = cd2;
        }
        if (cd3.compareDurata(longestCd.durata) > 0) {
            longestCd = cd3;
        }

        System.out.println("Il CD con la durata maggiore è:");
        System.out.println(longestCd.toString());
        
    }

}