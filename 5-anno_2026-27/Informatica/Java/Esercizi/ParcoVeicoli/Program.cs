using System;

namespace ParcoVeicoli
{
    class Program
    {
        static void Main(string[] args)
        {
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
                // input non num -> 0 (non valida)
                int.TryParse(Console.ReadLine(), out scelta);

                switch (scelta)
                {
                    case 1:
                    case 2:
                        // dati comuni
                        Console.Write("Targa: ");
                        string targa = Console.ReadLine();
                        Console.Write("Marca: ");
                        string marca = Console.ReadLine();
                        Console.Write("Modello: ");
                        string modello = Console.ReadLine();
                        Console.Write("Km percorsi: ");
                        double km = double.Parse(Console.ReadLine());

                        if (scelta == 1)
                        {
                            Console.Write("Numero porte: ");
                            int porte = int.Parse(Console.ReadLine());
                            flotta.AggiungiVeicolo(new Auto(targa, marca, modello, km, porte));
                        }
                        else
                        {
                            Console.Write("Capacità carico (t): ");
                            double carico = double.Parse(Console.ReadLine());
                            flotta.AggiungiVeicolo(new Camion(targa, marca, modello, km, carico));
                        }
                        Console.WriteLine("Veicolo inserito.");
                        break;

                    case 3:
                        flotta.VisualizzaFlotta();
                        break;

                    case 4:
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
        }
    }
}
