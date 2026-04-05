from abc import ABC, abstractmethod


class ContoBancario(ABC):
    def __init__(self, proprietario: str, saldo_iniziale: float = 0.0):
        self.proprietario = proprietario
        self._saldo = float(saldo_iniziale)

    def deposita(self, importo: float) -> bool:
        """Deposita l'importo sul conto.

        Restituisce True se il deposito è stato effettuato, False se l'importo
        non è valido (nessuna eccezione sollevata).
        """
        if importo <= 0:
            return False
        self._saldo += float(importo)
        return True

    @abstractmethod
    def preleva(self, importo: float) -> bool:
        """Preleva l'importo dal conto.

        Le sottoclassi dovrebbero implementare il metodo e restituire True se
        il prelievo è andato a buon fine, False altrimenti. Non solleviamo
        eccezioni per operazioni non valide.
        """
        pass

    def saldo(self) -> float:
        return self._saldo
