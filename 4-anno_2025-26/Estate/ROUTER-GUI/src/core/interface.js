// Interface - porta del router con indirizzo, netmask e stato up/down

import { parseIp, maskToPrefix } from './ip.js';

export class Interface {
    constructor(name, ip, mask, up) {
        if (typeof name !== 'string' || name.trim() === '') {
            throw new Error('nome dell\'interfaccia mancante');
        }
        parseIp(ip);        // errore se l'ip non è valido
        maskToPrefix(mask); // errore se la mask non è valida o non è contigua
        if (typeof up !== 'boolean') {
            throw new Error(`stato di ${name} non valido: up deve essere true o false`);
        }
        this.name = name;
        this.ip = ip;
        this.mask = mask;
        this.up = up;
    }
}
