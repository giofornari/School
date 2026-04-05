from media_item import MediaItem
from prestabile import Prestabile


class EBook(MediaItem, Prestabile):
    def __init__(self, titolo, anno, formato, dim_mb):
        super().__init__(titolo, anno)
        self.formato = formato
        self.dim_mb = dim_mb
        self.num_prestiti = 0

    def prestito(self) -> str:
        if self.disponibile:
            self.disponibile = False
            self.num_prestiti += 1
            return f"prestito ebook {self.titolo} formato {self.formato}"
        return f"ebook {self.titolo} gia in prestito"

    def restituzione(self) -> str:
        if not self.disponibile:
            self.disponibile = True
            return f"restituzione ebook {self.titolo}"
        return f"ebook {self.titolo} gia disponibile"

    def statistiche(self) -> None:
        print(f"EBook '{self.titolo}' prestato {self.num_prestiti} volte")

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} | formato: {self.formato} | dimensione: {self.dim_mb} mb | prestiti: {self.num_prestiti}"
