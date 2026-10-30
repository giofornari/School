#!/usr/bin/env python3
"""
B1 - Il livello 3: Rete, pag. 90-91 - PROGRAMMA "Routing CNLS e next hop"
Porting Python del sorgente C del libro.

TRACCIA
    Date le TdI di tre router R1, R2, R3, acquisire indirizzo mittente e
    destinatario di un pacchetto trasmesso dall'host A (connesso a R1) e
    mostrare il percorso del pacchetto. Il router di partenza e' sempre R1.

STRUTTURA DATI
    Una TdI e' una lista di righe con i 4 campi classici:
    add (indirizzo) | p (porta) | h (hop) | c (costo).
    Il costo e' riportato ma non usato, come dichiara il libro.

ALGORITMO DI INOLTRO, i 3 passi numerati dal libro a pag.91
    1. caricamento della TdI del router          (C righe 44-49)
    2. individuazione della riga di inoltro      (C righe 51-58)
    3. individuazione del router next hop        (C righe 62-69)
       oppure controllo dell'arrivo a destinazione (C righe 73-79)
    Sentinella h = -1 per prevenire loop ed errori.

BUG DEL LIBRO CORRETTO QUI
    In C il ciclo di ricerca usa sizeof(tdi) su un PUNTATORE (= 4 o 8 byte)
    invece di sizeof(tdiRn)/sizeof(TDI): la scansione della TdI e' sbagliata.
    In Python si itera sulla lista, quindi il problema non esiste.
    (La coppia malloc+memcpy del libro e' invece solo inutile: copia in
    memoria dinamica una tabella costante che non viene mai modificata.)
"""

# TdI: router -> list di righe (add, port, hop, cost)
TDI = {
    1: [("a", 1, 0, 0), ("b", 2, 1, 5), ("c", 2, 2, 2)],
    2: [("a", 3, 1, 0), ("b", 7, 0, 5), ("c", 2, 1, 2)],
    3: [("a", 9, 2, 0), ("b", 8, 1, 5), ("c", 9, 0, 0)],
}

# (ra, rb, p) -> "on porta p di ra è connected rb"
LINKROUTER = [
    ("R1", "R2", 2),
    ("R2", "R1", 4),
    ("R2", "R3", 2),
    ("R3", "R2", 5),
]

chS = input("put here source address (a,b,c): ")
chD = input("put here destination address (a,b,c): ")

r = 1                       # il libro parte always da R1
percorso = [chS]
h = -1                      # sentinel

while h != 0:
    percorso.append(f"R{r}")
    p, h = -1, -1           # reset ad ogni giro, come il C riga 40

    # passo 1+2: carico la TdI e cerco la riga di inoltro
    for add, porta, hop, _c in TDI[r]:
        if add == chD:
            p, h = porta, hop
            break

    if h > 0:
        # passo 3: chi è attached alla porta p di questo router?
        for ra, rb, porta in LINKROUTER:
            if int(ra[1]) == r and porta == p:
                r = int(rb[1])
                break
    elif h == 0:            # dest directly connected
        percorso.append(chD)
    else:                   # no rule in TdI
        print(f"no route to {chD}")
        raise SystemExit    # nel C: return 0

print("path: " + " ".join(percorso))
