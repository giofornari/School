namespace UtentiWinForms
{
    partial class WindowFormLogin
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
            labelUser = new Label();
            labelPassword = new Label();
            textBoxUser = new TextBox();
            textBoxPassword = new TextBox();
            buttonAccedi = new Button();
            labelRisultato = new Label();
            SuspendLayout();
            //
            // labelUser
            //
            labelUser.AutoSize = true;
            labelUser.Location = new Point(12, 15);
            labelUser.Name = "labelUser";
            labelUser.Size = new Size(38, 20);
            labelUser.TabIndex = 0;
            labelUser.Text = "User";
            //
            // labelPassword
            //
            labelPassword.AutoSize = true;
            labelPassword.Location = new Point(12, 49);
            labelPassword.Name = "labelPassword";
            labelPassword.Size = new Size(70, 20);
            labelPassword.TabIndex = 2;
            labelPassword.Text = "Password";
            //
            // textBoxUser
            //
            textBoxUser.Location = new Point(100, 12);
            textBoxUser.Name = "textBoxUser";
            textBoxUser.Size = new Size(240, 27);
            textBoxUser.TabIndex = 1;
            //
            // textBoxPassword
            //
            textBoxPassword.Location = new Point(100, 46);
            textBoxPassword.Name = "textBoxPassword";
            textBoxPassword.Size = new Size(240, 27);
            textBoxPassword.TabIndex = 3;
            textBoxPassword.UseSystemPasswordChar = true;
            //
            // buttonAccedi
            //
            buttonAccedi.Location = new Point(100, 82);
            buttonAccedi.Name = "buttonAccedi";
            buttonAccedi.Size = new Size(120, 30);
            buttonAccedi.TabIndex = 4;
            buttonAccedi.Text = "Accedi";
            buttonAccedi.UseVisualStyleBackColor = true;
            buttonAccedi.Click += buttonAccedi_Click;
            //
            // labelRisultato
            //
            labelRisultato.AutoSize = true;
            labelRisultato.Location = new Point(12, 125);
            labelRisultato.Name = "labelRisultato";
            labelRisultato.Size = new Size(0, 20);
            labelRisultato.TabIndex = 5;
            //
            // WindowFormLogin
            //
            AcceptButton = buttonAccedi;
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(360, 200);
            Controls.Add(labelRisultato);
            Controls.Add(buttonAccedi);
            Controls.Add(textBoxPassword);
            Controls.Add(textBoxUser);
            Controls.Add(labelPassword);
            Controls.Add(labelUser);
            Name = "WindowFormLogin";
            Text = "Login";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Label labelUser;
        private Label labelPassword;
        private TextBox textBoxUser;
        private TextBox textBoxPassword;
        private Button buttonAccedi;
        private Label labelRisultato;
    }
}
