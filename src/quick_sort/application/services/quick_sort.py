"""Implementación pura e instrumentada del algoritmo de ordenamiento Quick Sort.

Este módulo aplica el Principio de Responsabilidad Única (SRP) aislando la lógica
algorítmica y el conteo de operaciones elementales. Implementa el contrato `SorterProtocol`.
"""

from quick_sort.domain.models.metricas import MetricasQuickSort
from quick_sort.domain.protocols import SorterProtocol


class QuickSort(SorterProtocol):
    """Implementación del algoritmo Quick Sort con rastreo de métricas de complejidad.

    Utiliza el esquema de partición con el primer elemento como pivote (esquema Algoritmo 2-4),
    midiendo comparaciones, intercambios, iteraciones de partición y profundidad recursiva.

    Attributes:
        metricas (MetricasQuickSort): Objeto de dominio con los contadores operacionales.
    """

    def __init__(self) -> None:
        """Inicializa una nueva instancia de QuickSort con métricas en cero."""
        self.metricas = MetricasQuickSort()

    def reiniciar_metricas(self) -> None:
        """Restablece los contadores de métricas a sus valores iniciales (cero)."""
        self.metricas.reiniciar()

    def particionar(self, lista: list[int], inicio: int, fin: int) -> int:
        """Particiona la sublista lista[inicio:fin+1] alrededor del pivote.

        El pivote se selecciona como el primer elemento (`lista[inicio]`).
        Los punteros convergen intercambiando elementos desubicados hasta que el pivote
        alcanza su posición ordenada final definitiva.

        Args:
            lista: Lista de enteros a reordenar in-place.
            inicio: Índice inicial inclusivo de la partición.
            fin: Índice final inclusivo de la partición.

        Returns:
            int: Índice donde quedó ubicado definitivamente el pivote.
        """
        #  Selección del pivote en la posición inicial del segmento
        pivote = lista[inicio]

        #  Puntero izquierdo (i): avanza hacia la derecha buscando elementos > pivote
        i = inicio + 1

        #  Puntero derecho (j): retrocede hacia la izquierda buscando elementos <= pivote
        j = fin

        # Ciclo principal de partición: itera mientras los punteros no se hayan cruzado
        while i < j:
            self.metricas.iteraciones += 1

            #  Bucle de retroceso de j: busca el primer elemento menor al pivote
            while j >= inicio + 1:
                self.metricas.comparaciones += 1
                if lista[j] >= pivote:
                    j -= 1
                else:
                    break

            #  Bucle de avance de i: busca el primer elemento mayor al pivote
            while i <= fin:
                self.metricas.comparaciones += 1
                if lista[i] <= pivote:
                    i += 1
                else:
                    break

            # Si ambos punteros se detuvieron sin cruzarse, se realiza el intercambio (swap)
            if i < j:
                lista[i], lista[j] = lista[j], lista[i]
                self.metricas.intercambios += 1

        #  Ajuste correctivo si el puntero j se detuvo sobre un elemento mayor al pivote
        if lista[j] > pivote:
            j -= 1

        #  Reubicación final: intercambia el pivote con la posición j definitiva
        lista[inicio], lista[j] = lista[j], lista[inicio]
        self.metricas.intercambios += 1

        return j

    def ordenar(self, lista: list[int], inicio: int, fin: int) -> None:
        """Ordena una sublista in-place utilizando el algoritmo recursivo Quick Sort.

        Args:
            lista: Lista de enteros mutada in-place durante la ejecución.
            inicio: Índice inferior del subrango a ordenar.
            fin: Índice superior inclusivo del subrango a ordenar.
        """
        #  Registro de la llamada en la pila de recursión
        self.metricas.llamadas_recursivas += 1

        #  Caso Base: si la sublista tiene 0 o 1 elementos, ya está ordenada
        if inicio >= fin:
            return

        #  Fase Divide: particiona la lista y obtiene la posición final del pivote
        posicion_pivote = self.particionar(lista, inicio, fin)

        #  Fase Conquista: recursión simétrica sobre la partición izquierda
        self.ordenar(lista, inicio, posicion_pivote - 1)

        #  Fase Conquista: recursión simétrica sobre la partición derecha
        self.ordenar(lista, posicion_pivote + 1, fin)
