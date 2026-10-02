import csv
from pathlib import Path

from source.experimento.experiment_runner import ExperimentRunner


class CsvWriter:
    def __init__(self, directorio_salida: str = "output/resultados/csv") -> None:
        self.directorio_salida = Path(directorio_salida)
        self.directorio_salida.mkdir(parents=True, exist_ok=True)

    def guardar_csv(self, experiment_runner: ExperimentRunner) -> None:
        """Exporta los resultados del benchmark a archivos CSV estructurados.

        Genera dos archivos independientes en el directorio de salida configurado:
        1. 'tiempos.csv': Métricas de tiempo de ejecución real por caso y repetición.
        2. 'operaciones.csv': Conteo de operaciones elementales del algoritmo
           (comparaciones, intercambios, iteraciones y llamadas recursivas).

        Args:
            experiment_runner (ExperimentRunner): Instancia que contiene las
                colecciones de métricas recolectadas (`registros_tiempos` y
                `registros_operaciones`).

        Raises:
            OSError: Si ocurren errores de E/S o permisos al crear o escribir
                en los archivos.
        """
        # --- 1. Persistencia de métricas de tiempo ---
        # Resolución dinámica de la ruta destino mediante pathlib
        ruta_tiempos = self.directorio_salida / "tiempos.csv"

        # newline="" previene filas vacías adicionales en sistemas Windows (PEP 305)
        with open(ruta_tiempos, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            # Encabezados del esquema relacional para tiempos
            writer.writerow(["tamano", "caso", "repeticion", "tiempo_segundos"])

            # Volcado secuencial de registros de tiempo
            for rt in experiment_runner.registros_tiempos:
                writer.writerow(
                    [
                        rt.tamano,
                        rt.caso,
                        rt.repeticion,
                        # Formateo fijo a 8 decimales para evitar notación científica y pérdida de precisión  # noqa: E501
                        f"{rt.tiempo_segundos:.8f}",
                    ]
                )

        # --- 2. Persistencia de métricas de operaciones algorítmicas ---
        ruta_operaciones = self.directorio_salida / "operaciones.csv"

        with open(ruta_operaciones, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            # Encabezados alineados con el seguimiento analítico de complejidad
            writer.writerow(
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

            # Volcado de métricas operacionales discretas (enteros sin formateo flotante) # noqa: E501
            for ro in experiment_runner.registros_operaciones:
                writer.writerow(
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
