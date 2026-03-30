from veicolo import Veicolo


class Moto(Veicolo):
    def descrivi(self) -> str:
        return f"Moto {self.marca}, velocita max {self.velocita_max} km/h"
