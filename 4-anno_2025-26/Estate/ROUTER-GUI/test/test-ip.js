gruppo('Ip — conversione');

eq('dotted2int 0.0.0.0', Ip.dotted2int('0.0.0.0'), 0);
eq('dotted2int 192.168.1.1', Ip.dotted2int('192.168.1.1'), 3232235777);
eq('dotted2int 255.255.255.255 resta positivo', Ip.dotted2int('255.255.255.255'), 4294967295);
eq('int2dotted 0', Ip.int2dotted(0), '0.0.0.0');
eq('int2dotted round-trip', Ip.int2dotted(Ip.dotted2int('196.13.2.5')), '196.13.2.5');
eq('int2dotted non si fa ingannare dal segno', Ip.int2dotted(-1), '255.255.255.255');
eq('dotted2int tollera gli spazi', Ip.dotted2int('  10.0.0.1  '), Ip.dotted2int('10.0.0.1'));

gruppo('Ip — input malformato');

lancia('ottetto fuori range', () => Ip.dotted2int('256.1.1.1'));
lancia('troppo pochi ottetti', () => Ip.dotted2int('1.2.3'));
lancia('troppi ottetti', () => Ip.dotted2int('1.2.3.4.5'));
lancia('ottetti non numerici', () => Ip.dotted2int('a.b.c.d'));
lancia('ottetto vuoto', () => Ip.dotted2int('1..3.4'));
lancia('stringa vuota', () => Ip.dotted2int(''));

gruppo('Ip — netmask');

eq('msk2pfx /0', Ip.msk2pfx(Ip.dotted2int('0.0.0.0')), 0);
eq('msk2pfx /8', Ip.msk2pfx(Ip.dotted2int('255.0.0.0')), 8);
eq('msk2pfx /17', Ip.msk2pfx(Ip.dotted2int('255.255.128.0')), 17);
eq('msk2pfx /24', Ip.msk2pfx(Ip.dotted2int('255.255.255.0')), 24);
eq('msk2pfx /32', Ip.msk2pfx(Ip.dotted2int('255.255.255.255')), 32);

eq('pfx2msk 0', Ip.pfx2msk(0), 0);
eq('pfx2msk 24', Ip.pfx2msk(24), Ip.dotted2int('255.255.255.0'));
eq('pfx2msk 32', Ip.pfx2msk(32), 4294967295);
eq('pfx2msk e msk2pfx sono inverse', Ip.msk2pfx(Ip.pfx2msk(19)), 19);
lancia('prefisso /33', () => Ip.pfx2msk(33));
lancia('prefisso negativo', () => Ip.pfx2msk(-1));

ok('mask contigua accettata', Ip.mskValida(Ip.dotted2int('255.255.128.0')));
ok('mask tutta a 1 accettata', Ip.mskValida(Ip.dotted2int('255.255.255.255')));
ok('mask tutta a 0 accettata', Ip.mskValida(0));
ok('mask con buchi rifiutata', !Ip.mskValida(Ip.dotted2int('255.0.255.0')));
ok('mask 0.255.0.0 rifiutata', !Ip.mskValida(Ip.dotted2int('0.255.0.0')));
lancia('msk2pfx su mask con buchi', () => Ip.msk2pfx(Ip.dotted2int('255.0.255.0')));

gruppo('Ip — parseMsk');

eq('parseMsk dotted', Ip.parseMsk('255.255.255.0'), Ip.pfx2msk(24));
eq('parseMsk /24', Ip.parseMsk('/24'), Ip.pfx2msk(24));
eq('parseMsk 24 nudo', Ip.parseMsk('24'), Ip.pfx2msk(24));
eq('parseMsk /0', Ip.parseMsk('/0'), 0);
lancia('parseMsk /33', () => Ip.parseMsk('/33'));
lancia('parseMsk vuota', () => Ip.parseMsk('   '));
lancia('parseMsk dotted con buchi', () => Ip.parseMsk('255.0.255.0'));
