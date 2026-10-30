namespace Biblioteca
{
    public abstract class Risorsa
    {
        public string Codice { get; set; }
        public string Titolo { get; set; }
        public string Autore { get; set; }
        // da quanti giorni la risorsa è in prestito
        public int GiorniPrestito { get; set; }

        public Risorsa(string codice, string titolo, string autore, int giorniPrestito)
        {
            Codice = codice;
            Titolo = titolo;
            Autore = autore;
            GiorniPrestito = giorniPrestito;
        }

        public virtual string StampaDettagli()
        {
            return $"Codice: {Codice} | Titolo: {Titolo} | Autore: {Autore} | Giorni prestito: {GiorniPrestito}";
        }

        // penale base: 0.20 euro per ogni giorno di prestito
        public virtual double CalcolaPenaleRitardo()
        {
            return GiorniPrestito * 0.20;
        }
    }
}
