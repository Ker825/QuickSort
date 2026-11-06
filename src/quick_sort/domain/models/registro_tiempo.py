"""Modelo de dominio para registrar tiempos de ejecución de un experimento."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RegistroTiempo:
    """Registro inmutable de la medición temporal de una corrida de benchmark.

    Attributes:
        tamano: Cantidad de elementos de la muestra evaluada (n).
        caso: Nombre descriptivo del escenario de prueba (ej. 'Mejor Caso', 'Promedio').
        repeticion: Número ordinal de repetición dentro del lote de pruebas.
        tiempo_segundos: Duración exacta en segundos medidos con reloj monotónico.
    """

    tamano: int
    caso: str
    repeticion: int
    tiempo_segundos: float

    def __post_init__(self) -> None:
        """Valida que los valores del registro sean físicamente coherentes."""
        if self.tamano <= 0:
            raise ValueError(f"El tamaño debe ser positivo, recibido: {self.tamano}")
        if self.repeticion <= 0:
            raise ValueError(
                f"La repetición debe ser >= 1, recibido: {self.repeticion}"
            )
        if self.tiempo_segundos < 0.0:
            raise ValueError(
                f"El tiempo transcurrido no puede ser negativo: {self.tiempo_segundos}"
            )
