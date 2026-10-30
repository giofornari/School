using System.Collections.Generic;

namespace AlbumMusicali
{
    public class Album
    {
        public int ID { get; set; }
        public string Titolo { get; set; }
        public string Autore { get; set; }
        public int Anno { get; set; }
        public string Categoria { get; set; }
        public int DurataMinuti { get; set; }

        public Album(int id, string titolo, string autore, int anno, string categoria, int durataMinuti)
        {
            ID = id;
            Titolo = titolo;
            Autore = autore;
            Anno = anno;
            Categoria = categoria;
            DurataMinuti = durataMinuti;
        }

        public static List<Album> GetSampleData()
        {
            return new List<Album>
            {
                new Album(190290, "The Dark Side of the Moon", "Pink Floyd", 1973, "rock", 57),
                new Album(190291, "Abbey Road", "The Beatles", 1969, "rock", 47),
                new Album(2903123, "Variazioni Goldberg", "Bach", 1741, "classica", 51),
                new Album(2903124, "Le quattro stagioni", "Vivaldi", 1725, "classica", 42),
                new Album(2609101, "The Visitors", "ABBA", 1981, "pop", 62),
                new Album(2609102, "Thriller", "Michael Jackson", 1982, "pop", 42),
                new Album(93401, "Kind of Blue", "Miles Davis", 1959, "jazz", 48),
                new Album(93402, "A Love Supreme", "John Coltrane", 1965, "jazz", 33)
            };
        }
    }
}
