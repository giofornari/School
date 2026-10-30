namespace LibreriaParcoVeicoli
{
    // abstract: non si può fare "new Veicolo(...)", si istanziano solo Auto e Camion
    public abstract class Veicolo
    {
        // Proprietà automatiche: sostituiscono attributo privato + getter/setter di Java
        public string Targa { get; set; }
        public string Marca { get; set; }
        public string Modello { get; set; }
        public double ChilometriPercorsi { get; set; }

        public Veicolo(string targa, string marca, string modello, double chilometriPercorsi)
        {
            Targa = targa;
            Marca = marca;
            Modello = modello;
            ChilometriPercorsi = chilometriPercorsi;
        }

        // virtual: permette alle sottoclassi di fare override (in Java è implicito, in C# no)
        public virtual string StampaDettagli()
        {
            return $"Targa: {Targa} | Marca: {Marca} | Modello: {Modello} | Km: {ChilometriPercorsi}";
        }

        // costo base: 0.05 euro per km
        public virtual double CalcolaCostoManutenzione()
        {
            return ChilometriPercorsi * 0.05;
        }
    }
}
