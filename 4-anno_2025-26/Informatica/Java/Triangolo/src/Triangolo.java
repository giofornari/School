public class Triangolo {
    private Punto p1;
    private Punto p2;
    private Punto p3;

    public Triangolo(Punto p1, Punto p2, Punto p3) {
        points(p1, p2, p3);
    }

    public Triangolo(Triangolo t) {
        this(t.p1, t.p2, t.p3);
    }

    public void setP1(Punto p1) {
        points(p1, this.p2, this.p3);
    }

    public void setP2(Punto p2) {
        points(this.p1, p2, this.p3);
    }

    public void setP3(Punto p3) {
        points(this.p1, this.p2, p3);
    }

    public Punto getP1() {
        return new Punto(this.p1);
    }

    public Punto getP2() {
        return new Punto(this.p2);
    }

    public Punto getP3() {
        return new Punto(this.p3);
    }

    public double perim() {
        double lato1 = len(this.p1, this.p2);
        double lato2 = len(this.p2, this.p3);
        double lato3 = len(this.p3, this.p1);
        return lato1 + lato2 + lato3;
    }

    public double area() {
        double lato1 = len(this.p1, this.p2);
        double lato2 = len(this.p2, this.p3);
        double lato3 = len(this.p3, this.p1);
        double semiP = (lato1 + lato2 + lato3) / 2.0;
        double areaQuad = semiP
                * (semiP - lato1)
                * (semiP - lato2)
                * (semiP - lato3);

        return Math.sqrt(Math.max(areaQuad, 0.0));
    }

    public boolean equals(Triangolo t) {
        if (t == null) {
            return false;
        }
        return this.p1.equals(t.p1)
                && this.p2.equals(t.p2)
                && this.p3.equals(t.p3);
    }

    public boolean equivale(Triangolo t) {
        if (t == null) {
            return false;
        }

        double[] latiMiei = {len(this.p1, this.p2), len(this.p2, this.p3), len(this.p3, this.p1)};
        double[] latiSuoi = {len(t.p1, t.p2), len(t.p2, t.p3), len(t.p3, t.p1)};

        sort(latiMiei);
        sort(latiSuoi);

        for (int i = 0; i < latiMiei.length; i++) {
            if (latiMiei[i] != latiSuoi[i]) {
                return false;
            }
        }
        return true;
    }

    @Override
    public String toString() {
        return "Tri{" +
                "p1=" + this.p1 +
                ", p2=" + this.p2 +
                ", p3=" + this.p3 +
                '}';
    }

    private void points(Punto nuovoP1, Punto nuovoP2, Punto nuovoP3) {

        this.p1 = new Punto(nuovoP1);
        this.p2 = new Punto(nuovoP2);
        this.p3 = new Punto(nuovoP3);
    }

    private boolean stannoInRiga(Punto pt1, Punto pt2, Punto pt3) {
        double areaDoppia = pt1.getX() * (pt2.getY() - pt3.getY())
                + pt2.getX() * (pt3.getY() - pt1.getY())
                + pt3.getX() * (pt1.getY() - pt2.getY());
        return areaDoppia == 0;
    }

    private double len(Punto pt1, Punto pt2) {
        return pt1.distanza(pt2);
    }

    private void sort(double[] lati) {
        for (int i = 0; i < lati.length - 1; i++) {
            for (int j = i + 1; j < lati.length; j++) {
                if (lati[i] > lati[j]) {
                    double tmp = lati[i];
                    lati[i] = lati[j];
                    lati[j] = tmp;
                }
            }
        }
    }

    public static void main(String[] args) {
        Punto p1 = new Punto(0, 0);
        Punto p2 = new Punto(6, 0);
        Punto p3 = new Punto(2, 5);

        Triangolo tri = new Triangolo(p1, p2, p3);
        System.out.println("Tri inizl: " + tri);
        System.out.println("Perimetr: " + tri.perim());
        System.out.println("Are: " + tri.area());

        Triangolo copia = new Triangolo(tri);
        System.out.println("\nCopi: " + copia);
        System.out.println("equals(copi) -> " + tri.equals(copia));

        Triangolo stessiPunti = new Triangolo(
                new Punto(2, 5),
                new Punto(0, 0),
                new Punto(6, 0)
        );
        System.out.println("\nStessi pnti, ordin divers: " + stessiPunti);
        System.out.println("equals(stessiPnti) -> " + tri.equals(stessiPunti));
        System.out.println("equivale(stessiPnti) -> " + tri.equivale(stessiPunti));

        Triangolo triSimile = new Triangolo(
                new Punto(0, 0),
                new Punto(3, 0),
                new Punto(1, 2.5)
        );
        System.out.println("\nLati in rapprt: " + triSimile);
        System.out.println("equivale(triSimile) -> " + tri.equivale(triSimile));
    }
}
