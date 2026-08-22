// Interfaccia di rete. Nel simulatore mono-router fa poco: da' un tipo alla
// colonna "Use" della TDI, che nel programma in C era una stringa di ottetti
// senza comportamento.
//
// Esiste gia' adesso perche' e' l'aggancio del multi-hop: un Link collegherà due
// Iface, non due stringhe.
class Iface {

  constructor(nome, ip, msk, su) {
    this.nome = String(nome).trim();
    if (this.nome === '') throw new Error('interfaccia senza nome');
    this.ip  = ip >>> 0;
    this.msk = msk >>> 0;
    if (!Ip.mskValida(this.msk)) {
      throw new Error('netmask non contigua su ' + this.nome + ': ' + Ip.int2dotted(this.msk));
    }
    this.su = su !== false;
  }

  get pfx() { return Ip.msk2pfx(this.msk); }

  // Vero se l'indirizzo appartiene alla rete di questa interfaccia.
  locale(ip) { return (((ip >>> 0) & this.msk) >>> 0) === ((this.ip & this.msk) >>> 0); }

  toJSON() {
    return {
      nome: this.nome,
      ip:   Ip.int2dotted(this.ip),
      msk:  Ip.int2dotted(this.msk),
      su:   this.su
    };
  }

  static daJSON(o) {
    if (!o || typeof o !== 'object') throw new Error('interfaccia non valida nel file');
    return new Iface(o.nome, Ip.dotted2int(o.ip), Ip.parseMsk(o.msk), o.su);
  }
}
