from media_item import MediaItem


class Libro(MediaItem):
    def __init__(self, titolo, anno, wrter, pg):
        super().__init__(titolo, anno)
        self.wrter = wrter
        self.pg = pg

    def prestito(self) -> str:
        if self.disponibile:
            self.disponibile = False
            return f"prestito libro {self.titolo} di {self.wrter}"
        return f"libro {self.titolo} gia in prestito"

    def restituzione(self) -> str:
        if not self.disponibile:
            self.disponibile = True
            return f"restituzione libro {self.titolo}"
        return f"libro {self.titolo} gia disponibile"

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} | autore: {self.wrter} | pagine: {self.pg}"
