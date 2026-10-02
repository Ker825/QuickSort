from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

from .visualizador_csv import CargadorResultados


class Graficador:
    """
    Clase encargada de generar visualizaciones gráficas de los resultados
    obtenidos en las pruebas de rendimiento de Quick Sort.
    """

    def __init__(self) -> None:
        """
        Inicializa el graficador cargando los datos de tiempos y operaciones
        desde los archivos CSV generados.
        """
        self.cargador = CargadorResultados(
            ruta_tiempos="output/resultados/csv/tiempos.csv",
            ruta_operaciones="output/resultados/csv/operaciones.csv",
        )  # noqa: E501
        self.df_tiempos = self.cargador.cargar_tiempos_agrupados()
        self.df_operaciones = self.cargador.cargar_operaciones_agrupadas()

    def graficar_tiempo_vs_tamano(
        self, df_tiempos: pd.DataFrame, ruta_salida: Path | str
    ) -> None:
        """
        Genera un gráfico que compara el tamaño de la entrada con el tiempo
        de ejecución real para los diferentes casos (Mejor, Promedio, Peor).

        Args:
            df_tiempos (pd.DataFrame): DataFrame con los datos de tiempo agrupados.
            ruta_salida (Path | str): Ruta donde se guardará la imagen generada.
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        # Obtener los diferentes tipos de casos (ej. Aleatorio, Ordenado, etc.)
        casos_unicos = df_tiempos["caso"].unique()

        for caso in casos_unicos:
            datos_caso = df_tiempos[df_tiempos["caso"] == caso]

            # Graficar serie de tiempo para cada caso
            ax.plot(
                datos_caso["tamano"],
                datos_caso["tiempo_segundos"],
                marker="o",
                label=caso,
            )

        # Configuración estética del gráfico
        ax.set_title("Quick Sort: Tamaño de entrada vs Tiempo real")
        ax.set_xlabel("Tamaño de entrada (n)")
        ax.set_ylabel("Tiempo de ejecución (segundos)")
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.legend()

        # Guardar y cerrar para liberar memoria
        fig.savefig(ruta_salida, dpi=300, bbox_inches="tight")
        plt.close(fig)

    def graficar_n_vs_operaciones(
        self, df_operaciones: pd.DataFrame, ruta_salida: Path | str
    ) -> None:
        """
        Genera un gráfico que muestra la relación entre el tamaño de la entrada
        y el número de comparaciones realizadas por el algoritmo.

        Args:
            df_operaciones (pd.DataFrame): DataFrame con los datos de operaciones agrupados.
            ruta_salida (Path | str): Ruta donde se guardará la imagen generada.
        """  # noqa: E501
        fig, ax = plt.subplots(figsize=(10, 6))

        casos_unicos = df_operaciones["caso"].unique()

        for caso in casos_unicos:
            datos_caso = df_operaciones[df_operaciones["caso"] == caso]

            ax.plot(
                datos_caso["tamano"],
                datos_caso["comparaciones"],
                marker="o",
                label=caso,
            )

        # Formatear el eje Y para mostrar números con separadores de miles
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
        ax.set_title("Quick Sort:  Tamaño (n) frente a Operaciones ")
        ax.set_xlabel("Tamaño de la entrada (n)")
        ax.set_ylabel("Numero de Operaciones (comparaciones)")
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.legend()

        fig.savefig(ruta_salida, dpi=300, bbox_inches="tight")
        plt.close(fig)

    def graficar_exp_vs_teoria(
        self, df_tiempos: pd.DataFrame, ruta_salida: Path | str
    ) -> None:
        """Genera una comparativa grafica entre los tiempos empiricos y las curvas teoricas.

        Ajusta las complejidades asintoticas de Quick Sort (O(n^2) para el peor caso
        y O(n log n) para el caso promedio) calculando una constante de escala k
        con base en la medicion del tamano maximo analizado.

        Args:
            df_tiempos: DataFrame con las columnas 'caso', 'tamano' y 'tiempo_segundos'.
            ruta_salida: Ruta del sistema de archivos donde se guardara la imagen generada.

        Raises:
            KeyError: Si faltan columnas requeridas en el DataFrame.
            IndexError: Si n_max no existe dentro de las series de peor caso o promedio.
        """  # noqa: E501

        # Filtrar datos por casos específicos para la comparación teórica
        df_peor = df_tiempos[df_tiempos["caso"] == "Peor Caso"]
        df_prom = df_tiempos[df_tiempos["caso"] == "Promedio"]

        # Crear una figura con dos subgráficos
        fig, (ax_peor, ax_prom) = plt.subplots(1, 2, figsize=(14, 6))

        n_min = df_tiempos["tamano"].min()
        n_max = df_tiempos["tamano"].max()

        # Generar puntos intermedios para curvas teóricas suaves
        n_teorico = np.linspace(n_min, n_max, 200)

        # ─── Peor caso: O(n²) ───

        # Ajuste simple de la curva teórica basada en el último punto experimental
        t_max_peor = df_peor.loc[
            df_peor["tamano"] == n_max,
            "tiempo_segundos",
        ].values[0]

        # Calculo de constante k para normalizar unidades: t = k * n^2  =>  k = t / n^2
        k_peor = t_max_peor / (n_max**2)

        # Graficado de mediciones empiricas (puntos discretos)
        ax_peor.plot(
            df_peor["tamano"],
            df_peor["tiempo_segundos"],
            marker="o",
            label="Experimental",
        )

        # Proyeccion de la funcion teorica escalada
        ax_peor.plot(
            n_teorico,
            k_peor * n_teorico**2,
            label="Teórico O(n²)",
        )

        # ─── Caso promedio: O(n log n) ───

        # Ajuste de la curva O(n log n)
        # Tiempo real maximo para el caso promedio
        t_max_prom = df_prom.loc[
            df_prom["tamano"] == n_max,
            "tiempo_segundos",
        ].values[0]

        # Constante k para orden logaritmico-lineal: t = k * (n * log2(n))
        k_prom = t_max_prom / (n_max * np.log2(n_max))

        # Mediciones empiricas del caso promedio
        ax_prom.plot(
            df_prom["tamano"],
            df_prom["tiempo_segundos"],
            marker="o",
            label="Experimental",
        )

        # Proyeccion de la funcion teorica escalada
        ax_prom.plot(
            n_teorico,
            k_prom * n_teorico * np.log2(n_teorico),
            label="Teórico O(n log n)",
        )

        # ─── Ejes, leyendas y exportacion ───

        ax_peor.set_title("Quick Sort: Peor caso")
        ax_peor.set_xlabel("Tamaño de la entrada (n)")
        ax_peor.set_ylabel("Tiempo (segundos)")
        ax_peor.grid(True, linestyle="--", alpha=0.6)
        ax_peor.legend()

        ax_prom.set_title("Quick Sort: Caso promedio")
        ax_prom.set_xlabel("Tamaño de la entrada (n)")
        ax_prom.set_ylabel("Tiempo (segundos)")
        ax_prom.grid(True, linestyle="--", alpha=0.6)
        ax_prom.legend()

        # Guardado en disco y liberacion de memoria del backend grafico
        fig.savefig(ruta_salida, dpi=300, bbox_inches="tight")
