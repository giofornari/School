// Config - conversione tra il json della configurazione e il router

import { Router } from '../core/router.js';
import { Interface } from '../core/interface.js';
import { Route } from '../core/route.js';

// campi copiati uno per uno: nel file non devono finire prefix o la struttura interna della tdi
export function toJson(router) {
    const dati = {
        name: router.name,
        interfaces: router.interfaces.map(iface => ({ name: iface.name, ip: iface.ip, mask: iface.mask, up: iface.up })),
        routes: router.tdi.routes.map(route => ({
            network: route.network,
            mask: route.mask,
            nextHop: route.nextHop,
            iface: route.iface,
            metric: route.metric,
        })),
    };
    return JSON.stringify(dati, null, 4);
}

// costruisce un router nuovo: se una voce è sbagliata si ferma e quello attuale resta com'è
export function fromJson(testo) {
    let dati;
    try {
        dati = JSON.parse(testo);
    } catch {
        throw new Error('il file non e un json valido');
    }
    if (dati === null || !Array.isArray(dati.interfaces) || !Array.isArray(dati.routes)) {
        throw new Error('configurazione non valida: servono name, interfaces e routes');
    }

    const router = new Router(dati.name);
    // prima le interfacce, perché le route le cercano per nome
    for (let i = 0; i < dati.interfaces.length; i++) {
        const voce = dati.interfaces[i] ?? {}; // con una voce null l'errore sarà sul campo mancante
        try {
            router.addInterface(new Interface(voce.name, voce.ip, voce.mask, voce.up));
        } catch (errore) {
            throw new Error(`interfaccia ${i + 1}: ${errore.message}`);
        }
    }
    for (let i = 0; i < dati.routes.length; i++) {
        const voce = dati.routes[i] ?? {};
        try {
            router.addRoute(new Route(voce.network, voce.mask, voce.nextHop, voce.iface, voce.metric));
        } catch (errore) {
            throw new Error(`route ${i + 1}: ${errore.message}`);
        }
    }
    return router;
}
