namespace OrdiniWinForms;

public class Articolo
{
    public string nome;
    public int ido;
    public double imp;

    public Articolo(string nome, int ido, double imp)
    {
        this.nome = nome;
        this.ido = ido;
        this.imp = imp;
    }

    public static List<Articolo> GetSampleData()
    {
        List<Articolo> l = new List<Articolo>();
        l.Add(new Articolo("Iphone 15", 2012, 1200.20));
        l.Add(new Articolo("PC Macbook pro xled 14", 2012, 230.45));
        l.Add(new Articolo("PC thikpad carbon x1 gen 14", 9020, 320.50));
        l.Add(new Articolo("mic to talk with claude (not optional)", 3340, 31.00));
        return l;
    }
}
