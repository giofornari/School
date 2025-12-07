# SpeseManager

## Descrizione

Realizzare un’applicazione in Java (OOP) per gestire le spese effettuate da una persona.
Ogni spesa è caratterizzata da:
• una data (ad esempio LocalDate),
• un importo (valore numerico positivo in euro),
• una categoria (es. “Alimentari”, “Trasporti”, “Svago”, “Istruzione”, “Altro”),
• una modalità di pagamento (es. “Contanti”, “Carta di credito”, “Bonifico”).

Implementare nella classe **Spesa**, il metodo **applicaIVA** che restituisce il prezzo aggiungendo l’iva al 22%.

---

## Funzionalità dell’applicazione

L’applicazione deve permettere di:

1. Inserire un certo numero di spese direttamente da codice (hard coded).

2. Calcolare:

   * la spesa totale complessiva,
   * la spesa media,
   * la spesa massima e minima.

3. Determinare:

   * la categoria con la spesa media più alta e quella con la spesa media più bassa,
   * la modalità di pagamento con la spesa totale più alta o più bassa.


---

## Implementazione

Il progetto è organizzato nella seguente struttura di cartelle:

```
SpeseManager/
├── bin/
├── src/
    ├── Main.java
    ├── SpesaManager.java
    └── Spese.java
    └── README.md
```

### 🔹 `Spese.java`

Contiene la definizione della classe **Spese**, che rappresenta una singola spesa.
Ogni oggetto include:

* `LocalDate data`
* `double importo`
* `String categoria`
* `String pagamento`

La classe implementa il metodo:

```java
public double applicaIVA() {
    return importo * 1.22;
}
```

che restituisce l’importo comprensivo di IVA al 22%.

---

### 🔹 `SpesaManager.java`

Contiene i metodi per la **gestione delle spese**, tra cui:

* Calcolo della **spesa totale complessiva**
* Calcolo della **spesa media**
* Individuazione della **spesa massima e minima**
* Calcolo delle **categorie con spesa media più alta e più bassa**
* Calcolo delle **modalità di pagamento con spesa totale più alta e più bassa**

---

### 🔹 `Main.java`

Contiene il **metodo `main`**, che:

1. Crea un insieme di spese (inserite direttamente nel codice, *hard coded*).
2. Utilizza la classe `SpesaManager` per eseguire i calcoli richiesti.
3. Stampa i risultati a video in modo leggibile.

Esempio:

```java
public static void main(String[] args) {
    SpesaManager manager = new SpesaManager();
    manager.[....]();
    manager.[....]();
}
```
