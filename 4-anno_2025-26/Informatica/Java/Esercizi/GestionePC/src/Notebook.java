// Notebook classico
public class Notebook extends PCPortatile {
    private boolean webcam;
    private double resWebcam;

    public Notebook(String tipoProc, int ramGb, int memGb,
                    String marca, String modello, String sistOp,
                    double pesoKg, double altCm, double largCm, double profCm,
                    double diagPol, boolean wifi,
                    boolean webcam, double resWebcam) {
        super(tipoProc, ramGb, memGb, marca, modello, sistOp,
              pesoKg, altCm, largCm, profCm, diagPol, wifi);
        this.webcam = webcam;
        this.resWebcam = webcam ? resWebcam : 0;
    }

    public boolean hasWebcam() {
        return webcam;
    }

    public double getResWebcam() {
        return resWebcam;
    }

    @Override
    public String toString() {
        String info = webcam ?
            String.format("Webcam: Sì (%.1fMP)", resWebcam) : "Webcam: No";
        return "[Notebook] " + super.toString() + ", " + info;
    }
}
