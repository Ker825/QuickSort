"""Pruebas unitarias para DataGenerator y validaciones defensivas."""

import pytest

from quick_sort.application.services.data_generator import DataGenerator
from quick_sort.domain.exceptions import TamanoInvalidoError


def test_generador_caso_promedio() -> None:
    """Verifica la generación de datos aleatorios sin duplicados."""
    datos = DataGenerator.generar_caso_promedio(100)

    assert len(datos) == 100
    assert len(set(datos)) == 100


def test_generador_peor_caso() -> None:
    """Verifica que el peor caso genere una secuencia estrictamente creciente."""
    datos = DataGenerator.generar_peor_caso(100)

    assert datos == list(range(1, 101))


def test_generador_mejor_caso() -> None:
    """Verifica que el mejor caso contenga exactamente los elementos esperados."""
    datos = DataGenerator.generar_mejor_caso(100)

    assert len(datos) == 100
    assert sorted(datos) == list(range(1, 101))


@pytest.mark.parametrize("tamano_invalido", [0, -1, -50])
def test_generador_tamanos_invalidos_lanzan_excepcion(tamano_invalido: int) -> None:
    """Verifica el manejo defensivo ante tamaños de muestra menores o iguales a cero."""
    with pytest.raises(TamanoInvalidoError):
        DataGenerator.generar_caso_promedio(tamano_invalido)

    with pytest.raises(TamanoInvalidoError):
        DataGenerator.generar_peor_caso(tamano_invalido)

    with pytest.raises(TamanoInvalidoError):
        DataGenerator.generar_mejor_caso(tamano_invalido)
