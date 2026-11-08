namespace OrdiniWinForms;

public partial class WindowsFormArticoli : Form
{
    int ido;
    Dati d;

    public WindowsFormArticoli(int ido, Dati d)
    {
        InitializeComponent();
        this.ido = ido;
        this.d = d;
        dg1.DataSource = d.ArticoliPerOrdine(ido);
    }

    private void b1_Click(object sender, EventArgs e)
    {
        l1.Text = "somma: " + d.Somma(ido) + " media: " + d.Media(ido);
    }

    private void b2_Click(object sender, EventArgs e)
    {
        d.AddArticolo(t1.Text, ido, double.Parse(t2.Text));
        dg1.DataSource = d.ArticoliPerOrdine(ido);
    }
}
