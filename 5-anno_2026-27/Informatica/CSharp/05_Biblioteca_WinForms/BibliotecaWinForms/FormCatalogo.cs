using LibreriaBiblioteca;

namespace BibliotecaWinForms
{
    public partial class FormCatalogo : Form
    {
        Catalogo catalogo;

        public FormCatalogo()
        {
            InitializeComponent();
            catalogo = new Catalogo();
            catalogo.CaricaDatiDiProva();
        }

        // LETTURA
        private void buttonCarica_Click(object sender, EventArgs e)
        {
            dataGridViewRisorse.DataSource = catalogo.Risorse;
        }

        private void radioButtonLibro_CheckedChanged(object sender, EventArgs e)
        {
            labelExtra.Text = radioButtonLibro.Checked ? "Numero pagine" : "Durata (minuti)";
        }

        private void dataGridViewRisorse_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            if (e.RowIndex < 0) return;

            Risorsa r = catalogo.Risorse[e.RowIndex];
            textBoxCodice.Text = r.Codice;
            textBoxTitolo.Text = r.Titolo;
            textBoxAutore.Text = r.Autore;
            textBoxGiorni.Text = r.GiorniPrestito.ToString();

            if (r is Libro l)
            {
                radioButtonLibro.Checked = true;
                textBoxExtra.Text = l.NumeroPagine.ToString();
            }
            else if (r is Audiolibro a)
            {
                radioButtonAudiolibro.Checked = true;
                textBoxExtra.Text = a.DurataMinuti.ToString();
            }

            labelDettagli.Text = r.StampaDettagli() + $"\nPenale: {r.CalcolaPenaleRitardo():F2} €";
        }

        // INSERIMENTO
        private void buttonInserisci_Click(object sender, EventArgs e)
        {
            if (catalogo.CercaPerCodice(textBoxCodice.Text) != null)
            {
                MessageBox.Show("Codice già presente.");
                return;
            }

            int giorni = Convert.ToInt32(textBoxGiorni.Text);
            int extra = Convert.ToInt32(textBoxExtra.Text);
            Risorsa r;
            if (radioButtonLibro.Checked)
                r = new Libro(textBoxCodice.Text, textBoxTitolo.Text, textBoxAutore.Text, giorni, extra);
            else
                r = new Audiolibro(textBoxCodice.Text, textBoxTitolo.Text, textBoxAutore.Text, giorni, extra);

            catalogo.AggiungiRisorsa(r);
        }

        // MODIFICA (il codice è la chiave)
        private void buttonModifica_Click(object sender, EventArgs e)
        {
            Risorsa? r = catalogo.CercaPerCodice(textBoxCodice.Text);
            if (r == null)
            {
                MessageBox.Show("Risorsa non trovata.");
                return;
            }

            r.Titolo = textBoxTitolo.Text;
            r.Autore = textBoxAutore.Text;
            r.GiorniPrestito = Convert.ToInt32(textBoxGiorni.Text);
            if (r is Libro l)
                l.NumeroPagine = Convert.ToInt32(textBoxExtra.Text);
            else if (r is Audiolibro a)
                a.DurataMinuti = Convert.ToInt32(textBoxExtra.Text);

            dataGridViewRisorse.Refresh();
        }

        // CANCELLAZIONE
        private void buttonCancella_Click(object sender, EventArgs e)
        {
            Risorsa? r = catalogo.CercaPerCodice(textBoxCodice.Text);
            if (r != null)
            {
                catalogo.RimuoviRisorsa(r);
                labelDettagli.Text = "";
            }
        }

        private void buttonVisualizza_Click(object sender, EventArgs e)
        {
            MessageBox.Show(catalogo.VisualizzaCatalogo(), "Catalogo");
        }

        private void buttonPenale_Click(object sender, EventArgs e)
        {
            MessageBox.Show($"Penale totale: {catalogo.CalcolaPenaleTotale():F2} €");
        }

        private void buttonChiudi_Click(object sender, EventArgs e)
        {
            Close();
        }
    }
}
