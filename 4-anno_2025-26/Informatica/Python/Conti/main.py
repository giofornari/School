from conto_corrente import ContoCorrente
from conto_risparmio import ContoDiRisparmio


def main() -> None:
    cc = ContoCorrente("Mario Rossi", 1000)
    cr = ContoDiRisparmio("Luigi Bianchi", 500, limite_prelievi_mensili=2)

    print("Conto Corrente:", cc.proprietario)
    print("Saldo iniziale:", cc.saldo())
    deposito_ok = cc.deposita(200)
    print("Dopo deposito 200:", cc.saldo(), "- Deposito riuscito:", deposito_ok)
    if not cc.preleva(1500):
        print("Prelievo 1500 non riuscito (troppo grande o importo non valido)")
    if not cc.preleva(1000):
        print("Prelievo 1000 non riuscito")
    else:
        print("Dopo prelievo 1000:", cc.saldo())

    print("\nConto Risparmio:", cr.proprietario)
    print("Saldo iniziale:", cr.saldo())
    if not cr.preleva(100):
        print("Primo prelievo non riuscito")
    print("Dopo primo prelievo:", cr.saldo(), "- Prelievi rimasti:", cr.prelievi_rimanenti())
    if not cr.preleva(100):
        print("Secondo prelievo non riuscito")
    print("Dopo secondo prelievo:", cr.saldo(), "- Prelievi rimasti:", cr.prelievi_rimanenti())
    if not cr.preleva(50):
        print("Terzo prelievo non riuscito (limite raggiunto o importo non valido)")


if __name__ == "__main__":
    main()
