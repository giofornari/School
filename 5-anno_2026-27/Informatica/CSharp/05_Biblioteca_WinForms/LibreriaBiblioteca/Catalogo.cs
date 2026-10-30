using System.ComponentModel;

namespace LibreriaBiblioteca
{
    public class Catalogo
    {
        // BindingList: la DataGridView si aggiorna da sola su Add/Remove
        private BindingList<Risorsa> risorse = new BindingList<Risorsa>();

        public BindingList<Risorsa> Risorse { get => risorse; }

        public void AggiungiRisorsa(Risorsa r)
        {
            risorse.Add(r);
        }

        public void RimuoviRisorsa(Risorsa r)
        {
            risorse.Remove(r);
        }

        // primo elemento con quel codice, oppure null
        public Risorsa? CercaPerCodice(string codice)
        {
            return risorse.FirstOrDefault(r => r.Codice == codice);
        }

        public string VisualizzaCatalogo()
        {
            string risultato = "";
            foreach (Risorsa r in risorse)
            {
                risultato += r.StampaDettagli() + "\n";
            }
            return risultato;
        }

        public double CalcolaPenaleTotale()
        {
            return risorse.Sum(r => r.CalcolaPenaleRitardo());
        }

        public void CaricaDatiDiProva()
        {
            AggiungiRisorsa(new Libro("L01", "Il nome della rosa", "Umberto Eco", 10, 500));
            AggiungiRisorsa(new Audiolibro("A01", "Sapiens", "Yuval Harari", 10, 300));
            AggiungiRisorsa(new Libro("L02", "Il barone rampante", "Italo Calvino", 3, 280));
        }
    }
}
