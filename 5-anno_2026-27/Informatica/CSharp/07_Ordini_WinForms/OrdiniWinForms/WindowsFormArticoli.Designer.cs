namespace OrdiniWinForms
{
    partial class WindowsFormArticoli
    {
        private System.ComponentModel.IContainer components = null;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        private void InitializeComponent()
        {
            dg1 = new DataGridView();
            b1 = new Button();
            l1 = new Label();
            t1 = new TextBox();
            t2 = new TextBox();
            b2 = new Button();
            ((System.ComponentModel.ISupportInitialize)dg1).BeginInit();
            SuspendLayout();
            //
            // dg1
            //
            dg1.AllowUserToAddRows = false;
            dg1.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dg1.Location = new Point(12, 12);
            dg1.Name = "dg1";
            dg1.ReadOnly = true;
            dg1.RowHeadersWidth = 51;
            dg1.Size = new Size(460, 150);
            dg1.TabIndex = 0;
            //
            // b1
            //
            b1.Location = new Point(12, 175);
            b1.Name = "b1";
            b1.Size = new Size(130, 30);
            b1.TabIndex = 1;
            b1.Text = "somma e media";
            b1.UseVisualStyleBackColor = true;
            b1.Click += b1_Click;
            //
            // l1
            //
            l1.AutoSize = true;
            l1.Location = new Point(160, 181);
            l1.Name = "l1";
            l1.Size = new Size(0, 20);
            l1.TabIndex = 2;
            //
            // t1
            //
            t1.Location = new Point(12, 220);
            t1.Name = "t1";
            t1.Size = new Size(150, 27);
            t1.TabIndex = 3;
            //
            // t2
            //
            t2.Location = new Point(170, 220);
            t2.Name = "t2";
            t2.Size = new Size(80, 27);
            t2.TabIndex = 4;
            //
            // b2
            //
            b2.Location = new Point(260, 218);
            b2.Name = "b2";
            b2.Size = new Size(100, 30);
            b2.TabIndex = 5;
            b2.Text = "aggiungi";
            b2.UseVisualStyleBackColor = true;
            b2.Click += b2_Click;
            //
            // WindowsFormArticoli
            //
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(484, 261);
            Controls.Add(dg1);
            Controls.Add(b1);
            Controls.Add(l1);
            Controls.Add(t1);
            Controls.Add(t2);
            Controls.Add(b2);
            Name = "WindowsFormArticoli";
            Text = "Articoli";
            ((System.ComponentModel.ISupportInitialize)dg1).EndInit();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private DataGridView dg1;
        private Button b1;
        private Label l1;
        private TextBox t1;
        private TextBox t2;
        private Button b2;
    }
}
