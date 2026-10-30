#!/usr/bin/env python3
"""
B3 - Indirizzamento IP, pag. 134-135 - PROGRAMMA "Calcolo delle subnet"
Porting Python del sorgente C del libro.

TRACCIA
    Dato un indirizzo IP privato e una subnet mask in formato CIDR (il numero
    di bit a 1), calcolare e stampare tutte le subnet disponibili.

METODO
    Gruppi privati (RFC 1918) usati dal libro:

        10.0.0.0     netmask /8
        172.16.0.0   netmask /16
        192.168.0.0  netmask /24        <- il libro usa /24, non /16

    Dati indirizzo e subnetmask /m:
        subnetlen = m - netmasklen        (bit "presi in prestito" all'hostId)
        hostlen   = 32 - m                (bit rimasti all'hostId)
        n_subnet  = 2 ** subnetlen
    L'i-esima sottorete ha indirizzo di rete  i << hostlen  sommato al netId.

NOTA
    DectoszBin e' una funzione anche nel C (il libro la include da
    "dectoszbin.c"), quindi resta una funzione anche qui. Tutto il resto e'
    lineare come dentro main().

BUG DEL LIBRO CORRETTO QUI
    Nel `case 2:` (gruppo 192.168) il C stampa
        Ipp[idx].id1, Ipp[idx].id2, Ipp[idx].id2, (u & 0x000000ff)
    cioe' ripete 168 anche come TERZO ottetto. Per questo l'OUTPUT stampato
    a pag.134 dice "192.168.168.0 / .64 / .128 / .192", che e' sbagliato:
    le sottoreti corrette sono 192.168.0.0 / .64 / .128 / .192.
    Qui il terzo ottetto viene calcolato, non copiato.
    (Altro refuso del libro: `Subnetmask = 26;` con la S maiuscola.)
"""

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
