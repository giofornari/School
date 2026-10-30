# Sfondo della planimetria per Packet Tracer

| File | Uso |
|---|---|
| `sfondo_planimetria.png` | **2200 × 1300** — lo sfondo da caricare in Packet Tracer |
| `sfondo_planimetria_1600.png` | 1600 × 945 — stessa immagine per schermi piccoli o finestra non massimizzata |
| `sfondo_planimetria.svg` | Sorgente vettoriale: modifica qui, non i PNG |
| `genera_varianti.py` | Rigenera tutti i PNG e la versione annotata dalla sorgente |

## Come si carica in Packet Tracer

1. Vai nel **Logical Workspace** (in alto a sinistra, non *Physical*).
2. Nella barra sopra l'area di lavoro clicca **Set Tiled Background**.
3. Spunta **Display Background Image**, poi **Browse** e scegli
   `sfondo_planimetria.png`.
4. **Togli** la spunta a *Tile the Background Image*: altrimenti l'immagine
   viene ripetuta a mosaico invece che disegnata una volta sola.
5. **Apply**, poi **OK**.

L'immagine è più larga della finestra di Packet Tracer: si scorre, ed è voluto.
Serve spazio per posare 21 dispositivi IoT più dieci apparati di rete senza che
le etichette si sovrappongano. Se preferisci vedere tutto insieme senza
scorrere, carica la versione `_1600`. Per una misura diversa cambia i numeri in
`genera_varianti.py` e rilancialo: la sorgente è vettoriale, quindi non perde
qualità a nessuna dimensione.

## L'edificio

Villa unifamiliare su un piano: ingresso, cucina, bagno con lavanderia, camera
matrimoniale, un corridoio di distribuzione che attraversa tutta la casa,
soggiorno, studio, camera singola e **locale tecnico**. Fuori: garage con
accesso carrabile e giardino esposto a sud.

Rispetto alla prima versione — un appartamento — la villa dà due vantaggi
concreti. Il locale tecnico diventa una **stanza vera** invece di un armadio a
muro, quindi c'è spazio per il rack, il modem, il controller wireless, i due
access point autonomi e i cinque server senza accatastarli. E il giardino sostituisce il balcone come area esterna: il
pannello solare, il sensore di luce e l'irrigazione automatica hanno molto più
senso su un prato che su sei metri di ringhiera.

## Come è stata disegnata, e perché così

Uno sfondo per Packet Tracer ha vincoli diversi da una tavola architettonica da
stampare, perché sopra ci finiscono decine di icone con la loro etichetta.

**Colori chiarissimi.** Le icone di Packet Tracer sono scure e colorate: uno
sfondo saturo le rende illeggibili. Qui l'unico elemento scuro sono i muri, che
occupano pochissima superficie.

**Centro dei locali completamente vuoto.** Niente arredi, niente sanitari,
niente testo, niente retini in mezzo alle stanze: quello è lo spazio dove
trascini gli apparati. Il soggiorno è un rettangolo di 494 × 325 px di pavimento
libero, il corridoio una fascia continua di 1378 × 120 px.

**Etichette nell'angolo in alto a sinistra.** Le etichette dei dispositivi in
Packet Tracer compaiono *sotto* l'icona: tenere i nomi dei locali in alto evita
che si sovrappongano.

**Le porte si aprono dentro le stanze, mai nel corridoio.** Non è un vezzo: il
corridoio è la fascia più grande e più sgombra del disegno, e otto archi di
apertura rivolti lì dentro l'avrebbero resa inutilizzabile.

**Dimensione dei locali proporzionale agli apparati che ospitano.** Il soggiorno
e il locale tecnico sono i più grandi perché accolgono più dispositivi; il
giardino è una fascia larga su tutto il fronte. È il motivo per cui la pianta
non è in scala, e va detto: è uno schema funzionale, non un progetto edilizio.

**Cantina e rete dell'operatore non sono locali.** Hanno bordo arrotondato e
nessun muro proprio per segnalare che sono zone di posa: la cantina è al piano
interrato, la rete dell'operatore non è nemmeno in casa.

## Le due varianti

Da un'unica sorgente escono due immagini con scopi diversi:

- **`sfondo_planimetria.png`** — pulita, senza marker. È lo sfondo del `.pkt`.
- **`../planimetria.png`** — la stessa pianta con i 21 marker numerati e la
  legenda. Va nella relazione, dove serve dire *quale* dispositivo sta *dove*.

Non mettere la versione annotata come sfondo: i marker finirebbero sotto le
icone di Packet Tracer e si leggerebbero due informazioni sovrapposte.

Se sposti un muro nella sorgente, rilancia lo script e si aggiornano entrambe.

```bash
python3 genera_varianti.py
```

Richiede `cairosvg` e `pillow` (`pip install cairosvg pillow`). Senza di essi lo
script rigenera solo l'SVG annotato e salta i PNG.
