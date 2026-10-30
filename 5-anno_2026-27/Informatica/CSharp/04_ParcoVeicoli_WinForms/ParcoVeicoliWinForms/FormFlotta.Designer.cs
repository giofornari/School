namespace ParcoVeicoliWinForms
{
    partial class FormFlotta
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
            dataGridViewVeicoli = new DataGridView();
            radioButtonAuto = new RadioButton();
            radioButtonCamion = new RadioButton();
            labelTarga = new Label();
            labelMarca = new Label();
            labelModello = new Label();
            labelKm = new Label();
            labelExtra = new Label();
            textBoxTarga = new TextBox();
            textBoxMarca = new TextBox();
            textBoxModello = new TextBox();
            textBoxKm = new TextBox();
            textBoxExtra = new TextBox();
            buttonInserisci = new Button();
            buttonModifica = new Button();
            buttonCancella = new Button();
            buttonVisualizza = new Button();
            buttonCosto = new Button();
            buttonChiudi = new Button();
            labelDettagli = new Label();
            ((System.ComponentModel.ISupportInitialize)dataGridViewVeicoli).BeginInit();
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
            // dataGridViewVeicoli
            //
            dataGridViewVeicoli.AllowUserToAddRows = false;
            dataGridViewVeicoli.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
            dataGridViewVeicoli.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dataGridViewVeicoli.Location = new Point(12, 50);
            dataGridViewVeicoli.MultiSelect = false;
            dataGridViewVeicoli.Name = "dataGridViewVeicoli";
            dataGridViewVeicoli.ReadOnly = true;
            dataGridViewVeicoli.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
            dataGridViewVeicoli.Size = new Size(796, 200);
            dataGridViewVeicoli.TabIndex = 1;
            dataGridViewVeicoli.CellClick += dataGridViewVeicoli_CellClick;
            //
            // radioButtonAuto
            //
            radioButtonAuto.AutoSize = true;
            radioButtonAuto.Checked = true;
            radioButtonAuto.Location = new Point(12, 265);
            radioButtonAuto.Name = "radioButtonAuto";
            radioButtonAuto.Size = new Size(51, 19);
            radioButtonAuto.TabIndex = 2;
            radioButtonAuto.TabStop = true;
            radioButtonAuto.Text = "Auto";
            radioButtonAuto.UseVisualStyleBackColor = true;
            radioButtonAuto.CheckedChanged += radioButtonAuto_CheckedChanged;
            //
            // radioButtonCamion
            //
            radioButtonCamion.AutoSize = true;
            radioButtonCamion.Location = new Point(90, 265);
            radioButtonCamion.Name = "radioButtonCamion";
            radioButtonCamion.Size = new Size(67, 19);
            radioButtonCamion.TabIndex = 3;
            radioButtonCamion.Text = "Camion";
            radioButtonCamion.UseVisualStyleBackColor = true;
            //
            // labelTarga
            //
            labelTarga.AutoSize = true;
            labelTarga.Location = new Point(12, 300);
            labelTarga.Name = "labelTarga";
            labelTarga.Size = new Size(37, 15);
            labelTarga.TabIndex = 4;
            labelTarga.Text = "Targa";
            //
            // labelMarca
            //
            labelMarca.AutoSize = true;
            labelMarca.Location = new Point(170, 300);
            labelMarca.Name = "labelMarca";
            labelMarca.Size = new Size(40, 15);
            labelMarca.TabIndex = 5;
            labelMarca.Text = "Marca";
            //
            // labelModello
            //
            labelModello.AutoSize = true;
            labelModello.Location = new Point(328, 300);
            labelModello.Name = "labelModello";
            labelModello.Size = new Size(51, 15);
            labelModello.TabIndex = 6;
            labelModello.Text = "Modello";
            //
            // labelKm
            //
            labelKm.AutoSize = true;
            labelKm.Location = new Point(486, 300);
            labelKm.Name = "labelKm";
            labelKm.Size = new Size(82, 15);
            labelKm.TabIndex = 7;
            labelKm.Text = "Km percorsi";
            //
            // labelExtra
            //
            labelExtra.AutoSize = true;
            labelExtra.Location = new Point(644, 300);
            labelExtra.Name = "labelExtra";
            labelExtra.Size = new Size(82, 15);
            labelExtra.TabIndex = 8;
            labelExtra.Text = "Numero porte";
            //
            // textBoxTarga
            //
            textBoxTarga.Location = new Point(12, 320);
            textBoxTarga.Name = "textBoxTarga";
            textBoxTarga.Size = new Size(150, 23);
            textBoxTarga.TabIndex = 9;
            //
            // textBoxMarca
            //
            textBoxMarca.Location = new Point(170, 320);
            textBoxMarca.Name = "textBoxMarca";
            textBoxMarca.Size = new Size(150, 23);
            textBoxMarca.TabIndex = 10;
            //
            // textBoxModello
            //
            textBoxModello.Location = new Point(328, 320);
            textBoxModello.Name = "textBoxModello";
            textBoxModello.Size = new Size(150, 23);
            textBoxModello.TabIndex = 11;
            //
            // textBoxKm
            //
            textBoxKm.Location = new Point(486, 320);
            textBoxKm.Name = "textBoxKm";
            textBoxKm.Size = new Size(150, 23);
            textBoxKm.TabIndex = 12;
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
            buttonVisualizza.Text = "Visualizza flotta";
            buttonVisualizza.UseVisualStyleBackColor = true;
            buttonVisualizza.Click += buttonVisualizza_Click;
            //
            // buttonCosto
            //
            buttonCosto.Location = new Point(516, 360);
            buttonCosto.Name = "buttonCosto";
            buttonCosto.Size = new Size(120, 30);
            buttonCosto.TabIndex = 18;
            buttonCosto.Text = "Costo totale";
            buttonCosto.UseVisualStyleBackColor = true;
            buttonCosto.Click += buttonCosto_Click;
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
            labelDettagli.Text = "Clicca un veicolo per vederne i dettagli.";
            //
            // FormFlotta
            //
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(820, 480);
            Controls.Add(labelDettagli);
            Controls.Add(buttonChiudi);
            Controls.Add(buttonCosto);
            Controls.Add(buttonVisualizza);
            Controls.Add(buttonCancella);
            Controls.Add(buttonModifica);
            Controls.Add(buttonInserisci);
            Controls.Add(textBoxExtra);
            Controls.Add(textBoxKm);
            Controls.Add(textBoxModello);
            Controls.Add(textBoxMarca);
            Controls.Add(textBoxTarga);
            Controls.Add(labelExtra);
            Controls.Add(labelKm);
            Controls.Add(labelModello);
            Controls.Add(labelMarca);
            Controls.Add(labelTarga);
            Controls.Add(radioButtonCamion);
            Controls.Add(radioButtonAuto);
            Controls.Add(dataGridViewVeicoli);
            Controls.Add(buttonCarica);
            Name = "FormFlotta";
            Text = "Gestione Parco Veicoli";
            ((System.ComponentModel.ISupportInitialize)dataGridViewVeicoli).EndInit();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Button buttonCarica;
        private DataGridView dataGridViewVeicoli;
        private RadioButton radioButtonAuto;
        private RadioButton radioButtonCamion;
        private Label labelTarga;
        private Label labelMarca;
        private Label labelModello;
        private Label labelKm;
        private Label labelExtra;
        private TextBox textBoxTarga;
        private TextBox textBoxMarca;
        private TextBox textBoxModello;
        private TextBox textBoxKm;
        private TextBox textBoxExtra;
        private Button buttonInserisci;
        private Button buttonModifica;
        private Button buttonCancella;
        private Button buttonVisualizza;
        private Button buttonCosto;
        private Button buttonChiudi;
        private Label labelDettagli;
    }
}
