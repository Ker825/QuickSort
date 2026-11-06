"""Enumeraciones de dominio para el benchmark y análisis de Quick Sort."""

from enum import StrEnum


class CasoPrueba(StrEnum):
    """Escenarios teóricos y empíricos evaluados en el algoritmo Quick Sort.

    Attributes:
        MEJOR_CASO: Partición óptima balanceada O(n log n).
        CASO_PROMEDIO: Datos aleatorios con orden promedio O(n log n).
        PEOR_CASO: Partición desbalanceada que degenera a O(n^2).
    """

    MEJOR_CASO = "Mejor Caso"
    CASO_PROMEDIO = "Promedio"
    PEOR_CASO = "Peor Caso"


class MetodoAgrupacion(StrEnum):
    """Estrategia estadística para sintetizar múltiples repeticiones de una medición.

    Attributes:
        MEDIA: Media aritmética estándar (sensible a valores extremos).
        MEDIANA: Mediana estadística (resistente a picos de CPU del sistema operativo).
    """

    MEDIA = "media"
    MEDIANA = "mediana"
