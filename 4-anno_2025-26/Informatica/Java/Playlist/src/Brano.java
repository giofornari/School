import java.time.LocalDate;
import java.util.Objects;

public class Brano {
    private final String titolo;
    private final String artista;
    private final String genere;
    private final int durataSec;
    private final LocalDate dataUscita;
    private int ascolti;

    public Brano(String titolo, String artista, String genere, int durataSec, LocalDate dataUscita) {
        if (titolo == null || titolo.isBlank()) {
            throw new IllegalArgumentException("titolo != null ");
        }
        if (artista == null || artista.isBlank()) {
            throw new IllegalArgumentException("artista != null ");
        }
        if (genere == null || genere.isBlank()) {
            throw new IllegalArgumentException("genere != null");
        }
        if (durataSec <= 0) {
            throw new IllegalArgumentException("durata > 0");
        }
        if (dataUscita == null) {
            throw new IllegalArgumentException("data di uscita != null");
        }
        this.titolo = titolo;
        this.artista = artista;
        this.genere = genere;
        this.durataSec = durataSec;
        this.dataUscita = dataUscita;
        this.ascolti = 0;
    }

    public Brano(String titolo, String artista, String genere, int durataSec, LocalDate dataUscita, int ascolti) {
        this(titolo, artista, genere, durataSec, dataUscita);
        if (ascolti < 0) {
            throw new IllegalArgumentException("Gli ascolti non possono essere negativi");
        }
        this.ascolti = ascolti;
    }

    public String getTitolo() {
        return titolo;
    }

    public String getArtista() {
        return artista;
    }

    public String getGenere() {
        return genere;
    }

    public int getDurataSec() {
        return durataSec;
    }

    public LocalDate getDataUscita() {
        return dataUscita;
    }

    public int getAscolti() {
        return ascolti;
    }

    public void incrementaAscolti() {
        ascolti++;
    }

    public long getSecondiTotaliAscoltati() {
        return (long) ascolti * durataSec;
    }

    @Override
    public String toString() {
        int minuti = durataSec / 60;
        int secondi = durataSec % 60;
        return String.format("%s - %s (%s, %d:%02d) [%d ascolti]", 
                           titolo, artista, genere, minuti, secondi, ascolti);
    }

}
