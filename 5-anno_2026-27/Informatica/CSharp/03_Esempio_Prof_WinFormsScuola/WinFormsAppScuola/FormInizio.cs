using System.ComponentModel;
using WinFormsLibraryScuola;

namespace WinFormsAppScuola
{
    public partial class FormInizio : Form
    {
        BindingList<Studente> studenti;
        public FormInizio()
        {
            InitializeComponent();
            studenti = Studente.GetStudenti();
        }

        private void buttonCaricaStudenti_Click(object sender, EventArgs e)
        {
            dataGridViewStudenti.DataSource = studenti;
        }

        private void dataGridViewStudenti_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
            Studente studente = ((BindingList<Studente>)dataGridViewStudenti.DataSource)[e.RowIndex];
            if (e.ColumnIndex == 0)
            {
                List<int> voti = studente.Voti;
                var v = voti.Select(vo => new { Voto = vo }).Cast<Object>().ToList();
                FormVoti formVoti = new FormVoti(v, studente);
                formVoti.ShowDialog();
            }
            else
            {
                textBoxMatricola.Text = studente.Matricola.ToString();
                textBoxCognome.Text = studente.Cognome;
                textBoxNome.Text = studente.Nome;
                textBoxDataNascita.Text = studente.DataNascita.ToString();
            }
        }

        private void buttonCancella_Click(object sender, EventArgs e)
        {
            Studente studente = studenti.FirstOrDefault(s => s.Matricola.ToString() == textBoxMatricola.Text);
            if (studente != null)
            {
                studenti.Remove(studente);
            }
        }

        private void buttonInserisciStudente_Click(object sender, EventArgs e)
        {
            Studente s = new Studente(Convert.ToInt32(textBoxMatricola.Text), textBoxNome.Text, textBoxCognome.Text, DateTime.Parse(textBoxDataNascita.Text), new List<int> { 3, 4, 5 });
            studenti.Add(s);
        }

        private void buttonModificaStudente_Click(object sender, EventArgs e)
        {
            /*
            foreach (Studente s in studenti)
                if (s.Matricola.ToString() == textBoxMatricola.Text)
                {
                    s.Cognome = textBoxCognome.Text;
                    s.Nome = textBoxNome.Text;
                    s.DataNascita = DateTime.Parse(textBoxDataNascita.Text);
                }
            */
            Studente studente = studenti.FirstOrDefault(s => s.Matricola.ToString() == textBoxMatricola.Text);
            if (studente != null)
            {
                studente.Cognome = textBoxCognome.Text;
                studente.Nome = textBoxNome.Text;
                studente.DataNascita = DateTime.Parse(textBoxDataNascita.Text);
            }
            dataGridViewStudenti.Refresh();
        }

        private void buttonChiudi_Click(object sender, EventArgs e)
        {
            Close();
        }
    }
}