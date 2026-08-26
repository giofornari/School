// Il router: un nome, una TDI, un po' di interfacce.
class Router {

  constructor(nome) {
    this.nome   = String(nome || 'R1').trim();
    this.tdi    = new Tdi();
    this.ifaces = [];
  }

  aggIface(i) {
    if (this.iface(i.nome)) throw new Error('interfaccia già presente: ' + i.nome);
    this.ifaces.push(i);
  }

  rimuoviIface(nome) {
    const k = this.ifaces.findIndex(x => x.nome === nome);
    if (k < 0) throw new Error('interfaccia inesistente: ' + nome);
    this.ifaces.splice(k, 1);
  }

  // La TDI cita l'interfaccia d'uscita per nome, come fa un router vero. È qui
  // che il nome torna a essere un oggetto. Quando arriverà Rete, questo è il
  // punto in cui si aggancerà il Link — e Rotta non dovrà cambiare di una virgola.
  iface(nome) {
    return this.ifaces.find(x => x.nome === nome) || null;
  }

  // Sottile di proposito: qui, un giorno, Rete.invia() chiamerà in ciclo.
  inoltra(pkt) { return this.tdi.cerca(pkt.dst); }

  toJSON() {
    return {
      nome:   this.nome,
      ifaces: this.ifaces.map(i => i.toJSON()),
      tdi:    this.tdi.toJSON()
    };
  }

  static daJSON(o) {
    if (!o || typeof o !== 'object') throw new Error('il file non contiene un router');
    const r = new Router(o.nome);
    (o.ifaces || []).forEach(x => r.aggIface(Iface.daJSON(x)));
    r.tdi = Tdi.daJSON(o.tdi || []);
    return r;
  }
}
