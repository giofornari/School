using System.Collections.Generic;

namespace AlbumMusicali
{
    public class Brani
    {
        public int IDAlbum { get; set; }
        public string Titolo { get; set; }

        public Brani(int idAlbum, string titolo)
        {
            IDAlbum = idAlbum;
            Titolo = titolo;
        }

        public static List<Brani> GetSampleData()
        {
            return new List<Brani>
            {
                new Brani(190290, "Time"),
                new Brani(190290, "Money"),
                new Brani(190291, "Come Together"),
                new Brani(190291, "Here Comes the Sun"),
                new Brani(2903123, "Aria"),
                new Brani(2903123, "Variazione 1"),
                new Brani(2903124, "La primavera"),
                new Brani(2903124, "L'estate"),
                new Brani(2609101, "The Visitors"),
                new Brani(2609101, "One of Us"),
                new Brani(2609102, "Thriller"),
                new Brani(2609102, "Billie Jean"),
                new Brani(93401, "So What"),
                new Brani(93401, "Freddie Freeloader"),
                new Brani(93402, "Acknowledgement"),
                new Brani(93402, "Resolution")
            };
        }
    }
}
