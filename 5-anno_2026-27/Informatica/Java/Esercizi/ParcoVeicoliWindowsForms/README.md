# Parco Veicoli — Windows Forms

Versione Windows Forms dell'esercizio C# già presente in `../ParcoVeicoli`.

## Avvio su Windows

1. Installa Visual Studio con il carico di lavoro **Sviluppo di applicazioni desktop .NET** e l'SDK .NET 8.
2. Apri `../ParcoVeicoli.sln`.
3. Imposta `ParcoVeicoliWindowsForms` come progetto di avvio e premi **F5**.

Con il solo SDK .NET 8, dalla radice del repository:

```powershell
dotnet run --project Esercizi/ParcoVeicoliWindowsForms
```

L'applicazione richiede Windows. `EnableWindowsTargeting` permette di compilarla da Linux, ma non di eseguirla su Linux.

## Uso

- Scegli Auto o Camion e compila targa, marca, modello e chilometri percorsi.
- Per le auto è attivo il numero di porte; per i camion la capacità di carico in tonnellate.
- **Inserisci** aggiunge il mezzo, aggiorna tabella e totale, poi pulisce i campi.
- **Visualizza flotta** aggiorna l'elenco; **Calcola manutenzione** ricalcola il totale.
- Selezionando una riga si vedono i dettagli ottenuti da `StampaDettagli()`.
- **Pulisci campi** svuota solo il modulo; **Esci** chiude l'applicazione.

I valori monetari usano il formato italiano. I campi di testo sono obbligatori: gli spazi iniziali e finali vengono rimossi e la targa viene convertita in maiuscolo. I controlli numerici accettano km da 0 a 1.000.000.000, porte da 1 a 99 e carico da 0,01 a 1.000.000 t; km e carico hanno due cifre decimali. Sono limiti della GUI, non nuove regole del modello originale. Le targhe duplicate sono ammesse, come nella console.

La flotta resta in memoria fino alla chiusura: il compito non richiede salvataggio su file, modifica o eliminazione dei veicoli.

## Separazione tra interfaccia e logica

| File | Responsabilità |
|---|---|
| `../ParcoVeicoli/Veicolo.cs`, `Auto.cs`, `Camion.cs` | Modello originale, ereditarietà e costi, senza modifiche |
| `../ParcoVeicoli/Flotta.cs` | Lista privata, inserimento, dettagli e somma dei costi |
| `MainForm.cs` | Gestori degli eventi, controlli di input e aggiornamento della GUI |
| `MainForm.Designer.cs` | Creazione dei controlli e layout, definito in codice |
| `Program.cs` | Avvio della finestra, cultura italiana e impostazioni grafiche |

Il progetto GUI include i quattro sorgenti del modello tramite collegamenti `Compile`: non contiene copie delle classi né delle formule. Il layout è costruito in codice; per cambiarlo si modifica `MainForm.Designer.cs`.

`Flotta.VisualizzaFlotta()` ora restituisce un elenco di stringhe e non usa `Console.WriteLine`. Il programma console stampa questo risultato e gestisce il messaggio della flotta vuota. La GUI legge la vista della lista in sola lettura e richiama gli stessi metodi polimorfici; la lista non può essere svuotata o modificata dall'esterno.

| Classe | Costo manutenzione originale |
|---|---|
| `Veicolo` | km × 0,05 € |
| `Auto` | km × 0,05 € + 100 € |
| `Camion` | km × 0,15 € + capacità in t × 50 € |

## Verifiche

Dalla radice del repository:

```powershell
dotnet build Esercizi/ParcoVeicoli.sln --configuration Release
dotnet run --project Esercizi/ParcoVeicoli.Verifiche
```

Il progetto di verifica non usa pacchetti esterni. Su Linux verifica 17 casi del modello e della flotta. Su Windows esegue anche 15 controlli dell'interfaccia, aprendo brevemente la finestra: campi obbligatori, cambio tipo, inserimenti, costi, dettagli del veicolo selezionato, pulizia dei campi, aggiornamento e uscita. Un errore interrompe l'esecuzione con un'eccezione.

Esempio da provare anche manualmente:

| Mezzo | Km | Dato specifico | Costo atteso |
|---|---:|---|---:|
| Auto Fiat Panda | 10.000 | 5 porte | 600,00 € |
| Camion Iveco Daily | 20.000 | 10 t | 3.500,00 € |
| Totale | | | **4.100,00 €** |

Prima della consegna, eseguire su Windows le verifiche e controllare il ridimensionamento della finestra con lo zoom dello schermo utilizzato.

## Requisiti verificati

- Notifica scolastica dell'8 ottobre 2026: riscrivere l'esercizio del Parco Veicoli Aziende con Windows Form, consegna 12 ottobre.
- Notifica del compito originale del 24 settembre: proprietà, ereditarietà, `List<Veicolo>`, polimorfismo, inserimento, visualizzazione, manutenzione totale e uscita.
- Repository controllato sul commit `18ff71b6df667862adc8f8109727826e16463ee7`, del 27 settembre 2026: presente soltanto la versione console. Anche il branch della flotta contiene gli stessi sorgenti.
- La pagina Classroom richiede un nuovo accesso: eventuali commenti, allegati o modifiche successivi alle notifiche non sono stati verificati.

Fonti: [compito Windows Forms](https://classroom.google.com/c/NzE3NTQ0MTk0NDA2/a/ODg5OTEyNzQ1ODcx/details), [esercizio originale](https://classroom.google.com/c/NzE3NTQ0MTk0NDA2/a/ODg3MDM0Nzk3NDc3/details), [repository](https://github.com/bigBrodyG/JavaProjects/tree/main/Esercizi/ParcoVeicoli), [compilazione da Linux](https://learn.microsoft.com/en-us/dotnet/core/project-sdk/msbuild-props#enablewindowstargeting).
