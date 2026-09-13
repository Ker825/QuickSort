from pathlib import Path

import pandas as pd  # type: ignore[import-untyped]


class CargadorResultados:
    """Responsable exclusiva de leer, validar y agregar los datos experimentales."""

    def __init__(self, ruta_tiempos: Path | str, ruta_operaciones: Path | str) -> None:
        self.ruta_tiempos = Path(ruta_tiempos)
        self.ruta_operaciones = Path(ruta_operaciones)

    def cargar_tiempos_agrupados(self, usar_mediana: bool = False) -> pd.DataFrame:
        """
        Carga tiempos.csv y calcula el valor representativo por (tamano, caso).
        Columnas esperadas de entrada: tamano, caso, repeticion, tiempo_segundos
        """
        df = pd.read_csv(self.ruta_tiempos)

        # Agrupar repeticiones por tamaño y escenario
        agrupador = df.groupby(["tamano", "caso"])["tiempo_segundos"]
        df_resumen = agrupador.median() if usar_mediana else agrupador.mean()

        # reset_index para regresar 'tamaño' y 'caso' como columnas normales
        return df_resumen.reset_index()

    def cargar_operaciones_agrupadas(self, usar_mediana: bool = False) -> pd.DataFrame:
        """
        Carga operaciones.csv y calcula el valor representativo por (tamano, caso).
        Columnas esperadas de entrada: tamano, caso, repeticion, comparaciones,
                                      intercambios, iteraciones, llamadas
        """
        df = pd.read_csv(self.ruta_operaciones)

        columnas_metricas = ["comparaciones", "intercambios", "iteraciones", "llamadas"]
        agrupador = df.groupby(["tamano", "caso"])[columnas_metricas]

        df_resumen = agrupador.median() if usar_mediana else agrupador.mean()

        return df_resumen.reset_index()
