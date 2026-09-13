import csv
from pathlib import Path

from source.experimento.experiment_runner import ExperimentRunner


class CsvWriter:
    def __init__(self, directorio_salida: str = "output/resultados/cvs"):
        self.directorio_salida = Path(directorio_salida)
        self.directorio_salida.mkdir(parents=True, exist_ok=True)

    def guardar_csv(self, experiment_runer: ExperimentRunner) -> None:
        """Exporta los datos capturados a tiempos.csv y operaciones.csv."""
        ruta_tiempos = self.directorio_salida / "tiempos.csv"
        with open(ruta_tiempos, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["tamano", "caso", "repeticion", "tiempo_segundos"])
            for rt in experiment_runer.registros_tiempos:
                writer.writerow(
                    [
                        rt.tamano,
                        rt.caso,
                        rt.repeticion,
                        f"{rt.tiempo_segundos:.8f}",
                    ]
                )

        ruta_operaciones = self.directorio_salida / "operaciones.csv"
        with open(ruta_operaciones, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
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
            for ro in experiment_runer.registros_operaciones:
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
