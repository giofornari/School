// Salvataggio e caricamento della configurazione.
//
// Una pagina web non può scrivere su disco: non esiste API per sovrascrivere un
// file. Si salva generando un Blob e simulando il click su un link con
// l'attributo download, si carica con un <input type="file"> e una FileReader.
// localStorage non è un file e quindi non conta.
//
// Si serializza il Router intero, non la sola TDI: cosi' il futuro formato
// multi-router ({versione:2, routers:[...], links:[...]}) sarà un superset di
// questo, e i file salvati oggi continueranno a caricarsi con un if sulla versione.
const Persistenza = {

  VERSIONE: 1,

  serializza(router) {
    return { versione: Persistenza.VERSIONE, router: router.toJSON() };
  },

  deserializza(o) {
    if (!o || typeof o !== 'object') throw new Error('il file non contiene un oggetto JSON');
    if (o.versione !== Persistenza.VERSIONE) {
      throw new Error('versione del file non supportata: ' + o.versione +
                      ' (questa applicazione legge la ' + Persistenza.VERSIONE + ')');
    }
    if (!o.router) throw new Error('il file non contiene un router');
    return Router.daJSON(o.router);
  },

  esporta(router, nomeFile) {
    const testo = JSON.stringify(Persistenza.serializza(router), null, 2);
    const url = URL.createObjectURL(new Blob([testo], { type: 'application/json' }));
    const a = document.createElement('a');
    a.href = url;
    a.download = nomeFile || 'config.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  },

  importa(file) {
    return new Promise((risolvi, rifiuta) => {
      const fr = new FileReader();
      fr.onerror = () => rifiuta(new Error('impossibile leggere il file'));
      fr.onload = () => {
        try {
          risolvi(Persistenza.deserializza(JSON.parse(fr.result)));
        } catch (e) {
          rifiuta(new Error('file non valido: ' + e.message));
        }
      };
      fr.readAsText(file);
    });
  }
};
