namespace ParcoVeicoli
{
    class Auto : Veicolo
    {
        public int NumeroPorte { get; set; }

        public Auto(string targa, string marca, string modello, double chilometriPercorsi, int numeroPorte)
            : base(targa, marca, modello, chilometriPercorsi)
        {
            NumeroPorte = numeroPorte;
        }

        public override string StampaDettagli()
        {
            return "[AUTO] " + base.StampaDettagli() + $" | Porte: {NumeroPorte}";
        }

        // costo base + 100 revisione
        public override double CalcolaCostoManutenzione()
        {
            return base.CalcolaCostoManutenzione() + 100;
        }
    }
}
