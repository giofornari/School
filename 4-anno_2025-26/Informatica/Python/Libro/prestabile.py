from abc import ABC, abstractmethod


class Prestabile(ABC):
    @abstractmethod
    def prestito(self) -> str:
        pass

    @abstractmethod
    def restituzione(self) -> str:
        pass
