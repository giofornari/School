namespace WinFormsAppScuola
{
    partial class FormVoti
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
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
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            dataGridViewVoti = new DataGridView();
            buttonChiudi = new Button();
            label1 = new Label();
            labelStudente = new Label();
            ((System.ComponentModel.ISupportInitialize)dataGridViewVoti).BeginInit();
            SuspendLayout();
            // 
            // dataGridViewVoti
            // 
            dataGridViewVoti.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dataGridViewVoti.Location = new Point(25, 72);
            dataGridViewVoti.Name = "dataGridViewVoti";
            dataGridViewVoti.RowHeadersWidth = 51;
            dataGridViewVoti.Size = new Size(486, 218);
            dataGridViewVoti.TabIndex = 0;
            // 
            // buttonChiudi
            // 
            buttonChiudi.ForeColor = Color.Brown;
            buttonChiudi.Location = new Point(12, 12);
            buttonChiudi.Name = "buttonChiudi";
            buttonChiudi.Size = new Size(94, 29);
            buttonChiudi.TabIndex = 1;
            buttonChiudi.Text = "Chiudi";
            buttonChiudi.UseVisualStyleBackColor = true;
            buttonChiudi.Click += buttonChiudi_Click;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Location = new Point(136, 16);
            label1.Name = "label1";
            label1.Size = new Size(138, 20);
            label1.TabIndex = 2;
            label1.Text = "Voti delllo studente";
            // 
            // labelStudente
            // 
            labelStudente.AutoSize = true;
            labelStudente.Font = new Font("Segoe UI", 12F, FontStyle.Bold | FontStyle.Italic, GraphicsUnit.Point, 0);
            labelStudente.Location = new Point(293, 10);
            labelStudente.Name = "labelStudente";
            labelStudente.Size = new Size(70, 28);
            labelStudente.TabIndex = 3;
            labelStudente.Text = "label2";
            // 
            // FormVoti
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(528, 319);
            Controls.Add(labelStudente);
            Controls.Add(label1);
            Controls.Add(buttonChiudi);
            Controls.Add(dataGridViewVoti);
            Name = "FormVoti";
            Text = "Voti";
            ((System.ComponentModel.ISupportInitialize)dataGridViewVoti).EndInit();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private DataGridView dataGridViewVoti;
        private Button buttonChiudi;
        private Label label1;
        private Label labelStudente;
    }
}