class Veicolo:
    def __init__(self, marca: str, velocita_max: int):
        self.marca = marca
        self.velocita_max = velocita_max

    def descrivi(self) -> str:
        return f"Veicolo marca {self.marca}, velocita max {self.velocita_max} km/h"
