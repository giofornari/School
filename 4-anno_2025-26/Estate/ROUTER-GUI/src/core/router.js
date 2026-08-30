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
        const utilizzabili = []; // compatibili con interfaccia up
        const scartate = [];     // compatibili con interfaccia down
        for (const route of this.tdi.routes) {
            const compatibile = route.matches(ip);
            controlli.push({ route, rete: formatIp(route.applyMask(ip)), compatibile });
            if (!compatibile) {
                continue;
            }
            if (this.findInterface(route.iface).up) {
                utilizzabili.push(route);
            } else {
                scartate.push(route);
            }
        }

        // prefisso più lungo, poi metrica più bassa; sort è stabile, quindi a parità resta l'ordine della TDI
        utilizzabili.sort((a, b) => b.prefix - a.prefix || a.metric - b.metric);
        const scelta = utilizzabili.length > 0 ? utilizzabili[0] : null;

        return {
            ip,
            controlli,
            scelta,
            fallback: utilizzabili.slice(1),
            scartate,
            motivo: explain(ip, scelta, utilizzabili, scartate),
        };
    }
}

// spiega in italiano cosa ha deciso la scelta; utilizzabili è già in ordine di preferenza
function explain(ip, scelta, utilizzabili, scartate) {
    let motivo;
    if (scelta === null && scartate.length === 0) {
        motivo = `Nessuna route compatibile con ${ip}: il pacchetto non può essere inoltrato.`;
    } else if (scelta === null) {
        motivo = `Nessuna route utilizzabile per ${ip}: il pacchetto non può essere inoltrato.`;
    } else if (utilizzabili.length === 1) {
        motivo = `Scelta ${scelta}: è l'unica route utilizzabile.`;
    } else {
        const prefisso = scelta.prefix;
        const metrica = scelta.metric;
        let pariPrefisso = 0; // utilizzabili con lo stesso prefisso della scelta, lei compresa
        let pariMetrica = 0;  // di queste, quante hanno anche la stessa metrica
        for (const route of utilizzabili) {
            if (route.prefix === prefisso) {
                pariPrefisso++;
                if (route.metric === metrica) {
                    pariMetrica++;
                }
            }
        }
        if (pariPrefisso === 1) {
            motivo = `Scelta ${scelta}: ha il prefisso più lungo (/${prefisso}) tra ${utilizzabili.length} route utilizzabili.`;
        } else if (pariMetrica === 1) {
            motivo = `Scelta ${scelta}: ${pariPrefisso} route hanno il prefisso più lungo (/${prefisso}), decide la metrica più bassa (${metrica}).`;
        } else {
            motivo = `Scelta ${scelta}: tra le ${pariPrefisso} route con prefisso /${prefisso}, ${pariMetrica} hanno la metrica più bassa (${metrica}): vince la prima inserita nella TDI.`;
        }
    }
    if (scartate.length > 0) {
        motivo += ` Route scartate per interfaccia down: ${scartate.join(', ')}.`;
    }
    return motivo;
}
