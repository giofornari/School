using System;
using System.Collections.Generic;

namespace ParcoVeicoli
{
    class Flotta
    {
        private List<Veicolo> veicoli = new List<Veicolo>();

        public void AggiungiVeicolo(Veicolo v)
        {
            veicoli.Add(v);
        }

        public void VisualizzaFlotta()
        {
            if (veicoli.Count == 0)
            {
                Console.WriteLine("Nessun veicolo in flotta.");
                return;
            }

            // polimorfismo: chiama la versione giusta
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
