import java.util.Objects;

public abstract class Abitazione {

    private final int numStan;
    private final double sup;
    private final String indir;
    private final String citta;

    protected Abitazione(int numStan, double sup, String indir, String citta) {
        if (numStan <= 0) {
            throw new IllegalArgumentException("Il numero di stanze deve essere positivo");
        }
        if (sup <= 0) {
            throw new IllegalArgumentException("La superficie deve essere positiva");
        }
        this.numStan = numStan;
        this.sup = sup;
        this.indir = Objects.requireNonNull(indir, "L'indirizzo non può essere nullo");
        this.citta = Objects.requireNonNull(citta, "La città non può essere nulla");
    }

    public int getNumStan() {
        return numStan;
    }

    public double getSup() {
        return sup;
    }

    public String getIndir() {
        return indir;
    }

    public String getCitta() {
        return citta;
    }

    public String descrivi() {
        return toString();
    }

    @Override
    public String toString() {
        return String.format(
                "Abitazione con %d stanze, %.2f mq, indirizzo: %s (%s)",
                numStan, sup, indir, citta
        );
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj == null || getClass() != obj.getClass()) {
            return false;
        }
        Abitazione that = (Abitazione) obj;
        return numStan == that.numStan
                && Double.compare(that.sup, sup) == 0
                && indir.equals(that.indir)
                && citta.equals(that.citta);
    }

    @Override
    public int hashCode() {
        return Objects.hash(numStan, sup, indir, citta);
    }
}
