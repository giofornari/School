# Consegna — porting Python dei sorgenti C (B1, B3)

Cartella pronta per il caricamento. Convenzione `Es##P### - Cognome.py`,
dove `###` è la pagina del libro su cui sta il sorgente C originale.

| File | Libro | Programma |
|---|---|---|
| `Es01P087 - Fornari.py` | B1 pag. 87 | Hops — percorso di un pacchetto fra R1..R4 |
| `Es02P090 - Fornari.py` | B1 pag. 90 | Routing CNLS e next hop — instradamento tramite TdI |
| `Es03P126 - Fornari.py` | B3 pag. 126 | Classful — classe e netId di 4 indirizzi IP |
| `Es04P129 - Fornari.py` | B3 pag. 129 | Instradamento classful — valutazione delle regole di TdI |
| `Es05P134 - Fornari.py` | B3 pag. 134 | Calcolo delle subnet di una rete privata |

## Librerie

**Nessuna.** I cinque programmi usano solo Python 3 standard: nessun `import`,
quindi non serve nessuna procedura di installazione automatica.

```bash
python3 "Es01P087 - Fornari.py"
```

`Es01`, `Es02` e `Es04` leggono i dati da tastiera; `Es03` e `Es05` hanno i dati
hard coded nel sorgente, come nell'originale in C.

## Numerazione

I sorgenti C del libro sono riquadri **PROGRAMMA** dentro il testo e non hanno
un numero d'esercizio. La numerazione `Es01`–`Es05` è quindi progressiva,
nell'ordine in cui i programmi compaiono nei capitoli; la pagina nel nome del
file è quella reale ed è il riferimento univoco.

## Nota sul programma di pag. 134

L'output stampato sul libro a pag. 134 riporta `192.168.168.0`,
`192.168.168.64`, `192.168.168.128`, `192.168.168.192`. È **sbagliato**: nel
`case 2:` il sorgente C stampa `Ipp[idx].id2` anche come terzo ottetto invece
del valore calcolato. Le sottoreti corrette di `192.168.0.0/24` con subnet mask
`/26` sono `192.168.0.0`, `.64`, `.128`, `.192`, ed è quello che stampa il
porting.

Verifica indipendente: cambiando le due righe hard coded in `a = 172` e
`subnetmask = 20`, il programma produce le 16 sottoreti `172.16.0.0`,
`172.16.16.0` … `172.16.240.0`, identiche alla figura di pag. 139 del libro.
