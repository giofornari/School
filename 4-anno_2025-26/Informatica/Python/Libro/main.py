from catalogo import Catalogo
from dvd import DVD
from ebook import EBook
from libro import Libro
from rivista import Rivista

cat = Catalogo()

cat.aggiungi(Libro("il nome della rosa", 1980, "umberto eco", 512))
cat.aggiungi(Rivista("national geographic", 2024, 1, "gennaio"))
cat.aggiungi(DVD("interstellar", 2014, "christopher nolan", 169))
cat.aggiungi(EBook("clean code", 2008, "PDF", 2.5))

cat.stampa_catalogo()
print()
print(cat.articoli[0].prestito())
print(cat.articoli[3].prestito())
cat.report()
cat.articoli[3].statistiche()