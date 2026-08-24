// Controller: tiene il router, collega le viste al dominio, ridisegna.
// Nessuna aritmetica sugli indirizzi nemmeno qui — al massimo si chiede a Ip di
// convertire cio' che l'utente ha digitato, che e' lettura di input.
const App = {

  router: null,
  vTdi: null,
  vSim: null,
  ultimoEsito: null,

  avvia() {
    this.router = App.esempio();

    this.vTdi = new VistaTdi(document.getElementById('tab-tdi'),
                             document.getElementById('tdi-vuota'));
    this.vSim = new VistaSim(document.getElementById('form-sim'),
                             document.getElementById('in-dest'),
                             document.getElementById('esito'),
                             document.getElementById('err-sim'));

    this.vTdi.onElimina(i => {
      this.router.tdi.rimuovi(i);
      this.scordaEsito();
      this.ridisegna();
    });

    this.vSim.onSimula(testo => {
      try {
        const pkt = new Pacchetto(0, Ip.dotted2int(testo));
        this.ultimoEsito = this.router.inoltra(pkt);
        this.vSim.mostra(this.ultimoEsito);
        this.ridisegna();
      } catch (e) {
        this.vSim.errore('Indirizzo non valido: ' + e.message);
      }
    });

    document.getElementById('form-rotta').addEventListener('submit', ev => {
      ev.preventDefault();
      this.aggiungiRotta();
    });

    document.getElementById('b-salva').addEventListener('click', () => {
      Persistenza.esporta(this.router, 'router-' + this.router.nome + '.json');
      this.nota('Configurazione scaricata.');
    });

    document.getElementById('b-carica').addEventListener('click', () => {
      document.getElementById('in-file').click();
    });

    document.getElementById('in-file').addEventListener('change', ev => {
      const f = ev.target.files[0];
      if (!f) return;
      Persistenza.importa(f)
        .then(r => {
          this.router = r;
          this.scordaEsito();
          this.ridisegna();
          this.nota('Caricata la configurazione di ' + r.nome + '.');
        })
        .catch(e => this.nota('Caricamento fallito: ' + e.message + ' — la tabella attuale resta com\'era.'));
      // Cosi' ricaricare due volte lo stesso file rilancia l'evento change.
      ev.target.value = '';
    });

    document.getElementById('b-esempio').addEventListener('click', () => {
      this.router = App.esempio();
      this.scordaEsito();
      this.ridisegna();
      this.nota('Caricata la tabella d\'esempio.');
    });

    document.getElementById('b-svuota').addEventListener('click', () => {
      this.router.tdi.svuota();
      this.scordaEsito();
      this.ridisegna();
    });

    this.ridisegna();
  },

  aggiungiRotta() {
    const err = document.getElementById('err-rotta');
    try {
      this.router.tdi.agg(Rotta.daDotted(
        document.getElementById('in-rete').value,
        document.getElementById('in-msk').value,
        document.getElementById('in-gw').value,
        document.getElementById('in-iface').value,
        document.getElementById('in-metr').value
      ));
      err.hidden = true;
      document.getElementById('in-rete').value = '';
      document.getElementById('in-msk').value = '';
      document.getElementById('in-gw').value = '0.0.0.0';
      document.getElementById('in-rete').focus();
      this.scordaEsito();
      this.ridisegna();
    } catch (e) {
      err.textContent = e.message;
      err.hidden = false;
    }
  },

  // Dopo ogni modifica alla tabella l'evidenziazione precedente non vuol piu'
  // dire niente: meglio toglierla che lasciare colori che mentono.
  scordaEsito() {
    this.ultimoEsito = null;
    this.vSim.pulisci();
  },

  ridisegna() { this.vTdi.disegna(this.router.tdi, this.ultimoEsito); },

  nota(msg) {
    const el = document.getElementById('msg-file');
    el.textContent = msg;
    el.hidden = false;
  },

  // La TDI di pag. 129 (default route + rete connessa) piu' le righe che quel
  // programma non poteva esprimere: una destinazione raggiungibile per due strade
  // diverse, dove a decidere e' la metrica.
  esempio() {
    const r = new Router('R1');
    r.aggIface(new Iface('eth0', Ip.dotted2int('196.13.1.1'), Ip.pfx2msk(24)));
    r.aggIface(new Iface('eth1', Ip.dotted2int('196.13.5.1'), Ip.pfx2msk(24)));

    r.tdi.agg(Rotta.daDotted('196.13.1.0', '/24', '0.0.0.0',      'eth0',  1));
    r.tdi.agg(Rotta.daDotted('196.13.5.0', '/24', '0.0.0.0',      'eth1',  1));
    r.tdi.agg(Rotta.daDotted('196.13.2.0', '/24', '196.13.1.2',   'eth0',  5));
    r.tdi.agg(Rotta.daDotted('196.13.2.0', '/24', '196.13.5.2',   'eth1', 20));
    r.tdi.agg(Rotta.daDotted('0.0.0.0',    '/0',  '196.13.1.254', 'eth0', 10));
    return r;
  }
};

document.addEventListener('DOMContentLoaded', () => App.avvia());
