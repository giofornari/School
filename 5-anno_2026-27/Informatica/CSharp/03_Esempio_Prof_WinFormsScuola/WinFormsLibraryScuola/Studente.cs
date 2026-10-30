using System.ComponentModel;

namespace WinFormsLibraryScuola
{
    public class Studente
    {
        int matricola;
        string nome;
        string cognome;
        DateTime dataNascita;
        List<int> voti;
        public Studente() { }

        public Studente(int matricola, string nome, string cognome, DateTime dataNascita, List<int> voti)
        {
            Matricola = matricola;
            Nome = nome;
            Cognome = cognome;
            DataNascita = dataNascita;
            Voti = voti;
        }

        public int Matricola { get => matricola; set => matricola = value; }
        public string Nome { get => nome; set => nome = value; }
        public string Cognome { get => cognome; set => cognome = value; }
        public DateTime DataNascita { get => dataNascita; set => dataNascita = value; }
        public List<int> Voti { get => voti; set => voti = value; }

        public static BindingList<Studente> GetStudenti() {
            return new BindingList<Studente> {
                new Studente(12,"pippo","pippo",DateTime.Parse("2008-04-12"), new List<int> { 10, 6, 4}),
                new Studente {Matricola = 11, Cognome = "pluto", Nome = "pluto", DataNascita = DateTime.Parse("2011-01-01"), Voti = new List <int> {10,6,4} },
                new Studente {Matricola = 9, Cognome = "beta", Nome = "eta", DataNascita = DateTime.Parse("2011-01-01"), Voti = new List <int> {10,6,4} }
            };
        }
    }
}
