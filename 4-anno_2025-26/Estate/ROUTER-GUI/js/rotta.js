// Una riga della TDI: dove si va, con che mask, per quale gateway, da quale
// interfaccia e a che costo.
//
// Gli indirizzi entrano gia' come interi a 32 bit. Convertire dal dotted e'
// compito di chi legge il form o il file JSON, non di questa classe.
class Rotta {

  constructor(rete, msk, gw, iface, metr) {
    msk = msk >>> 0;
    if (!Ip.mskValida(msk)) {
      throw new Error('netmask non contigua: ' + Ip.int2dotted(msk));
    }
    rete = rete >>> 0;

    // Chi scrive 192.168.1.77/24 intende 192.168.1.0/24. Mascherare in silenzio
    // funzionerebbe, ma nasconderebbe un errore di ragionamento: meglio dirlo.
    if (((rete & msk) >>> 0) !== rete) {
      throw new Error('la rete ' + Ip.int2dotted(rete) + ' ha bit accesi fuori dalla mask /' +
                      Ip.msk2pfx(msk) + ' — forse intendevi ' + Ip.int2dotted((rete & msk) >>> 0));
    }

    const m = Number(metr);
    if (!Number.isFinite(m) || m < 0) throw new Error('metrica non valida: ' + metr);

    this.rete  = rete;
    this.msk   = msk;
    this.gw    = gw >>> 0;
    this.iface = String(iface).trim();
    this.metr  = m;

    if (this.iface === '') throw new Error('interfaccia d\'uscita mancante');
  }

  get pfx() { return Ip.msk2pfx(this.msk); }

  // Gateway 0.0.0.0 vuol dire "la rete e' attaccata qui": nessun next hop.
  get connessa() { return this.gw === 0; }

  copre(ip) { return (((ip >>> 0) & this.msk) >>> 0) === this.rete; }

  // Come copre(), ma restituisce anche i passaggi intermedi: e' cio' che la GUI
  // mostra per spiegare il match, l'equivalente del printf del programma in C.
  calcolo(ip) {
    const and = (((ip >>> 0) & this.msk) >>> 0);
    return { and: and, rete: this.rete, esito: and === this.rete };
  }

  // Stessa destinazione ma gateway diverso e' legittimo: e' la rotta di riserva.
  stessaDest(a) { return this.rete === a.rete && this.msk === a.msk; }

  // Stessa destinazione E stesso gateway invece e' solo la stessa istruzione
  // scritta due volte.
  identicaA(a) { return this.stessaDest(a) && this.gw === a.gw; }

  toJSON() {
    return {
      rete:  Ip.int2dotted(this.rete),
      msk:   Ip.int2dotted(this.msk),
      gw:    Ip.int2dotted(this.gw),
      iface: this.iface,
      metr:  this.metr
    };
  }

  static daJSON(o) {
    if (!o || typeof o !== 'object') throw new Error('rotta non valida nel file');
    return Rotta.daDotted(o.rete, o.msk, o.gw, o.iface, o.metr);
  }

  static daDotted(rete, msk, gw, iface, metr) {
    return new Rotta(Ip.dotted2int(rete), Ip.parseMsk(msk), Ip.dotted2int(gw), iface, metr);
  }
}
