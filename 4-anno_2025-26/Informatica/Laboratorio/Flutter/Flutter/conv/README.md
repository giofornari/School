# Convertitore Euro → Dollari

App Flutter che converte un importo in euro nel corrispondente valore in dollari, usando un tasso di cambio fisso (1 € = 1.09 $).

## Descrizione

L'app mostra un campo di testo in cui l'utente inserisce una cifra in euro. Premendo il bottone "Converti", il valore viene moltiplicato per 1.09 e il risultato in dollari viene visualizzato a schermo. Gestisce input non validi e campi vuoti.

---

## Struttura delle classi

Il progetto è composto da tre classi principali in `lib/main.dart`:

| Classe | Tipo | Responsabilità |
|--------|------|----------------|
| `MyApp` | `StatelessWidget` | Widget radice: configura il tema e lancia `HomePageProva` |
| `HomePageProva` | `StatefulWidget` | Widget della schermata principale, mantiene il titolo |
| `_HomePageProvaState` | `State<HomePageProva>` | Gestisce lo stato: input, validazione e calcolo della conversione |

---

## Diagramma delle Classi (UML)

```mermaid
classDiagram
    class StatelessWidget {
        <<abstract>>
        +build(BuildContext) Widget
    }
    class StatefulWidget {
        <<abstract>>
        +createState() State
    }
    class MyApp {
        +build(BuildContext) Widget
    }
    class HomePageProva {
        +String title
        +createState() _HomePageProvaState
    }
    class _HomePageProvaState {
        -String _msg
        -TextEditingController _controller
        +build(BuildContext) Widget
    }

    StatelessWidget <|-- MyApp
    StatefulWidget <|-- HomePageProva
    MyApp ..> HomePageProva : crea
    HomePageProva ..> _HomePageProvaState : crea
    _HomePageProvaState --> HomePageProva : widget associato
```

---

## Diagramma delle Attività (UML)

```mermaid
flowchart TD
    A([Avvio app]) --> B[MyApp costruisce\nil tema e il layout]
    B --> C[Mostra UI:\nTextField + Bottone Converti]
    C --> D[Utente inserisce\nun valore in euro]
    D --> E[Utente preme\nil bottone 'Converti']
    E --> F{Il campo\nè vuoto?}
    F -- Sì --> G[Mostra '0.00 $']
    G --> D
    F -- No --> H{Il testo è\nun numero valido?}
    H -- No --> I[Mostra 'Errore']
    I --> D
    H -- Sì --> J["Calcola:\nvalore × 1.09"]
    J --> K[Formatta il risultato\na 2 decimali]
    K --> L[Aggiorna l'interfaccia\ncon il risultato in dollari]
    L --> D
```

---

## Come eseguire

```bash
flutter pub get
flutter run
```

Richiede Flutter SDK installato. Compatibile con Android, iOS, macOS e Linux.

---

## Note tecniche

- La conversione gestisce sia la virgola che il punto come separatore decimale (`replaceAll(',', '.')`)
- Il tasso di cambio è fisso: **1 € = 1.09 $**
- L'aggiornamento dell'interfaccia avviene tramite `setState()` che forza il rebuild del widget
- Il `TextEditingController` permette di leggere il contenuto del `TextField` dall'handler del bottone
