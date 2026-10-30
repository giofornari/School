using System;
using System.Globalization;
using System.Windows.Forms;

namespace ParcoVeicoli
{
    public partial class MainForm : Form
    {
        private readonly Flotta flotta = new Flotta();
        private static readonly CultureInfo cultura = CultureInfo.GetCultureInfo("it-IT");

        public MainForm()
        {
            InitializeComponent();
            cmbTipo.SelectedIndex = 0;
            AggiornaFlotta();
        }

        private void cmbTipo_SelectedIndexChanged(object sender, EventArgs e)
        {
            bool auto = cmbTipo.SelectedIndex == 0;
            numPorte.Enabled = auto;
            numCarico.Enabled = !auto;
            lblPorte.Enabled = auto;
            lblCarico.Enabled = !auto;
        }

        private void btnInserisci_Click(object sender, EventArgs e)
        {
            errori.Clear();
            bool datiValidi = true;
            TextBox[] campiObbligatori = { txtTarga, txtMarca, txtModello };

            foreach (TextBox campo in campiObbligatori)
            {
                if (string.IsNullOrWhiteSpace(campo.Text))
                {
                    errori.SetError(campo, "Compila questo campo.");
                    datiValidi = false;
                }
            }

            if (!datiValidi)
            {
                foreach (TextBox campo in campiObbligatori)
                {
                    if (string.IsNullOrWhiteSpace(campo.Text))
                    {
                        campo.Focus();
                        break;
                    }
                }
                return;
            }

            string targa = txtTarga.Text.Trim().ToUpperInvariant();
            string marca = txtMarca.Text.Trim();
            string modello = txtModello.Text.Trim();
            double km = (double)numKm.Value;
            Veicolo veicolo;

            if (cmbTipo.SelectedIndex == 0)
                veicolo = new Auto(targa, marca, modello, km, (int)numPorte.Value);
            else
                veicolo = new Camion(targa, marca, modello, km, (double)numCarico.Value);

            flotta.AggiungiVeicolo(veicolo);
            AggiornaFlotta();
            dgvFlotta.ClearSelection();
            dgvFlotta.Rows[dgvFlotta.Rows.Count - 1].Selected = true;
            dgvFlotta.CurrentCell = dgvFlotta.Rows[dgvFlotta.Rows.Count - 1].Cells[0];

            lblStato.Text = "Veicolo " + targa + " inserito.";
            PulisciCampi();
        }

        private void btnVisualizza_Click(object sender, EventArgs e)
        {
            AggiornaFlotta();
            lblStato.Text = flotta.Veicoli.Count == 0
                ? "Nessun veicolo in flotta."
                : "Flotta aggiornata: " + flotta.Veicoli.Count + " veicoli.";
        }

        private void AggiornaFlotta()
        {
            dgvFlotta.Rows.Clear();
            foreach (Veicolo veicolo in flotta.Veicoli)
            {
                Auto auto = veicolo as Auto;
                Camion camion = veicolo as Camion;
                int indice = dgvFlotta.Rows.Add(
                    auto != null ? "Auto" : "Camion",
                    veicolo.Targa, veicolo.Marca, veicolo.Modello,
                    veicolo.ChilometriPercorsi,
                    auto != null ? (object)auto.NumeroPorte : null,
                    camion != null ? (object)camion.CapacitaCarico : null,
                    veicolo.CalcolaCostoManutenzione());
                dgvFlotta.Rows[indice].Tag = veicolo;
            }

            lblNumeroVeicoli.Text = "Veicoli in flotta: " + flotta.Veicoli.Count;
            AggiornaTotale();
            AggiornaDettagli();
        }

        private void btnCosto_Click(object sender, EventArgs e)
        {
            AggiornaTotale();
            lblStato.Text = "Costo totale di manutenzione calcolato.";
        }

        private void AggiornaTotale()
        {
            lblTotale.Text = "Manutenzione totale: "
                + flotta.CalcolaCostoTotaleManutenzione().ToString("C2", cultura);
        }

        private void dgvFlotta_SelectionChanged(object sender, EventArgs e)
        {
            AggiornaDettagli();
        }

        private void AggiornaDettagli()
        {
            Veicolo selezionato = dgvFlotta.SelectedRows.Count == 0
                ? null : dgvFlotta.SelectedRows[0].Tag as Veicolo;
            lblDettagli.Text = selezionato == null
                ? "Seleziona un veicolo per vedere i dettagli."
                : selezionato.StampaDettagli();
        }

        private void btnPulisci_Click(object sender, EventArgs e)
        {
            PulisciCampi();
        }

        private void PulisciCampi()
        {
            txtTarga.Clear();
            txtMarca.Clear();
            txtModello.Clear();
            numKm.Value = 0;
            numPorte.Value = 5;
            numCarico.Value = 1;
            errori.Clear();
            txtTarga.Focus();
        }

        private void btnEsci_Click(object sender, EventArgs e)
        {
            Close();
        }
    }
}
