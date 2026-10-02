from source.algoritmo.metricas import MetricasQuickSort

from .models.nodo_recursion import NodoRecursion


class QuickSortVisual:
    """Implementación visual de Quick Sort.

    Mantiene la misma lógica del algoritmo Quick Sort,
    pero además construye un árbol de las llamadas recursivas.
    """

    def __init__(self) -> None:
        """Inicializa QuickSortVisual."""
        self.metricas = MetricasQuickSort()
        self.raiz: NodoRecursion | None = None

    def reiniciar(self) -> None:
        """Restablece las métricas y el árbol."""
        self.metricas = MetricasQuickSort()
        self.raiz = None

    def ordenar(
        self,
        lista: list[int],
        f: int,
        l: int,
        nodo: NodoRecursion | None = None,
    ) -> None:
        """Ordena una sublista y construye su árbol de recursión.

        Args:
            lista: Lista de enteros que será modificada.
            f: Índice inicial de la sublista.
            l: Índice final inclusivo de la sublista.
            nodo: Nodo correspondiente a la llamada recursiva actual.
        """

        # =========================================================
        # INICIO
        # =========================================================

        # Solo ocurre en la primera llamada.
        if nodo is None:
            self.reiniciar()

            self.raiz = NodoRecursion(sublista=lista[f : l + 1].copy())

            nodo = self.raiz

        # =========================================================
        # LLAMADA RECURSIVA
        # =========================================================

        self.metricas.llamadas_recursivas += 1

        # =========================================================
        # CASO BASE
        # =========================================================

        if f >= l:
            nodo.es_caso_base = True
            nodo.resultado = lista[f : l + 1].copy()
            return

        # =========================================================
        # PIVOTE
        # =========================================================

        pivote = lista[f]

        nodo.pivote = pivote

        # =========================================================
        # PUNTEROS
        # =========================================================

        i = f + 1
        j = l

        # =========================================================
        # PARTICIÓN
        # =========================================================

        while i < j:
            self.metricas.iteraciones += 1

            # -----------------------------------------------------
            # DECREMENTO DE j
            # -----------------------------------------------------

            while j >= f + 1:
                self.metricas.comparaciones += 1

                if lista[j] >= pivote:
                    j -= 1
                else:
                    break

            # -----------------------------------------------------
            # INCREMENTO DE i
            # -----------------------------------------------------

            while i <= l:
                self.metricas.comparaciones += 1

                if lista[i] <= pivote:
                    i += 1
                else:
                    break

            # -----------------------------------------------------
            # INTERCAMBIO
            # -----------------------------------------------------

            if i < j:
                lista[i], lista[j] = lista[j], lista[i]

                self.metricas.intercambios += 1

        # =========================================================
        # AJUSTE DEL PUNTERO j
        # =========================================================

        if lista[j] > pivote:
            j -= 1

        # =========================================================
        # COLOCAR PIVOTE
        # =========================================================

        lista[f], lista[j] = lista[j], lista[f]

        self.metricas.intercambios += 1

        # Guardamos la posición final del pivote.
        nodo.posicion_pivote = j

        # Guardamos el estado de la partición.
        nodo.resultado = lista[f : l + 1].copy()

        # =========================================================
        # CREAR PARTICIONES
        # =========================================================

        nodo.izquierda = NodoRecursion(sublista=lista[f:j].copy())

        nodo.derecha = NodoRecursion(sublista=lista[j + 1 : l + 1].copy())

        # =========================================================
        # RECURSIÓN
        # =========================================================

        self.ordenar(
            lista,
            f,
            j - 1,
            nodo.izquierda,
        )

        self.ordenar(
            lista,
            j + 1,
            l,
            nodo.derecha,
        )

    def obtener_arbol(self) -> NodoRecursion | None:
        """Devuelve el árbol de recursión."""
        return self.raiz
