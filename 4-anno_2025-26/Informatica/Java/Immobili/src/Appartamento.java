import java.util.Objects;

public class Appartamento extends Abitazione {

    private final int piano;
    private final boolean asc;
    private final int numTer;

    public Appartamento(int numStan, double sup, String indir, String citta,
                        int piano, boolean asc, int numTer) {
        super(numStan, sup, indir, citta);
        this.piano = piano;
        if (numTer < 0) {
            throw new IllegalArgumentException("Il numero di terrazzi non può essere negativo");
        }
        this.asc = asc;
        this.numTer = numTer;
    }

    public int getPiano() {
        return piano;
    }

    public boolean hasAsc() {
        return asc;
    }

    public int getNumTer() {
        return numTer;
    }

    @Override
    public String toString() {
        return String.format(
                "Appartamento: %s, piano %d, ascensore %s, %d terrazzi",
                super.toString(), piano, asc ? "presente" : "assente", numTer
        );
    }

    @Override
    public boolean equals(Object obj) {
        if (!super.equals(obj)) {
            return false;
        }
        Appartamento that = (Appartamento) obj;
        return piano == that.piano
                && asc == that.asc
                && numTer == that.numTer;
    }

}
