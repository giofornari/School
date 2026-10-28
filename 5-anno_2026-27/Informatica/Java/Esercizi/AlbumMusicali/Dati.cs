using System.Data;

namespace AlbumMusicali
{
    public class Dati
    {
        public DataTable AlbumDiCategoria(string categoria)
        {
            DataTable tabella = new DataTable();
            tabella.Columns.Add("ID", typeof(int));
            tabella.Columns.Add("Titolo", typeof(string));
            tabella.Columns.Add("Autore", typeof(string));
            tabella.Columns.Add("Anno", typeof(int));
            tabella.Columns.Add("Categoria", typeof(string));
            tabella.Columns.Add("DurataMinuti", typeof(int));

            foreach (Album album in Album.GetSampleData())
            {
                if (album.Categoria == categoria)
                    tabella.Rows.Add(album.ID, album.Titolo, album.Autore, album.Anno, album.Categoria, album.DurataMinuti);
            }
            return tabella;
        }

        public DataTable BraniAlbum(int idAlbum)
        {
            DataTable tabella = new DataTable();
            tabella.Columns.Add("IDAlbum", typeof(int));
            tabella.Columns.Add("Titolo", typeof(string));

            foreach (Brani brano in Brani.GetSampleData())
            {
                if (brano.IDAlbum == idAlbum)
                    tabella.Rows.Add(brano.IDAlbum, brano.Titolo);
            }
            return tabella;
        }

        public string TitoloAlbumPiuVecchio(DataTable album)
        {
            if (album.Rows.Count == 0)
                return "Nessun album";

            DataRow piuVecchio = album.Rows[0];
            foreach (DataRow riga in album.Rows)
            {
                if ((int)riga["Anno"] < (int)piuVecchio["Anno"])
                    piuVecchio = riga;
            }
            return (string)piuVecchio["Titolo"];
        }

        public double MediaDurata(DataTable album)
        {
            if (album.Rows.Count == 0)
                return 0;

            int totale = 0;
            foreach (DataRow riga in album.Rows)
                totale += (int)riga["DurataMinuti"];
            return (double)totale / album.Rows.Count;
        }
    }
}
