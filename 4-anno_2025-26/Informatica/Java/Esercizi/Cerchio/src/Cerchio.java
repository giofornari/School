public class Cerchio {
    private double raggio;

    public Cerchio() {
        this.raggio = 10;
    }
    public Cerchio(double r) {
        this.raggio = r;
    }
    public double getraggio() {
        return raggio;
    }
    public void setraggio(double r) {
        this.raggio = r;
    }
    public double area() {
        return Math.PI * raggio * raggio;
    }
    public double circonferenza() {
        return 2 * Math.PI * raggio;
    }

    public static void main(String[] args) {
        Cerchio CIrl1 = new Cerchio();
        System.out.println(CIrl1.getraggio());
        System.out.println(CIrl1.area());
        System.out.println(CIrl1.circonferenza());
        System.out.println();

        Cerchio CIrl2 = new Cerchio(5);
        System.out.println(CIrl2.getraggio());
        System.out.println(CIrl2.area());
        System.out.println(CIrl2.circonferenza());
        System.out.println();

        Cerchio CIrl3 = new Cerchio(7.5);
        System.out.println(CIrl3.getraggio());
        System.out.println(CIrl3.area());
        System.out.println(CIrl3.circonferenza());
    }
}