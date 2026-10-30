# Gestione Parco Veicoli Aziendale (C#)

Gestione di una flotta di `Auto` e `Camion` che ereditano da `Veicolo`, con una `Flotta` basata su `List<Veicolo>`.

| Classe | Costo manutenzione |
|---|---|
| `Veicolo` | 0.05 €/km |
| `Auto` | 0.05 €/km + 100 € revisione |
| `Camion` | 0.15 €/km + 50 € per tonnellata |

## Esecuzione

```bash
cd Esercizi/ParcoVeicoli
dotnet run
```

Il menu permette di inserire auto e camion, vedere la flotta e il costo totale di manutenzione.
