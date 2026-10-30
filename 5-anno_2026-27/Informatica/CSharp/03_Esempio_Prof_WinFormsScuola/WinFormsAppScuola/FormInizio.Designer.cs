namespace WinFormsAppScuola
{
    partial class FormInizio
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
            buttonCaricaStudenti = new Button();
            dataGridViewStudenti = new DataGridView();
            Carica = new DataGridViewButtonColumn();
            buttonCancella = new Button();
            textBoxMatricola = new TextBox();
            textBoxNome = new TextBox();
            textBoxCognome = new TextBox();
            textBoxDataNascita = new TextBox();
            buttonInserisciStudente = new Button();
            label1 = new Label();
            label2 = new Label();
            label3 = new Label();
            label4 = new Label();
            buttonModificaStudente = new Button();
            panelTop = new Panel();
            buttonChiudi = new Button();
            ((System.ComponentModel.ISupportInitialize)dataGridViewStudenti).BeginInit();
            panelTop.SuspendLayout();
            SuspendLayout();
            // 
            // buttonCaricaStudenti
            // 
            buttonCaricaStudenti.Location = new Point(12, 85);
            buttonCaricaStudenti.Margin = new Padding(3, 4, 3, 4);
            buttonCaricaStudenti.Name = "buttonCaricaStudenti";
            buttonCaricaStudenti.Size = new Size(201, 31);
            buttonCaricaStudenti.TabIndex = 0;
            buttonCaricaStudenti.Text = "Carica Dati Studenti";
            buttonCaricaStudenti.UseVisualStyleBackColor = true;
            buttonCaricaStudenti.Click += buttonCaricaStudenti_Click;
            // 
            // dataGridViewStudenti
            // 
            dataGridViewStudenti.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dataGridViewStudenti.Columns.AddRange(new DataGridViewColumn[] { Carica });
            dataGridViewStudenti.Location = new Point(220, 85);
            dataGridViewStudenti.Margin = new Padding(3, 4, 3, 4);
            dataGridViewStudenti.Name = "dataGridViewStudenti";
            dataGridViewStudenti.RowHeadersWidth = 51;
            dataGridViewStudenti.Size = new Size(754, 200);
            dataGridViewStudenti.TabIndex = 1;
            dataGridViewStudenti.CellContentClick += dataGridViewStudenti_CellContentClick;
            // 
            // Carica
            // 
            Carica.HeaderText = "Carica";
            Carica.MinimumWidth = 6;
            Carica.Name = "Carica";
            Carica.Text = "Vedi voti";
            Carica.UseColumnTextForButtonValue = true;
            Carica.Width = 125;
            // 
            // buttonCancella
            // 
            buttonCancella.Location = new Point(737, 458);
            buttonCancella.Name = "buttonCancella";
            buttonCancella.Size = new Size(94, 29);
            buttonCancella.TabIndex = 3;
            buttonCancella.Text = "Cancella";
            buttonCancella.UseVisualStyleBackColor = true;
            buttonCancella.Click += buttonCancella_Click;
            // 
            // textBoxMatricola
            // 
            textBoxMatricola.BackColor = SystemColors.ControlDark;
            textBoxMatricola.Location = new Point(14, 390);
            textBoxMatricola.Name = "textBoxMatricola";
            textBoxMatricola.Size = new Size(125, 27);
            textBoxMatricola.TabIndex = 4;
            // 
            // textBoxNome
            // 
            textBoxNome.Location = new Point(208, 390);
            textBoxNome.Name = "textBoxNome";
            textBoxNome.Size = new Size(125, 27);
            textBoxNome.TabIndex = 5;
            // 
            // textBoxCognome
            // 
            textBoxCognome.Location = new Point(381, 390);
            textBoxCognome.Name = "textBoxCognome";
            textBoxCognome.Size = new Size(125, 27);
            textBoxCognome.TabIndex = 6;
            // 
            // textBoxDataNascita
            // 
            textBoxDataNascita.Location = new Point(566, 390);
            textBoxDataNascita.Name = "textBoxDataNascita";
            textBoxDataNascita.Size = new Size(125, 27);
            textBoxDataNascita.TabIndex = 7;
            // 
            // buttonInserisciStudente
            // 
            buttonInserisciStudente.Location = new Point(737, 388);
            buttonInserisciStudente.Name = "buttonInserisciStudente";
            buttonInserisciStudente.Size = new Size(94, 29);
            buttonInserisciStudente.TabIndex = 8;
            buttonInserisciStudente.Text = "Inserisci";
            buttonInserisciStudente.UseVisualStyleBackColor = true;
            buttonInserisciStudente.Click += buttonInserisciStudente_Click;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Location = new Point(14, 354);
            label1.Name = "label1";
            label1.Size = new Size(72, 20);
            label1.TabIndex = 9;
            label1.Text = "matricola";
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Location = new Point(381, 349);
            label2.Name = "label2";
            label2.Size = new Size(72, 20);
            label2.TabIndex = 10;
            label2.Text = "cognome";
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Location = new Point(208, 349);
            label3.Name = "label3";
            label3.Size = new Size(47, 20);
            label3.TabIndex = 11;
            label3.Text = "nome";
            // 
            // label4
            // 
            label4.AutoSize = true;
            label4.Location = new Point(570, 349);
            label4.Name = "label4";
            label4.Size = new Size(89, 20);
            label4.TabIndex = 12;
            label4.Text = "data nascita";
            // 
            // buttonModificaStudente
            // 
            buttonModificaStudente.Location = new Point(737, 423);
            buttonModificaStudente.Name = "buttonModificaStudente";
            buttonModificaStudente.Size = new Size(94, 29);
            buttonModificaStudente.TabIndex = 13;
            buttonModificaStudente.Text = "Modifica";
            buttonModificaStudente.UseVisualStyleBackColor = true;
            buttonModificaStudente.Click += buttonModificaStudente_Click;
            // 
            // panelTop
            // 
            panelTop.Controls.Add(buttonChiudi);
            panelTop.Dock = DockStyle.Top;
            panelTop.Location = new Point(0, 0);
            panelTop.Name = "panelTop";
            panelTop.Size = new Size(1003, 65);
            panelTop.TabIndex = 14;
            // 
            // buttonChiudi
            // 
            buttonChiudi.BackColor = SystemColors.Control;
            buttonChiudi.ForeColor = Color.Brown;
            buttonChiudi.Location = new Point(12, 12);
            buttonChiudi.Name = "buttonChiudi";
            buttonChiudi.Size = new Size(94, 29);
            buttonChiudi.TabIndex = 0;
            buttonChiudi.Text = "Chiudi";
            buttonChiudi.UseVisualStyleBackColor = false;
            buttonChiudi.Click += buttonChiudi_Click;
            // 
            // FormInizio
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(1003, 600);
            Controls.Add(panelTop);
            Controls.Add(buttonModificaStudente);
            Controls.Add(label4);
            Controls.Add(label3);
            Controls.Add(label2);
            Controls.Add(label1);
            Controls.Add(buttonInserisciStudente);
            Controls.Add(textBoxDataNascita);
            Controls.Add(textBoxCognome);
            Controls.Add(textBoxNome);
            Controls.Add(textBoxMatricola);
            Controls.Add(buttonCancella);
            Controls.Add(dataGridViewStudenti);
            Controls.Add(buttonCaricaStudenti);
            Margin = new Padding(3, 4, 3, 4);
            Name = "FormInizio";
            Text = "Studenti";
            ((System.ComponentModel.ISupportInitialize)dataGridViewStudenti).EndInit();
            panelTop.ResumeLayout(false);
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Button buttonCaricaStudenti;
        private DataGridView dataGridViewStudenti;
        private Button buttonCancella;
        private TextBox textBoxMatricola;
        private TextBox textBoxNome;
        private TextBox textBoxCognome;
        private TextBox textBoxDataNascita;
        private Button buttonInserisciStudente;
        private Label label1;
        private Label label2;
        private Label label3;
        private Label label4;
        private Button buttonModificaStudente;
        private DataGridViewButtonColumn Carica;
        private Panel panelTop;
        private Button buttonChiudi;
    }
}
