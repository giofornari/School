// Format - colori, badge e calcolo di ogni riga della TDI, presi dal risultato di router.lookup

// le classi sono scritte per intero: tailwind trova solo quelle che compaiono così nei file di src/ui
export function formatRows(risultato) {
    const righe = []; // una per route, nello stesso ordine della tdi
    for (const { route, rete, compatibile } of risultato.controlli) {
        const riga = {
            calcolo: `${risultato.ip} and ${route.mask} = ${rete}`,
            esito: compatibile ? '✓' : '✗',
            classe: 'text-slate-400', // grigio: non compatibile
            badge: '',
            classeBadge: '',
        };
        if (route === risultato.scelta) {
            riga.classe = 'bg-green-100';
            riga.badge = 'scelta';
            riga.classeBadge = 'bg-green-600 text-white';
        } else if (risultato.scartate.includes(route)) {
            riga.classe = 'text-slate-400 line-through';
            riga.badge = 'interfaccia down';
            riga.classeBadge = 'bg-red-100 text-red-700';
        } else if (compatibile) {
            // compatibile, non scelta e con interfaccia up: è un fallback
            riga.classe = 'bg-amber-50';
            riga.badge = `fallback ${risultato.fallback.indexOf(route) + 1}`;
            riga.classeBadge = 'bg-amber-400 text-amber-950';
        }
        righe.push(riga);
    }
    return righe;
}
