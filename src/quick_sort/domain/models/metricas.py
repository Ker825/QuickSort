"""Modelo de dominio para el seguimiento de métricas operacionales de Quick Sort."""

from dataclasses import dataclass


@dataclass
class MetricasQuickSort:
    """Métricas operacionales elementales registradas durante la ejecución de Quick Sort.

    Attributes:
        comparaciones: Número de veces que dos elementos fueron comparados en los bucles.
        intercambios: Cantidad de permutaciones o swaps realizados en la lista.
        iteraciones: Total de ciclos completados en los bucles de partición.
        llamadas_recursivas: Total de invocaciones de la función recursiva.
    """

    comparaciones: int = 0
    intercambios: int = 0
    iteraciones: int = 0
    llamadas_recursivas: int = 0

    def reiniciar(self) -> None:
        """Restablece todos los contadores de métricas a cero."""
        self.comparaciones = 0
        self.intercambios = 0
        self.iteraciones = 0
        self.llamadas_recursivas = 0

    @property
    def total_operaciones(self) -> int:
        """Calcula la suma total de comparaciones e intercambios elementales."""
        return self.comparaciones + self.intercambios
