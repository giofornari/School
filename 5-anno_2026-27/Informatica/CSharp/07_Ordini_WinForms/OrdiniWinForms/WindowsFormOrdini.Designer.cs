namespace OrdiniWinForms
{
    partial class WindowsFormOrdini
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
            dg1.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
            dg1.Size = new Size(420, 200);
            dg1.TabIndex = 0;
            dg1.CellClick += dg1_CellClick;
            //
            // WindowsFormOrdini
            //
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(444, 224);
            Controls.Add(dg1);
            Name = "WindowsFormOrdini";
            Text = "Ordini";
            Load += WindowsFormOrdini_Load;
            ((System.ComponentModel.ISupportInitialize)dg1).EndInit();
            ResumeLayout(false);
        }

        #endregion

        private DataGridView dg1;
    }
}
