"""Pruebas unitarias para el algoritmo QuickSort y QuickSortVisual."""

import pytest

from quick_sort.application.services.quick_sort import QuickSort
from quick_sort.application.services.quick_sort_visual import QuickSortVisual


@pytest.fixture
def sorter() -> QuickSort:
    """Fixture que provee una instancia limpia de QuickSort."""
    return QuickSort()


@pytest.fixture
def visual_sorter() -> QuickSortVisual:
    """Fixture que provee una instancia de QuickSortVisual."""
    return QuickSortVisual()


@pytest.mark.parametrize(
    "datos",
    [
        [],
        [1],
        [2, 1],
        [3, 2, 1],
        [1, 2, 3],
        [5, 5, 5],
        [4, 1, 3, 2, 5],
        [10, -2, 7, 0, -5, 3],
    ],
)
def test_quick_sort_ordena_correctamente(
    sorter: QuickSort,
    datos: list[int],
) -> None:
    """Valida que QuickSort ordene in-place cualquier permutación de enteros."""
    esperado = sorted(datos)
    sorter.ordenar(datos, 0, len(datos) - 1)
    assert datos == esperado


def test_quick_sort_lista_vacia(sorter: QuickSort) -> None:
    """Verifica que una lista vacía no genere excepciones y se preserve."""
    datos: list[int] = []
    sorter.ordenar(datos, 0, -1)
    assert datos == []


def test_quick_sort_metricas_se_incrementan(sorter: QuickSort) -> None:
    """Verifica que las métricas operacionales se cuenten en cada ordenamiento."""
    datos = [4, 2, 1, 3]
    sorter.ordenar(datos, 0, len(datos) - 1)

    assert sorter.metricas.comparaciones > 0
    assert sorter.metricas.llamadas_recursivas > 0
    assert sorter.metricas.total_operaciones > 0

    sorter.reiniciar_metricas()
    assert sorter.metricas.comparaciones == 0
    assert sorter.metricas.intercambios == 0


def test_quick_sort_visual_construye_arbol(visual_sorter: QuickSortVisual) -> None:
    """Verifica que QuickSortVisual genere el árbol de recursión y sus métricas."""
    datos = [15, 8, 3, 12, 25, 20, 30]
    visual_sorter.ordenar(datos, 0, len(datos) - 1)

    assert datos == sorted([15, 8, 3, 12, 25, 20, 30])
    raiz = visual_sorter.obtener_arbol()
    assert raiz is not None
    assert raiz.pivote == 15
    assert raiz.calcular_profundidad_maxima() >= 2
    assert raiz.contar_nodos_totales() >= 5
