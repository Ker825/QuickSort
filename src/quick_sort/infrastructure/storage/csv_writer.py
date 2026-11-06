"""Componente de infraestructura para persistencia de benchmarks en formato CSV.

Aplica el Principio de Responsabilidad Única (SRP): desacopla la serialización y
escritura en disco de los resultados del algoritmo y de la ejecución del benchmark.
"""

import csv
from pathlib import Path

from quick_sort.application.services.experiment_runner import ExperimentRunner
from quick_sort.domain.exceptions import PersistenciaDatosError


class CsvWriter:
    """Escritor de resultados de benchmarks a archivos CSV tabulares.

    Attributes:
        directorio_salida (Path): Directorio destino para los archivos CSV.
    """

    def __init__(self, directorio_salida: Path | str = "output/resultados/csv") -> None:
        """Inicializa el escritor creando el directorio de salida si no existe.

        Args:
            directorio_salida: Ruta de la carpeta donde se persistirán los CSVs.
        """
        # [LÍNEA CLAVE] Normalización defensiva a Path para compatibilidad multiplataforma
        self.directorio_salida = Path(directorio_salida)
        self.directorio_salida.mkdir(parents=True, exist_ok=True)

    def guardar_csv(self, experiment_runner: ExperimentRunner) -> tuple[Path, Path]:
        """Exporta los registros de tiempos y operaciones a archivos CSV separados.

        Genera:
        1. 'tiempos.csv': tamano, caso, repeticion, tiempo_segundos
        2. 'operaciones.csv': tamano, caso, repeticion, comparaciones, intercambios, iteraciones, llamadas

        Args:
            experiment_runner: Orquestador con las colecciones de registros en memoria.

        Returns:
            tuple[Path, Path]: Rutas de los archivos (tiempos.csv, operaciones.csv).

        Raises:
            PersistenciaDatosError: Si ocurre un error de permisos o E/S al escribir en disco.
        """
        ruta_tiempos = self.directorio_salida / "tiempos.csv"
        ruta_operaciones = self.directorio_salida / "operaciones.csv"

        try:
            # [LÍNEA CLAVE] Persistencia de tiempos: newline='' evita líneas vacías en Windows (PEP 305)
            with open(
                ruta_tiempos, mode="w", newline="", encoding="utf-8"
            ) as f_tiempos:
                writer_tiempos = csv.writer(f_tiempos)
                writer_tiempos.writerow(
                    ["tamano", "caso", "repeticion", "tiempo_segundos"]
                )
                for rt in experiment_runner.registros_tiempos:
                    writer_tiempos.writerow(
                        [
                            rt.tamano,
                            rt.caso,
                            rt.repeticion,
                            # [LÍNEA CLAVE] Formato fijo a 8 decimales para evitar notación científica
                            f"{rt.tiempo_segundos:.8f}",
                        ]
                    )

            # [LÍNEA CLAVE] Persistencia de operaciones elementales del algoritmo
            with open(
                ruta_operaciones, mode="w", newline="", encoding="utf-8"
            ) as f_ops:
                writer_ops = csv.writer(f_ops)
                writer_ops.writerow(
                    [
                        "tamano",
                        "caso",
                        "repeticion",
                        "comparaciones",
                        "intercambios",
                        "iteraciones",
                        "llamadas",
                    ]
                )
                for ro in experiment_runner.registros_operaciones:
                    writer_ops.writerow(
                        [
                            ro.tamano,
                            ro.caso,
                            ro.repeticion,
                            ro.comparaciones,
                            ro.intercambios,
                            ro.iteraciones,
                            ro.llamadas_recursivas,
                        ]
                    )

            return ruta_tiempos, ruta_operaciones

        except OSError as exc:
            raise PersistenciaDatosError(
                f"Error al escribir archivos CSV en {self.directorio_salida}: {exc}"
            ) from exc
