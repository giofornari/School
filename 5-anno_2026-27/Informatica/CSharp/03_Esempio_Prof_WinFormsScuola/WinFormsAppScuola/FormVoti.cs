using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using WinFormsLibraryScuola;

namespace WinFormsAppScuola
{
    public partial class FormVoti : Form
    {
        List<Object> voti;
        public FormVoti(List<Object> l, Studente s)
        {
            InitializeComponent();
            voti = l;
            labelStudente.Text = s.Cognome + " " + s.Nome;
            dataGridViewVoti.DataSource = voti;
        }

        private void buttonChiudi_Click(object sender, EventArgs e)
        {
            Close();
        }
    }
}
