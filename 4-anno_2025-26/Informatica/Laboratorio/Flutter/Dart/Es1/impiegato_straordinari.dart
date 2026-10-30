import 'impiegato.dart';

// classe impiegato con straordinari
class ImpiegatoStraordinari extends Impiegato {
  static double tariffaOraria = 15.0; // stessa per tutti
  double oreStraord;

  ImpiegatoStraordinari(
    String n,
    String s,
    DateTime d,
    int l,
    double sb,
    this.oreStraord,
  ) : super(n, s, d, l, sb);

  double get oreStraordinari => oreStraord;
  static double get tariffaOraria_ => tariffaOraria;

  static void setTariffaOraria(double t) {
    tariffaOraria = t;
  }

  @override
  double calcolStipEffettivo() {
    // stipendio base + straordinari
    return stBase + (oreStraord * tariffaOraria);
  }

  @override
  String toString() {
    return 'Straord{${super.toString()}, ore_str: $oreStraord, tar_or: $tariffaOraria, stip_eff: ${calcolStipEffettivo()}}';
  }
}
