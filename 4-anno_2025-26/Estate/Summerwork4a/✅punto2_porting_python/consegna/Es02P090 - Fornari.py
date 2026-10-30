# B1 pag.90 - Routing CNLS e next hop: instradamento tramite TdI

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
