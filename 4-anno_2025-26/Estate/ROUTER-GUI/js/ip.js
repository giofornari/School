// Un indirizzo IPv4 e' un numero a 32 bit. La notazione dotted e' solo il vestito
// che indossa per farsi leggere dagli umani: nasce qui, muore qui, e nel resto del
// programma circolano soltanto interi.
//
// Avvertenza valida per tutto il file: in JavaScript gli operatori bit a bit
// lavorano su interi a 32 bit CON SEGNO. Senza il ">>> 0" finale, 255.255.255.255
// verrebbe fuori come -1, il che rende i confronti d'ordine molto creativi.
const Ip = {

  dotted2int(s) {
    const p = String(s).trim().split('.');
    if (p.length !== 4) throw new Error('servono esattamente 4 ottetti: "' + s + '"');
    let n = 0;
    for (const o of p) {
      if (!/^\d{1,3}$/.test(o)) throw new Error('ottetto non numerico in "' + s + '"');
      const v = parseInt(o, 10);
      if (v > 255) throw new Error('ottetto fuori range 0-255 in "' + s + '"');
      n = (n << 8) | v;
    }
    return n >>> 0;
  },

  int2dotted(n) {
    n = n >>> 0;
    return ((n >>> 24) & 255) + '.' + ((n >>> 16) & 255) + '.' +
           ((n >>>  8) & 255) + '.' + ( n         & 255);
  },

  // Una netmask valida e' una fila di 1 seguita da una fila di 0, senza buchi.
  // Complementandola si ottiene 0...01...1; sommando 1 resta una sola potenza di
  // due (o si va in overflow a 0, che e' il caso /0). E "x & (x-1) === 0" e' il
  // classico test per le potenze di due.
  mskValida(m) {
    const c = (((~m) >>> 0) + 1) >>> 0;
    return c === 0 || (c & (c - 1)) === 0;
  },

  msk2pfx(m) {
    m = m >>> 0;
    if (!Ip.mskValida(m)) throw new Error('netmask non contigua: ' + Ip.int2dotted(m));
    let n = 0;
    for (let i = 0; i < 32; i++) {
      if (m & (1 << (31 - i))) n++;
    }
    return n;
  },

  pfx2msk(p) {
    if (!Number.isInteger(p) || p < 0 || p > 32) throw new Error('prefisso fuori range: /' + p);
    // Il /0 va trattato a parte: lo shift usa solo i 5 bit bassi del secondo
    // operando, quindi "<< 32" equivale a "<< 0" e restituirebbe tutti 1.
    return p === 0 ? 0 : (0xFFFFFFFF << (32 - p)) >>> 0;
  },

  // Accetta sia "255.255.255.0" sia "/24" sia "24", perche' nessuno ha voglia di
  // ricordarsi quale delle tre voleva il form.
  parseMsk(s) {
    const t = String(s).trim();
    if (t === '') throw new Error('netmask vuota');
    if (t.indexOf('.') >= 0) {
      const m = Ip.dotted2int(t);
      if (!Ip.mskValida(m)) throw new Error('netmask non contigua: ' + t);
      return m;
    }
    const cidr = t[0] === '/' ? t.slice(1) : t;
    if (!/^\d{1,2}$/.test(cidr)) throw new Error('netmask non riconosciuta: "' + s + '"');
    return Ip.pfx2msk(parseInt(cidr, 10));
  }
};
