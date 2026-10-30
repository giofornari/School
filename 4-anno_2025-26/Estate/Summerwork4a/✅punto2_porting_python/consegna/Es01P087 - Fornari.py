# B1 pag.87 - Hops: percorso di un pacchetto fra i router R1..R4

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
