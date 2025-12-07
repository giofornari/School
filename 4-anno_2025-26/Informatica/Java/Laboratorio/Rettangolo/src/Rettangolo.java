public class Rettangolo {
    private double base;
    private double altezza;
    private Punto centro;

    // costruttore
    public Rettangolo(double base, double altezza, Punto centro) {
        this.base = base;
        this.altezza = altezza;
        this.centro = centro;
    }

    // getter e setter
    public double getBase() { return base; }
    public void setBase(double base) { this.base = base; }

    public double getAltezza() { return altezza; }
    public void setAltezza(double altezza) { this.altezza = altezza; }
    
    public Punto getCentro() { return centro; }
    public void setCentro(Punto centro) { this.centro = centro; }

    public Punto[] calcolaVertici() {
        Punto[] vertici = new Punto[4];
        double b2 = base / 2;
        double h2 = altezza / 2;
        
        vertici[0] = new Punto(centro.getX() - b2, centro.getY() + h2); // A
        vertici[1] = new Punto(centro.getX() + b2, centro.getY() + h2); // B
        vertici[2] = new Punto(centro.getX() + b2, centro.getY() - h2); // C
        vertici[3] = new Punto(centro.getX() - b2, centro.getY() - h2); // D
        
        return vertici;
    }

    public boolean isInside(Punto a) {
        double xa = a.getX();
        double ya = a.getY();
        
        double minX = centro.getX() - base / 2;
        double maxX = centro.getX() + base / 2;
        double minY = centro.getY() - altezza / 2;
        double maxY = centro.getY() + altezza / 2;
        
        return (xa > minX && xa < maxX && ya > minY && ya < maxY);
    }
    public Punto minAss() {
        Punto[] vertici = calcolaVertici();
        Punto minPunto = vertici[0];
        double min = Math.sqrt(vertici[0].getX() * vertici[0].getX() + vertici[0].getY() * vertici[0].getY());
        
        for (int i = 1; i < vertici.length; i++) {
            double dist = Math.sqrt(Math.pow(vertici[i].getX(),2) + Math.pow(vertici[i].getY(), 2));
            if (dist < min) {
                min = dist;
                minPunto = vertici[i];
            }
        }
        
        return minPunto;
    }
    public static void main(String[] args) {
        Punto centro = new Punto(5, 14);
        Rettangolo r = new Rettangolo(7, 11, centro);
        
        Punto[] vertici = r.calcolaVertici();
        System.out.println("Vertici:");
        for (int i = 0; i < vertici.length; i++) {
            System.out.println((char)('A' + i) + ": " + vertici[i]);
        }
        
        Punto test = new Punto(6, 9);
        System.out.println("\nPunto (3,4) contenuto: " + r.isInside(test));
        
        Punto vicino = r.minAss();
        System.out.println("\nVertice più vicino all'origine: " + vicino);
    }
}
