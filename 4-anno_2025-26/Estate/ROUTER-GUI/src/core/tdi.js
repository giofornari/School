// TDI - Tabella di Instradamento

export class TDI {
    constructor() {
        this.routes = []; // in ordine di inserimento: a parità di prefisso e metrica vince la prima
    }

    // stessa rete, mask, next hop e interfaccia: è la stessa route anche con un'altra metrica
    // la stessa rete con un altro next hop invece serve come fallback
    addRoute(route) {
        for (const presente of this.routes) {
            const uguale = presente.network === route.network && presente.mask === route.mask
                && presente.nextHop === route.nextHop && presente.iface === route.iface;
            if (uguale) {
                throw new Error(`route gia presente: ${route}`);
            }
        }
        this.routes.push(route);
    }

    // l'indice arriva dalla riga della tabella
    removeRoute(indice) {
        this.routes.splice(indice, 1);
    }
}
