#!/usr/bin/env python3
"""
Verifica automatica delle tabelle di routing statico della WAN 160.80.0.0/16.

Non sostituisce i ping in Packet Tracer: serve a dimostrare *prima* di
configurare che le tabelle scritte a mano sono complete e coerenti.

Controlla tre cose:
  1. completezza  - ogni router conosce tutte e 10 le reti
  2. assenza di loop - seguendo i next hop si arriva sempre a destinazione
  3. raggiungibilita end-to-end - tutte le coppie di host si raggiungono

Uso:  python3 verifica_routing.py
"""

# --------------------------------------------------------------------------
# Topologia: per ogni router, IP delle sue interfacce -> rete di appartenenza
# --------------------------------------------------------------------------
INTERFACCE = {
    "R1": {"160.80.1.1": "160.80.1.0",    # rete A
           "160.80.7.1": "160.80.7.0",    # link R1-R2
           "160.80.10.1": "160.80.10.0",  # link R1-R3
           "160.80.8.1": "160.80.8.0"},   # link R1-R4
    "R2": {"160.80.3.1": "160.80.3.0",    # rete B
           "160.80.7.2": "160.80.7.0",
           "160.80.9.1": "160.80.9.0",    # link R2-R3
           "160.80.6.1": "160.80.6.0"},   # rete F
    "R3": {"160.80.5.1": "160.80.5.0",    # rete C
           "160.80.10.2": "160.80.10.0",
           "160.80.9.2": "160.80.9.0"},
    "R4": {"160.80.4.1": "160.80.4.0",    # rete E
           "160.80.8.2": "160.80.8.0"},
    "R5": {"160.80.2.1": "160.80.2.0",    # rete D
           "160.80.4.2": "160.80.4.0",    # rete E
           "160.80.6.2": "160.80.6.0"},   # rete F
}

# --------------------------------------------------------------------------
# Rotte statiche: le STESSE che vanno incollate nella CLI dei router.
# rete_destinazione -> indirizzo del next hop
# --------------------------------------------------------------------------
ROTTE_STATICHE = {
    "R1": {"160.80.2.0": "160.80.8.2", "160.80.3.0": "160.80.7.2",
           "160.80.4.0": "160.80.8.2", "160.80.5.0": "160.80.10.2",
           "160.80.6.0": "160.80.7.2", "160.80.9.0": "160.80.7.2"},
    "R2": {"160.80.1.0": "160.80.7.1", "160.80.2.0": "160.80.6.2",
           "160.80.4.0": "160.80.6.2", "160.80.5.0": "160.80.9.2",
           "160.80.8.0": "160.80.7.1", "160.80.10.0": "160.80.7.1"},
    "R3": {"160.80.1.0": "160.80.10.1", "160.80.2.0": "160.80.9.1",
           "160.80.3.0": "160.80.9.1", "160.80.4.0": "160.80.9.1",
           "160.80.6.0": "160.80.9.1", "160.80.7.0": "160.80.10.1",
           "160.80.8.0": "160.80.10.1"},
    "R4": {"160.80.1.0": "160.80.8.1", "160.80.2.0": "160.80.4.2",
           "160.80.3.0": "160.80.8.1", "160.80.5.0": "160.80.8.1",
           "160.80.6.0": "160.80.4.2", "160.80.7.0": "160.80.8.1",
           "160.80.9.0": "160.80.8.1", "160.80.10.0": "160.80.8.1"},
    "R5": {"160.80.1.0": "160.80.6.1", "160.80.3.0": "160.80.6.1",
           "160.80.5.0": "160.80.6.1", "160.80.7.0": "160.80.6.1",
           "160.80.8.0": "160.80.4.1", "160.80.9.0": "160.80.6.1",
           "160.80.10.0": "160.80.6.1"},
}

# host: nome -> (rete, ip, default gateway)
HOST = {
    "PC A":  ("160.80.1.0", "160.80.1.10", "160.80.1.1"),
    "PC B":  ("160.80.3.0", "160.80.3.10", "160.80.3.1"),
    "PC C1": ("160.80.5.0", "160.80.5.10", "160.80.5.1"),
    "PC C2": ("160.80.5.0", "160.80.5.11", "160.80.5.1"),
    "PC D":  ("160.80.2.0", "160.80.2.10", "160.80.2.1"),
    "PC E":  ("160.80.4.0", "160.80.4.10", "160.80.4.1"),
    "PC F":  ("160.80.6.0", "160.80.6.10", "160.80.6.1"),
}

# --------------------------------------------------------------------------
PROPRIETARIO = {ip: r for r, d in INTERFACCE.items() for ip in d}
CONNESSE = {r: set(d.values()) for r, d in INTERFACCE.items()}
RETI = sorted({s for d in INTERFACCE.values() for s in d.values()},
              key=lambda x: int(x.split(".")[2]))


def percorso(router_partenza, rete_destinazione):
    """Segue i next hop finche' la rete non e' direttamente connessa.
    Ritorna (ok, lista_router_attraversati)."""
    corrente = router_partenza
    visitati = [corrente]
    while rete_destinazione not in CONNESSE[corrente]:
        next_hop = ROTTE_STATICHE[corrente].get(rete_destinazione)
        if next_hop is None:
            return False, visitati + ["DROP: nessuna rotta"]
        if next_hop not in PROPRIETARIO:
            return False, visitati + [f"DROP: next hop {next_hop} inesistente"]
        # il next hop deve stare su una rete DIRETTAMENTE CONNESSA
        rete_nh = INTERFACCE[PROPRIETARIO[next_hop]][next_hop]
        if rete_nh not in CONNESSE[corrente]:
            return False, visitati + [f"ERRORE: {next_hop} non e' adiacente a {corrente}"]
        corrente = PROPRIETARIO[next_hop]
        if corrente in visitati:
            return False, visitati + [corrente, "LOOP"]
        visitati.append(corrente)
    return True, visitati


def main():
    errori = 0

    # --- 1. completezza -----------------------------------------------
    print("1) COMPLETEZZA — ogni router deve conoscere tutte e 10 le reti")
    for r in INTERFACCE:
        note = CONNESSE[r] | set(ROTTE_STATICHE[r])
        mancanti = [n for n in RETI if n not in note]
        stato = "OK" if not mancanti else f"MANCANO {mancanti}"
        if mancanti:
            errori += 1
        print(f"   {r}: {len(CONNESSE[r])} connesse + "
              f"{len(ROTTE_STATICHE[r])} statiche = {len(note)} reti  [{stato}]")

    # --- 2. forwarding router -> rete ---------------------------------
    print("\n2) FORWARDING — da ogni router verso ogni rete "
          f"({len(INTERFACCE) * len(RETI)} casi)")
    ko = [(r, n, p) for r in INTERFACCE for n in RETI
          for ok, p in [percorso(r, n)] if not ok]
    if ko:
        errori += len(ko)
        for r, n, p in ko:
            print(f"   FALLITO {r} -> {n}: {' -> '.join(p)}")
    else:
        print("   OK — nessun loop, nessuna rotta mancante, "
              "tutti i next hop sono adiacenti")

    # --- 3. raggiungibilita' end-to-end -------------------------------
    coppie = [(a, b) for a in HOST for b in HOST
              if a != b and HOST[a][0] != HOST[b][0]]
    print(f"\n3) PING HOST -> HOST ({len(coppie)} coppie di sottoreti diverse)")
    ko2, massimo = [], 0
    for a, b in coppie:
        ok, p = percorso(PROPRIETARIO[HOST[a][2]], HOST[b][0])
        if not ok:
            ko2.append((a, b, p))
        massimo = max(massimo, len(p))
    if ko2:
        errori += len(ko2)
        for a, b, p in ko2:
            print(f"   FALLITO {a} -> {b}: {' -> '.join(p)}")
    else:
        print(f"   OK — tutte raggiungibili, "
              f"massimo {massimo} router attraversati")

    # --- 4. percorsi attesi (da confrontare con tracert) --------------
    print("\n4) PERCORSI ATTESI — confrontali con 'tracert' in Packet Tracer")
    for a, b in [("PC A", "PC D"), ("PC C1", "PC F"),
                 ("PC E", "PC B"), ("PC D", "PC C2")]:
        _, p = percorso(PROPRIETARIO[HOST[a][2]], HOST[b][0])
        print(f"   {a:6} -> {b:6}: {' -> '.join(p)}")

    tot = sum(len(v) for v in ROTTE_STATICHE.values())
    print(f"\nTotale rotte statiche da configurare: {tot}")
    print("ESITO:", "TUTTO OK" if errori == 0 else f"{errori} PROBLEMI")
    return 0 if errori == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
