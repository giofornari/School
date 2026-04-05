from media_item import MediaItem


class Rivista(MediaItem):
    def __init__(self, titolo, anno, num, mese):
        super().__init__(titolo, anno)
        self.num = num
        self.mese = mese

    def prestito(self) -> str:
        if self.disponibile:
            self.disponibile = False
            return f"prestito rivista {self.titolo} numero {self.num} mese {self.mese}"
        return f"rivista {self.titolo} gia in prestito"

    def restituzione(self) -> str:
        if not self.disponibile:
            self.disponibile = True
            return f"restituzione rivista {self.titolo}"
        return f"rivista {self.titolo} gia disponibile"

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} | numero: {self.num} | mese: {self.mese}"
