# Esercizio 2 – Apertura ripetuta di file

## Obiettivo
Esplorare errori reali di sistema aprendo ripetutamente un file finché il sistema non rifiuta ulteriori aperture.

## Consegne

1. Scrivi un programma C chiamato `openloop`.

2. Crea una opportuna struttura dati dinamica che possa archiviare opportunamente, per ogni apertura file:
    - `fp` (File pointer)
    - indice progressivo di apertura del file
    - handle kernel del file

    e una `struct OpenInfo` contenente:
    - numero totale di aperture riuscite
    - numero di aperture fallite
    - puntatore alla precedente lista
    - dimensione della precedente lista

3. In un ciclo `while (true)`:
    - prova a fare `fopen("test.txt", "r")`
    - se ha successo, aggiungi il `FILE*` a un array dinamico
    - se fallisce:
      - usa `perror("fopen")`
      - incrementa il contatore di errori
      - esci dal ciclo

4. Chiudi **tutti** i file rimasti aperti.

5. Stampa un report finale su `stdout`.

6. Stampa su `stderr` eventuali condizioni anomale (es. impossibile chiudere un file).

## Verifica

- Quale errore di sistema viene segnalato da `perror` quando finiscono i file descriptor?
    
    `EMFILE` (Too many open files) - il processo ha raggiunto il limite massimo di fd aperti.

- Il programma rilascia correttamente tutte le risorse?

    fa ti! se tutti i `FILE*` vengono chiusi con `fclose()` e la memoria liberata con `free()`.

- Riesci a far provocare altri tipi di errore al SO?

    si, cancellando explorer.exe da windows :>

- (Solo per Linux/MAC) Cosa cambia se riduci le risorse del processo con `ulimit -n`?

    definisco quante fd posso aprire in una singola sessione
