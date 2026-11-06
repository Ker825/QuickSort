"""Modelo de dominio que representa un nodo en el árbol de recursión de Quick Sort."""

from dataclasses import dataclass


@dataclass
class NodoRecursion:
    """Representa una llamada en el árbol de recursión del algoritmo Quick Sort.

    Attributes:
        sublista: Segmento de la lista procesada en la llamada actual.
        pivote: Valor del elemento elegido como pivote (None si es caso base).
        posicion_pivote: Índice final donde quedó posicionado el pivote tras la partición.
        resultado: Estado de la sublista una vez reubicado el pivote.
        es_caso_base: Indica si la sublista tiene 0 o 1 elementos y no requiere partición.
        izquierda: Subárbol con la partición de elementos menores o iguales al pivote.
        derecha: Subárbol con la partición de elementos mayores al pivote.
    """

    sublista: list[int]
    pivote: int | None = None
    posicion_pivote: int | None = None
    resultado: list[int] | None = None
    es_caso_base: bool = False
    izquierda: "NodoRecursion | None" = None
    derecha: "NodoRecursion | None" = None

    @property
    def es_hoja(self) -> bool:
        """Determina si el nodo no tiene ramas hijas."""
        return self.izquierda is None and self.derecha is None

    def calcular_profundidad_maxima(self) -> int:
        """Calcula recursivamente la altura o profundidad máxima del árbol de llamadas.

        Returns:
            int: Altura del árbol (1 para árbol de un solo nodo).
        """
        alt_izq = self.izquierda.calcular_profundidad_maxima() if self.izquierda else 0
        alt_der = self.derecha.calcular_profundidad_maxima() if self.derecha else 0
        return 1 + max(alt_izq, alt_der)

    def contar_nodos_totales(self) -> int:
        """Cuenta el total de nodos en este subárbol de llamadas.

        Returns:
            int: Número total de nodos invocados recursivamente.
        """
        nodos_izq = self.izquierda.contar_nodos_totales() if self.izquierda else 0
        nodos_der = self.derecha.contar_nodos_totales() if self.derecha else 0
        return 1 + nodos_izq + nodos_der
