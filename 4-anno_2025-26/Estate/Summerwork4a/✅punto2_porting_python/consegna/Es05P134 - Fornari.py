# B3 pag.134 - Calcolo delle subnet di una rete privata

# (id1, id2, netmask len del private group)
GRUPPI_PRIVATI = [
    (10, 0, 8),
    (172, 16, 16),
    (192, 168, 24),
]


def dec_to_bin(valore, nbit):       # C: DectoszBin(), da "dectoszbin.c"
    # valore in binario su nbit cifre: la larghezza nbit va nella
    # format spec, che a sua volta può essere una f-string annidata
    return f"{valore:0{nbit}b}"


a = 192                     # C righe 17-18: i due dati sono hard coded
subnetmask = 26

idx = -1
for i, g in enumerate(GRUPPI_PRIVATI):              # C righe 20-22
    if a == g[0]:
        idx = i                                     # private group found
if idx == -1:
    raise SystemExit        # nel C: return 1

id1, id2, netmasklen = GRUPPI_PRIVATI[idx]
if subnetmask < netmasklen:
    raise SystemExit        # nel C: return 2

subnetlen = subnetmask - netmasklen     # bit borrowed all'hostId
hostlen = 32 - subnetmask
n_subnet = 1 << subnetlen               # shift a sinistra = 2**subnetlen

print(f"private net del gruppo {id1}.{id2}.0.0 (netmask /{netmasklen})")
print(f"Subnet Mask /{subnetmask}; subnetid: "
      f"{dec_to_bin(n_subnet - 1, subnetlen)}")
print("subnet available:")

for i in range(n_subnet):                           # C righe 35-50
    u = i << hostlen        # sposto il subnetId a sinistra dell'hostId
    if idx == 0:            # 10.0.0.0/8  -> 24 bit free
        b = (u & 0x00FF0000) >> 16
        c = (u & 0x0000FF00) >> 8
        d = u & 0x000000FF
        print(f"{id1}.{b}.{c}.{d}")
    elif idx == 1:          # 172.16.0.0/16 -> 16 bit free
        c = (u & 0x0000FF00) >> 8
        d = u & 0x000000FF
        print(f"{id1}.{id2}.{c}.{d}")
    else:                   # 192.168.0.0/24 -> 8 bit free
        d = u & 0x000000FF
        print(f"{id1}.{id2}.0.{d}")
