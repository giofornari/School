import java.util.Objects;

// Vagone base astratto
public abstract class Vagone {
    protected final String id;
    protected final double tara;
    protected final String manufactor;
    protected final int created;

    protected Vagone(String id, double tara, String manufactor, int created) {
        Objects.requireNonNull(id, "id != null");
        Objects.requireNonNull(manufactor, "azienda != null");
        
        if (id.trim().isEmpty()) {
            throw new IllegalArgumentException("id non vuoto");
        }
        if (tara <= 0) {
            throw new IllegalArgumentException("peso vuoto > 0");
        }
        if (created < 1800 || created > 2100) {
            throw new IllegalArgumentException("anno tra 1800 e 2100");
        }
        
        this.id = id;
        this.tara = tara;
        this.manufactor = manufactor;
        this.created = created;
    }

    public abstract double totPeso();

    public String getid() {
        return id;
    }

    public double gettara() {
        return tara;
    }

    public String getmanufactor() {
        return manufactor;
    }

    public int getcreated() {
        return created;
    }

    @Override
    public String toString() {
        return String.format("id: %s, Peso a vuoto: %.2f kg, Costruttore: %s, Anno: %d",
                id, tara, manufactor, created);
    }
}
