# C# per la verifica: da Java a C#, console e Windows Forms

Ordine di studio, dal più semplice al più complesso:

| # | Cartella | Cosa è | Gira su Linux? |
|---|---|---|---|
| 1 | `01_ParcoVeicoli_Console` | Esercizio del 24/09, console | sì |
| 2 | `02_Biblioteca_Console` | Stesso schema, nomi diversi: è il tuo **allenamento** | sì |
| 3 | `03_Esempio_Prof_WinFormsScuola` | Codice del prof (dallo zip), da **leggere** | compila soltanto |
| 4 | `04_ParcoVeicoli_WinForms` | Esercizio 1 in grafica, stile prof | compila soltanto |
| 5 | `05_Biblioteca_WinForms` | Esercizio 2 in grafica | compila soltanto |
| 6 | `06_Utenti_WinForms` | Compito DataTable + DataGridView + login | compila soltanto |

Domani c'è la console: se sai scrivere la 1 e la 2 a memoria sei a posto. I punti dal 3 al 5 servono per la parte grafica.

---

## 0. Ambiente

### Linux (adesso)

Il .NET 10 SDK è già installato e in VS Code ho aggiunto l'estensione `ms-dotnettools.csharp`, che dà suggerimenti ed errori in tempo reale.

```bash
dotnet run --project 01_ParcoVeicoli_Console/ParcoVeicoli    # compila ed esegue
dotnet build 04_ParcoVeicoli_WinForms/ParcoVeicoliWinForms.slnx   # solo compilazione
dotnet new console -n Prova      # nuovo progetto console (come "Nuovo progetto" in VS)
```

I progetti Windows Forms **compilano** su Linux grazie a `Directory.Build.props` (`EnableWindowsTargeting`), ma **non si avviano**: WinForms esiste solo su Windows. Per vederli girare hai tre strade:
- PC della scuola, con Visual Studio: è quello che userai in verifica;
- una VM Windows sul tuo Proxmox: è la soluzione migliore per esercitarsi a casa;
- Wine: con WinForms su .NET 10 non è affidabile, lascialo perdere.

### Windows + Visual Studio 2026 (in verifica)

Il prof usa VS 2026: la cartella `.vs/v18` e il formato `.slnx` lo confermano.

| Azione | Come |
|---|---|
| Nuova console | File → Nuovo → Progetto → **App console** → .NET 10 |
| Nuova app grafica | **App Windows Forms** → .NET 10 |
| Libreria del modello | tasto destro sulla soluzione → Aggiungi → Nuovo progetto → **Libreria di classi Windows Forms** |
| Collegare la libreria | tasto destro su *Dipendenze* del progetto app → **Aggiungi riferimento al progetto** → spunta la libreria |
| Nuova classe | tasto destro sul progetto → Aggiungi → Classe (Shift+Alt+C) |
| Avvio | F5 (con debug), Ctrl+F5 (senza) |
| Progetto che parte | tasto destro → **Imposta come progetto di avvio** |

Scorciatoie che fanno risparmiare minuti:
- `prop` + Tab Tab crea una proprietà;
- `ctor` + Tab Tab crea un costruttore;
- `Ctrl+.` sul nome della classe → *Genera costruttore*;
- scrivendo `override ` e uno spazio, VS elenca i metodi che puoi ridefinire e scrive lui la firma.

---

## 1. Java → C#: cosa cambia

Le idee di OOP le conosci già: ereditarietà, override, liste e polimorfismo restano uguali. Cambia la sintassi, e soprattutto **una regola** (vedi 1.1).

| Java | C# |
|---|---|
| `class Auto extends Veicolo` | `class Auto : Veicolo` |
| `implements I` | `: I` (stesso simbolo, separato da virgole) |
| `super(a, b)` dentro il costruttore | `: base(a, b)` **dopo** la firma del costruttore |
| `super.metodo()` | `base.Metodo()` |
| `@Override` facoltativo | `override` **obbligatorio**, e nella base serve `virtual` |
| `getTarga()` / `setTarga()` | proprietà `Targa { get; set; }` |
| `ArrayList<Veicolo>` | `List<Veicolo>` |
| `.size()`, `.get(i)` | `.Count`, `[i]` |
| `for (Veicolo v : lista)` | `foreach (Veicolo v in lista)` |
| `System.out.println` | `Console.WriteLine` |
| `new Scanner(System.in).nextLine()` | `Console.ReadLine()` |
| `Integer.parseInt(s)` | `int.Parse(s)` / `Convert.ToInt32(s)` |
| `String.format("%.2f", x)` | `$"{x:F2}"` (stringa interpolata) |
| `boolean`, `String` | `bool`, `string` |
| `s1.equals(s2)` | `s1 == s2` (con le stringhe confronta il contenuto) |
| `if (v instanceof Auto) { Auto a = (Auto) v; }` | `if (v is Auto a) { ... }` |
| `toString()` | `public override string ToString()` |
| `package` / `import` | `namespace` / `using` |
| lambda `x -> x * 2` | `x => x * 2` |
| Stream `filter / map / sum` | LINQ `Where / Select / Sum` |
| metodi in camelCase | metodi e proprietà in **PascalCase** (`StampaDettagli`) |

### 1.1 La regola più importante: `virtual` + `override`

In Java ogni metodo è "ridefinibile" per default. **In C# no.** Perché il polimorfismo funzioni devi scrivere:
- nella classe base, `public virtual string StampaDettagli()`;
- nella derivata, `public override string StampaDettagli()`.

Se ne dimentichi uno:

| Errore | Cosa succede |
|---|---|
| `override` senza `virtual` nella base | **CS0506** "cannot override … not marked virtual", non compila |
| `virtual` nella base, ma nella figlia manca `override` | warning **CS0114** "hides inherited member": compila, ma **il polimorfismo non funziona** |
| `override` con un nome scritto male | **CS0115** "no suitable method found to override" |

L'ho provato davvero: con una `List<A>` che contiene un `B`, senza `virtual`/`override` il `foreach` stampa **"versione di A"**. È il bug più subdolo che può capitarti in verifica, perché il programma compila e sembra funzionare.

> Nel suo `ConsoleAppEredita` la tua compagna ha scritto che "per avere il binding dinamico come Java bisogna usare `dynamic`". **È sbagliato**: in C# il binding dinamico si ottiene con `virtual`/`override`. `dynamic` è un'altra cosa e non c'entra.

### 1.2 `abstract`: classe astratta o metodo astratto?

La traccia dice "classe astratta (o normale)" e dà a `Veicolo` un costo **di base** (0,05 €/km). Quindi:
- la **classe** è `abstract`: non si può scrivere `new Veicolo(...)` (CS0144), si creano solo Auto e Camion;
- i **metodi** sono `virtual` e hanno un corpo, perché la traccia chiede "chiama il metodo della classe base".

La tua compagna invece ha reso **astratti i metodi** (`public abstract string StampaDettagli();`). In questo modo `base.StampaDettagli()` non si può chiamare (CS0205, verificato) e ogni figlia deve riscrivere a mano Targa, Marca e Modello. Compila, ma **non rispetta la traccia**. Usa la mia versione.

| | metodo `virtual` | metodo `abstract` |
|---|---|---|
| ha un corpo nella base? | sì | no (finisce con `;`) |
| la figlia deve ridefinirlo? | può | **deve** |
| `base.Metodo()` si può chiamare? | sì | no |
| può stare in una classe non astratta? | sì | no |

### 1.3 Proprietà: forma corta e forma del prof

Le due forme qui sotto fanno **la stessa cosa**:

```csharp
// forma corta (proprietà automatica): l'ho usata io
public string Targa { get; set; }

// forma del prof e della compagna: attributo privato + proprietà
private string targa;
public string Targa { get => targa; set => targa = value; }
```

`value` è il valore che stai assegnando (`v.Targa = "AB123CD"` → `value` vale `"AB123CD"`). Dall'esterno si usa come un attributo: `v.Targa`, senza `get` né parentesi. In verifica vanno bene tutte e due. Quella corta è più veloce da scrivere e non genera warning (vedi 1.6).

Sola lettura: `public BindingList<Veicolo> Veicoli { get => veicoli; }` ha solo il `get`.

### 1.4 Costruttore della classe derivata

```csharp
public Auto(string targa, string marca, string modello, double km, int numeroPorte)
    : base(targa, marca, modello, km)     // = super(...) di Java, ma va QUI e non dentro le graffe
{
    NumeroPorte = numeroPorte;            // dentro le graffe va solo il campo nuovo
}
```

Se dimentichi `: base(...)` e la base non ha un costruttore vuoto ottieni **CS7036** "There is no argument given that corresponds to the required parameter". La compagna, dopo aver chiamato `base(...)`, riassegna di nuovo `this.Codice = codice`: è inutile, lo ha già fatto la base.

### 1.5 `Program.cs` senza `Main` (top-level statements)

Il template di .NET 10 crea un `Program.cs` **senza** `class Program` e senza `static void Main`: scrivi le istruzioni direttamente, e il `Main` lo genera il compilatore. Le regole sono due:
1. le istruzioni vanno **prima** di eventuali classi scritte nello stesso file;
2. se le classi stanno in un `namespace` (come le mie: `namespace ParcoVeicoli`), in cima serve `using ParcoVeicoli;`, altrimenti ottieni **CS0246** "type or namespace not found".

La forma classica funziona ugualmente:

```csharp
class Program
{
    static void Main(string[] args) { /* ... */ }
}
```

**In verifica**, se vuoi andare veloce puoi mettere tutto in `Program.cs`: prima il menu, sotto le classi. È quello che fa la compagna in `GestioneParcoVeicoliAziendali`. Un file per classe è più ordinato, ma non obbligatorio.

### 1.6 Warning gialli di nullability

I progetti hanno `<Nullable>enable</Nullable>`: il compilatore ti avvisa quando qualcosa *potrebbe* essere `null`. Sono **warning, non errori**: il programma parte comunque. Anche il codice del prof ne ha 10 (li ho visti compilandolo).

- `Console.ReadLine()` restituisce `string?` (cioè "stringa o null"). Per questo scrivo `Console.ReadLine() ?? ""`: se è null, usa `""`.
- `Veicolo?` vuol dire "un Veicolo, oppure null". `FirstOrDefault` restituisce proprio questo.
- `?.` chiama un membro solo se l'oggetto non è null: `v?.Targa`.

### 1.7 `switch`: niente "fall-through"

```csharp
case 1:              // due etichette attaccate SENZA codice in mezzo: ammesso
case 2:
    ...codice comune...
    break;           // obbligatorio alla fine di ogni case che contiene codice
```

- Se un `case` con del codice non finisce con `break` ottieni **CS0163** "Control cannot fall through". In Java invece si passa al case successivo senza errori.
- Tutto lo `switch` è **un unico blocco**: se dichiari `string targa` sia nel case 1 sia nel case 2 ottieni **CS0128** "already defined in this scope". Anche per questo i case 1 e 2 condividono la lettura dei dati comuni.

### 1.8 Leggere numeri: occhio alla virgola

| Metodo | Con `"abc"` | Con `null` |
|---|---|---|
| `int.Parse(s)` | eccezione | eccezione |
| `Convert.ToInt32(s)` | eccezione | restituisce 0 |
| `int.TryParse(s, out n)` | restituisce `false` e mette `n = 0` | come a sinistra |

Per il menu uso `TryParse`: un input sbagliato diventa 0 e finisce nel `default` ("Scelta non valida"). Per i dati uso `Convert`, come il prof.

`out n` vuol dire che il metodo scrive il risultato dentro `n`: così `TryParse` può restituire insieme un `bool` e il numero.

⚠️ **Separatore decimale.** `Convert.ToDouble` usa la lingua del sistema. L'ho provato:
- Windows in italiano: `"12,5"` → 12,5 ✔, mentre `"12.5"` → **125** (qui è il punto a fare da separatore delle migliaia);
- il tuo Linux (en_US): `"12,5"` → **125** (la virgola viene presa come separatore delle migliaia, senza nessun errore).

In verifica, sui PC della scuola, **i decimali si scrivono con la virgola**.

### 1.9 Formattazione

`$"Targa: {Targa} | Km: {ChilometriPercorsi}"` è come `"Targa: " + Targa + ...`. `{x:F2}` stampa due decimali. In console scrivo "euro" e non "€", perché la console di Windows a volte mostra `?` al posto del simbolo; nelle form invece "€" funziona.

---

## 2. Esercizio 1: Parco Veicoli (console)

**Ordine di scrittura in verifica:** `Veicolo` → `Auto` → `Camion` → `Flotta` → `Program`. Compila (Ctrl+Shift+B) dopo ogni classe, così gli errori arrivano uno alla volta.

### `Veicolo.cs`
- `abstract class`, quattro proprietà, un costruttore che le assegna.
- `virtual string StampaDettagli()` **restituisce** una stringa (la traccia dice "restituisce"), non stampa.
- `virtual double CalcolaCostoManutenzione()` → `ChilometriPercorsi * 0.05`.

### `Auto.cs`
- `: Veicolo`, aggiunge `NumeroPorte`, costruttore con `: base(...)`.
- `StampaDettagli()` → `base.StampaDettagli() + porte`: la traccia dice "chiama il metodo della classe base".
- Costo → `base.CalcolaCostoManutenzione() + 100`.

### `Camion.cs`
- Il costo **non** usa `base`, perché cambia la tariffa al km: `km * 0.15 + carico * 50`. Se scrivessi `base... + km * 0.10` il risultato sarebbe giusto, ma è contorto: scrivi la formula diretta.

### `Flotta.cs`
- `private List<Veicolo> veicoli = new List<Veicolo>();`: lista **privata**, come chiede la traccia.
- `VisualizzaFlotta()` cicla e stampa `v.StampaDettagli()`. **Questo è il polimorfismo**: `v` è dichiarato `Veicolo`, ma viene eseguita la versione di Auto o di Camion.
- `CalcolaCostoTotaleManutenzione()` usa un `foreach` con `totale +=`. In alternativa, con LINQ: `return veicoli.Sum(v => v.CalcolaCostoManutenzione());`.

### `Program.cs`
Un menu `do { ... } while (scelta != 5);` con uno `switch`, e le cinque voci della traccia.

**Prova di controllo** (eseguita):

| Mezzo | Calcolo | Costo |
|---|---|---|
| Auto Panda, 10.000 km, 5 porte | 10000 × 0,05 + 100 | 600 |
| Camion Daily, 20.000 km, 10 t | 20000 × 0,15 + 10 × 50 | 3500 |
| **Totale** | | **4100,00** ✔ |

## 3. Esercizio 2: Biblioteca (console)

È **identico** all'esercizio 1 con i nomi cambiati, e dimostra che il prof ripropone sempre lo stesso schema:

| Parco Veicoli | Biblioteca |
|---|---|
| Veicolo | Risorsa |
| Auto / Camion | Libro / Audiolibro |
| Flotta | Catalogo |
| CalcolaCostoManutenzione | CalcolaPenaleRitardo |
| 0,05 × km | 0,20 × giorni |
| Auto: base + 100 | Libro: base + 5 |
| Camion: 0,15 × km + 50 × t | Audiolibro: 0,50 × giorni + 0,01 × minuti |

**Prova:** Libro, 10 giorni → 2 + 5 = **7**. Audiolibro, 10 giorni e 300 minuti → 5 + 3 = **8**. Totale **15,00** ✔.

> La versione della compagna (`LibraryWindowsForm`) è **sbagliata rispetto alla traccia**: usa 0,30 e 0,1 al posto di 0,50 e 0,01, e aggiunge al metodo un parametro `giorniPrestitoEffettivi` che la traccia non prevede. Ricopiarla vuol dire perdere punti.

**Allenamento per stasera:** chiudi la cartella 02 e riscrivi la Biblioteca da zero in **30 minuti**, senza guardare. Se ci riesci, domani sei a posto.

---

## 4. Windows Forms

### 4.1 Struttura (come il prof)

```
ParcoVeicoliWinForms.slnx          ← soluzione: contiene 2 progetti
├── LibreriaParcoVeicoli/          ← "Libreria di classi": SOLO il modello
│   Veicolo.cs  Auto.cs  Camion.cs  Flotta.cs
└── ParcoVeicoliWinForms/          ← "App Windows Forms": SOLO la grafica
    Program.cs                     ← avvia la form
    FormFlotta.cs                  ← il TUO codice: gestori degli eventi
    FormFlotta.Designer.cs         ← codice GENERATO dal designer: i controlli
```

Perché due progetti? Il modello (le classi) non sa nulla della grafica e si potrebbe riusare anche in console. Infatti `Veicolo`, `Auto` e `Camion` sono **copiati identici** dalla console: cambia solo il namespace. L'unica classe che cambia è `Flotta`.

Nella form servono `using LibreriaParcoVeicoli;` e il riferimento al progetto (vedi la tabella del paragrafo 0).

### 4.2 `partial class` e Designer

`public partial class FormFlotta : Form` vuol dire che la classe è divisa in due file:
- `FormFlotta.Designer.cs` contiene `InitializeComponent()`, che crea i controlli e ne imposta posizione, testo e collegamenti agli eventi;
- `FormFlotta.cs` contiene il tuo codice.

In Visual Studio il Designer **non lo scrivi a mano**: trascini i controlli dalla *Casella degli strumenti* (Ctrl+Alt+X) e imposti `Name` e `Text` da *Proprietà* (F4). Io l'ho scritto a mano solo perché su Linux il designer non c'è. È nello stesso formato di VS, quindi su Windows si apre normalmente.

**Convenzione dei nomi del prof:** tipo + scopo, per esempio `buttonInserisci`, `textBoxTarga`, `dataGridViewVeicoli`, `labelExtra`. **Imposta `Name` prima di fare doppio click**: il nome del gestore viene da lì (`buttonInserisci_Click`).

### 4.3 Eventi

Il doppio click su un bottone nel designer fa due cose:
1. crea in `FormFlotta.cs` il metodo `private void buttonInserisci_Click(object sender, EventArgs e) { }`;
2. aggiunge nel Designer `buttonInserisci.Click += buttonInserisci_Click;`.

`+=` "iscrive" il metodo all'evento: quando l'utente clicca, il metodo viene chiamato.

⚠️ **Errore classico:** se cancelli il metodo da `FormFlotta.cs`, la riga `+=` resta nel Designer, il programma non compila più e il designer si rompe. Togli anche quella riga (doppio click sull'errore e cancellala), oppure svuota l'evento dalla finestra Proprietà → icona del fulmine.

Per gli altri eventi (`CellClick`, `CheckedChanged`) seleziona il controllo → Proprietà → **fulmine** → doppio click sull'evento.

### 4.4 `BindingList` e `DataGridView`

```csharp
dataGridViewVeicoli.DataSource = flotta.Veicoli;   // collega la lista alla griglia
```

- La griglia crea **una colonna per ogni proprietà pubblica** del tipo della lista. Visto che la lista è di `Veicolo`, compaiono Targa, Marca, Modello e ChilometriPercorsi, ma **non** NumeroPorte (che esiste solo in Auto). Per questo, quando selezioni una riga, i dettagli completi li mostro in `labelDettagli` con `StampaDettagli()`.
- **`BindingList` invece di `List`:** quando aggiungi o rimuovi un elemento, avvisa la griglia, che si aggiorna da sola. Con una `List` normale la griglia non se ne accorgerebbe.
- Se invece **modifichi una proprietà** di un oggetto già in lista, la lista non cambia e la griglia non lo sa: serve `dataGridViewVeicoli.Refresh();`, come nel `buttonModificaStudente_Click` del prof.

### 4.5 CRUD: il pattern del prof

| Operazione | Codice |
|---|---|
| **Lettura** | `DataSource = lista` nel bottone "Carica" |
| **Selezione** | `CellClick` → `lista[e.RowIndex]` → riempi le TextBox |
| **Inserimento** | leggi le TextBox → `new Auto(...)` → `lista.Add(...)` |
| **Modifica** | `FirstOrDefault(v => v.Targa == textBoxTarga.Text)` → cambia le proprietà → `Refresh()` |
| **Cancellazione** | stesso `FirstOrDefault` → `lista.Remove(v)` |

- `FirstOrDefault(v => v.Targa == ...)` restituisce il primo elemento per cui la condizione è vera, oppure `null`. **Controlla sempre il null** prima di usarlo: le versioni della compagna non lo fanno e vanno in crash se la targa non esiste.
- `if (e.RowIndex < 0) return;` serve perché il click sull'intestazione delle colonne dà `RowIndex = -1`, e `lista[-1]` manderebbe in crash il programma.
- Il prof usa `CellContentClick`, che scatta solo se clicchi **sul testo** della cella. Io uso `CellClick`, che scatta ovunque nella cella ed è più comodo. Va bene uno qualsiasi dei due.
- Il campo specifico (porte o carico) lo gestisco con il pattern `is`:
  ```csharp
  if (v is Auto a) a.NumeroPorte = ...;
  else if (v is Camion c) c.CapacitaCarico = ...;
  ```
  Nella sua `buttonModifica` la compagna scrive `camion.ChilometriPercorsi = ...` dove dovrebbe esserci `CapacitaCarico`: è un bug.

### 4.6 Leggere il codice del prof (`03_Esempio_Prof_WinFormsScuola`)

- `Studente.GetStudenti()` è un metodo `static` che crea i dati di prova. Usa due stili: il costruttore `new Studente(12, "pippo", ...)` e l'**inizializzatore di oggetto** `new Studente { Matricola = 11, Nome = "pluto" }`. Il secondo assegna le proprietà dopo aver chiamato il costruttore vuoto, ed è per questo che la classe ha `public Studente() { }`.
- `voti.Select(vo => new { Voto = vo })` trasforma ogni `int` in un oggetto anonimo con una proprietà `Voto`. Serve perché la griglia mostra **proprietà**, e un `int` non ne ha: senza questo passaggio vedresti colonne vuote.
- `FormVoti formVoti = new FormVoti(v, studente); formVoti.ShowDialog();` apre una seconda finestra e blocca la prima finché non la chiudi. Per passare i dati, la seconda form li riceve nel costruttore.

---

## 5. Checklist per la verifica

- [ ] `virtual` nella base **e** `override` nelle figlie (su entrambi i metodi)
- [ ] `: base(...)` in ogni costruttore delle derivate
- [ ] le derivate chiamano `base.StampaDettagli()` (lo chiede la traccia)
- [ ] la lista è `private` nella classe di gestione
- [ ] `using NomeNamespace;` in `Program.cs`
- [ ] `break` alla fine di ogni `case`
- [ ] formule ricontrollate con un esempio a mano (calcola **prima** il risultato atteso)
- [ ] decimali con la virgola sul PC di scuola
- [ ] i warning gialli non contano, gli **errori rossi sì**

### Errori del compilatore: cosa vogliono dire

| Codice | Causa tipica |
|---|---|
| CS0506 | `override` su un metodo che nella base non è `virtual` |
| CS0115 | `override` con il nome o i parametri sbagliati |
| CS0114 (warning) | manca `override` → **il polimorfismo non funziona** |
| CS7036 | manca `: base(...)` nel costruttore |
| CS0144 | `new` di una classe astratta |
| CS0205 | `base.Metodo()` su un metodo `abstract` |
| CS0163 | `case` senza `break` |
| CS0128 | stessa variabile dichiarata in due `case` |
| CS0246 | manca un `using` o hai sbagliato il nome di una classe |
| `FormatException` (a runtime) | hai scritto lettere in un campo numerico, o il punto al posto della virgola |

Tutti questi codici li ho verificati compilando esempi apposta: non sono andato a memoria.
