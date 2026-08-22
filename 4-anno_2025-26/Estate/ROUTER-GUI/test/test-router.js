gruppo('Router, Iface, Pacchetto');

function routerEsempio() {
  const r = new Router('R1');
  r.aggIface(new Iface('eth0', Ip.dotted2int('196.13.1.1'), Ip.pfx2msk(24)));
  r.tdi.agg(Rotta.daDotted('196.13.1.0', '/24', '0.0.0.0',    'eth0',  1));
  r.tdi.agg(Rotta.daDotted('0.0.0.0',    '/0',  '196.13.1.254', 'eth0', 10));
  return r;
}

const r = routerEsempio();
const es = r.inoltra(new Pacchetto(0, Ip.dotted2int('196.13.1.9')));
eq('inoltra sceglie la rete connessa', es.scelta.pfx, 24);
ok('la rotta scelta è connessa', es.scelta.connessa);

const esFuori = r.inoltra(Pacchetto.daDotted('196.13.1.1', '8.8.8.8'));
eq('verso l\'esterno passa dalla default', esFuori.scelta.pfx, 0);

eq('risoluzione nome → interfaccia', r.iface('eth0').nome, 'eth0');
ok('interfaccia inesistente restituisce null', r.iface('eth9') === null);
lancia('interfaccia duplicata rifiutata',
       () => r.aggIface(new Iface('eth0', Ip.dotted2int('10.0.0.1'), Ip.pfx2msk(8))));

eq('ttl di default', new Pacchetto(0, 0).ttl, 64);
eq('ttl esplicito', new Pacchetto(0, 0, 5).ttl, 5);
eq('Pacchetto.daDotted converte', Pacchetto.daDotted('1.2.3.4', '5.6.7.8').dst,
   Ip.dotted2int('5.6.7.8'));

gruppo('Iface');

const eth = new Iface('eth0', Ip.dotted2int('196.13.1.1'), Ip.pfx2msk(24));
eq('pfx dell\'interfaccia', eth.pfx, 24);
ok('l\'interfaccia nasce su', eth.su);
ok('riconosce un indirizzo locale', eth.locale(Ip.dotted2int('196.13.1.200')));
ok('riconosce un indirizzo remoto', !eth.locale(Ip.dotted2int('196.13.2.1')));
lancia('interfaccia senza nome', () => new Iface('  ', 0, 0));
lancia('interfaccia con mask a buchi',
       () => new Iface('eth0', 0, Ip.dotted2int('255.0.255.0')));

gruppo('Router — serializzazione');

const rj = Router.daJSON(routerEsempio().toJSON());
eq('round-trip: nome', rj.nome, 'R1');
eq('round-trip: rotte', rj.tdi.elenco().length, 2);
eq('round-trip: interfacce', rj.ifaces.length, 1);
eq('round-trip: comportamento',
   rj.inoltra(new Pacchetto(0, Ip.dotted2int('196.13.1.9'))).scelta.pfx, 24);
lancia('daJSON su nulla', () => Router.daJSON(null));
