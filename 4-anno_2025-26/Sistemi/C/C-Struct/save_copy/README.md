# Scheda di Lavoro – Compito

## Esercizio 1 – safe_copy avanzato

**Obiettivo:** realizzare un programma C chiamato `safe_copy` che gestisce la copia sicura di file, usando `perror()`, `struct`, `stdout`/`stderr` e parametri da CLI.

**Nota (Windows):** anche se `stdout` e `stderr` appaiono entrambi nella console, sono due flussi distinti. Per verificarne la separazione, esegui il programma da cmd o PowerShell usando la redirezione:

```bash
safe_copy sorgente.txt destinazione.txt 2>err.log
```

**Controlla:**
- **shell** → contiene il resoconto "normale" (`stdout`)
- **err.log** → contiene solo i messaggi di errore (`stderr`) generati dal programma

---

## Consegne:

1. Il programma deve essere eseguito come:
    ```bash
    ./safe_copy sorgente.txt destinazione.txt
    ```

2. Definisci una `struct CopyStats` che contenga:
    - numero di byte copiati
    - numero di errori di lettura
    - numero di errori di scrittura

3. Apri il file sorgente in sola lettura e il file destinazione in scrittura.

4. Se `fopen()` fallisce su uno dei due file, usa `perror()` e termina.

5. Copia il contenuto a blocchi di 256 byte.

6. Se `fread()` fallisce (`fread < size` richiesto e non per EOF), usa `perror()` e incrementa errori di lettura.

7. Se `fwrite()` fallisce, usa `perror()` e incrementa errori di scrittura.

8. Al termine:
    - stampa su `stdout` un resoconto della `struct CopyStats`
    - stampa su `stderr` eventuali anomalie non critiche

9. Modifica i permessi del file sorgente per generare volutamente un errore e annotalo.

---

## Verifica:

- Riesci a distinguere cosa finisce su `stdout` e cosa su `stderr`?
- `perror` mostra messaggi diversi a seconda del tipo di errore?
- La `struct` viene popolata correttamente?

---
