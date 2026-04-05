from media_item import MediaItem


class DVD(MediaItem):
    def __init__(self, titolo, anno, reg, dur):
        super().__init__(titolo, anno)
        self.reg = reg
        self.dur = dur

    def prestito(self) -> str:
        if self.disponibile:
            self.disponibile = False
            return f"prestito dvd {self.titolo} regista {self.reg} durata {self.dur} minuti"
        return f"dvd {self.titolo} gia in prestito"

    def restituzione(self) -> str:
        if not self.disponibile:
            self.disponibile = True
            return f"restituzione dvd {self.titolo}"
        return f"dvd {self.titolo} gia disponibile"

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} | regista: {self.reg} | durata: {self.dur} minuti"
