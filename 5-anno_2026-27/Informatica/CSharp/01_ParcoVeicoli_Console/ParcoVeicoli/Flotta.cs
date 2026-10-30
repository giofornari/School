namespace ParcoVeicoli
{
    public class Flotta
    {
        // List<T> = ArrayList<T> di Java
        private List<Veicolo> veicoli = new List<Veicolo>();

        public void AggiungiVeicolo(Veicolo v)
        {
            veicoli.Add(v);
        }

        public void VisualizzaFlotta()
        {
            // .Count (proprietà) invece di .size() di Java
            if (veicoli.Count == 0)
            {
                Console.WriteLine("Nessun veicolo in flotta.");
                return;
            }

            // polimorfismo: v è dichiarato Veicolo, ma viene chiamato
            // lo StampaDettagli() di Auto o di Camion a seconda dell'oggetto reale
            foreach (Veicolo v in veicoli)
            {
                Console.WriteLine(v.StampaDettagli());
            }
        }

        public double CalcolaCostoTotaleManutenzione()
        {
            double totale = 0;
            foreach (Veicolo v in veicoli)
            {
                totale += v.CalcolaCostoManutenzione();
            }
            return totale;
        }
    }
}
