"""Protocolos e interfaces de dominio para cumplimiento estricto de SOLID (ISP y DIP).

Permiten desacoplar los orquestadores de las implementaciones concretas de ordenamiento,
generación de datos y telemetría de consola.
"""

from collections.abc import Callable
from typing import Protocol, runtime_checkable

from quick_sort.domain.models.metricas import MetricasQuickSort
from quick_sort.domain.models.nodo_recursion import NodoRecursion

# Firma del callback de progreso: (nombre_caso, n, repeticion_actual, total_repeticiones) -> None
ProgresoCallback = Callable[[str, int, int, int], None]

# Firma del generador de datos: (tamano_n) -> list[int]
GeneradorDatosFn = Callable[[int], list[int]]


@runtime_checkable
class SorterProtocol(Protocol):
    """Protocolo que define el contrato elemental para algoritmos de ordenamiento evaluables."""

    metricas: MetricasQuickSort

    def reiniciar_metricas(self) -> None:
        """Restablece los contadores de métricas operacionales a su estado inicial."""
        ...

    def ordenar(self, lista: list[int], inicio: int, fin: int) -> None:
        """Ordena in-place el segmento comprendido entre los índices inicio y fin.

        Args:
            lista: Lista de enteros a ordenar in-place.
            inicio: Índice inicial de la sublista a procesar.
            fin: Índice final inclusivo de la sublista a procesar.
        """
        ...


@runtime_checkable
class VisualSorterProtocol(SorterProtocol, Protocol):
    """Protocolo para algoritmos de ordenamiento que además capturan el árbol de recursión."""

    def obtener_arbol(self) -> NodoRecursion | None:
        """Retorna la raíz del árbol de recursión generado durante la ordenación.

        Returns:
            NodoRecursion | None: Nodo raíz del árbol de llamadas o None si no se ejecutó.
        """
        ...
