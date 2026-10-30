# B3 pag.126 - Classful: classe e netId di 4 indirizzi IP

# (mask di test, leading bit attesi, netmask di classe)
CLASSI_IP = [
    (0x80, 0x00, 0xFF000000),   # A
    (0xC0, 0x80, 0xFFFF0000),   # B
    (0xE0, 0xC0, 0xFFFFFF00),   # C
]

INDIRIZZI = [
    (10, 1, 0, 3),
    (192, 168, 0, 1),
    (137, 168, 0, 1),
    (137, 168, 249, 17),
]

netid = []
for (a, b, c, d) in INDIRIZZI:                      # C righe 26-38
    # i 4 ottetti sono le cifre di un numero in base 256.
    # nel C questa riga sta DENTRO il ciclo su j, quindi la ricalcola 3 volte
    ip = a * 0x1000000 + b * 0x10000 + c * 0x100 + d

    nid = 0                     # nel C i globali partono già a 0
    for j, (mask, leading, netmask) in enumerate(CLASSI_IP):
        if (a & mask) == leading:                   # class test sul primo byte
            nid = ip & netmask
            print(f"{a:3d}.{b:3d}.{c:3d}.{d:3d} class {chr(ord('A') + j)} "
                  f"(netmask: {netmask:08x}) and netId {nid:08X}")
    netid.append(nid)

print()
# confronto a coppie: j parte da i+1, così niente repetitions
for i in range(len(INDIRIZZI) - 1):                 # C righe 40-50
    for j in range(i + 1, len(INDIRIZZI)):
        if netid[i] == netid[j]:
            ia, ib, ic, idd = INDIRIZZI[i]
            ja, jb, jc, jd = INDIRIZZI[j]
            print(f"{ia}.{ib}.{ic}.{idd} and {ja}.{jb}.{jc}.{jd} same net")
