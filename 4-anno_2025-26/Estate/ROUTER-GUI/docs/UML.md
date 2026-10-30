# Diagramma delle classi

Il primo diagramma mostra le classi del core, cioè il modello del router e la logica di instradamento. Le classi marcate `<<futura>>` non sono implementate: servono a far vedere come il progetto può crescere verso una rete con più router collegati (spiegato nella [relazione](RELAZIONE.md#evoluzione-verso-più-router)).

```mermaid
classDiagram
    direction TB

    class Router {
        +name: string
        +interfaces: Interface[]
        +tdi: TDI
        +findInterface(name) Interface
        +addInterface(iface)
        +removeInterface(name)
        +addRoute(route)
        +lookup(ip) risultato
    }

    class TDI {
        +routes: Route[]
        +addRoute(route)
        +removeRoute(indice)
    }

    class Route {
        +network: string
        +mask: string
        +nextHop: string
        +iface: string
        +metric: number
        +prefix: number
        +applyMask(ip) number
        +matches(ip) boolean
        +toString() string
    }

    class Interface {
        +name: string
        +ip: string
        +mask: string
        +up: boolean
    }

    class Rete {
        <<futura>>
        +routers: Router[]
        +links: Link[]
        +send(packet, router)
    }

    class Link {
        <<futura>>
        +a: Interface
        +b: Interface
        +up: boolean
        +other(iface) Interface
    }

    class Packet {
        <<futura>>
        +source: string
        +destination: string
        +ttl: number
        +path: string[]
    }

    Router "1" *-- "1" TDI : tdi
    Router "1" *-- "0..*" Interface : interfaces
    TDI "1" *-- "0..*" Route : routes
    Route "0..*" --> "1" Interface : iface (per nome)

    Rete "1" o-- "1..*" Router : routers
    Rete "1" o-- "0..*" Link : links
    Link "0..1" -- "2" Interface : collega
    Rete ..> Packet : inoltra
    Router ..> Packet : forward(packet)

    note for Route "nextHop è null se la rete è direttamente connessa"
    note for Router "forward(packet) è futuro: userà lookup(packet.destination)"
```

Come si legge:

- un `Router` ha una sola `TDI` e da zero a molte `Interface`. Sono composizioni perché TDI e interfacce esistono solo dentro il loro router.
- la `TDI` contiene le `Route` in un array, nell'ordine in cui sono state inserite.
- ogni `Route` punta a una `Interface` di uscita. Nel codice il collegamento è il nome (`route.iface`), che il router cerca con `findInterface`. Per questo il router non lascia eliminare un'interfaccia usata da una route.
- `Link` collega esattamente due interfacce, e un'interfaccia ha al massimo un link. `Rete` tiene insieme router e link e fa viaggiare un `Packet` da un router all'altro.

## Risultato di lookup

`lookup(ip)` restituisce un oggetto con la route scelta e tutto quello che serve alla pagina per colorare la tabella e scrivere il motivo:

| campo | contenuto |
| --- | --- |
| `ip` | l'indirizzo cercato |
| `controlli` | una voce per ogni route, in ordine di TDI: `{ route, rete, compatibile }`, dove `rete` è IP AND mask |
| `scelta` | la route vincente, oppure `null` |
| `fallback` | le altre route compatibili con interfaccia up, in ordine di preferenza |
| `scartate` | le route compatibili ma con interfaccia down |
| `motivo` | la spiegazione in italiano della scelta |

## Livelli del programma

Il secondo diagramma mostra come sono divisi i file. Persistenza e interfaccia grafica sono moduli di funzioni, non classi, quindi compaiono con lo stereotipo `<<modulo>>`. Le frecce tratteggiate sono dipendenze: la UI usa il core e la persistenza, la persistenza usa il core, il core non usa nessuno dei due.

```mermaid
classDiagram
    direction TB

    class main {
        <<modulo>>
        start() partenza
    }

    class simulator {
        <<componente Alpine>>
        +router: Router
        +risultato
        +righe
        +init()
        +run(ip)
        +simulate()
        +changed()
        +addRoute()
        +removeRoute(indice)
        +addInterface()
        +removeInterface(name)
        +toggle(iface)
        +save()
        +load(evento)
        +restore()
    }

    class format {
        <<modulo>>
        +formatRows(risultato) righe
    }

    class storage {
        <<modulo>>
        +download(router)
        +upload(file) Router
        +saveLocal(router)
        +loadLocal() Router
        +loadExample() Router
    }

    class config {
        <<modulo>>
        +toJson(router) string
        +fromJson(testo) Router
    }

    class core {
        <<modulo>>
        Router
        TDI
        Route
        Interface
    }

    main ..> simulator : registra
    main ..> storage : configurazione iniziale
    main ..> core : router vuoto se manca l'esempio
    simulator ..> format : colori delle righe
    simulator ..> storage : salva e carica
    simulator ..> core : lookup e modifiche
    storage ..> config : json
    config ..> core : crea il router
```
