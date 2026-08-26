// La Tabella di Instradamento: un array di Rotta, più l'algoritmo che sceglie.
//
// Array e scansione lineare, non un trie. Un router vero usa un Patricia trie
// perché ha centinaia di migliaia di rotte; qui ne ha dieci, e soprattutto la
// scansione completa È la visualizzazione. Un trie salta le regole non
// compatibili, che è esattamente l'informazione che questa GUI deve mostrare.
class Tdi {

  constructor() { this.rotte = []; }

  agg(r) {
    if (this.rotte.some(x => x.identicaA(r))) {
      throw new Error('rotta già presente: ' + Ip.int2dotted(r.rete) + '/' + r.pfx +
                      ' via ' + Ip.int2dotted(r.gw) +
                      '. Per una rotta di riserva serve un gateway diverso.');
    }
    this.rotte.push(r);
  }

  rimuovi(i) {
    if (!Number.isInteger(i) || i < 0 || i >= this.rotte.length) {
      throw new Error('indice fuori dalla tabella: ' + i);
    }
    this.rotte.splice(i, 1);
  }

  svuota() { this.rotte = []; }

  elenco() { return this.rotte.slice(); }

  get vuota() { return this.rotte.length === 0; }

  // Longest Prefix Match, in una passata sola. Nessuna regola viene saltata:
  // l'esito di ogni confronto finisce in righe[], che è quello che la vista
  // colora.
  cerca(ip) {
    ip = ip >>> 0;

    const righe = this.rotte.map((rt, idx) => {
      const c = rt.calcolo(ip);
      return { rotta: rt, idx: idx, and: c.and, esito: c.esito };
    });

    const match = righe.filter(r => r.esito).map(r => r.rotta);

    // Prefisso più lungo, poi metrica più bassa. A parità di entrambi decide
    // l'ordine in tabella: sort è stabile da ES2019, quindi non serve altro.
    match.sort((a, b) => b.pfx - a.pfx || a.metr - b.metr);

    const scelta = match.length ? match[0] : null;

    return {
      ip: ip,
      righe: righe,
      scelta: scelta,
      alternative: match.slice(1),
      motivo: this._motivo(ip, scelta, match)
    };
  }

  _motivo(ip, scelta, match) {
    const d = Ip.int2dotted(ip);

    if (!scelta) {
      return 'Destinazione ' + d + ' irraggiungibile: nessuna regola della tabella la copre, ' +
             'e non c\'è una default route a fare da rete di sicurezza. Il pacchetto viene scartato.';
    }

    const dest = Ip.int2dotted(scelta.rete) + '/' + scelta.pfx;
    let s = 'Per ' + d + ' vince ' + dest + '. ';

    s += scelta.pfx === 0
      ? 'È la default route: compatibile con qualunque indirizzo, ma con prefisso di lunghezza 0 ' +
        'resta sempre l\'ultima scelta possibile. Viene usata perché nessuna regola più specifica corrisponde. '
      : 'Fissa ' + scelta.pfx + ' bit di prefisso, più di ogni altra regola compatibile. ';

    s += scelta.connessa
      ? 'La rete è direttamente connessa su ' + scelta.iface + ': nessun next hop. '
      : 'Next hop ' + Ip.int2dotted(scelta.gw) + ' su ' + scelta.iface + '. ';

    const alt = match.slice(1);

    if (alt.length === 0) {
      return s + 'Nessuna alternativa: se questa via cade, il pacchetto non ha dove andare.';
    }

    if (alt[0].pfx === scelta.pfx) {
      s += 'Stesso prefisso anche via ' + Ip.int2dotted(alt[0].gw) +
           ', quindi ha deciso la metrica: ' + scelta.metr + ' contro ' + alt[0].metr + '. ';
    }

    s += alt.length === 1 ? '1 alternativa disponibile come fallback: '
                          : alt.length + ' alternative disponibili come fallback, nell\'ordine: ';

    return s + alt.map(r =>
      Ip.int2dotted(r.rete) + '/' + r.pfx +
      (r.connessa ? ' connessa su ' + r.iface : ' via ' + Ip.int2dotted(r.gw)) +
      ' (metrica ' + r.metr + ')'
    ).join(', ') + '.';
  }

  toJSON() { return this.rotte.map(r => r.toJSON()); }

  static daJSON(arr) {
    if (!Array.isArray(arr)) throw new Error('la tabella nel file non è un elenco');
    const t = new Tdi();
    arr.forEach(o => t.agg(Rotta.daJSON(o)));
    return t;
  }
}
