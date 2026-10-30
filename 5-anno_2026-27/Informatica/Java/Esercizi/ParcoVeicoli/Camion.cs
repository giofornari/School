namespace ParcoVeicoli
{
    class Camion : Veicolo
    {
        public double CapacitaCarico { get; set; }

        public Camion(string targa, string marca, string modello, double chilometriPercorsi, double capacitaCarico)
            : base(targa, marca, modello, chilometriPercorsi)
        {
            CapacitaCarico = capacitaCarico;
        }

        public override string StampaDettagli()
        {
            return "[CAMION] " + base.StampaDettagli() + $" | Carico: {CapacitaCarico} t";
        }

        // 0.15 euro/km + 50 euro/t
        public override double CalcolaCostoManutenzione()
        {
            return ChilometriPercorsi * 0.15 + CapacitaCarico * 50;
        }
    }
}
