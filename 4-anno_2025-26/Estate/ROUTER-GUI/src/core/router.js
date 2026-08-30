// Router - interfacce, TDI e scelta della route con Longest Prefix Match

import { parseIp, formatIp } from './ip.js';
import { TDI } from './tdi.js';

export class Router {
    constructor(name) {
        if (typeof name !== 'string' || name.trim() === '') {
            throw new Error('nome del router mancante');
        }
        this.name = name;
        this.interfaces = [];
        this.tdi = new TDI();
    }

    findInterface(name) {
        return this.interfaces.find(iface => iface.name === name);
    }

    addInterface(iface) {
        if (this.findInterface(iface.name)) {
            throw new Error(`interfaccia ${iface.name} già presente`);
        }
        this.interfaces.push(iface);
    }

    removeInterface(name) {
        for (const route of this.tdi.routes) {
            if (route.iface === name) {
                throw new Error(`l'interfaccia ${name} è usata da una route: elimina prima la route`);
            }
        }
        this.interfaces = this.interfaces.filter(iface => iface.name !== name);
    }

    // la TDI non conosce le interfacce: il controllo spetta al router
    addRoute(route) {
        if (!this.findInterface(route.iface)) {
            throw new Error(`interfaccia ${route.iface} inesistente`);
        }
        this.tdi.addRoute(route);
    }

    lookup(ip) {
        parseIp(ip); // errore se l'ip non è valido, anche con la TDI vuota
        const controlli = [];
        const usable = [];   // compatibili con interfaccia up
        const scartate = []; // compatibili con interfaccia down
        for (const route of this.tdi.routes) {
            const compatibile = route.matches(ip);
            controlli.push({ route, rete: formatIp(route.applyMask(ip)), compatibile });
            if (!compatibile) {
                continue;
            }
            if (this.findInterface(route.iface).up) {
                usable.push(route);
            } else {
                scartate.push(route);
            }
        }

        // prefisso più lungo, poi metrica più bassa; sort è stabile, quindi a parità resta l'ordine della TDI
        usable.sort((a, b) => b.prefix - a.prefix || a.metric - b.metric);
        const scelta = usable.length > 0 ? usable[0] : null;

        return {
            ip,
            controlli,
            scelta,
            fallback: usable.slice(1),
            scartate,
            motivo: explain(ip, scelta, usable, scartate),
        };
    }
}

// spiega in italiano cosa ha deciso la scelta; usable è già in ordine di preferenza
function explain(ip, scelta, usable, scartate) {
    let motivo;
    if (scelta === null && scartate.length === 0) {
        motivo = `nessuna route compatibile con ${ip}: il pachetto non può essere inoltrato.`;
    } else if (scelta === null) {
        motivo = `nessuna route usabile per ${ip}: il pachetto non può essere inoltrato.`;
    } else if (usable.length === 1) {
        motivo = `scelta ${scelta}: è l'unica route usabile.`;
    } else {
        const prefisso = scelta.prefix;
        const metrica = scelta.metric;
        let samePrefix = 0; // route usabili con lo stesso prefisso della scelta, lei compresa
        let sameMetric = 0; // di queste, quante hanno anche la stessa metrica
        for (const route of usable) {
            if (route.prefix === prefisso) {
                samePrefix++;
                if (route.metric === metrica) {
                    sameMetric++;
                }
            }
        }
        if (samePrefix === 1) {
            motivo = `scelta ${scelta}: ha il prefisso più lungo (/${prefisso}) tra ${usable.length} route usabili.`;
        } else if (sameMetric === 1) {
            motivo = `scelta ${scelta}: ${samePrefix} route usabili hanno il prefisso più lungo (/${prefisso}), decide la metrica più bassa (${metrica}).`;
        } else {
            motivo = `scelta ${scelta}: tra le ${samePrefix} route usabili con prefisso /${prefisso}, ${sameMetric} hanno la metrica più bassa (${metrica}): a parità decide l'ordine di inserimento nella tdi.`;
        }
    }
    if (scartate.length > 0) {
        motivo += ` route scartate per interfaccia down: ${scartate.join(', ')}.`;
    }
    return motivo;
}
