from veicolo import Veicolo


class Bicicletta(Veicolo):
    def descrivi(self) -> str:
        return f"Bicicletta {self.marca}, velocita max {self.velocita_max} km/h"
