namespace Biblioteca
{
    public class Catalogo
    {
        private List<Risorsa> risorse = new List<Risorsa>();

        public void AggiungiRisorsa(Risorsa r)
        {
            risorse.Add(r);
        }

        public void VisualizzaCatalogo()
        {
            if (risorse.Count == 0)
            {
                Console.WriteLine("Catalogo vuoto.");
                return;
            }

            // polimorfismo: parte lo StampaDettagli() di Libro o di Audiolibro
            foreach (Risorsa r in risorse)
            {
                Console.WriteLine(r.StampaDettagli());
            }
        }

        public double CalcolaPenaleTotale()
        {
            double totale = 0;
            foreach (Risorsa r in risorse)
            {
                totale += r.CalcolaPenaleRitardo();
            }
            return totale;
        }
    }
}
