"""Pruebas unitarias para la infraestructura de almacenamiento y configuración."""

from pathlib import Path

import pytest

from quick_sort.application.services.data_generator import DataGenerator
from quick_sort.application.services.experiment_runner import ExperimentRunner
from quick_sort.application.services.quick_sort import QuickSort
from quick_sort.core.config import ConfiguracionExperimento
from quick_sort.infrastructure.storage.csv_loader import CargadorResultados
from quick_sort.infrastructure.storage.csv_writer import CsvWriter


def test_configuracion_experimento_valida_parametros() -> None:
    """Verifica que la configuración rechace valores no positivos."""
    with pytest.raises(ValueError):
        ConfiguracionExperimento(repeticiones=0)

    with pytest.raises(ValueError):
        ConfiguracionExperimento(tamanos=())


def test_flujo_csv_writer_y_loader(tmp_path: Path) -> None:
    """Verifica el ciclo de vida completo: benchmark -> CSV -> lectura ETL agrupada."""
    sorter = QuickSort()
    runner = ExperimentRunner(sorter=sorter)

    # Benchmark pequeño para prueba rápida
    runner.ejecutar_caso(
        nombre_caso="Caso Test",
        generador_fn=DataGenerator.generar_caso_promedio,
        tamanos=[10, 20],
        repeticiones=2,
    )

    writer = CsvWriter(directorio_salida=tmp_path)
    ruta_tiempos, ruta_operaciones = writer.guardar_csv(runner)

    assert ruta_tiempos.exists()
    assert ruta_operaciones.exists()

    cargador = CargadorResultados(ruta_tiempos, ruta_operaciones)
    df_tiempos = cargador.cargar_tiempos_agrupados()
    df_operaciones = cargador.cargar_operaciones_agrupadas()

    assert len(df_tiempos) == 2
    assert "tiempo_segundos" in df_tiempos.columns
    assert len(df_operaciones) == 2
    assert "comparaciones" in df_operaciones.columns
