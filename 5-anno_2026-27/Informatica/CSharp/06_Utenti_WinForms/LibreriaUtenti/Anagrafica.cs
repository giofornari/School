namespace LibreriaUtenti
{
    public class Anagrafica
    {
        public int Id { get; set; }
        public string Cognome { get; set; }
        public string Nome { get; set; }

        public Anagrafica(int id, string cognome, string nome)
        {
            Id = id;
            Cognome = cognome;
            Nome = nome;
        }

        public static List<Anagrafica> GetSampleData()
        {
            return new List<Anagrafica> {
                new Anagrafica(190290, "Bianchi", "Mirko"),
                new Anagrafica(193460, "Verdi", "Marco"),
                new Anagrafica(234746, "Verdi", "Marco")
            };
        }
    }
}
