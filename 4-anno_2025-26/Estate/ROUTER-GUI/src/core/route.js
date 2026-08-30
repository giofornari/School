// Route - una riga della Tabella di Instradamento

import { parseIp, formatIp, maskToPrefix } from './ip.js';

export class Route {
    constructor(network, mask, nextHop, iface, metric) {
        this.network = network;
        this.mask = mask;
        this.nextHop = nextHop; // null se la rete è direttamente connessa
        this.iface = iface;     // nome dell'interfaccia di uscita
        this.metric = metric;
        this.prefix = maskToPrefix(mask); // errore se la mask non è contigua

        const rete = this.applyMask(network);
        if (rete !== parseIp(network)) {
            throw new Error(`bit di host non a zero: forse intendevi ${formatIp(rete)}?`);
        }
        if (nextHop !== null) {
            parseIp(nextHop); // errore se il next hop non è un ip valido
        }
        if (!Number.isInteger(metric) || metric < 0) {
            throw new Error(`metrica non valida: ${JSON.stringify(metric)} (serve un intero magiore o uguale a 0)`);
        }
    }

    // ip AND mask, come intero senza segno
    applyMask(ip) {
        return (parseIp(ip) & parseIp(this.mask)) >>> 0; // & lavora con segno: >>> 0 lo toglie
    }

    matches(ip) {
        return this.applyMask(ip) === parseIp(this.network);
    }

    // "172.16.0.0/16 via 10.0.0.2 su eth1", usata nel motivo della scelta
    toString() {
        const via = this.nextHop === null ? 'diretta' : `via ${this.nextHop}`;
        return `${this.network}/${this.prefix} ${via} su ${this.iface}`;
    }
}
