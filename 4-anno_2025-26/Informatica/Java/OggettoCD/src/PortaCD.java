
public class PortaCD {
    private final Cd[] slots;
    private int count;

    public PortaCD(int capacity) {
        this.slots = new Cd[capacity];
        this.count = 0;
    }

    public Cd getCD(int position) {
        validateIndex(position);
        return slots[position];
    }

    public void setCD(int position, Cd cd) {
        validateIndex(position);
        if (slots[position] == null) {
            count++;
        }
        slots[position] = cd;
    }

    public void killCD(int position) {
        if (slots[position] != null) {
            slots[position] = null;
            count--;
        }
    }

    public int getN() {
        return count;
    }

    public int cercaCDperTitolo(String titolo) {
        if (titolo == null) {
            return -1;
        }
        for (int i = 0; i < slots.length; i++) {
            Cd cd = slots[i];
            if (cd != null && Objects.equals(titolo, cd.getTitolo())) {
                return i;
            }
        }
        return -1;
    }

    public int confrontaCollezione(PortaCD altra) {
        if (altra == null) {
            return 0;
        }
        int matches = 0;
        boolean[] alreadyMatched = new boolean[altra.slots.length];
        for (Cd cd : slots) {
            if (cd == null) {
                continue;
            }
            for (int j = 0; j < altra.slots.length; j++) {
                if (alreadyMatched[j]) {
                    continue;
                }
                Cd other = altra.slots[j];
                if (other != null && equalsCd(cd, other)) {
                    alreadyMatched[j] = true;
                    matches++;
                    break;
                }
            }
        }
        return matches;
    }

    public String toString() {
        StringBuilder builder = new StringBuilder();
        for (Cd cd : slots) {
            if (cd == null) {
                continue;
            }
            if (builder.length() > 0) {
                builder.append(System.lineSeparator());
            }
            builder.append(cd.getTitolo());
        }
        return builder.length() == 0 ? "(nessun CD)" : builder.toString();
    }


    private boolean equalsCd(Cd first, Cd second) {
        return Objects.equals(first.getTitolo(), second.getTitolo())
            && Objects.equals(first.getAutore(), second.getAutore())
            && first.getNumBrani() == second.getNumBrani()
            && Double.compare(first.getDurata(), second.getDurata()) == 0;
    }
}
