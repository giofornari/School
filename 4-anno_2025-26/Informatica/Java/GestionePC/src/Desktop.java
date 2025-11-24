// Desktop fisso
public class Desktop extends PCFisso {
    private String gpu;
    private String audio;

    public Desktop(String tipoProc, int ramGb, int memGb,
                   String marca, String modello, String sistOp, String tipoCab,
                   String gpu, String audio) {
        super(tipoProc, ramGb, memGb, marca, modello, sistOp, tipoCab);
        this.gpu = gpu;
        this.audio = audio;
    }

    public String getGpu() {
        return gpu;
    }

    public String getAudio() {
        return audio;
    }

    @Override
    public String toString() {
        return "[Desktop] " + super.toString() +
               String.format(", Scheda Video: %s, Scheda Audio: %s", gpu, audio);
    }
}
