import 'dipendente.dart';

// classe docente
class Docente extends Dipendente {
  double oreDoc;

  Docente(String n, String s, DateTime d, this.oreDoc, double sb)
    : super(n, s, d, sb);

  double get oreDocenza => oreDoc;

  @override
  double calcolStipEffettivo() {
    // stipendio base docente
    return stBase;
  }

  @override
  String toString() {
    return 'Docente{${super.toString()}, ore_doc: $oreDoc, stip_eff: ${calcolStipEffettivo()}}';
  }
}
