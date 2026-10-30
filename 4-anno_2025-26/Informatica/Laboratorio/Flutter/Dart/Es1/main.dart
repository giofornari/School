import 'dipendente.dart';
import 'docente.dart';
import 'impiegato.dart';
import 'impiegato_straordinari.dart';

void _printDipendente(int idx, Dipendente d) {
  print('$idx. ${d.runtimeType}:');
  print('   $d');
}

void main() {
  final doc1 = Docente('Marco Rossi', 'M', DateTime(1980, 5, 15), 18.0, 2000.0);
  final imp1 = Impiegato('Anna Bianchi', 'F', DateTime(1985, 8, 22), 3, 1500.0);
  final impstr1 = ImpiegatoStraordinari(
    'Luigi Verdi',
    'M',
    DateTime(1990, 3, 10),
    2,
    1800.0,
    8.5,
  );
  final impstr2 = ImpiegatoStraordinari(
    'Giovanna Rossi',
    'F',
    DateTime(1995, 12, 5),
    1,
    1600.0,
    5.0,
  );

  _printDipendente(1, doc1);
  _printDipendente(2, imp1);
  _printDipendente(3, impstr1);

  ImpiegatoStraordinari.setTariffaOraria(18.0);
  print('\n3B nuova tariffa 18.0: ${impstr1.calcolStipEffettivo()}\n');

  _printDipendente(4, impstr2);

  print('\nstipendi:');
  [doc1, imp1, impstr1, impstr2].forEach(
    (d) => print('${d.nome} ${d.calcolStipEffettivo().toStringAsFixed(2)}'),
  );
}
