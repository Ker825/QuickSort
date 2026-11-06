"""Paquete principal para el análisis, benchmarking y visualización de Quick Sort.

Este paquete implementa una arquitectura limpia (Clean Architecture / DDD)
diseñada bajo principios SOLID, separando el dominio algorítmico, los casos
de uso de experimentación, la infraestructura de almacenamiento/gráficos
y la presentación en terminal mediante Rich.
"""

from quick_sort.application.services.data_generator import DataGenerator
from quick_sort.application.services.experiment_runner import ExperimentRunner
from quick_sort.application.services.quick_sort import QuickSort
from quick_sort.application.services.quick_sort_visual import QuickSortVisual
from quick_sort.core.config import ConfiguracionExperimento
from quick_sort.domain.enums import CasoPrueba
from quick_sort.domain.models.metricas import MetricasQuickSort
from quick_sort.domain.models.nodo_recursion import NodoRecursion

__all__ = [
    "CasoPrueba",
    "ConfiguracionExperimento",
    "DataGenerator",
    "ExperimentRunner",
    "MetricasQuickSort",
    "NodoRecursion",
    "QuickSort",
    "QuickSortVisual",
]
