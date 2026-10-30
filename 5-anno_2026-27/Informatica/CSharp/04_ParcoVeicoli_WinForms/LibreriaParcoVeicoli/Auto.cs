namespace LibreriaParcoVeicoli
{
    // ":" = extends di Java
    public class Auto : Veicolo
    {
        public int NumeroPorte { get; set; }

        // ": base(...)" = super(...) di Java, chiama il costruttore di Veicolo
        public Auto(string targa, string marca, string modello, double chilometriPercorsi, int numeroPorte)
            : base(targa, marca, modello, chilometriPercorsi)
        {
            NumeroPorte = numeroPorte;
        }

        // override obbligatorio in C# (in Java @Override è facoltativo)
        public override string StampaDettagli()
        {
            return "[AUTO] " + base.StampaDettagli() + $" | Porte: {NumeroPorte}";
        }

        // costo base (km * 0.05) + 100 euro di revisione
        public override double CalcolaCostoManutenzione()
        {
            return base.CalcolaCostoManutenzione() + 100;
        }
    }
}
