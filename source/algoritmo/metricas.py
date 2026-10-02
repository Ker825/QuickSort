from dataclasses import dataclass


@dataclass
class MetricasQuickSort:
    """Clase que representa las métricas del algoritmo Quick Sort."""

    comparaciones: int = 0
    intercambios: int = 0
    iteraciones: int = 0
    llamadas_recursivas: int = 0
