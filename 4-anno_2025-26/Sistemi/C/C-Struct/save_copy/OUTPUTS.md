# Annotazioni Errori - safe_copy

## Data: 2025-12-04
## Autore: giordii (admin@giordii.dev)

---

## Errore 1: File Sorgente Inesistente

### Comando eseguito:
```bash
./bin/safe_copy file_inesistente.txt output.txt 2>err.log
```

### Output STDOUT (console):
```
Inizio copia file...
Sorgente: notafile.txt
Destinazione: output.txt


Byte copiati: 0
Errori di lettura: 0
Errori di scrittura: 0
```

### Output STDERR (err.log):
```
Errore apertura sorgente: No such file or directory

OPERAZIONE COMPLETATA CON ERRORI
Nessun byte copiato
```

### Analisi:
- **Funzione fallita**: `fopen()` sul file sorgente
- **errno settato a**: ENOENT (No such file or directory)
- **Comportamento**: Terminazione immediata con EXIT_FAILURE prima di iniziare la copia
- **stdout vs stderr**: stdout contiene solo il resoconto, stderr contiene gli errori di perror() e le anomalie

---

## Errore 2: Permission Denied (Lettura)

### Preparazione:
```bash
echo "contenuto protetto" > protected.txt
chmod 000 protected.txt
```

### Comando eseguito:
```bash
./bin/safe_copy protected.txt output.txt 2>err_perm.log
```

### Output STDOUT (console):
```
Inizio copia file...
Sorgente: flag.txt
Destinazione: output.txt


Byte copiati: 0
Errori di lettura: 0
Errori di scrittura: 0
```

### Output STDERR (err_perm.log):
```
Errore apertura sorgente: Permission denied

OPERAZIONE COMPLETATA CON ERRORI
Nessun byte copiato
```

### Analisi:
- **Funzione fallita**: `fopen()` sul file sorgente
- **errno settato a**: EACCES (Permission denied)
- **Comportamento**: Il programma non può aprire il file per mancanza di permessi
- **Verifica permessi**: `ls -l flag.txt` mostra `----------` (nessun permesso)

---

## Errore 3: Permission Denied (Scrittura)

### Preparazione:
```bash
touch anotherflag.txt
chmod 444 anotherflag.txt  # Solo lettura
echo "sorgente ok" > anotherflag.txt
```

### Comando eseguito:
```bash
./bin/safe_copy anotherflag.txt anotherflag.txt 2>err_write.log
```

### Output STDERR:
```
Errore apertura destinazione: Permission denied

OPERAZIONE COMPLETATA CON ERRORI
Nessun byte copiato
```

### Analisi:
- **Funzione fallita**: `fopen()` sul file destinazione (modalità "wb")
- **errno settato a**: EACCES

---

## Test Separazione stdout/stderr

### Comando:
```bash
./bin/safe_copy input.txt output.txt 1>stdout.log 2>stderr.log
```

### Risultato Copia Normale:

**stdout.log contiene:**
```
Inizio copia file...
Sorgente: input.txt
Destinazione: output.txt


Byte copiati: 110
Errori di lettura: 0
Errori di scrittura: 0

Copia completata!
```

**stderr.log contiene:**
```
(no errors)
```

### Risultato con Errore:

**stdout.log contiene:**
```
Inizio copia file...
Sorgente: file_inesistente.txt
Destinazione: output.txt


Byte copiati: 0
Errori di lettura: 0
Errori di scrittura: 0
```

**stderr.log contiene:**
```
Errore apertura sorgente: No such file or directory

OPERAZIONE COMPLETATA CON ERRORI
Nessun byte copiato
```

---

## Verifica Blocchi di 256 Byte

### Test con File di 10 KB:
```bash
dd if=/dev/urandom of=large.bin bs=1024 count=10
./bin/safe_copy large.bin large_copy.bin
```

### Output:
```
Byte copiati: 10240
Errori di lettura: 0
Errori di scrittura: 0
```

### Analisi:
- 10240 byte = 10 KB
- Numero di blocchi copiati: 10240 / 256 = 40 blocchi

---
