gruppo('Persistenza');

// esporta() e importa() aprono un download e leggono un file: non sono testabili
// senza un utente che clicchi. Serializzazione e deserializzazione — cioè tutta
// la logica vera — invece si'.
function routerDaSalvare() {
  const r = new Router('R1');
  r.aggIface(new Iface('eth0', Ip.dotted2int('10.0.0.1'), Ip.pfx2msk(24)));
  r.tdi.agg(Rotta.daDotted('10.0.0.0', '/24', '0.0.0.0',  'eth0', 1));
  r.tdi.agg(Rotta.daDotted('0.0.0.0',  '/0',  '10.0.0.254', 'eth0', 10));
  return r;
}

const o = Persistenza.serializza(routerDaSalvare());
eq('versione presente', o.versione, 1);
eq('il router è dentro', o.router.nome, 'R1');
eq('gli indirizzi sono salvati in dotted', o.router.tdi[0].rete, '10.0.0.0');
eq('anche le mask sono in dotted', o.router.tdi[0].msk, '255.255.255.0');
ok('il JSON è davvero serializzabile', typeof JSON.stringify(o) === 'string');

const r2 = Persistenza.deserializza(JSON.parse(JSON.stringify(o)));
eq('round-trip: nome', r2.nome, 'R1');
eq('round-trip: rotte', r2.tdi.elenco().length, 2);
eq('round-trip: interfacce', r2.ifaces.length, 1);
eq('round-trip: lookup funziona ancora',
   r2.inoltra(new Pacchetto(0, Ip.dotted2int('10.0.0.5'))).scelta.pfx, 24);

lancia('versione ignota rifiutata',
       () => Persistenza.deserializza({ versione: 99, router: {} }));
lancia('router mancante rifiutato', () => Persistenza.deserializza({ versione: 1 }));
lancia('oggetto nullo rifiutato', () => Persistenza.deserializza(null));
lancia('stringa al posto dell\'oggetto', () => Persistenza.deserializza('ciao'));
lancia('tabella corrotta nel file',
       () => Persistenza.deserializza({ versione: 1, router: { nome: 'R1', tdi: [{ rete: '999.1.1.1' }] } }));
