public class Punto {
    private double x;
    private double y;

    public Punto(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public Punto(Punto p) {
        this.x = p.x;
        this.y = p.y;
    }

    public void setX(double x) {
        this.x = x;
    }

    public void setY(double y) {
        this.y = y;
    }

    public double getX() {
        return x;
    }

    public double getY() {
        return y;
    }

    public double distanza(Punto p) {
        double dx = this.x - p.x;
        double dy = this.y - p.y;
        return Math.sqrt(dx * dx + dy * dy);
    }

    public boolean equals(Punto p) {
        return this.x == p.x && this.y == p.y;
    }

    @Override
    public String toString() {
        return "(" + x + ", " + y + ")";
    }
    public static void main(String[] args) {
        Punto p1 = new Punto(3.0, 4.0);
        Punto p2 = new Punto(0.0, 0.0);
        Punto p3 = new Punto(p1);
    
        System.out.println("p1: " + p1);
        System.out.println("p2: " + p2);
        System.out.println("p3: " + p3);
    
        System.out.println("space tra p1 e p2: " + p1.distanza(p2));
        
        System.out.println("p1 == p2: " + p1.equals(p2));
        System.out.println("p1 == p3: " + p1.equals(p3));
    
        p2.setX(3.0);
        p2.setY(4.0);
        System.out.println("p2: " + p2);
        System.out.println("p1 == p2: " + p1.equals(p2));
    }
}