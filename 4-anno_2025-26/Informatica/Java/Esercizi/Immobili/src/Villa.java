import java.util.Objects;

public class Villa extends Abitazione {

    private final int numPiani;
    private final double supGiard;
    private final boolean pisc;

    public Villa(int numStan, double sup, String indir, String citta,
                 int numPiani, double supGiard, boolean pisc) {
        super(numStan, sup, indir, citta);
        if (numPiani <= 0) {
            throw new IllegalArgumentException("Il numero di piani deve essere positivo");
        }
        if (supGiard < 0) {
            throw new IllegalArgumentException("La superficie del giardino non può essere negativa");
        }
        this.numPiani = numPiani;
        this.supGiard = supGiard;
        this.pisc = pisc;
    }

    public int getNumPiani() {
        return numPiani;
    }

    public double getSupGiard() {
        return supGiard;
    }

    public boolean hasPisc() {
        return pisc;
    }

    @Override
    public String toString() {
        return String.format(
                "Villa: %s, %d piani, giardino %.2f mq, piscina %s",
                super.toString(), numPiani, supGiard,
                pisc ? "presente" : "assente"
        );
    }

    @Override
    public boolean equals(Object obj) {
        if (!super.equals(obj)) {
            return false;
        }
        Villa villa = (Villa) obj;
        return numPiani == villa.numPiani
                && Double.compare(villa.supGiard, supGiard) == 0
                && pisc == villa.pisc;
    }

}
