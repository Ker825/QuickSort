from dataclasses import dataclass


@dataclass
class RegistroTiempo:
    tamano: int
    caso: str
    repeticion: int
    tiempo_segundos: float
