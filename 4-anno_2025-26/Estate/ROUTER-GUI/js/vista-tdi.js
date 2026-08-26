// Disegna la tabella e basta. Qui dentro non si fa aritmetica sugli indirizzi:
// l'unica cosa che questa classe chiede a Ip è int2dotted, che è formattazione,
// non calcolo. Chi ha deciso quale rotta vince è stato Tdi.cerca().
class VistaTdi {

  constructor(tabella, elVuota) {
    this.tab    = tabella;
    this.tbody  = tabella.querySelector('tbody');
    this.elVuota = elVuota;
    this.cbElimina = null;

    // Delega: i bottoni nascono e muoiono a ogni ridisegno, l'ascoltatore no.
    this.tbody.addEventListener('click', ev => {
      const b = ev.target.closest('button[data-i]');
      if (b && this.cbElimina) this.cbElimina(Number(b.dataset.i));
    });
  }

  onElimina(cb) { this.cbElimina = cb; }

  disegna(tdi, esito) {
    const rotte = tdi.elenco();

    this.tab.classList.toggle('simulata', !!esito);
    this.elVuota.hidden = rotte.length > 0;
    this.tbody.textContent = '';

    rotte.forEach((rt, i) => {
      const riga = esito ? esito.righe[i] : null;
      const tr = document.createElement('tr');

      if (esito) {
        if (rt === esito.scelta) tr.className = 'scelta';
        else if (esito.alternative.indexOf(rt) >= 0) tr.className = 'alt';
        else tr.className = 'no';
      }

      tr.appendChild(this._td(String(i + 1), 'num'));

      const tdRete = this._td(Ip.int2dotted(rt.rete), 'ind');
      if (esito && rt === esito.scelta) tdRete.appendChild(this._etichetta('scelta'));
      else if (esito) {
        const k = esito.alternative.indexOf(rt);
        if (k >= 0) tdRete.appendChild(this._etichetta('fallback ' + (k + 1)));
      }
      tr.appendChild(tdRete);

      tr.appendChild(this._td(Ip.int2dotted(rt.msk) + '  /' + rt.pfx, 'ind'));
      tr.appendChild(this._td(rt.connessa ? '— connessa' : Ip.int2dotted(rt.gw), 'ind'));
      tr.appendChild(this._td(rt.iface));
      tr.appendChild(this._td(String(rt.metr), 'num'));

      const tdAz = document.createElement('td');
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'mini';
      b.dataset.i = i;
      b.textContent = 'elimina';
      b.title = 'Elimina questa rotta';
      tdAz.appendChild(b);
      tr.appendChild(tdAz);

      this.tbody.appendChild(tr);

      // Il calcolo va su una riga tutta sua: in colonna starebbe stretto e
      // manderebbe la tabella in scroll orizzontale proprio sulla cosa che
      // interessa di più vedere.
      if (riga) this.tbody.appendChild(this._dettaglio(esito.ip, rt, riga, tr.className));
    });
  }

  // Il conto che il programma in C stampava con printf, qui scritto per esteso:
  // indirizzo AND netmask, e il confronto col valore della colonna Rete.
  _dettaglio(ip, rt, riga, cls) {
    const tr = document.createElement('tr');
    tr.className = 'dettaglio ' + cls;
    const td = document.createElement('td');
    td.colSpan = 7;
    td.className = 'verifica';

    td.appendChild(this._span('calc',
      Ip.int2dotted(ip) + ' & ' + Ip.int2dotted(rt.msk) + ' = ' + Ip.int2dotted(riga.and)));
    td.appendChild(this._span('segno', riga.esito ? ' = ' : ' ≠ '));
    td.appendChild(this._span('calc', Ip.int2dotted(rt.rete)));
    td.appendChild(this._span('esito ' + (riga.esito ? 'si' : 'no'),
      riga.esito ? '  ✓ regola compatibile' : '  ✗ regola non compatibile'));

    tr.appendChild(td);
    return tr;
  }

  _span(cls, testo) {
    const s = document.createElement('span');
    s.className = cls;
    s.textContent = testo;
    return s;
  }

  _td(testo, cls) {
    const td = document.createElement('td');
    td.textContent = testo;
    if (cls) td.className = cls;
    return td;
  }

  _etichetta(testo) {
    const s = document.createElement('span');
    s.className = 'etichetta';
    s.textContent = testo;
    return s;
  }
}
