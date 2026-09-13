import pytest

from source.algoritmo.quick_sort import QuickSort


@pytest.fixture
def sorter() -> QuickSort:
    return QuickSort()  # type: ignore[no-untyped-call]


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
    esperado = sorted(datos)

    sorter.ordenar(datos, 0, len(datos) - 1)

    assert datos == esperado


def test_quick_sort_lista_vacia(sorter: QuickSort) -> None:
    datos: list[int] = []

    sorter.ordenar(datos, 0, -1)

    assert datos == []
