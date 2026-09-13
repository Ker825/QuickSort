from source.experimento.data_generator import DataGenerator


def test_generador_caso_promedio() -> None:
    datos = DataGenerator.generar_caso_promedio(100)

    assert len(datos) == 100
    assert len(set(datos)) == 100


def test_generador_peor_caso() -> None:
    datos = DataGenerator.generar_peor_caso(100)

    assert datos == list(range(1, 101))


def test_generador_mejor_caso() -> None:
    datos = DataGenerator.generar_mejor_caso(100)

    assert len(datos) == 100
    assert sorted(datos) == list(range(1, 101))
