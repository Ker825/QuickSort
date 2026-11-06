"""Capa de ingesta, agregación y transformación de datos experimentales (ETL).

Aplica el Principio de Responsabilidad Única (SRP): centraliza la lectura y
procesamiento estadístico de los archivos CSV generados por el benchmark,
proporcionando DataFrames consolidados para análisis y graficación.
"""

from pathlib import Path

import pandas as pd

from quick_sort.domain.exceptions import DatosInsuficientesError, PersistenciaDatosError


class CargadorResultados:
    """Carga y procesa estadísticamente las métricas de benchmarks persistidas en CSV.

    Attributes:
        ruta_tiempos (Path): Ruta al archivo con registros de tiempo.
        ruta_operaciones (Path): Ruta al archivo con registros de operaciones.
    """

    def __init__(self, ruta_tiempos: Path | str, ruta_operaciones: Path | str) -> None:
        """Inicializa el cargador normalizando rutas.

        Args:
            ruta_tiempos: Ubicación de tiempos.csv.
            ruta_operaciones: Ubicación de operaciones.csv.
        """
        # [LÍNEA CLAVE] Normalización a Path para soporte multiplataforma
        self.ruta_tiempos = Path(ruta_tiempos)
        self.ruta_operaciones = Path(ruta_operaciones)

    def cargar_tiempos_agrupados(self, usar_mediana: bool = False) -> pd.DataFrame:
        """Carga y sintetiza las repeticiones temporales por tamaño y escenario.

        Calcula una medida de tendencia central (media o mediana) para reducir
        múltiples repeticiones de una misma entrada (n) a un valor escalar representativo.

        Args:
            usar_mediana: Si es True, utiliza la mediana para mitigar ruido térmico
                o interrupciones del kernel. Si es False, usa la media aritmética.

        Returns:
            pd.DataFrame: Columnas ['tamano', 'caso', 'tiempo_segundos'].

        Raises:
            PersistenciaDatosError: Si el archivo no existe o no es accesible.
            DatosInsuficientesError: Si faltan columnas requeridas en el dataset.
        """
        if not self.ruta_tiempos.exists():
            raise PersistenciaDatosError(
                f"No se encontró el archivo de tiempos en: {self.ruta_tiempos}"
            )

        try:
            # [LÍNEA CLAVE] Lectura tabular del CSV mediante Pandas
            df = pd.read_csv(self.ruta_tiempos)
        except Exception as exc:
            raise PersistenciaDatosError(
                f"Error al leer {self.ruta_tiempos}: {exc}"
            ) from exc

        columnas_requeridas = {"tamano", "caso", "tiempo_segundos"}
        if not columnas_requeridas.issubset(df.columns):
            raise DatosInsuficientesError(
                f"El archivo {self.ruta_tiempos} debe contener las columnas {columnas_requeridas}"
            )

        # [LÍNEA CLAVE] Agrupación por clave compuesta (tamano, caso)
        agrupador = df.groupby(["tamano", "caso"], as_index=False)[["tiempo_segundos"]]

        # [LÍNEA CLAVE] Agregación estadística: la mediana es más robusta frente a outliers de SO
        df_resumen = agrupador.median() if usar_mediana else agrupador.mean()

        return df_resumen

    def cargar_operaciones_agrupadas(self, usar_mediana: bool = False) -> pd.DataFrame:
        """Carga y sintetiza el conteo de operaciones elementales por tamaño y escenario.

        Reduce las métricas computacionales (comparaciones, intercambios, iteraciones,
        llamadas recursivas) a un resumen representativo por (tamano, caso).

        Args:
            usar_mediana: Aplica mediana en lugar de media sobre las operaciones.

        Returns:
            pd.DataFrame: Columnas ['tamano', 'caso', 'comparaciones',
                'intercambios', 'iteraciones', 'llamadas'].

        Raises:
            PersistenciaDatosError: Si el archivo no existe o no es accesible.
            DatosInsuficientesError: Si el CSV carece de las columnas esperadas.
        """
        if not self.ruta_operaciones.exists():
            raise PersistenciaDatosError(
                f"No se encontró el archivo de operaciones en: {self.ruta_operaciones}"
            )

        try:
            df = pd.read_csv(self.ruta_operaciones)
        except Exception as exc:
            raise PersistenciaDatosError(
                f"Error al leer {self.ruta_operaciones}: {exc}"
            ) from exc

        columnas_metricas = [
            "comparaciones",
            "intercambios",
            "iteraciones",
            "llamadas",
        ]
        columnas_requeridas = set(["tamano", "caso"] + columnas_metricas)
        if not columnas_requeridas.issubset(df.columns):
            raise DatosInsuficientesError(
                f"El archivo {self.ruta_operaciones} debe contener {columnas_requeridas}"
            )

        # [LÍNEA CLAVE] Agregación multivariable agrupada por tamaño y escenario
        agrupador = df.groupby(["tamano", "caso"], as_index=False)[columnas_metricas]
        df_resumen = agrupador.median() if usar_mediana else agrupador.mean()

        return df_resumen
