namespace LibreriaUtenti
{
    public class Utente
    {
        public int Id { get; set; }
        public string User { get; set; }
        public string Password { get; set; }
        public string Email { get; set; }

        public Utente(int id, string user, string password, string email)
        {
            Id = id;
            User = user;
            Password = password;
            Email = email;
        }

        public static List<Utente> GetSampleData()
        {
            return new List<Utente> {
                new Utente(190290, "mirko.bianchi", "kjn4_2", "mirko.bianchi@itis.pr.it"),
                new Utente(193460, "marco.verdi", "poi9_A", "marco.verdi@itis.pr.it"),
                new Utente(234746, "marco.verdi1", "asAwL_c", "marco.verdi1@itis.pr.it")
            };
        }
    }
}
