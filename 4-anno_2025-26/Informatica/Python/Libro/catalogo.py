from dvd import DVD
from ebook import EBook
from libro import Libro
from rivista import Rivista


class Catalogo:
    def __init__(self):
        self.articoli = []

    def aggiungi(self, item):
        self.articoli.append(item)

    def stampa_catalogo(self):
        for item in self.articoli:
            print(item)

    def disponibili(self):
        return [item for item in self.articoli if item.disponibile]

    def cerca_per_tipo(self, tipo):
        return [item for item in self.articoli if isinstance(item, tipo)]

    def report(self):
        tot = len(self.articoli)
        disp = len(self.disponibili())
        in_prestito = tot - disp

        print(f"totale articoli: {tot}")
        print(f"disponibili: {disp}")
        print(f"in prestito: {in_prestito}")

        for tipo in (Libro, Rivista, DVD, EBook):
            pezzi = [item for item in self.articoli if isinstance(item, tipo)]
            disp_tipo = len([item for item in pezzi if item.disponibile])
            pres_tipo = len(pezzi) - disp_tipo
            print(
                f"{tipo.__name__}: totali {len(pezzi)}, "
                f"disponibili {disp_tipo}, in prestito {pres_tipo}"
            )
