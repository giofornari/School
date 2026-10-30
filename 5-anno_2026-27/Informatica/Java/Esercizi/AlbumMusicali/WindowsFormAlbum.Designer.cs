using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;

namespace AlbumMusicali
{
    partial class WindowsFormAlbum
    {
        private IContainer components = null;
        private ComboBox cmbCategoria;
        private DataGridView dgvAlbum;
        private DataGridView dgvBrani;
        private Button btnVisualizza;
        private Button btnCalcola;
        private Label lblCategoria;
        private Label lblAlbum;
        private Label lblBrani;
        private Label lblRisultato;

        protected override void Dispose(bool disposing)
        {
            if (disposing && components != null)
                components.Dispose();
            base.Dispose(disposing);
        }

        private void InitializeComponent()
        {
            cmbCategoria = new ComboBox();
            dgvAlbum = new DataGridView();
            dgvBrani = new DataGridView();
            btnVisualizza = new Button();
            btnCalcola = new Button();
            lblCategoria = new Label();
            lblAlbum = new Label();
            lblBrani = new Label();
            lblRisultato = new Label();
            ((ISupportInitialize)dgvAlbum).BeginInit();
            ((ISupportInitialize)dgvBrani).BeginInit();
            SuspendLayout();

            lblCategoria.AutoSize = true;
            lblCategoria.Location = new Point(20, 23);
            lblCategoria.Text = "Categoria:";
            cmbCategoria.DropDownStyle = ComboBoxStyle.DropDownList;
            cmbCategoria.Items.AddRange(new object[] { "rock", "classica", "jazz", "pop" });
            cmbCategoria.Location = new Point(90, 20);
            cmbCategoria.Size = new Size(150, 23);
            cmbCategoria.Name = "cmbCategoria";
            btnVisualizza.Location = new Point(255, 18);
            btnVisualizza.Size = new Size(130, 28);
            btnVisualizza.Text = "Visualizza album";
            btnVisualizza.Name = "btnVisualizza";
            btnVisualizza.Click += btnVisualizza_Click;
            lblAlbum.AutoSize = true;
            lblAlbum.Location = new Point(20, 62);
            lblAlbum.Text = "Album";
            dgvAlbum.Location = new Point(20, 82);
            dgvAlbum.Size = new Size(760, 180);
            dgvAlbum.Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right;
            dgvAlbum.Name = "dgvAlbum";
            dgvAlbum.ReadOnly = true;
            dgvAlbum.AllowUserToAddRows = false;
            dgvAlbum.AllowUserToDeleteRows = false;
            dgvAlbum.MultiSelect = false;
            dgvAlbum.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
            dgvAlbum.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
            dgvAlbum.SelectionChanged += dgvAlbum_SelectionChanged;
            btnCalcola.Location = new Point(20, 275);
            btnCalcola.Size = new Size(150, 28);
            btnCalcola.Text = "Calcola statistiche";
            btnCalcola.Name = "btnCalcola";
            btnCalcola.Click += btnCalcola_Click;
            lblRisultato.AutoSize = true;
            lblRisultato.Location = new Point(180, 281);
            lblRisultato.Name = "lblRisultato";
            lblBrani.AutoSize = true;
            lblBrani.Location = new Point(20, 325);
            lblBrani.Text = "Brani dell'album selezionato";
            dgvBrani.Location = new Point(20, 345);
            dgvBrani.Size = new Size(760, 180);
            dgvBrani.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
            dgvBrani.Name = "dgvBrani";
            dgvBrani.ReadOnly = true;
            dgvBrani.AllowUserToAddRows = false;
            dgvBrani.AllowUserToDeleteRows = false;
            dgvBrani.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;

            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(800, 545);
            MinimumSize = new Size(650, 500);
            Controls.Add(lblCategoria);
            Controls.Add(cmbCategoria);
            Controls.Add(btnVisualizza);
            Controls.Add(lblAlbum);
            Controls.Add(dgvAlbum);
            Controls.Add(btnCalcola);
            Controls.Add(lblRisultato);
            Controls.Add(lblBrani);
            Controls.Add(dgvBrani);
            Name = "WindowsFormAlbum";
            StartPosition = FormStartPosition.CenterScreen;
            Text = "Album musicali";
            ((ISupportInitialize)dgvAlbum).EndInit();
            ((ISupportInitialize)dgvBrani).EndInit();
            ResumeLayout(false);
            PerformLayout();
        }
    }
}
