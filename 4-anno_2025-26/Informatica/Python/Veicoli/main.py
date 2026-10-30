from auto import Auto
from moto import Moto
from bicicletta import Bicicletta


def main() -> None:
    veicoli = [
        Auto("Fiat", 220),
        Moto("Yamaha", 280),
        Bicicletta("Bianchi", 45),
    ]

    for veicolo in veicoli:
        print(veicolo.descrivi())


if __name__ == "__main__":
    main()
