using System.Data;

namespace LibreriaUtenti
{
    public class Dati
    {
        List<Anagrafica> anagrafiche;
        List<Utente> utenti;
        Random random = new Random();

        public Dati()
        {
            anagrafiche = Anagrafica.GetSampleData();
            utenti = Utente.GetSampleData();
        }

        public DataTable GetAnagrafica()
        {
            DataTable dt = new DataTable("Anagrafica");
            dt.Columns.Add("id", typeof(int));
            dt.Columns.Add("cognome", typeof(string));
            dt.Columns.Add("nome", typeof(string));
            foreach (Anagrafica a in anagrafiche)
                dt.Rows.Add(a.Id, a.Cognome, a.Nome);
            return dt;
        }

        public DataTable GetUtenti()
        {
            DataTable dt = new DataTable("Utenti");
            dt.Columns.Add("id", typeof(int));
            dt.Columns.Add("user", typeof(string));
            dt.Columns.Add("password", typeof(string));
            dt.Columns.Add("email", typeof(string));
            foreach (Utente u in utenti)
                dt.Rows.Add(u.Id, u.User, u.Password, u.Email);
            return dt;
        }

        // unisce anagrafica e utente con lo stesso id
        public DataTable GetUtentiCompleti()
        {
            DataTable dt = new DataTable("UtentiCompleti");
            dt.Columns.Add("id", typeof(int));
            dt.Columns.Add("cognome", typeof(string));
            dt.Columns.Add("nome", typeof(string));
            dt.Columns.Add("user", typeof(string));
            dt.Columns.Add("password", typeof(string));
            dt.Columns.Add("email", typeof(string));
            foreach (Anagrafica a in anagrafiche)
            {
                Utente? u = utenti.FirstOrDefault(x => x.Id == a.Id);
                if (u != null)
                    dt.Rows.Add(a.Id, a.Cognome, a.Nome, u.User, u.Password, u.Email);
            }
            return dt;
        }

        // restituisce la riga dell'utente se user e password sono giusti, altrimenti null
        public DataRow? Login(string user, string password)
        {
            foreach (DataRow r in GetUtentiCompleti().Rows)
                if (r["user"].ToString() == user && r["password"].ToString() == password)
                    return r;
            return null;
        }

        public Utente Inserisci(string cognome, string nome, string password)
        {
            int id;
            do
                id = random.Next(100000, 1000000);
            while (anagrafiche.Any(a => a.Id == id));

            // omonimia: se "marco.verdi" esiste già provo marco.verdi1, marco.verdi2, ...
            string userBase = (nome + "." + cognome).ToLower().Replace(" ", "");
            string user = userBase;
            int n = 1;
            while (utenti.Any(u => u.User == user))
            {
                user = userBase + n;
                n++;
            }

            Utente nuovo = new Utente(id, user, password, user + "@itis.pr.it");
            anagrafiche.Add(new Anagrafica(id, cognome, nome));
            utenti.Add(nuovo);
            return nuovo;
        }
    }
}
