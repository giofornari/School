#!/usr/bin/env python3
"""
B1 - Il livello 3: Rete, pag. 87 - PROGRAMMA "Hops"
Porting Python del sorgente C del libro (Ollari, Corso di Sistemi e Reti vol.2).

TRACCIA
    Dato lo schema di rete del paragrafo "Routing CNLS: by network address",
    digitati due numeri (router di partenza e router di arrivo), stampare il
    percorso dell'ipotetico pacchetto.

IDEA DELL'ALGORITMO
    La topologia e' descritta da una lista di TRIPLETTE (ra, rb, p) che si
    leggono cosi': "sulla porta p del router ra e' connesso il router rb".
    In tutto 6 triplette per i 4 router R1..R4 in catena:

        R1 --P2----P4-- R2 --P2----P5-- R3 --P3----P1-- R4

    Ad ogni passo il pacchetto cerca la prima tripletta che gli permette di
    uscire dal router corrente SENZA tornare da dove e' venuto. Se non ne
    esiste nessuna, si accontenta di tornare indietro.

NOTA (limiti dell'algoritmo, dichiarati dal libro stesso)
    a) da R2 verso R4 il pacchetto "torna indietro" a R1 e poi risale;
    b) da R3 verso R1 si comporta razionalmente;
    c) con una destinazione inesistente (es. R9) cerca il percorso
       indefinitamente, finche' non scatta il TTL.
"""

# (ra, rb, p) -> "on porta p di ra è connected rb"
LINKROUTER = [
    ("R1", "R2", 2),
    ("R2", "R1", 4),
    ("R2", "R3", 2),
    ("R3", "R2", 5),
    ("R3", "R4", 3),
    ("R4", "R3", 1),
]

MAX_HOP = 24          # TTL: nel C  n<70 sui printed chars

rm = int(input("put here source router  (1..4): "))      # C righe 16-21
rd = int(input("put here destination router (1..4): "))  # C righe 18-22

r = -1                      # router source (-1 = nessuno)
hops = [rm]

while rm != rd and len(hops) <= MAX_HOP:            # C riga 28
    ok = None               # index di last tripletta d'exit found
    mosso = False

    for i, (ra, rb, _p) in enumerate(LINKROUTER):   # C righe 31-44
        if int(ra[1]) != rm:
            continue
        ok = i
        if int(rb[1]) != r:         # non è la entry port
            r, rm = rm, int(rb[1])
            mosso = True
            break

    if not mosso:
        if ok is None:              # no exit: router isolated
            print(f"no exit from R{rm} to R{rd}")   # C righe 50-54
            raise SystemExit        # nel C: return 0
        # the only exit disponibile: torno indietro
        r, rm = rm, int(LINKROUTER[ok][1][1])       # C righe 45-49

    hops.append(rm)
    print("track: " + " ".join(f"R{x}" for x in hops))   # C righe 56-57

print("ok" if rm == rd else "error TTL!")           # C riga 60
