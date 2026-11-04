using LibreriaUtenti;

namespace UtentiWinForms
{
    public partial class WindowsFormUtenti : Form
    {
        Dati dati;

        public WindowsFormUtenti()
        {
            InitializeComponent();
            dati = new Dati();
            dataGridViewUtenti.DataSource = dati.GetUtentiCompleti();
        }

        private void buttonLogin_Click(object sender, EventArgs e)
        {
            WindowFormLogin formLogin = new WindowFormLogin(dati);
            formLogin.ShowDialog();
        }

        private void buttonInserisci_Click(object sender, EventArgs e)
        {
            if (textBoxCognome.Text == "" || textBoxNome.Text == "" || textBoxPassword.Text == "")
            {
                MessageBox.Show("Compila tutti i campi.");
                return;
            }

            Utente u = dati.Inserisci(textBoxCognome.Text, textBoxNome.Text, textBoxPassword.Text);
            // DataTable è una copia: la ricreo per vedere il nuovo utente
            dataGridViewUtenti.DataSource = dati.GetUtentiCompleti();
            MessageBox.Show($"Creato utente {u.User} (id {u.Id})");
        }

        private void buttonChiudi_Click(object sender, EventArgs e)
        {
            Close();
        }
    }
}
