"""Modelo de dominio para registrar operaciones elementales de un experimento."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RegistroOperacion:
    """Registro inmutable de las operaciones elementales de una corrida de benchmark.

    Attributes:
        tamano: Cantidad de elementos de la muestra evaluada (n).
        caso: Nombre descriptivo del escenario de prueba.
        repeticion: Número ordinal de repetición dentro del lote de pruebas.
        comparaciones: Cantidad de comparaciones entre elementos.
        intercambios: Cantidad de intercambios de posición de elementos (swaps).
        iteraciones: Total de iteraciones realizadas en los bucles de partición.
        llamadas_recursivas: Total de invocaciones de la función recursiva.
    """

    tamano: int
    caso: str
    repeticion: int
    comparaciones: int
    intercambios: int
    iteraciones: int
    llamadas_recursivas: int

    def __post_init__(self) -> None:
        """Valida que los contadores no contengan valores negativos inconsistentes."""
        if self.tamano <= 0:
            raise ValueError(f"El tamaño debe ser positivo, recibido: {self.tamano}")
        if self.repeticion <= 0:
            raise ValueError(
                f"La repetición debe ser >= 1, recibido: {self.repeticion}"
            )
        for attr in (
            "comparaciones",
            "intercambios",
            "iteraciones",
            "llamadas_recursivas",
        ):
            if getattr(self, attr) < 0:
                raise ValueError(
                    f"El campo '{attr}' no puede ser negativo: {getattr(self, attr)}"
                )
