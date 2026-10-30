namespace ParcoVeicoli
{
    public class Camion : Veicolo
    {
        // in tonnellate
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

        // qui NON si usa base: il costo al km cambia (0.15 invece di 0.05) + 50 euro per tonnellata
        public override double CalcolaCostoManutenzione()
        {
            return ChilometriPercorsi * 0.15 + CapacitaCarico * 50;
        }
    }
}
