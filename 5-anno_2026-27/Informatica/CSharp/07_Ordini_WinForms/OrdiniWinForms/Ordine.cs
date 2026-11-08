namespace OrdiniWinForms;

public class Ordine
{
    public int id;
    public int idc;
    public string data;

    public Ordine(int id, int idc, string data)
    {
        this.id = id;
        this.idc = idc;
        this.data = data;
    }

    public static List<Ordine> GetSampleData()
    {
        List<Ordine> l = new List<Ordine>();
        l.Add(new Ordine(2012, 1210, "12/12/2020"));
        l.Add(new Ordine(9020, 801, "01/04/2021"));
        l.Add(new Ordine(3340, 651, "12/06/2021"));
        return l;
    }
}
