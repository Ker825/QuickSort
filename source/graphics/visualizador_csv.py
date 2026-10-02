from pathlib import Path

import pandas as pd


class CargadorResultados:
    """Capa de ingesta, agregación y transformación de datos experimentales (ETL).

    Aplica el Principio de Responsabilidad Única (SRP): centraliza la lectura
    y procesamiento estadístico de los archivos CSV generados por el benchmark,
    proporcionando DataFrames consolidados listos para análisis y graficación.

    Attributes:
        ruta_tiempos (Path): Ruta al archivo CSV con registros de tiempos.
        ruta_operaciones (Path): Ruta al archivo CSV con métricas de operaciones.
    """

    def __init__(self, ruta_tiempos: Path | str, ruta_operaciones: Path | str) -> None:
        """Normaliza las rutas de entrada a objetos Path para portabilidad de SO.

        Args:
            ruta_tiempos (Path | str): Ubicación del archivo de tiempos.
            ruta_operaciones (Path | str): Ubicación del archivo de operaciones.
        """
        # Normalización defensiva: asegura soporte multiplataforma (Windows/Linux/POSIX)
        self.ruta_tiempos = Path(ruta_tiempos)
        self.ruta_operaciones = Path(ruta_operaciones)

    def cargar_tiempos_agrupados(self, usar_mediana: bool = False) -> pd.DataFrame:
        """Carga y sintetiza las repeticiones temporales por tamaño y escenario.

        Calcula una medida de tendencia central para colapsar las múltiples
        repeticiones de un mismo tamaño de entrada (n) en un valor único representativo.

        Args:
            usar_mediana (bool, optional): Si es True, usa la mediana para mitigar
                el impacto de ruidos del SO (interrupciones, throttling térmico, GC).
                Si es False, usa la media aritmética estándar. Defaults to False.

        Returns:
            pd.DataFrame: DataFrame agrupado con columnas ['tamano', 'caso', 'tiempo_segundos'].

        Raises:
            FileNotFoundError: Si el archivo en `ruta_tiempos` no existe en disco.
            KeyError: Si el CSV carece de las columnas esperadas.
        """  # noqa: E501
        # Carga del dataset crudo de tiempos desde disco
        df = pd.read_csv(self.ruta_tiempos)

        # Proyección de la métrica objetivo agrupada por clave compuesta (tamaño, escenario) # noqa: E501
        agrupador = df.groupby(["tamano", "caso"])["tiempo_segundos"]

        # La mediana es estadísticamente más robusta ante outliers producidos por el planificador del kernel # noqa: E501
        df_resumen = agrupador.median() if usar_mediana else agrupador.mean()

        # reset_index aplana el MultiIndex resultante para que 'tamano' y 'caso' vuelvan a ser columnas # noqa: E501
        return df_resumen.reset_index()

    def cargar_operaciones_agrupadas(self, usar_mediana: bool = False) -> pd.DataFrame:
        """Carga y sintetiza el conteo de operaciones elementales por tamaño y escenario.

        Reduce las métricas computacionales (comparaciones, intercambios,
        iteraciones y llamadas recursivas) a un único resumen representativo por (tamano, caso).

        Args:
            usar_mediana (bool, optional): Determina si se aplica mediana en vez de
                media sobre las operaciones registradas. Defaults to False.

        Returns:
            pd.DataFrame: DataFrame agrupado con ['tamano', 'caso', 'comparaciones',
                'intercambios', 'iteraciones', 'llamadas'].

        Raises:
            FileNotFoundError: Si el archivo en `ruta_operaciones` no existe en disco.
            KeyError: Si alguna de las métricas clave no se encuentra en el CSV.
        """  # noqa: E501
        # Carga del dataset crudo de operaciones algorítmicas
        df = pd.read_csv(self.ruta_operaciones)

        # Selección explícita de variables dependientes para evitar procesar la columna 'repeticion' # noqa: E501
        columnas_metricas = ["comparaciones", "intercambios", "iteraciones", "llamadas"]
        agrupador = df.groupby(["tamano", "caso"])[columnas_metricas]

        # Agregación vectorial de todas las columnas métricas en una sola operación
        df_resumen = agrupador.median() if usar_mediana else agrupador.mean()

        # Convierte el MultiIndex de la agrupación en columnas tabulares regulares
        return df_resumen.reset_index()
