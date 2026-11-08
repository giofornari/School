using System.Data;

namespace OrdiniWinForms;

public class Dati
{
    static List<Ordine> lo = Ordine.GetSampleData();
    static List<Articolo> la = Articolo.GetSampleData();

    public DataTable GetOrdini()
    {
        DataTable dt = new DataTable();
        dt.Columns.Add("idOrdine", typeof(int));
        dt.Columns.Add("idCliente", typeof(int));
        dt.Columns.Add("data", typeof(string));
        foreach (Ordine o in lo)
        {
            dt.Rows.Add(o.id, o.idc, o.data);
        }
        return dt;
    }

    public DataTable GetArticoli()
    {
        DataTable dt = new DataTable();
        dt.Columns.Add("nomeArticolo", typeof(string));
        dt.Columns.Add("idOrdine", typeof(int));
        dt.Columns.Add("importo", typeof(double));
        foreach (Articolo a in la)
        {
            dt.Rows.Add(a.nome, a.ido, a.imp);
        }
        return dt;
    }

    public DataTable ArticoliPerOrdine(int ido)
    {
        DataTable dt = GetArticoli().Clone();
        foreach (Articolo a in la)
        {
            if (a.ido == ido)
            {
                dt.Rows.Add(a.nome, a.ido, a.imp);
            }
        }
        return dt;
    }

    public double Somma(int ido)
    {
        double s = 0;
        foreach (Articolo a in la)
        {
            if (a.ido == ido)
            {
                s += a.imp;
            }
        }
        return s;
    }

    public double Media(int ido)
    {
        double s = 0;
        int n = 0;
        foreach (Articolo a in la)
        {
            if (a.ido == ido)
            {
                s += a.imp;
                n++;
            }
        }
        if (n == 0)
        {
            return 0;
        }
        return s / n;
    }

    public void AddArticolo(string nome, int ido, double imp)
    {
        la.Add(new Articolo(nome, ido, imp));
    }
}
