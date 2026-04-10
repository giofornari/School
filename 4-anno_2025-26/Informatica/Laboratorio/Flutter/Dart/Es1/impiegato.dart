import 'dipendente.dart';

// classe impiegato
class Impiegato extends Dipendente {
  int liv;

  Impiegato(String n, String s, DateTime d, this.liv, double sb)
    : super(n, s, d, sb);

  int get livello => liv;

  @override
  double calcolStipEffettivo() {
    // stipendio base impiegato
    return stBase;
  }

  @override
  String toString() {
    return 'Impiegato{${super.toString()}, livello: $liv, stip_eff: ${calcolStipEffettivo()}}';
  }
}
