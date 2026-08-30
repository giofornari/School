// Storage - configurazione su file scaricato, file caricato e localStorage

import { toJson, fromJson } from './config.js';

const CHIAVE = 'router-gui'; // nome della voce in localStorage

// il browser scarica router-config.json con la configurazione attuale
export function download(router) {
    const link = document.createElement('a');
    link.href = 'data:application/json;charset=utf-8,' + encodeURIComponent(toJson(router));
    link.download = 'router-config.json';
    link.click();
}

// file scelto dall'utente con <input type="file">
export async function upload(file) {
    return fromJson(await file.text());
}

export function saveLocal(router) {
    localStorage.setItem(CHIAVE, toJson(router));
}

// null se non c'è niente di salvato, errore se il contenuto è corrotto
export function loadLocal() {
    const testo = localStorage.getItem(CHIAVE);
    return testo === null ? null : fromJson(testo);
}

export async function loadExample() {
    const risposta = await fetch('esempi/router-esempio.json'); // relativo: su pages il sito sta sotto /ROUTER-GUI/
    if (!risposta.ok) {
        throw new Error(`impossibile caricare l'esempio (errore ${risposta.status})`);
    }
    return fromJson(await risposta.text());
}
