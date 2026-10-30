# B3 pag.129 - Instradamento classful: valutazione delle regole di TdI

# Address, Mask, Gateway (next hop), Use (interfaccia d'uscita)
TDI_HOST = [
    ((0, 0, 0, 0),    (0, 0, 0, 0),        (196, 13, 1, 254), (196, 13, 1, 1)),
    ((196, 13, 1, 0), (255, 255, 255, 0),  (196, 13, 1, 1),   (196, 13, 1, 1)),
]

a, b, c, d = 196, 13, 2, 5          # C riga 24: l'address da instradare
dest = f"{a}.{b}.{c}.{d}"


def dotted_to_decimal(a, b, c, d):  # C righe 43-49
    # i 4 ottetti sono le cifre di un numero in base 256
    return a * 0x1000000 + b * 0x10000 + c * 0x100 + d


# stampa della TdI, C righe 20-22. I nomi Ia..Ud sono quelli dei 16 campi
# della struct TDI del libro
print(f"{'Address':<17}{'Mask':<17}{'Gateway':<17}{'Use'}")
for (Ia, Ib, Ic, Id), (Ma, Mb, Mc, Md), (Ga, Gb, Gc, Gd), (Ua, Ub, Uc, Ud) in TDI_HOST:
    print(f"{Ia}.{Ib}.{Ic}.{Id}".ljust(17)
          + f"{Ma}.{Mb}.{Mc}.{Md}".ljust(17)
          + f"{Ga}.{Gb}.{Gc}.{Gd}".ljust(17)
          + f"{Ua}.{Ub}.{Uc}.{Ud}")
print()

for i, (indirizzo, mask, gw, use) in enumerate(TDI_HOST, start=1):  # C righe 25-37
    u = dotted_to_decimal(*mask)
    u = u & dotted_to_decimal(a, b, c, d)
    esito = "true" if u == dotted_to_decimal(*indirizzo) else "false"
    print(f"rule n.{i} for {dest}: {esito}.")

# fra le regole true vince quella con la mask più lunga (pag.129):
# una mask più lunga, letta come intero, è anche più grande
best = -1
for indirizzo, mask, gw, use in TDI_HOST:
    m = dotted_to_decimal(*mask)
    if (dotted_to_decimal(a, b, c, d) & m) == dotted_to_decimal(*indirizzo):
        if m > best:
            best, scelta_gw, scelta_use = m, gw, use

Ga, Gb, Gc, Gd = scelta_gw
Ua, Ub, Uc, Ud = scelta_use
print(f"\n-> next hop {Ga}.{Gb}.{Gc}.{Gd} on interface {Ua}.{Ub}.{Uc}.{Ud}")
