// "Top-level statements": niente class Program / static void Main,
// il compilatore lo genera da solo. È il template di default di .NET 10.
using ParcoVeicoli;

Flotta flotta = new Flotta();
int scelta;

do
{
    Console.WriteLine();
    Console.WriteLine("=== GESTIONE PARCO VEICOLI ===");
    Console.WriteLine("1. Inserisci auto");
    Console.WriteLine("2. Inserisci camion");
    Console.WriteLine("3. Visualizza flotta");
    Console.WriteLine("4. Costo totale manutenzione");
    Console.WriteLine("5. Esci");
    Console.Write("Scelta: ");

    // se l'input non è un numero, TryParse mette 0 in scelta (-> "Scelta non valida")
    int.TryParse(Console.ReadLine(), out scelta);

    switch (scelta)
    {
        // due case attaccati senza codice in mezzo = stesso blocco (dati comuni)
        case 1:
        case 2:
            Console.Write("Targa: ");
            string targa = Console.ReadLine() ?? "";   // ?? "": se ReadLine dà null usa ""
            Console.Write("Marca: ");
            string marca = Console.ReadLine() ?? "";
            Console.Write("Modello: ");
            string modello = Console.ReadLine() ?? "";
            Console.Write("Km percorsi: ");
            double km = Convert.ToDouble(Console.ReadLine());

            if (scelta == 1)
            {
                Console.Write("Numero porte: ");
                int porte = Convert.ToInt32(Console.ReadLine());
                flotta.AggiungiVeicolo(new Auto(targa, marca, modello, km, porte));
            }
            else
            {
                Console.Write("Capacità di carico (t): ");
                double carico = Convert.ToDouble(Console.ReadLine());
                flotta.AggiungiVeicolo(new Camion(targa, marca, modello, km, carico));
            }
            Console.WriteLine("Veicolo inserito.");
            break;

        case 3:
            flotta.VisualizzaFlotta();
            break;

        case 4:
            // :F2 = due cifre decimali (come %.2f in Java)
            Console.WriteLine($"Costo totale manutenzione: {flotta.CalcolaCostoTotaleManutenzione():F2} euro");
            break;

        case 5:
            Console.WriteLine("Uscita dal programma.");
            break;

        default:
            Console.WriteLine("Scelta non valida.");
            break;
    }
} while (scelta != 5);
