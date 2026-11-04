using System.Data;
using LibreriaUtenti;

namespace UtentiWinForms
{
    public partial class WindowFormLogin : Form
    {
        Dati dati;

        public WindowFormLogin(Dati d)
        {
            InitializeComponent();
            dati = d;
        }

        private void buttonAccedi_Click(object sender, EventArgs e)
        {
            DataRow? r = dati.Login(textBoxUser.Text, textBoxPassword.Text);
            if (r == null)
                labelRisultato.Text = "User o password errati.";
            else
                labelRisultato.Text = $"Benvenuto {r["nome"]} {r["cognome"]}\nEmail: {r["email"]}";
        }
    }
}
