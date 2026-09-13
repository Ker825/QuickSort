from dataclasses import dataclass


@dataclass
class MetricasQuickSort:
    comparaciones: int = 0
    intercambios: int = 0
    iteraciones: int = 0
    llamadas_recursivas: int = 0
