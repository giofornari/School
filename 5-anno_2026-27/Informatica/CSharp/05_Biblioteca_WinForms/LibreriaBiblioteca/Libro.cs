namespace LibreriaBiblioteca
{
    public class Libro : Risorsa
    {
        public int NumeroPagine { get; set; }

        public Libro(string codice, string titolo, string autore, int giorniPrestito, int numeroPagine)
            : base(codice, titolo, autore, giorniPrestito)
        {
            NumeroPagine = numeroPagine;
        }

        public override string StampaDettagli()
        {
            return "[LIBRO] " + base.StampaDettagli() + $" | Pagine: {NumeroPagine}";
        }

        // penale base (giorni * 0.20) + 5 euro di tassa fissa
        public override double CalcolaPenaleRitardo()
        {
            return base.CalcolaPenaleRitardo() + 5.00;
        }
    }
}
