from dataclasses import dataclass


@dataclass
class NodoRecursion:
    """Representa una llamada recursiva de Quick Sort."""

    sublista: list[int]

    pivote: int | None = None
    posicion_pivote: int | None = None

    resultado: list[int] | None = None

    es_caso_base: bool = False

    izquierda: "NodoRecursion | None" = None
    derecha: "NodoRecursion | None" = None
