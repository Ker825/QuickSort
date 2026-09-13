from dataclasses import dataclass


@dataclass
class RegistroOperacion:
    tamano: int
    caso: str
    repeticion: int
    comparaciones: int
    intercambios: int
    iteraciones: int
    llamadas_recursivas: int
