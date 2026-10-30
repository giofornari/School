using Biblioteca;

Catalogo catalogo = new Catalogo();
int scelta;

do
{
    Console.WriteLine();
    Console.WriteLine("=== BIBLIOTECA SCOLASTICA ===");
    Console.WriteLine("1. Inserisci libro");
    Console.WriteLine("2. Inserisci audiolibro");
    Console.WriteLine("3. Visualizza catalogo");
    Console.WriteLine("4. Penale totale");
    Console.WriteLine("5. Esci");
    Console.Write("Scelta: ");
    int.TryParse(Console.ReadLine(), out scelta);

    switch (scelta)
    {
        case 1:
        case 2:
            Console.Write("Codice: ");
            string codice = Console.ReadLine() ?? "";
            Console.Write("Titolo: ");
            string titolo = Console.ReadLine() ?? "";
            Console.Write("Autore: ");
            string autore = Console.ReadLine() ?? "";
            Console.Write("Giorni di prestito: ");
            int giorni = Convert.ToInt32(Console.ReadLine());

            if (scelta == 1)
            {
                Console.Write("Numero pagine: ");
                int pagine = Convert.ToInt32(Console.ReadLine());
                catalogo.AggiungiRisorsa(new Libro(codice, titolo, autore, giorni, pagine));
            }
            else
            {
                Console.Write("Durata (minuti): ");
                int minuti = Convert.ToInt32(Console.ReadLine());
                catalogo.AggiungiRisorsa(new Audiolibro(codice, titolo, autore, giorni, minuti));
            }
            Console.WriteLine("Risorsa inserita.");
            break;

        case 3:
            catalogo.VisualizzaCatalogo();
            break;

        case 4:
            Console.WriteLine($"Penale totale: {catalogo.CalcolaPenaleTotale():F2} euro");
            break;

        case 5:
            Console.WriteLine("Uscita dal programma.");
            break;

        default:
            Console.WriteLine("Scelta non valida.");
            break;
    }
} while (scelta != 5);
