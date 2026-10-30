// Avvio - sceglie la configurazione di partenza e registra il componente Alpine

import { Router } from './core/router.js';
import { loadLocal, loadExample } from './persistence/storage.js';
import { simulator } from './ui/simulator.js';

// prima quella salvata nel browser, se non c'è l'esempio
async function start() {
    let avviso = '';
    try {
        const router = loadLocal();
        if (router !== null) {
            return { router, avviso };
        }
    } catch {
        avviso = 'la configurazone salvata nel browser non era valida: al suo posto c\'è l\'esempio';
    }
    try {
        return { router: await loadExample(), avviso };
    } catch (errore) {
        // senza un router la pagina resterebbe vuota: così si può almeno caricare un file
        return { router: new Router('R1'), avviso: `${errore.message}: si parte da un router vuoto` };
    }
}

const partenza = start(); // parte subito, il componente aspetta il risultato nel suo init

// main.js è caricato prima di Alpine, quindi il listener c'è già quando Alpine parte
document.addEventListener('alpine:init', () => {
    Alpine.data('simulator', () => simulator(partenza));
});
