using LibreriaParcoVeicoli;

namespace ParcoVeicoliWinForms
{
    // partial: l'altra metà della classe è in FormFlotta.Designer.cs (i controlli)
    public partial class FormFlotta : Form
    {
        Flotta flotta;

        public FormFlotta()
        {
            InitializeComponent();   // crea i controlli (metodo del Designer)
            flotta = new Flotta();
            flotta.CaricaDatiDiProva();
        }

        // LETTURA: collega la lista alla griglia
        private void buttonCarica_Click(object sender, EventArgs e)
        {
            dataGridViewVeicoli.DataSource = flotta.Veicoli;
        }

        // cambia l'etichetta del campo specifico (porte o carico)
        private void radioButtonAuto_CheckedChanged(object sender, EventArgs e)
        {
            labelExtra.Text = radioButtonAuto.Checked ? "Numero porte" : "Capacità carico (t)";
        }

        // click su una riga: riempie i campi con i dati del veicolo
        private void dataGridViewVeicoli_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            if (e.RowIndex < 0) return;   // click sull'intestazione delle colonne

            Veicolo v = flotta.Veicoli[e.RowIndex];
            textBoxTarga.Text = v.Targa;
            textBoxMarca.Text = v.Marca;
            textBoxModello.Text = v.Modello;
            textBoxKm.Text = v.ChilometriPercorsi.ToString();

            // "is Auto a": se v è un'Auto, la mette già convertita in a (instanceof + cast di Java)
            if (v is Auto a)
            {
                radioButtonAuto.Checked = true;
                textBoxExtra.Text = a.NumeroPorte.ToString();
            }
            else if (v is Camion c)
            {
                radioButtonCamion.Checked = true;
                textBoxExtra.Text = c.CapacitaCarico.ToString();
            }

            labelDettagli.Text = v.StampaDettagli() + $"\nCosto manutenzione: {v.CalcolaCostoManutenzione():F2} €";
        }

        // INSERIMENTO
        private void buttonInserisci_Click(object sender, EventArgs e)
        {
            if (flotta.CercaPerTarga(textBoxTarga.Text) != null)
            {
                MessageBox.Show("Targa già presente.");
                return;
            }

            double km = Convert.ToDouble(textBoxKm.Text);
            Veicolo v;
            if (radioButtonAuto.Checked)
                v = new Auto(textBoxTarga.Text, textBoxMarca.Text, textBoxModello.Text, km, Convert.ToInt32(textBoxExtra.Text));
            else
                v = new Camion(textBoxTarga.Text, textBoxMarca.Text, textBoxModello.Text, km, Convert.ToDouble(textBoxExtra.Text));

            flotta.AggiungiVeicolo(v);   // la BindingList avvisa la griglia: nessun Refresh necessario
        }

        // MODIFICA: cerca per targa e aggiorna i campi (la targa è la "chiave", non si modifica)
        private void buttonModifica_Click(object sender, EventArgs e)
        {
            Veicolo? v = flotta.CercaPerTarga(textBoxTarga.Text);
            if (v == null)
            {
                MessageBox.Show("Veicolo non trovato.");
                return;
            }

            v.Marca = textBoxMarca.Text;
            v.Modello = textBoxModello.Text;
            v.ChilometriPercorsi = Convert.ToDouble(textBoxKm.Text);
            if (v is Auto a)
                a.NumeroPorte = Convert.ToInt32(textBoxExtra.Text);
            else if (v is Camion c)
                c.CapacitaCarico = Convert.ToDouble(textBoxExtra.Text);

            // qui serve Refresh: è cambiato un oggetto, non la lista
            dataGridViewVeicoli.Refresh();
        }

        // CANCELLAZIONE
        private void buttonCancella_Click(object sender, EventArgs e)
        {
            Veicolo? v = flotta.CercaPerTarga(textBoxTarga.Text);
            if (v != null)
            {
                flotta.RimuoviVeicolo(v);
                labelDettagli.Text = "";
            }
        }

        private void buttonVisualizza_Click(object sender, EventArgs e)
        {
            MessageBox.Show(flotta.VisualizzaFlotta(), "Flotta");
        }

        private void buttonCosto_Click(object sender, EventArgs e)
        {
            MessageBox.Show($"Costo totale manutenzione: {flotta.CalcolaCostoTotaleManutenzione():F2} €");
        }

        private void buttonChiudi_Click(object sender, EventArgs e)
        {
            Close();
        }
    }
}
