gruppo('Tdi — Longest Prefix Match');

// La TDI dell'host A di pag. 129, più una rotta più specifica per vedere l'LPM
// fare davvero qualcosa.
function tdiEsempio() {
  const t = new Tdi();
  t.agg(Rotta.daDotted('0.0.0.0',    '/0',  '196.13.1.1', 'eth0', 10));
  t.agg(Rotta.daDotted('196.13.0.0', '/16', '196.13.1.1', 'eth0',  5));
  t.agg(Rotta.daDotted('196.13.2.0', '/24', '196.13.1.2', 'eth1',  5));
  return t;
}

const e = tdiEsempio().cerca(Ip.dotted2int('196.13.2.5'));
eq('righe: una per ogni rotta', e.righe.length, 3);
eq('vince la /24', e.scelta.pfx, 24);
eq('restano due alternative', e.alternative.length, 2);
eq('prima alternativa: la /16', e.alternative[0].pfx, 16);
eq('ultima alternativa: la default', e.alternative[1].pfx, 0);
ok('il motivo cita il prefisso vincente', e.motivo.indexOf('/24') >= 0);

const e2 = tdiEsempio().cerca(Ip.dotted2int('8.8.8.8'));
eq('fuori rete vince la default', e2.scelta.pfx, 0);
eq('la default non ha alternative', e2.alternative.length, 0);
eq('anche qui tutte le righe sono valutate', e2.righe.length, 3);
eq('due righe su tre non compatibili', e2.righe.filter(r => !r.esito).length, 2);

const e3 = tdiEsempio().cerca(Ip.dotted2int('196.13.9.9'));
eq('dentro la /16 ma fuori dalla /24 vince la /16', e3.scelta.pfx, 16);
eq('la default resta come unica alternativa', e3.alternative.length, 1);

gruppo('Tdi — prefisso contro metrica');

const pfxVsMetr = new Tdi();
pfxVsMetr.agg(Rotta.daDotted('192.168.0.0', '/16', '1.1.1.1', 'eth0',  1));
pfxVsMetr.agg(Rotta.daDotted('192.168.0.0', '/17', '2.2.2.2', 'eth1', 99));
eq('il prefisso batte la metrica',
   pfxVsMetr.cerca(Ip.dotted2int('192.168.1.1')).scelta.pfx, 17);

// Floating static route: stessa destinazione, gateway diversi. Qui, e solo qui,
// la metrica può decidere — due rotte con lo stesso prefisso che coprono lo
// stesso indirizzo hanno per forza stessa rete e stessa mask.
const tie = new Tdi();
tie.agg(Rotta.daDotted('10.0.0.0', '/8', '1.1.1.1', 'eth0', 20));
tie.agg(Rotta.daDotted('10.0.0.0', '/8', '2.2.2.2', 'eth1',  3));
const eTie = tie.cerca(Ip.dotted2int('10.1.2.3'));
eq('a parità di prefisso vince la metrica minore', Ip.int2dotted(eTie.scelta.gw), '2.2.2.2');
eq('l\'altra resta come fallback', Ip.int2dotted(eTie.alternative[0].gw), '1.1.1.1');
ok('il motivo spiega che ha deciso la metrica',
   eTie.motivo.toLowerCase().indexOf('metrica') >= 0);

// A parità di prefisso E di metrica decide l'ordine di inserimento: sort è
// stabile da ES2019.
const pari = new Tdi();
pari.agg(Rotta.daDotted('172.16.0.0', '/12', '9.9.9.9', 'eth0', 7));
pari.agg(Rotta.daDotted('172.16.0.0', '/12', '8.8.8.8', 'eth1', 7));
eq('a parità piena vince chi è stato inserito prima',
   Ip.int2dotted(pari.cerca(Ip.dotted2int('172.20.0.1')).scelta.gw), '9.9.9.9');

gruppo('Tdi — nessun match');

const senzaDefault = new Tdi();
senzaDefault.agg(Rotta.daDotted('10.0.0.0', '/8', '0.0.0.0', 'eth0', 1));
const e4 = senzaDefault.cerca(Ip.dotted2int('8.8.8.8'));
ok('senza default e senza match la scelta è nulla', e4.scelta === null);
eq('nessuna alternativa', e4.alternative.length, 0);
ok('il motivo dice irraggiungibile',
   e4.motivo.toLowerCase().indexOf('irraggiungibile') >= 0);

gruppo('Tdi — gestione della tabella');

lancia('rotta identica (stesso gateway) rifiutata', () => {
  const t = new Tdi();
  t.agg(Rotta.daDotted('10.0.0.0', '/8', '1.1.1.1', 'eth0', 1));
  t.agg(Rotta.daDotted('10.0.0.0', '/8', '1.1.1.1', 'eth0', 7));
});

const backup = new Tdi();
backup.agg(Rotta.daDotted('10.0.0.0', '/8', '1.1.1.1', 'eth0', 1));
backup.agg(Rotta.daDotted('10.0.0.0', '/8', '2.2.2.2', 'eth1', 9));
eq('stessa destinazione con gateway diverso è ammessa', backup.elenco().length, 2);

const daSvuotare = tdiEsempio();
daSvuotare.rimuovi(1);
eq('rimuovi toglie una riga', daSvuotare.elenco().length, 2);
eq('rimuovi toglie quella giusta', daSvuotare.elenco()[1].pfx, 24);
lancia('rimuovi con indice fuori tabella', () => daSvuotare.rimuovi(99));
daSvuotare.svuota();
ok('svuota lascia la tabella vuota', daSvuotare.vuota);

const copia = tdiEsempio().elenco();
copia.push('spazzatura');
eq('elenco restituisce una copia difensiva', tdiEsempio().elenco().length, 3);

gruppo('Tdi — serializzazione');

eq('round-trip JSON conserva le rotte',
   Tdi.daJSON(tdiEsempio().toJSON()).elenco().length, 3);
eq('round-trip JSON conserva il comportamento',
   Tdi.daJSON(tdiEsempio().toJSON()).cerca(Ip.dotted2int('196.13.2.5')).scelta.pfx, 24);
lancia('daJSON su qualcosa che non è un elenco', () => Tdi.daJSON({ rotte: [] }));
