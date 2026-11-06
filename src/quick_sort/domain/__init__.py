"""Capa de Dominio del proyecto Quick Sort."""

from quick_sort.domain.enums import CasoPrueba, MetodoAgrupacion
from quick_sort.domain.exceptions import (
    DatosInsuficientesError,
    IndiceInvalidoError,
    PersistenciaDatosError,
    QuickSortError,
    TamanoInvalidoError,
)
from quick_sort.domain.models import (
    MetricasQuickSort,
    NodoRecursion,
    RegistroOperacion,
    RegistroTiempo,
)
from quick_sort.domain.protocols import (
    GeneradorDatosFn,
    ProgresoCallback,
    SorterProtocol,
    VisualSorterProtocol,
)

__all__ = [
    "CasoPrueba",
    "DatosInsuficientesError",
    "GeneradorDatosFn",
    "IndiceInvalidoError",
    "MetodoAgrupacion",
    "MetricasQuickSort",
    "NodoRecursion",
    "PersistenciaDatosError",
    "ProgresoCallback",
    "QuickSortError",
    "RegistroOperacion",
    "RegistroTiempo",
    "SorterProtocol",
    "TamanoInvalidoError",
    "VisualSorterProtocol",
]
