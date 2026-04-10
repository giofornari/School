// classe astratta base dipendenti
abstract class Dipendente {
  String nom;
  String sesso;
  DateTime dataN;
  double stBase;

  Dipendente(this.nom, this.sesso, this.dataN, this.stBase);

  String get nome => nom;
  String get genere => sesso;
  DateTime get dataNascita => dataN;
  double get stipBase => stBase;

  double calcolStipEffettivo();

  @override
  String toString() {
    return 'nom: $nom, sesso: $sesso, data: ${dataN.year}-${dataN.month.toString().padLeft(2, '0')}-${dataN.day.toString().padLeft(2, '0')}, stip.base: $stBase';
  }
}
