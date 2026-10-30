import java.util.ArrayList;

public class LibreriaMusicale {
    private final String titolo;
    private final ArrayList<Brano> brani;

    public LibreriaMusicale(String titolo) {
        if (titolo == null || titolo.isBlank()) {
            throw new IllegalArgumentException("title required");
        }
        this.titolo = titolo;
        this.brani = new ArrayList<>();
    }

    public String getTitolo() {
        return titolo;
    }

    public ArrayList<Brano> getBrani() {
        return new ArrayList<>(brani);
    }

    public boolean aggiungiBrano(Brano brano) {
        if (brano == null) {
            throw new IllegalArgumentException("not null song please");
        }
        for (Brano b : brani) {
            if (b.equals(brano)) {
                return false;
            }
        }
        return brani.add(brano);
    }

    public boolean rimuoviBrano(String titolo, String artista) {
        if (titolo == null || titolo.isBlank() || artista == null || artista.isBlank()) {
            throw new IllegalArgumentException("title and artist required");
        }
        boolean del = false;
        for (int i = 0; i < brani.size(); i++) {
            Brano b = brani.get(i);
            if (b.getTitolo().equalsIgnoreCase(titolo)
                    && b.getArtista().equalsIgnoreCase(artista)) {
                brani.remove(i);
                del = true;
                i--;
            }
        }
        return del;
    }

    public int getMinutiAscoltati() {
        long totSec = 0;
        for (Brano b : brani) {
            totSec += b.getSecondiTotaliAscoltati();
        }
        return (int) (totSec / 60);
    }

    public ArrayList<Brano> braniPerGenere(String genere) {
        if (genere == null || genere.isBlank()) {
            throw new IllegalArgumentException("genre required");
        }
        ArrayList<Brano> sel = new ArrayList<>();
        for (Brano b : brani) {
            if (b.getGenere().equalsIgnoreCase(genere)) {
                sel.add(b);
            }
        }
        for (int i = 0; i < sel.size() - 1; i++) {
            int idxMax = i;
            for (int j = i + 1; j < sel.size(); j++) {
                if (sel.get(j).getDataUscita().isAfter(sel.get(idxMax).getDataUscita())) {
                    idxMax = j;
                }
            }
            if (idxMax != i) {
                Brano tmp = sel.get(i);
                sel.set(i, sel.get(idxMax));
                sel.set(idxMax, tmp);
            }
        }
        return sel;
    }

    public int contaBraniPerArtista(String artista) {
        if (artista == null || artista.isBlank()) {
            throw new IllegalArgumentException("artist required");
        }
        int cnt = 0;
        for (Brano b : brani) {
            if (b.getArtista().equalsIgnoreCase(artista)) {
                cnt++;
            }
        }
        return cnt;
    }

    public Brano piuAscoltato() {
        Brano top = null;
        long max = -1;
        for (Brano b : brani) {
            long ascolti = b.getSecondiTotaliAscoltati();
            if (ascolti > max) {
                max = ascolti;
                top = b;
            }
        }
        return top;
    }

    public ArrayList<Brano> shuffleConSeed(String genere, int durataMax) {
        if (durataMax <= 0) {
            throw new IllegalArgumentException("max duration must be positive");
        }
        ArrayList<Brano> pool = new ArrayList<>();
        for (Brano b : brani) {
            if (b.getGenere().equalsIgnoreCase(genere) && b.getDurataSec() <= durataMax) {
                pool.add(b);
            }
        }
        if (pool.isEmpty()) {
            return new ArrayList<>();
        }
        
        long seed = 17;
        for (char c : genere.toLowerCase().toCharArray()) {
            seed = seed * 31 + c;
        }
        seed = seed * 31 + durataMax;
        seed = seed * 31 + pool.size();

        ArrayList<Brano> mix = new ArrayList<>();
        int totDur = 0;
        int idx = (int) (Math.abs(seed) % pool.size());
        
        while (!pool.isEmpty()) {
            Brano b = pool.remove(idx);
            if (totDur + b.getDurataSec() <= durataMax) {
                mix.add(b);
                totDur += b.getDurataSec();
            }
            if (!pool.isEmpty()) {
                idx = (int) (Math.abs(idx + seed) % pool.size());
            }
        }
        return mix;
    }
    public double getDurataMediaBrani() {
        if (brani.isEmpty()) {
            return 0;
        }
        int tot = 0;
        for (Brano b : brani) {
            tot += b.getDurataSec();
        }
        return (double) tot / brani.size();
    }
}