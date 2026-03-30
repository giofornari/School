from veicolo import Veicolo


class Auto(Veicolo):
    def descrivi(self) -> str:
        return f"Auto {self.marca}, velocita max {self.velocita_max} km/h"
