gruppo('Rotta');

const r24 = Rotta.daDotted('192.168.1.0', '255.255.255.0', '0.0.0.0', 'eth0', 1);
const def = Rotta.daDotted('0.0.0.0', '0.0.0.0', '192.168.1.254', 'eth0', 10);

eq('pfx di una /24', r24.pfx, 24);
eq('pfx della default', def.pfx, 0);
ok('gateway 0.0.0.0 = rete connessa', r24.connessa);
ok('la default non è connessa', !def.connessa);

ok('copre un indirizzo interno', r24.copre(Ip.dotted2int('192.168.1.77')));
ok('copre il proprio indirizzo di rete', r24.copre(Ip.dotted2int('192.168.1.0')));
ok('non copre un\'altra rete', !r24.copre(Ip.dotted2int('192.168.2.77')));
ok('la default copre tutto', def.copre(Ip.dotted2int('8.8.8.8')));
ok('la default copre anche 0.0.0.0', def.copre(0));
ok('la default copre anche il broadcast', def.copre(Ip.dotted2int('255.255.255.255')));

gruppo('Rotta — calcolo esposto alla GUI');

const c = r24.calcolo(Ip.dotted2int('192.168.1.77'));
eq('calcolo espone l\'AND', Ip.int2dotted(c.and), '192.168.1.0');
eq('calcolo espone la rete', Ip.int2dotted(c.rete), '192.168.1.0');
ok('calcolo espone l\'esito', c.esito === true);

const c2 = r24.calcolo(Ip.dotted2int('10.0.0.1'));
eq('AND su indirizzo esterno', Ip.int2dotted(c2.and), '10.0.0.0');
ok('esito falso su indirizzo esterno', c2.esito === false);

gruppo('Rotta — confronti');

ok('stessaDest vero anche con gw diverso',
   r24.stessaDest(Rotta.daDotted('192.168.1.0', '/24', '1.1.1.1', 'eth9', 5)));
ok('stessaDest falso se cambia la mask',
   !r24.stessaDest(Rotta.daDotted('192.168.1.0', '/25', '0.0.0.0', 'eth0', 1)));
ok('identicaA falso se cambia il gateway',
   !r24.identicaA(Rotta.daDotted('192.168.1.0', '/24', '1.1.1.1', 'eth9', 5)));
ok('identicaA vero a parità di rete, mask e gateway',
   r24.identicaA(Rotta.daDotted('192.168.1.0', '/24', '0.0.0.0', 'eth1', 9)));

gruppo('Rotta — validazione');

lancia('mask con buchi rifiutata dal costruttore',
       () => Rotta.daDotted('10.0.0.0', '255.0.255.0', '0.0.0.0', 'eth0', 1));
lancia('bit accesi fuori dalla mask rifiutati',
       () => Rotta.daDotted('192.168.1.77', '255.255.255.0', '0.0.0.0', 'eth0', 1));
lancia('metrica negativa rifiutata',
       () => Rotta.daDotted('10.0.0.0', '/8', '0.0.0.0', 'eth0', -3));
lancia('interfaccia vuota rifiutata',
       () => Rotta.daDotted('10.0.0.0', '/8', '0.0.0.0', '  ', 1));

gruppo('Rotta — serializzazione');

const j = r24.toJSON();
eq('toJSON scrive in dotted', j.rete, '192.168.1.0');
eq('toJSON scrive la mask in dotted', j.msk, '255.255.255.0');
eq('toJSON conserva la metrica', j.metr, 1);
ok('round-trip JSON', Rotta.daJSON(j).copre(Ip.dotted2int('192.168.1.5')));
eq('round-trip conserva il gateway', Rotta.daJSON(def.toJSON()).gw, def.gw);
