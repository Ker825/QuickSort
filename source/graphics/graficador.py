from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

from .visualizador_csv import CargadorResultados


class Graficador:
    def __init__(self):
        self.cargador = CargadorResultados(
            ruta_tiempos="output/resultados/cvs/tiempos.csv",
            ruta_operaciones="output/resultados/cvs/operaciones.csv",
        )  # noqa: E501
        self.df_tiempos = self.cargador.cargar_tiempos_agrupados()
        self.df_operaciones = self.cargador.cargar_operaciones_agrupadas()

    def graficar_tiempo_vs_tamano(
        self, df_tiempos: pd.DataFrame, ruta_salida: Path | str
    ) -> None:
        fig, ax = plt.subplots(figsize=(10, 6))

        casos_unicos = df_tiempos["caso"].unique()

        for caso in casos_unicos:
            datos_caso = df_tiempos[df_tiempos["caso"] == caso]

            ax.plot(
                datos_caso["tamano"],
                datos_caso["tiempo_segundos"],
                marker="o",
                label=caso,
            )

        ax.set_title("Quick Sort: Tamaño de entrada vs Tiempo real")
        ax.set_xlabel("Tamaño de entrada (n)")
        ax.set_ylabel("Tiempo de ejecución (segundos)")
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.legend()

        fig.savefig(ruta_salida, dpi=300, bbox_inches="tight")
        plt.close(fig)

    def graficar_n_vs_operaciones(
        self, df_operaciones: pd.DataFrame, ruta_salida: Path | str
    ) -> None:

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

        df_peor = df_tiempos[df_tiempos["caso"] == "Peor Caso"]
        df_prom = df_tiempos[df_tiempos["caso"] == "Promedio"]

        fig, (ax_peor, ax_prom) = plt.subplots(1, 2, figsize=(14, 6))

        n_min = df_tiempos["tamano"].min()
        n_max = df_tiempos["tamano"].max()

        n_teorico = np.linspace(n_min, n_max, 200)

        # ─── Peor caso: O(n²) ───

        t_max_peor = df_peor.loc[
            df_peor["tamano"] == n_max,
            "tiempo_segundos",
        ].values[0]

        k_peor = t_max_peor / (n_max**2)

        ax_peor.plot(
            df_peor["tamano"],
            df_peor["tiempo_segundos"],
            marker="o",
            label="Experimental",
        )

        ax_peor.plot(
            n_teorico,
            k_peor * n_teorico**2,
            label="Teórico O(n²)",
        )

        # ─── Caso promedio: O(n log n) ───

        t_max_prom = df_prom.loc[
            df_prom["tamano"] == n_max,
            "tiempo_segundos",
        ].values[0]

        k_prom = t_max_prom / (n_max * np.log2(n_max))

        ax_prom.plot(
            df_prom["tamano"],
            df_prom["tiempo_segundos"],
            marker="o",
            label="Experimental",
        )

        ax_prom.plot(
            n_teorico,
            k_prom * n_teorico * np.log2(n_teorico),
            label="Teórico O(n log n)",
        )

        # ─── Configuración de gráficos ───

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

        fig.savefig(ruta_salida, dpi=300, bbox_inches="tight")
