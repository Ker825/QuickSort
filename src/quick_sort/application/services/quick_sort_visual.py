"""Implementación visual de Quick Sort que genera el árbol de llamadas recursivas.

Extiende y adapta la lógica de partición para generar un árbol explícito de
`NodoRecursion`, facilitando la auditoría pedagógica y visualización con Rich.
"""

from quick_sort.domain.models.metricas import MetricasQuickSort
from quick_sort.domain.models.nodo_recursion import NodoRecursion
from quick_sort.domain.protocols import VisualSorterProtocol


class QuickSortVisual(VisualSorterProtocol):
    """Implementación de Quick Sort orientada a la visualización y análisis pedagógico.

    A medida que ejecuta la partición y las llamadas recursivas, construye un
    árbol de objetos `NodoRecursion` que modela la jerarquía de decisiones tomadas.

    Attributes:
        metricas (MetricasQuickSort): Seguimiento de comparaciones, intercambios y llamadas.
        raiz (NodoRecursion | None): Nodo raíz del árbol de recursión de la última corrida.
    """

    def __init__(self) -> None:
        """Inicializa QuickSortVisual con métricas en cero y sin árbol previo."""
        self.metricas = MetricasQuickSort()
        self.raiz: NodoRecursion | None = None

    def reiniciar(self) -> None:
        """Restablece los contadores operacionales y descarta el árbol previo."""
        self.metricas.reiniciar()
        self.raiz = None

    def reiniciar_metricas(self) -> None:
        """Alias para cumplir el contrato SorterProtocol."""
        self.reiniciar()

    def ordenar(
        self,
        lista: list[int],
        inicio: int,
        fin: int,
        nodo: NodoRecursion | None = None,
    ) -> None:
        """Ordena una sublista in-place y registra cada estado en el árbol de recursión.

        Args:
            lista: Lista de enteros a ordenar in-place.
            inicio: Índice inicial inclusivo de la sublista.
            fin: Índice final inclusivo de la sublista.
            nodo: Nodo actual en el árbol de recursión (None en la llamada inicial).
        """
        # Inicialización de la raíz en la primera llamada de la recursión
        if nodo is None:
            self.reiniciar()
            self.raiz = NodoRecursion(sublista=lista[inicio : fin + 1].copy())
            nodo = self.raiz

        # Conteo de la llamada actual en la métrica global
        self.metricas.llamadas_recursivas += 1

        # Identificación del caso base (0 o 1 elementos)
        if inicio >= fin:
            nodo.es_caso_base = True
            nodo.resultado = lista[inicio : fin + 1].copy()
            return

        # Selección del pivote como primer elemento del subrango
        pivote = lista[inicio]
        nodo.pivote = pivote

        # Inicialización de punteros convergentes
        i = inicio + 1
        j = fin

        # Proceso de partición Hoare modificada
        while i < j:
            self.metricas.iteraciones += 1

            # Desplazamiento regresivo del puntero derecho
            while j >= inicio + 1:
                self.metricas.comparaciones += 1
                if lista[j] >= pivote:
                    j -= 1
                else:
                    break

            # Desplazamiento progresivo del puntero izquierdo
            while i <= fin:
                self.metricas.comparaciones += 1
                if lista[i] <= pivote:
                    i += 1
                else:
                    break

            # Intercambio de elementos cruzados
            if i < j:
                lista[i], lista[j] = lista[j], lista[i]
                self.metricas.intercambios += 1

        # Corrección de posición de cruce
        if lista[j] > pivote:
            j -= 1

        # Colocación definitiva del pivote en su posición ordenada
        lista[inicio], lista[j] = lista[j], lista[inicio]
        self.metricas.intercambios += 1

        # Actualización de metadata del nodo para inspección visual
        nodo.posicion_pivote = j
        nodo.resultado = lista[inicio : fin + 1].copy()

        # Bifurcación del árbol: creación de ramas izquierda y derecha
        nodo.izquierda = NodoRecursion(sublista=lista[inicio:j].copy())
        nodo.derecha = NodoRecursion(sublista=lista[j + 1 : fin + 1].copy())

        # Recursión sobre partición izquierda (elementos <= pivote)
        self.ordenar(lista, inicio, j - 1, nodo.izquierda)

        # Recursión sobre partición derecha (elementos >= pivote)
        self.ordenar(lista, j + 1, fin, nodo.derecha)

    def obtener_arbol(self) -> NodoRecursion | None:
        """Retorna la referencia a la raíz del árbol de recursión construido.

        Returns:
            NodoRecursion | None: Raíz del árbol jerárquico o None si no se ha ordenado.
        """
        return self.raiz
