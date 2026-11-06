"""Generador de datos desacoplado para experimentos y benchmarks de Quick Sort.

Aplica el Principio de Responsabilidad Única (SRP): proporciona fábricas deterministas
y estocásticas para generar secuencias de prueba correspondientes a las complejidades
asintóticas teóricas: O(n log n) para el mejor caso y promedio, y O(n^2) para el peor caso.
"""

import random

from quick_sort.domain.exceptions import TamanoInvalidoError


class DataGenerator:
    """Fábrica de datos sintéticos especializada en escenarios de análisis asintótico."""

    @staticmethod
    def generar_caso_promedio(tamano: int) -> list[int]:
        """Genera una lista con enteros aleatorios sin patrón fijo ni elementos repetidos.

        Representa el caso promedio con distribución uniforme, induciendo particiones
        aproximadamente balanceadas con complejidad esperada O(n log n).

        Args:
            tamano: Cantidad de enteros a generar (n).

        Returns:
            list[int]: Lista de enteros únicos aleatorios.

        Raises:
            TamanoInvalidoError: Si tamano es menor o igual a cero.
        """
        # [LÍNEA CLAVE] Validación defensiva del tamaño de la muestra
        if tamano <= 0:
            raise TamanoInvalidoError(
                f"El tamaño de muestra debe ser positivo, recibido: {tamano}"
            )

        # [LÍNEA CLAVE] Muestreo sin reemplazo sobre un universo amplio (evita duplicados)
        return random.sample(range(tamano * 10), tamano)

    @staticmethod
    def generar_peor_caso(tamano: int) -> list[int]:
        """Genera una lista ordenada ascendentemente del 1 al tamano.

        Para una implementación de Quick Sort cuyo pivote es siempre el primer elemento,
        una lista ya ordenada produce particiones con tamaños 0 y n - 1 en cada llamada,
        degenerando el árbol recursivo en una lista enlazada de altura O(n) y costo O(n^2).

        Args:
            tamano: Cantidad de enteros en la secuencia (n).

        Returns:
            list[int]: Lista estrictamente creciente [1, 2, ..., n].

        Raises:
            TamanoInvalidoError: Si tamano es menor o igual a cero.
        """
        if tamano <= 0:
            raise TamanoInvalidoError(
                f"El tamaño de muestra debe ser positivo, recibido: {tamano}"
            )

        # [LÍNEA CLAVE] Secuencia estrictamente creciente que maximiza el desbalance
        return list(range(1, tamano + 1))

    @staticmethod
    def generar_mejor_caso(tamano: int) -> list[int]:
        """Construye una permutación que fuerza particiones perfectamente equilibradas.

        Coloca deliberadamente la mediana en la posición del pivote (índice inicial)
        en cada nivel de recursión, garantizando la relación de recurrencia
        T(n) = 2T(n/2) + O(n), lo que conduce a la cota inferior óptima O(n log n).

        Args:
            tamano: Cantidad de enteros en la secuencia (n).

        Returns:
            list[int]: Permutación balanceada de los enteros [1, ..., n].

        Raises:
            TamanoInvalidoError: Si tamano es menor o igual a cero.
        """
        if tamano <= 0:
            raise TamanoInvalidoError(
                f"El tamaño de muestra debe ser positivo, recibido: {tamano}"
            )

        base = list(range(1, tamano + 1))
        # [LÍNEA CLAVE] Reordenamiento recursivo por mediana para lograr particiones simétricas
        return DataGenerator._construir_arbol_balanceado(base)

    @staticmethod
    def _construir_arbol_balanceado(arr: list[int]) -> list[int]:
        """Algoritmo auxiliar que reubica la mediana en el índice 0 recursivamente.

        Args:
            arr: Subarreglo ordenado a transformar.

        Returns:
            list[int]: Subarreglo con la mediana al frente y mitades equilibradas.
        """
        # Caso base recursivo: segmentos de 0, 1 o 2 elementos ya están balanceados
        if len(arr) <= 2:
            return arr

        # [LÍNEA CLAVE] Localización del elemento medio (mediana exacta o aproximada)
        medio = len(arr) // 2
        pivote = arr[medio]

        # Elementos restantes excluyendo el elemento pivote seleccionado
        resto = arr[:medio] + arr[medio + 1 :]

        # División equitativa de los elementos restantes
        mitad = len(resto) // 2

        # [LÍNEA CLAVE] Construcción balanceada recursiva de mitades izquierda y derecha
        izq = DataGenerator._construir_arbol_balanceado(resto[:mitad])
        der = DataGenerator._construir_arbol_balanceado(resto[mitad:])

        # El pivote encabeza la partición para ser seleccionado en la posición inicial
        return [pivote] + izq + der
