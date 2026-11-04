namespace UtentiWinForms
{
    partial class WindowsFormUtenti
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
            dataGridViewUtenti = new DataGridView();
            labelCognome = new Label();
            labelNome = new Label();
            labelPassword = new Label();
            textBoxCognome = new TextBox();
            textBoxNome = new TextBox();
            textBoxPassword = new TextBox();
            buttonInserisci = new Button();
            buttonLogin = new Button();
            buttonChiudi = new Button();
            ((System.ComponentModel.ISupportInitialize)dataGridViewUtenti).BeginInit();
            SuspendLayout();
            //
            // dataGridViewUtenti
            //
            dataGridViewUtenti.AllowUserToAddRows = false;
            dataGridViewUtenti.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
            dataGridViewUtenti.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dataGridViewUtenti.Location = new Point(12, 12);
            dataGridViewUtenti.Name = "dataGridViewUtenti";
            dataGridViewUtenti.ReadOnly = true;
            dataGridViewUtenti.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
            dataGridViewUtenti.Size = new Size(760, 200);
            dataGridViewUtenti.TabIndex = 0;
            //
            // labelCognome
            //
            labelCognome.AutoSize = true;
            labelCognome.Location = new Point(12, 231);
            labelCognome.Name = "labelCognome";
            labelCognome.Size = new Size(68, 20);
            labelCognome.TabIndex = 1;
            labelCognome.Text = "Cognome";
            //
            // labelNome
            //
            labelNome.AutoSize = true;
            labelNome.Location = new Point(12, 265);
            labelNome.Name = "labelNome";
            labelNome.Size = new Size(46, 20);
            labelNome.TabIndex = 3;
            labelNome.Text = "Nome";
            //
            // labelPassword
            //
            labelPassword.AutoSize = true;
            labelPassword.Location = new Point(12, 299);
            labelPassword.Name = "labelPassword";
            labelPassword.Size = new Size(70, 20);
            labelPassword.TabIndex = 5;
            labelPassword.Text = "Password";
            //
            // textBoxCognome
            //
            textBoxCognome.Location = new Point(100, 228);
            textBoxCognome.Name = "textBoxCognome";
            textBoxCognome.Size = new Size(200, 27);
            textBoxCognome.TabIndex = 2;
            //
            // textBoxNome
            //
            textBoxNome.Location = new Point(100, 262);
            textBoxNome.Name = "textBoxNome";
            textBoxNome.Size = new Size(200, 27);
            textBoxNome.TabIndex = 4;
            //
            // textBoxPassword
            //
            textBoxPassword.Location = new Point(100, 296);
            textBoxPassword.Name = "textBoxPassword";
            textBoxPassword.Size = new Size(200, 27);
            textBoxPassword.TabIndex = 6;
            //
            // buttonInserisci
            //
            buttonInserisci.Location = new Point(320, 226);
            buttonInserisci.Name = "buttonInserisci";
            buttonInserisci.Size = new Size(150, 30);
            buttonInserisci.TabIndex = 7;
            buttonInserisci.Text = "Inserisci utente";
            buttonInserisci.UseVisualStyleBackColor = true;
            buttonInserisci.Click += buttonInserisci_Click;
            //
            // buttonLogin
            //
            buttonLogin.Location = new Point(480, 226);
            buttonLogin.Name = "buttonLogin";
            buttonLogin.Size = new Size(150, 30);
            buttonLogin.TabIndex = 8;
            buttonLogin.Text = "Login";
            buttonLogin.UseVisualStyleBackColor = true;
            buttonLogin.Click += buttonLogin_Click;
            //
            // buttonChiudi
            //
            buttonChiudi.Location = new Point(640, 226);
            buttonChiudi.Name = "buttonChiudi";
            buttonChiudi.Size = new Size(132, 30);
            buttonChiudi.TabIndex = 9;
            buttonChiudi.Text = "Chiudi";
            buttonChiudi.UseVisualStyleBackColor = true;
            buttonChiudi.Click += buttonChiudi_Click;
            //
            // WindowsFormUtenti
            //
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(784, 340);
            Controls.Add(buttonChiudi);
            Controls.Add(buttonLogin);
            Controls.Add(buttonInserisci);
            Controls.Add(textBoxPassword);
            Controls.Add(textBoxNome);
            Controls.Add(textBoxCognome);
            Controls.Add(labelPassword);
            Controls.Add(labelNome);
            Controls.Add(labelCognome);
            Controls.Add(dataGridViewUtenti);
            Name = "WindowsFormUtenti";
            Text = "Utenti";
            ((System.ComponentModel.ISupportInitialize)dataGridViewUtenti).EndInit();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private DataGridView dataGridViewUtenti;
        private Label labelCognome;
        private Label labelNome;
        private Label labelPassword;
        private TextBox textBoxCognome;
        private TextBox textBoxNome;
        private TextBox textBoxPassword;
        private Button buttonInserisci;
        private Button buttonLogin;
        private Button buttonChiudi;
    }
}
