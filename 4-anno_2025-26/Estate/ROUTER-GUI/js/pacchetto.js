// Al momento di questo pacchetto interessa solo dst. src e ttl ci sono perche'
// quando arriverà l'inoltro multi-hop non si dovrà cambiare la firma di
// Router.inoltra(): il ttl serve li', a non far girare i pacchetti in tondo per
// sempre quando due router si rimbalzano la stessa destinazione.
class Pacchetto {

  constructor(src, dst, ttl) {
    this.src = src >>> 0;
    this.dst = dst >>> 0;
    this.ttl = ttl === undefined ? 64 : ttl;
  }

  static daDotted(src, dst, ttl) {
    return new Pacchetto(Ip.dotted2int(src), Ip.dotted2int(dst), ttl);
  }
}
