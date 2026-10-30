namespace Biblioteca
{
    public class Audiolibro : Risorsa
    {
        public int DurataMinuti { get; set; }

        public Audiolibro(string codice, string titolo, string autore, int giorniPrestito, int durataMinuti)
            : base(codice, titolo, autore, giorniPrestito)
        {
            DurataMinuti = durataMinuti;
        }

        public override string StampaDettagli()
        {
            return "[AUDIOLIBRO] " + base.StampaDettagli() + $" | Durata: {DurataMinuti} min";
        }

        // NON si usa base: 0.50 euro al giorno (invece di 0.20) + 0.01 euro per minuto
        public override double CalcolaPenaleRitardo()
        {
            return GiorniPrestito * 0.50 + DurataMinuti * 0.01;
        }
    }
}
