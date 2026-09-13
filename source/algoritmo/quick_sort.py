from .metricas import MetricasQuickSort


class QuickSort:
    def __init__(self):
        self.metricas = MetricasQuickSort()

    def reiniciar_metricas(self) -> None:
        self.metricas = MetricasQuickSort()

    def ordenar(self, lista: list[int], f: int, l: int):  # noqa: E741
        """
        Ordena una sublista in-place utilizando el algoritmo Quick Sort
        Y registra metricas importan`tes

        Args:
        arr: La lista de elementos a ordenar.
        f: Índice inicial de la sublista.
        l: Índice final (inclusivo) de la sublista.

        Returns:
            list[int]: retorna una lista ordenada de numeros
        """
        # Conteo de llamadas recursivas
        self.metricas.llamadas_recursivas += 1

        # Caso base: Si el subelemento tiene 0 o 1 elementos,
        # por definición ya esta ordenado, por lo que se detiene
        if f >= l:
            return

        # El primer elemento de la lista
        pivote = lista[f]

        # Puntero de particion: Avanza hacia la derecha buscando
        # elementos mayores al pivote lista[f]
        i = f + 1  # * Primer indice de la lista movido hacia la derecha

        # Puntero de particion: Retrocede hacia la izquierda buscando
        # elementos mayores al pivote lista[f]
        j = l  # * Ultimo indice de la lista

        # Ciclo while prioncipal, entrara siempre que el puntero i sea menor al j
        # 1. El ciclo principal debe ser estricto segun el Algoritmo 2-4
        while i < j:
            self.metricas.iteraciones += 1

            # Decremento de j
            while j >= f + 1:
                self.metricas.comparaciones += 1
                if lista[j] >= pivote:
                    j -= 1
                else:
                    break

            # Incremento de i
            while i <= l:
                self.metricas.comparaciones += 1
                if lista[i] <= pivote:
                    i += 1
                else:
                    break

            # Si no se han cruzado, intercambiar elementos
            if i < j:
                lista[i], lista[j] = lista[j], lista[i]
                self.metricas.intercambios += 1

        # 2. Ajuste del puntero j si se cruzo de mas con i
        if lista[j] > pivote:
            j -= 1

        # 3. Intercambio final del pivote a su posicion correcta
        lista[f], lista[j] = lista[j], lista[f]
        self.metricas.intercambios += 1

        # 4. Recursion sobre las particiones resultantes
        self.ordenar(lista, f, j - 1)
        self.ordenar(lista, j + 1, l)
