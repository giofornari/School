namespace BibliotecaWinForms
{
    partial class FormCatalogo
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            buttonCarica = new Button();
            dataGridViewRisorse = new DataGridView();
            radioButtonLibro = new RadioButton();
            radioButtonAudiolibro = new RadioButton();
            labelCodice = new Label();
            labelTitolo = new Label();
            labelAutore = new Label();
            labelGiorni = new Label();
            labelExtra = new Label();
            textBoxCodice = new TextBox();
            textBoxTitolo = new TextBox();
            textBoxAutore = new TextBox();
            textBoxGiorni = new TextBox();
            textBoxExtra = new TextBox();
            buttonInserisci = new Button();
            buttonModifica = new Button();
            buttonCancella = new Button();
            buttonVisualizza = new Button();
            buttonPenale = new Button();
            buttonChiudi = new Button();
            labelDettagli = new Label();
            ((System.ComponentModel.ISupportInitialize)dataGridViewRisorse).BeginInit();
            SuspendLayout();
            //
            // buttonCarica
            //
            buttonCarica.Location = new Point(12, 12);
            buttonCarica.Name = "buttonCarica";
            buttonCarica.Size = new Size(150, 30);
            buttonCarica.TabIndex = 0;
            buttonCarica.Text = "Carica dati";
            buttonCarica.UseVisualStyleBackColor = true;
            buttonCarica.Click += buttonCarica_Click;
            //
            // dataGridViewRisorse
            //
            dataGridViewRisorse.AllowUserToAddRows = false;
            dataGridViewRisorse.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
            dataGridViewRisorse.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dataGridViewRisorse.Location = new Point(12, 50);
            dataGridViewRisorse.MultiSelect = false;
            dataGridViewRisorse.Name = "dataGridViewRisorse";
            dataGridViewRisorse.ReadOnly = true;
            dataGridViewRisorse.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
            dataGridViewRisorse.Size = new Size(796, 200);
            dataGridViewRisorse.TabIndex = 1;
            dataGridViewRisorse.CellClick += dataGridViewRisorse_CellClick;
            //
            // radioButtonLibro
            //
            radioButtonLibro.AutoSize = true;
            radioButtonLibro.Checked = true;
            radioButtonLibro.Location = new Point(12, 265);
            radioButtonLibro.Name = "radioButtonLibro";
            radioButtonLibro.Size = new Size(51, 19);
            radioButtonLibro.TabIndex = 2;
            radioButtonLibro.TabStop = true;
            radioButtonLibro.Text = "Libro";
            radioButtonLibro.UseVisualStyleBackColor = true;
            radioButtonLibro.CheckedChanged += radioButtonLibro_CheckedChanged;
            //
            // radioButtonAudiolibro
            //
            radioButtonAudiolibro.AutoSize = true;
            radioButtonAudiolibro.Location = new Point(90, 265);
            radioButtonAudiolibro.Name = "radioButtonAudiolibro";
            radioButtonAudiolibro.Size = new Size(67, 19);
            radioButtonAudiolibro.TabIndex = 3;
            radioButtonAudiolibro.Text = "Audiolibro";
            radioButtonAudiolibro.UseVisualStyleBackColor = true;
            //
            // labelCodice
            //
            labelCodice.AutoSize = true;
            labelCodice.Location = new Point(12, 300);
            labelCodice.Name = "labelCodice";
            labelCodice.Size = new Size(37, 15);
            labelCodice.TabIndex = 4;
            labelCodice.Text = "Codice";
            //
            // labelTitolo
            //
            labelTitolo.AutoSize = true;
            labelTitolo.Location = new Point(170, 300);
            labelTitolo.Name = "labelTitolo";
            labelTitolo.Size = new Size(40, 15);
            labelTitolo.TabIndex = 5;
            labelTitolo.Text = "Titolo";
            //
            // labelAutore
            //
            labelAutore.AutoSize = true;
            labelAutore.Location = new Point(328, 300);
            labelAutore.Name = "labelAutore";
            labelAutore.Size = new Size(51, 15);
            labelAutore.TabIndex = 6;
            labelAutore.Text = "Autore";
            //
            // labelGiorni
            //
            labelGiorni.AutoSize = true;
            labelGiorni.Location = new Point(486, 300);
            labelGiorni.Name = "labelGiorni";
            labelGiorni.Size = new Size(82, 15);
            labelGiorni.TabIndex = 7;
            labelGiorni.Text = "Giorni prestito";
            //
            // labelExtra
            //
            labelExtra.AutoSize = true;
            labelExtra.Location = new Point(644, 300);
            labelExtra.Name = "labelExtra";
            labelExtra.Size = new Size(82, 15);
            labelExtra.TabIndex = 8;
            labelExtra.Text = "Numero pagine";
            //
            // textBoxCodice
            //
            textBoxCodice.Location = new Point(12, 320);
            textBoxCodice.Name = "textBoxCodice";
            textBoxCodice.Size = new Size(150, 23);
            textBoxCodice.TabIndex = 9;
            //
            // textBoxTitolo
            //
            textBoxTitolo.Location = new Point(170, 320);
            textBoxTitolo.Name = "textBoxTitolo";
            textBoxTitolo.Size = new Size(150, 23);
            textBoxTitolo.TabIndex = 10;
            //
            // textBoxAutore
            //
            textBoxAutore.Location = new Point(328, 320);
            textBoxAutore.Name = "textBoxAutore";
            textBoxAutore.Size = new Size(150, 23);
            textBoxAutore.TabIndex = 11;
            //
            // textBoxGiorni
            //
            textBoxGiorni.Location = new Point(486, 320);
            textBoxGiorni.Name = "textBoxGiorni";
            textBoxGiorni.Size = new Size(150, 23);
            textBoxGiorni.TabIndex = 12;
            //
            // textBoxExtra
            //
            textBoxExtra.Location = new Point(644, 320);
            textBoxExtra.Name = "textBoxExtra";
            textBoxExtra.Size = new Size(150, 23);
            textBoxExtra.TabIndex = 13;
            //
            // buttonInserisci
            //
            buttonInserisci.Location = new Point(12, 360);
            buttonInserisci.Name = "buttonInserisci";
            buttonInserisci.Size = new Size(120, 30);
            buttonInserisci.TabIndex = 14;
            buttonInserisci.Text = "Inserisci";
            buttonInserisci.UseVisualStyleBackColor = true;
            buttonInserisci.Click += buttonInserisci_Click;
            //
            // buttonModifica
            //
            buttonModifica.Location = new Point(138, 360);
            buttonModifica.Name = "buttonModifica";
            buttonModifica.Size = new Size(120, 30);
            buttonModifica.TabIndex = 15;
            buttonModifica.Text = "Modifica";
            buttonModifica.UseVisualStyleBackColor = true;
            buttonModifica.Click += buttonModifica_Click;
            //
            // buttonCancella
            //
            buttonCancella.Location = new Point(264, 360);
            buttonCancella.Name = "buttonCancella";
            buttonCancella.Size = new Size(120, 30);
            buttonCancella.TabIndex = 16;
            buttonCancella.Text = "Cancella";
            buttonCancella.UseVisualStyleBackColor = true;
            buttonCancella.Click += buttonCancella_Click;
            //
            // buttonVisualizza
            //
            buttonVisualizza.Location = new Point(390, 360);
            buttonVisualizza.Name = "buttonVisualizza";
            buttonVisualizza.Size = new Size(120, 30);
            buttonVisualizza.TabIndex = 17;
            buttonVisualizza.Text = "Visualizza catalogo";
            buttonVisualizza.UseVisualStyleBackColor = true;
            buttonVisualizza.Click += buttonVisualizza_Click;
            //
            // buttonPenale
            //
            buttonPenale.Location = new Point(516, 360);
            buttonPenale.Name = "buttonPenale";
            buttonPenale.Size = new Size(120, 30);
            buttonPenale.TabIndex = 18;
            buttonPenale.Text = "Penale totale";
            buttonPenale.UseVisualStyleBackColor = true;
            buttonPenale.Click += buttonPenale_Click;
            //
            // buttonChiudi
            //
            buttonChiudi.Location = new Point(688, 360);
            buttonChiudi.Name = "buttonChiudi";
            buttonChiudi.Size = new Size(120, 30);
            buttonChiudi.TabIndex = 19;
            buttonChiudi.Text = "Chiudi";
            buttonChiudi.UseVisualStyleBackColor = true;
            buttonChiudi.Click += buttonChiudi_Click;
            //
            // labelDettagli
            //
            labelDettagli.BorderStyle = BorderStyle.FixedSingle;
            labelDettagli.Location = new Point(12, 405);
            labelDettagli.Name = "labelDettagli";
            labelDettagli.Size = new Size(796, 60);
            labelDettagli.TabIndex = 20;
            labelDettagli.Text = "Clicca una risorsa per vederne i dettagli.";
            //
            // FormCatalogo
            //
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(820, 480);
            Controls.Add(labelDettagli);
            Controls.Add(buttonChiudi);
            Controls.Add(buttonPenale);
            Controls.Add(buttonVisualizza);
            Controls.Add(buttonCancella);
            Controls.Add(buttonModifica);
            Controls.Add(buttonInserisci);
            Controls.Add(textBoxExtra);
            Controls.Add(textBoxGiorni);
            Controls.Add(textBoxAutore);
            Controls.Add(textBoxTitolo);
            Controls.Add(textBoxCodice);
            Controls.Add(labelExtra);
            Controls.Add(labelGiorni);
            Controls.Add(labelAutore);
            Controls.Add(labelTitolo);
            Controls.Add(labelCodice);
            Controls.Add(radioButtonAudiolibro);
            Controls.Add(radioButtonLibro);
            Controls.Add(dataGridViewRisorse);
            Controls.Add(buttonCarica);
            Name = "FormCatalogo";
            Text = "Biblioteca Scolastica";
            ((System.ComponentModel.ISupportInitialize)dataGridViewRisorse).EndInit();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Button buttonCarica;
        private DataGridView dataGridViewRisorse;
        private RadioButton radioButtonLibro;
        private RadioButton radioButtonAudiolibro;
        private Label labelCodice;
        private Label labelTitolo;
        private Label labelAutore;
        private Label labelGiorni;
        private Label labelExtra;
        private TextBox textBoxCodice;
        private TextBox textBoxTitolo;
        private TextBox textBoxAutore;
        private TextBox textBoxGiorni;
        private TextBox textBoxExtra;
        private Button buttonInserisci;
        private Button buttonModifica;
        private Button buttonCancella;
        private Button buttonVisualizza;
        private Button buttonPenale;
        private Button buttonChiudi;
        private Label labelDettagli;
    }
}
