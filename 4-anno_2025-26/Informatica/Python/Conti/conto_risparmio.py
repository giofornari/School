from datetime import date
from conto_bancario import ContoBancario


class ContoDiRisparmio(ContoBancario):
    def __init__(self, proprietario: str, saldo_iniziale: float = 0.0, limite_prelievi_mensili: int = 3):
        super().__init__(proprietario, saldo_iniziale)
        self.limite_prelievi_mensili = int(limite_prelievi_mensili)
        self._prelievi_mese = 0
        self._mese_ultimo_prelievo = None  # (year, month)

    def _reset_se_nuovo_mese(self) -> None:
        oggi = date.today()
        if self._mese_ultimo_prelievo != (oggi.year, oggi.month):
            self._mese_ultimo_prelievo = (oggi.year, oggi.month)
            self._prelievi_mese = 0

    def preleva(self, importo: float) -> None:
        if importo <= 0:
            return False
        self._reset_se_nuovo_mese()
        if self._prelievi_mese >= self.limite_prelievi_mensili:
            return False
        if importo > self._saldo:
            return False
        self._saldo -= float(importo)
        self._prelievi_mese += 1
        return True

    def prelievi_rimanenti(self) -> int:
        self._reset_se_nuovo_mese()
        return self.limite_prelievi_mensili - self._prelievi_mese
