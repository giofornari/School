// Pannello della simulazione: raccoglie l'indirizzo e mostra l'esito.
// La spiegazione arriva gia' scritta dentro esito.motivo — qui non si ragiona,
// si impagina.
class VistaSim {

  constructor(form, ingresso, elEsito, elErrore) {
    this.form  = form;
    this.in    = ingresso;
    this.box   = elEsito;
    this.err   = elErrore;
    this.cb    = null;

    this.form.addEventListener('submit', ev => {
      ev.preventDefault();
      if (this.cb) this.cb(this.in.value);
    });
  }

  onSimula(cb) { this.cb = cb; }

  errore(msg) {
    this.err.textContent = msg;
    this.err.hidden = false;
    this.box.hidden = true;
  }

  pulisci() {
    this.err.hidden = true;
    this.box.hidden = true;
    this.box.textContent = '';
  }

  mostra(esito) {
    this.err.hidden = true;
    this.box.textContent = '';
    this.box.hidden = false;

    const v = document.createElement('div');
    v.className = 'verdetto' + (esito.scelta ? '' : ' ko');

    if (esito.scelta) {
      v.appendChild(document.createTextNode('Il pacchetto per ' + Ip.int2dotted(esito.ip) + ' esce da '));
      v.appendChild(this._forte(esito.scelta.iface));
      v.appendChild(document.createTextNode(esito.scelta.connessa
        ? ' verso la rete direttamente connessa '
        : ' con next hop '));
      v.appendChild(this._forte(esito.scelta.connessa
        ? Ip.int2dotted(esito.scelta.rete) + '/' + esito.scelta.pfx
        : Ip.int2dotted(esito.scelta.gw)));
      v.appendChild(document.createTextNode('.'));
    } else {
      v.textContent = 'Destinazione ' + Ip.int2dotted(esito.ip) +
                      ' irraggiungibile: il pacchetto viene scartato.';
    }
    this.box.appendChild(v);

    const p = document.createElement('p');
    p.className = 'motivo';
    p.textContent = esito.motivo;
    this.box.appendChild(p);

    if (esito.alternative.length) {
      const h = document.createElement('h3');
      h.textContent = 'Alternative utilizzabili come fallback';
      this.box.appendChild(h);

      const ol = document.createElement('ol');
      ol.className = 'fallback';
      esito.alternative.forEach(rt => {
        const li = document.createElement('li');
        li.appendChild(document.createTextNode(
          Ip.int2dotted(rt.rete) + '/' + rt.pfx +
          (rt.connessa ? ' — connessa su ' + rt.iface
                       : ' via ' + Ip.int2dotted(rt.gw) + ' su ' + rt.iface) + ' '));
        const m = document.createElement('span');
        m.className = 'metr';
        m.textContent = '(prefisso /' + rt.pfx + ', metrica ' + rt.metr + ')';
        li.appendChild(m);
        ol.appendChild(li);
      });
      this.box.appendChild(ol);
    }
  }

  _forte(testo) {
    const s = document.createElement('span');
    s.className = 'rotta';
    s.textContent = testo;
    return s;
  }
}
