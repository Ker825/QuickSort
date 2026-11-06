"""Jerarquía de excepciones de dominio para el sistema Quick Sort.

Define errores tipados específicos para la validación defensiva en capas de dominio,
aplicación e infraestructura, evitando el antipatrón de capturar excepciones genéricas.
"""


class QuickSortError(Exception):
    """Excepción base para todos los errores del dominio Quick Sort."""


class TamanoInvalidoError(QuickSortError, ValueError):
    """Se lanza cuando un tamaño de muestra no cumple los requisitos mínimos."""


class IndiceInvalidoError(QuickSortError, IndexError):
    """Se lanza cuando los límites de partición son inconsistentes o fuera de rango."""


class PersistenciaDatosError(QuickSortError, OSError):
    """Se lanza cuando falla la lectura o escritura de datos experimentales."""


class DatosInsuficientesError(QuickSortError, ValueError):
    """Se lanza cuando los datasets carecen de información para realizar cálculos estadísticos."""
