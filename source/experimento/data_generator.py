import random


class DataGenerator:
    """Generador de datos desacoplado para experimentos de ordenamiento."""

    @staticmethod
    def generar_caso_promedio(tamano: int) -> list[int]:
        """Genera una lista con enteros aleatorios sin patron fijo."""
        return random.sample(range(tamano * 10), tamano)  # tiene duplicados

    @staticmethod
    def generar_peor_caso(tamano: int) -> list[int]:
        """
        Genera una lista ordenada ascendentemente.
        Para un Quick Sort con pivote inicial, genera particiones maximamente desbalanceadas.
        """  # noqa: E501
        return list(range(1, tamano + 1))

    @staticmethod
    def generar_mejor_caso(tamano: int) -> list[int]:
        """
        Construye una permutacion donde la mediana siempre ocupa la posicion inicial (pivote)
        en cada nivel de recursion, forzando particiones equilibradas T(n) = 2T(n/2) + O(n).
        """  # noqa: E501
        base = list(range(1, tamano + 1))
        resultado: list[int] = [0] * tamano

        def construir_balanceado(
            arr_ordenado: list[int], inicio: int, fin: int
        ) -> None:
            if inicio > fin:
                return

            # Calcular la mediana del segmento actual
            medio = (inicio + fin) // 2

            # Colocar la mediana en la posicion del pivote (inicio)
            resultado[inicio] = arr_ordenado[medio]

            # Dividir los elementos restantes alrededor de la mediana
            izq = arr_ordenado[inicio:medio]
            der = arr_ordenado[medio + 1 : fin + 1]

            # Recursion simetrica en ambas mitades
            construir_balanceado(izq, inicio + 1, inicio + len(izq))
            construir_balanceado(der, inicio + len(izq) + 1, fin)

        # Alternativa iterativa/recursiva simple:
        # Una forma directa de forzar el mejor caso en Quick Sort
        # es colocar deliberadamente las medianas en los indices iniciales de cada particion.  # noqa: E501
        return DataGenerator._construir_arbol_balanceado(base)

    @staticmethod
    def _construir_arbol_balanceado(arr: list[int]) -> list[int]:
        """Coloca en el indice 0 la mediana de la particion recursivamente."""
        if len(arr) <= 2:
            return arr

        medio = len(arr) // 2
        pivote = arr[medio]
        resto = arr[:medio] + arr[medio + 1 :]

        mitad = len(resto) // 2
        izq = DataGenerator._construir_arbol_balanceado(resto[:mitad])
        der = DataGenerator._construir_arbol_balanceado(resto[mitad:])

        return [pivote] + izq + der
