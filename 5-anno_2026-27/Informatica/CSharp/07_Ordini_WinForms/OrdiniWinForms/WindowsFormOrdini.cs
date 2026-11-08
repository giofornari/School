namespace OrdiniWinForms;

public partial class WindowsFormOrdini : Form
{
    Dati d = new Dati();

    public WindowsFormOrdini()
    {
        InitializeComponent();
    }

    private void WindowsFormOrdini_Load(object sender, EventArgs e)
    {
        dg1.DataSource = d.GetOrdini();
    }

    private void dg1_CellClick(object sender, DataGridViewCellEventArgs e)
    {
        if (e.RowIndex >= 0)
        {
            int ido = int.Parse(dg1.Rows[e.RowIndex].Cells[0].Value.ToString());
            WindowsFormArticoli f = new WindowsFormArticoli(ido, d);
            f.ShowDialog();
        }
    }
}
