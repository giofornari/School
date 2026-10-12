using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;

namespace ParcoVeicoli
{
    partial class MainForm
    {
        private IContainer components;
        private ComboBox cmbTipo;
        private TextBox txtTarga;
        private TextBox txtMarca;
        private TextBox txtModello;
        private NumericUpDown numKm;
        private NumericUpDown numPorte;
        private NumericUpDown numCarico;
        private Label lblPorte;
        private Label lblCarico;
        private Label lblNumeroVeicoli;
        private Label lblTotale;
        private Label lblDettagli;
        private Label lblStato;
        private DataGridView dgvFlotta;
        private ErrorProvider errori;

        protected override void Dispose(bool disposing)
        {
            if (disposing && components != null)
                components.Dispose();
            base.Dispose(disposing);
        }

        private void InitializeComponent()
        {
            components = new Container();
            errori = new ErrorProvider(components);
            errori.ContainerControl = this;
            errori.BlinkStyle = ErrorBlinkStyle.NeverBlink;
            SuspendLayout();

            TableLayoutPanel layout = new TableLayoutPanel();
            layout.Dock = DockStyle.Fill;
            layout.Padding = new Padding(12);
            layout.ColumnCount = 2;
            layout.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 310));
            layout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
            layout.RowCount = 2;
            layout.RowStyles.Add(new RowStyle(SizeType.Percent, 100));
            layout.RowStyles.Add(new RowStyle(SizeType.Absolute, 34));

            GroupBox gruppoInserimento = new GroupBox();
            gruppoInserimento.Text = "Inserisci un veicolo";
            gruppoInserimento.Dock = DockStyle.Fill;
            gruppoInserimento.Padding = new Padding(12, 18, 18, 12);

            TableLayoutPanel campi = new TableLayoutPanel();
            campi.Dock = DockStyle.Fill;
            campi.AutoScroll = true;
            campi.ColumnCount = 2;
            campi.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 128));
            campi.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
            campi.RowCount = 10;
            for (int i = 0; i < 7; i++)
                campi.RowStyles.Add(new RowStyle(SizeType.Absolute, 38));
            campi.RowStyles.Add(new RowStyle(SizeType.Absolute, 46));
            campi.RowStyles.Add(new RowStyle(SizeType.Absolute, 64));
            campi.RowStyles.Add(new RowStyle(SizeType.Percent, 100));

            cmbTipo = new ComboBox();
            cmbTipo.Name = "cmbTipo";
            cmbTipo.DropDownStyle = ComboBoxStyle.DropDownList;
            cmbTipo.Items.AddRange(new object[] { "Auto", "Camion" });
            cmbTipo.SelectedIndexChanged += cmbTipo_SelectedIndexChanged;

            txtTarga = new TextBox();
            txtTarga.Name = "txtTarga";
            txtTarga.CharacterCasing = CharacterCasing.Upper;
            txtMarca = new TextBox();
            txtMarca.Name = "txtMarca";
            txtModello = new TextBox();
            txtModello.Name = "txtModello";

            numKm = new NumericUpDown();
            numKm.Name = "numKm";
            numKm.DecimalPlaces = 2;
            numKm.Maximum = 1000000000;
            numKm.ThousandsSeparator = true;

            numPorte = new NumericUpDown();
            numPorte.Name = "numPorte";
            numPorte.Minimum = 1;
            numPorte.Maximum = 99;
            numPorte.Value = 5;

            numCarico = new NumericUpDown();
            numCarico.Name = "numCarico";
            numCarico.DecimalPlaces = 2;
            numCarico.Minimum = 0.01m;
            numCarico.Maximum = 1000000;
            numCarico.Increment = 0.25m;
            numCarico.Value = 1;

            Label[] etichette = {
                new Label { Text = "Tipo" },
                new Label { Text = "Targa" },
                new Label { Text = "Marca" },
                new Label { Text = "Modello" },
                new Label { Text = "Km percorsi" },
                new Label { Text = "Numero porte" },
                new Label { Text = "Carico (tonnellate)" }
            };
            lblPorte = etichette[5];
            lblCarico = etichette[6];
            Control[] input = { cmbTipo, txtTarga, txtMarca, txtModello, numKm, numPorte, numCarico };
            for (int i = 0; i < input.Length; i++)
            {
                etichette[i].Dock = DockStyle.Fill;
                etichette[i].TextAlign = ContentAlignment.MiddleLeft;
                input[i].Dock = DockStyle.Fill;
                input[i].Margin = new Padding(3, 7, 3, 3);
                input[i].TabIndex = i;
                input[i].AccessibleName = etichette[i].Text;
                campi.Controls.Add(etichette[i], 0, i);
                campi.Controls.Add(input[i], 1, i);
            }

            FlowLayoutPanel pulsantiInserimento = new FlowLayoutPanel();
            pulsantiInserimento.Dock = DockStyle.Fill;
            Button btnInserisci = new Button();
            btnInserisci.Name = "btnInserisci";
            btnInserisci.Text = "&Inserisci";
            btnInserisci.AutoSize = true;
            btnInserisci.Padding = new Padding(6);
            btnInserisci.Click += btnInserisci_Click;
            Button btnPulisci = new Button();
            btnPulisci.Name = "btnPulisci";
            btnPulisci.Text = "&Pulisci campi";
            btnPulisci.AutoSize = true;
            btnPulisci.Padding = new Padding(6);
            btnPulisci.Click += btnPulisci_Click;
            pulsantiInserimento.Controls.Add(btnInserisci);
            pulsantiInserimento.Controls.Add(btnPulisci);
            campi.Controls.Add(pulsantiInserimento, 0, 7);
            campi.SetColumnSpan(pulsantiInserimento, 2);

            Label nota = new Label();
            nota.Text = "Targa, marca e modello sono obbligatori.\nI dati restano in memoria fino alla chiusura.";
            nota.Dock = DockStyle.Fill;
            nota.ForeColor = SystemColors.GrayText;
            campi.Controls.Add(nota, 0, 8);
            campi.SetColumnSpan(nota, 2);
            gruppoInserimento.Controls.Add(campi);

            GroupBox gruppoFlotta = new GroupBox();
            gruppoFlotta.Text = "Flotta aziendale";
            gruppoFlotta.Dock = DockStyle.Fill;
            gruppoFlotta.Padding = new Padding(10, 18, 10, 10);

            TableLayoutPanel elenco = new TableLayoutPanel();
            elenco.Dock = DockStyle.Fill;
            elenco.ColumnCount = 1;
            elenco.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
            elenco.RowCount = 5;
            elenco.RowStyles.Add(new RowStyle(SizeType.Absolute, 28));
            elenco.RowStyles.Add(new RowStyle(SizeType.Percent, 100));
            elenco.RowStyles.Add(new RowStyle(SizeType.Absolute, 60));
            elenco.RowStyles.Add(new RowStyle(SizeType.Absolute, 34));
            elenco.RowStyles.Add(new RowStyle(SizeType.Absolute, 44));

            lblNumeroVeicoli = new Label();
            lblNumeroVeicoli.Dock = DockStyle.Fill;
            lblNumeroVeicoli.TextAlign = ContentAlignment.MiddleLeft;
            elenco.Controls.Add(lblNumeroVeicoli, 0, 0);

            dgvFlotta = new DataGridView();
            dgvFlotta.Name = "dgvFlotta";
            dgvFlotta.Dock = DockStyle.Fill;
            dgvFlotta.ReadOnly = true;
            dgvFlotta.AllowUserToAddRows = false;
            dgvFlotta.AllowUserToDeleteRows = false;
            dgvFlotta.AllowUserToResizeRows = false;
            dgvFlotta.MultiSelect = false;
            dgvFlotta.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
            dgvFlotta.RowHeadersVisible = false;
            dgvFlotta.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
            dgvFlotta.BackgroundColor = SystemColors.Window;
            dgvFlotta.AccessibleName = "Veicoli della flotta";
            dgvFlotta.Columns.Add("Tipo", "Tipo");
            dgvFlotta.Columns.Add("Targa", "Targa");
            dgvFlotta.Columns.Add("Marca", "Marca");
            dgvFlotta.Columns.Add("Modello", "Modello");
            dgvFlotta.Columns.Add("Km", "Km percorsi");
            dgvFlotta.Columns.Add("Porte", "Porte");
            dgvFlotta.Columns.Add("Carico", "Carico (t)");
            dgvFlotta.Columns.Add("Costo", "Manutenzione");
            foreach (DataGridViewColumn colonna in dgvFlotta.Columns)
            {
                colonna.SortMode = DataGridViewColumnSortMode.NotSortable;
                colonna.MinimumWidth = 60;
            }
            dgvFlotta.Columns[7].MinimumWidth = 110;
            dgvFlotta.Columns[4].DefaultCellStyle.Format = "N2";
            dgvFlotta.Columns[6].DefaultCellStyle.Format = "N2";
            dgvFlotta.Columns[7].DefaultCellStyle.Format = "C2";
            dgvFlotta.DefaultCellStyle.FormatProvider = System.Globalization.CultureInfo.GetCultureInfo("it-IT");
            dgvFlotta.SelectionChanged += dgvFlotta_SelectionChanged;
            elenco.Controls.Add(dgvFlotta, 0, 1);

            lblDettagli = new Label();
            lblDettagli.Name = "lblDettagli";
            lblDettagli.Dock = DockStyle.Fill;
            lblDettagli.TextAlign = ContentAlignment.MiddleLeft;
            lblDettagli.AutoEllipsis = true;
            elenco.Controls.Add(lblDettagli, 0, 2);

            lblTotale = new Label();
            lblTotale.Name = "lblTotale";
            lblTotale.Dock = DockStyle.Fill;
            lblTotale.Font = new Font("Segoe UI", 10, FontStyle.Bold);
            lblTotale.TextAlign = ContentAlignment.MiddleLeft;
            elenco.Controls.Add(lblTotale, 0, 3);

            FlowLayoutPanel azioni = new FlowLayoutPanel();
            azioni.Dock = DockStyle.Fill;
            Button btnVisualizza = new Button();
            btnVisualizza.Name = "btnVisualizza";
            btnVisualizza.Text = "&Visualizza flotta";
            btnVisualizza.AutoSize = true;
            btnVisualizza.Padding = new Padding(6);
            btnVisualizza.Click += btnVisualizza_Click;
            Button btnCosto = new Button();
            btnCosto.Name = "btnCosto";
            btnCosto.Text = "&Calcola manutenzione";
            btnCosto.AutoSize = true;
            btnCosto.Padding = new Padding(6);
            btnCosto.Click += btnCosto_Click;
            Button btnEsci = new Button();
            btnEsci.Name = "btnEsci";
            btnEsci.Text = "&Esci";
            btnEsci.AutoSize = true;
            btnEsci.Padding = new Padding(6);
            btnEsci.Click += btnEsci_Click;
            azioni.Controls.Add(btnVisualizza);
            azioni.Controls.Add(btnCosto);
            azioni.Controls.Add(btnEsci);
            elenco.Controls.Add(azioni, 0, 4);
            gruppoFlotta.Controls.Add(elenco);

            lblStato = new Label();
            lblStato.Dock = DockStyle.Fill;
            lblStato.Text = "Nessun veicolo in flotta.";
            lblStato.TextAlign = ContentAlignment.MiddleLeft;
            layout.Controls.Add(gruppoInserimento, 0, 0);
            layout.Controls.Add(gruppoFlotta, 1, 0);
            layout.Controls.Add(lblStato, 0, 1);
            layout.SetColumnSpan(lblStato, 2);
            Controls.Add(layout);

            AcceptButton = btnInserisci;
            CancelButton = btnEsci;
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            Font = new Font("Segoe UI", 9F);
            ClientSize = new Size(1100, 600);
            MinimumSize = new Size(960, 540);
            StartPosition = FormStartPosition.CenterScreen;
            Text = "Gestione Parco Veicoli Aziendale";
            Name = "MainForm";
            ResumeLayout(false);
        }
    }
}
