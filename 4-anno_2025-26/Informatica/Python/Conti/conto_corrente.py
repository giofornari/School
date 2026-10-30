from conto_bancario import ContoBancario


class ContoCorrente(ContoBancario):
    def preleva(self, importo: float) -> bool:
        """Esegue un prelievo semplice.

        Restituisce True se il prelievo è andato a buon fine, False altrimenti
        (importo non valido o saldo insufficiente)."""
        if importo <= 0:
            return False
        if importo > self._saldo:
            return False
        self._saldo -= float(importo)
        return True
