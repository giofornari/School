public class Punto {
    private static final double EPSILON = 1e-9;
    private double x;
    private double y;

    public Punto(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public Punto(Punto p) {
        this(p.x, p.y);
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
        if (p == null) {
            return false;
        }
        return Math.abs(this.x - p.x) < EPSILON && Math.abs(this.y - p.y) < EPSILON;
    }

    @Override
    public String toString() {
        return "(" + x + ", " + y + ")";
    }
}
