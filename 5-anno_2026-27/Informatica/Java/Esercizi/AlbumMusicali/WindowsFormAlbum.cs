using System;
using System.Data;
using System.Windows.Forms;

namespace AlbumMusicali
{
    public partial class WindowsFormAlbum : Form
    {
        private readonly Dati dati = new Dati();
        private DataTable albumVisualizzati;

        public WindowsFormAlbum()
        {
            InitializeComponent();
            cmbCategoria.SelectedIndex = 0;
        }

        private void btnVisualizza_Click(object sender, EventArgs e)
        {
            albumVisualizzati = dati.AlbumDiCategoria(cmbCategoria.Text);
            dgvAlbum.DataSource = albumVisualizzati;
            lblRisultato.Text = "";
            MostraBrani();
        }

        private void btnCalcola_Click(object sender, EventArgs e)
        {
            if (albumVisualizzati == null || albumVisualizzati.Rows.Count == 0)
            {
                lblRisultato.Text = "Visualizza prima gli album di una categoria.";
                return;
            }

            lblRisultato.Text = "Album più vecchio: " + dati.TitoloAlbumPiuVecchio(albumVisualizzati)
                + "  |  Durata media: " + dati.MediaDurata(albumVisualizzati).ToString("0.##") + " minuti";
        }

        private void dgvAlbum_SelectionChanged(object sender, EventArgs e)
        {
            MostraBrani();
        }

        private void MostraBrani()
        {
            if (dgvAlbum.CurrentRow == null || dgvAlbum.CurrentRow.DataBoundItem == null)
            {
                dgvBrani.DataSource = null;
                return;
            }

            DataRowView riga = (DataRowView)dgvAlbum.CurrentRow.DataBoundItem;
            dgvBrani.DataSource = dati.BraniAlbum((int)riga["ID"]);
        }
    }
}
