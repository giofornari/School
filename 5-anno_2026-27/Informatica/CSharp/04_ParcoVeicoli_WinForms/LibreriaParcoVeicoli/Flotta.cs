using System.ComponentModel;

namespace LibreriaParcoVeicoli
{
    public class Flotta
    {
        // BindingList invece di List: quando aggiungi o togli un elemento
        // avvisa la DataGridView, che si aggiorna da sola
        private BindingList<Veicolo> veicoli = new BindingList<Veicolo>();

        // proprietà di sola lettura (solo get): serve per collegare la lista alla griglia
        public BindingList<Veicolo> Veicoli { get => veicoli; }

        public void AggiungiVeicolo(Veicolo v)
        {
            veicoli.Add(v);
        }

        public void RimuoviVeicolo(Veicolo v)
        {
            veicoli.Remove(v);
        }

        // FirstOrDefault + lambda: il primo veicolo con quella targa, oppure null se non c'è
        // "Veicolo?" = può valere null
        public Veicolo? CercaPerTarga(string targa)
        {
            return veicoli.FirstOrDefault(v => v.Targa == targa);
        }

        // in una libreria grafica non si usa Console: si restituisce la stringa
        // e la form la mostra dove vuole (qui in una MessageBox)
        public string VisualizzaFlotta()
        {
            string risultato = "";
            foreach (Veicolo v in veicoli)
            {
                risultato += v.StampaDettagli() + "\n";
            }
            return risultato;
        }

        // Sum + lambda: somma CalcolaCostoManutenzione() di ogni veicolo
        // (equivale al foreach con totale += ... della versione console)
        public double CalcolaCostoTotaleManutenzione()
        {
            return veicoli.Sum(v => v.CalcolaCostoManutenzione());
        }

        // dati di prova, come Studente.GetStudenti() del prof
        public void CaricaDatiDiProva()
        {
            AggiungiVeicolo(new Auto("AB123CD", "Fiat", "Panda", 10000, 5));
            AggiungiVeicolo(new Camion("XY456ZZ", "Iveco", "Daily", 20000, 10));
            AggiungiVeicolo(new Auto("EF789GH", "Ford", "Mustang", 30000, 3));
        }
    }
}
