from abc import ABC, abstractmethod


class MediaItem(ABC):
    def __init__(self, titolo, anno):
        self.titolo = titolo
        self.anno = anno
        self.disponibile = True

    @abstractmethod
    def prestito(self) -> str:
        pass

    @abstractmethod
    def restituzione(self) -> str:
        pass

    def descrivi(self) -> None:
        stato = "SI" if self.disponibile else "NO"
        print(f"[{self.anno}] {self.titolo} — Disponibile: {stato}")

    def __str__(self) -> str:
        return f"MediaItem: {self.titolo} ({self.anno})"
