// Simulator - componente Alpine della pagina: legge i form, chiama il core e salva ogni modifica

import { Route } from '../core/route.js';
import { Interface } from '../core/interface.js';
import { download, upload, saveLocal, loadExample } from '../persistence/storage.js';
import { formatRows } from './format.js';

// partenza: promise con { router, avviso } preparata da main.js
export function simulator(partenza) {
    return {
        router: null,
        avviso: '',      // messaggio in cima alla pagina, per esempio se la configurazione salvata era rovinata
        ip: '',          // campo della simulazione
        risultato: null, // ultimo lookup, null se non c'è una simulazione attiva
        righe: [],       // colori e badge delle righe, vuoto senza simulazione
        nuovaRoute: { network: '', mask: '', nextHop: '', iface: '', metric: 0 },
        nuovaIface: { name: '', ip: '', mask: '' },
        erroreSim: '',
        erroreRoute: '',
        erroreIface: '',
        erroreFile: '',

        async init() {
            const { router, avviso } = await partenza;
            this.router = router;
            this.avviso = avviso;
        },

        // i colori delle righe si preparano qui, così nell'html basta leggere righe[indice]
        run(ip) {
            const risultato = this.router.lookup(ip);
            this.righe = formatRows(risultato);
            this.risultato = risultato;
        },

        simulate() {
            try {
                this.run(this.ip);
                this.erroreSim = '';
            } catch (errore) {
                this.risultato = null; // con un ip sbagliato non resta la vecchia simulazione
                this.righe = [];
                this.erroreSim = errore.message;
            }
        },

        // dopo ogni modifica: rifà la simulazione attiva, così il fallback si vede subito, e salva nel browser
        changed() {
            if (this.risultato !== null) {
                this.run(this.risultato.ip);
            }
            try {
                saveLocal(this.router);
                this.avviso = ''; // la configurazione salvata adesso è di nuovo valida
            } catch {
                this.avviso = 'il browser non permette di salvare: ricaricando la pagina le modifiche si perdono';
            }
        },

        addRoute() {
            const { network, mask, nextHop, iface, metric } = this.nuovaRoute;
            if (iface === '') {
                this.erroreRoute = 'scegli un interfaccia di uscita';
                return;
            }
            try {
                // next hop vuoto: rete direttamente connessa
                this.router.addRoute(new Route(network, mask, nextHop === '' ? null : nextHop, iface, metric));
            } catch (errore) {
                this.erroreRoute = errore.message;
                return;
            }
            this.erroreRoute = '';
            this.nuovaRoute = { network: '', mask: '', nextHop: '', iface: '', metric: 0 };
            this.changed();
        },

        // l'indice è quello della riga, che segue l'ordine della tdi
        removeRoute(indice) {
            this.router.tdi.removeRoute(indice);
            this.changed();
        },

        addInterface() {
            const { name, ip, mask } = this.nuovaIface;
            try {
                this.router.addInterface(new Interface(name, ip, mask, true)); // una nuova interfaccia parte up
            } catch (errore) {
                this.erroreIface = errore.message;
                return;
            }
            this.erroreIface = '';
            this.nuovaIface = { name: '', ip: '', mask: '' };
            this.changed();
        },

        removeInterface(name) {
            try {
                this.router.removeInterface(name);
            } catch (errore) {
                this.erroreIface = errore.message;
                return;
            }
            this.erroreIface = '';
            this.changed();
        },

        toggle(iface) {
            iface.up = !iface.up;
            this.changed();
        },

        save() {
            download(this.router);
        },

        async load(evento) {
            const input = evento.target;
            try {
                this.router = await upload(input.files[0]); // se il file è sbagliato il router attuale resta com'è
                this.erroreFile = '';
                this.changed();
            } catch (errore) {
                this.erroreFile = errore.message;
            }
            input.value = ''; // così si può ricaricare anche lo stesso file
        },

        async restore() {
            try {
                this.router = await loadExample();
                this.erroreFile = '';
                this.changed();
            } catch (errore) {
                this.erroreFile = errore.message;
            }
        },
    };
}
