using System;
using System.Globalization;
using System.Windows.Forms;

namespace ParcoVeicoli
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("it-IT");
            CultureInfo.CurrentUICulture = CultureInfo.GetCultureInfo("it-IT");
            Application.SetHighDpiMode(HighDpiMode.SystemAware);
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new MainForm());
        }
    }
}
