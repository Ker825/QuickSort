"""Módulo de infraestructura para generación de figuras analíticas con Matplotlib.

Aplica el Principio de Responsabilidad Única (SRP): traduce los DataFrames de métricas
empíricas a visualizaciones gráficas comparativas, superponiendo cotas asintóticas teóricas.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

from quick_sort.domain.exceptions import DatosInsuficientesError
from quick_sort.infrastructure.storage.csv_loader import CargadorResultados


class Graficador:
    """Generador de gráficos estadísticos y asintóticos para Quick Sort."""

    def __init__(
        self,
        cargador: CargadorResultados | None = None,
        ruta_tiempos: Path | str = "output/resultados/csv/tiempos.csv",
        ruta_operaciones: Path | str = "output/resultados/csv/operaciones.csv",
    ) -> None:
        """Inicializa el graficador inyectando el cargador o construyendo uno por defecto.

        Args:
            cargador: Instancia de CargadorResultados (DIP).
            ruta_tiempos: Ruta por defecto si no se inyecta cargador.
            ruta_operaciones: Ruta por defecto si no se inyecta cargador.
        """
        # [LÍNEA CLAVE] Inversión de dependencias (DIP) con valor por defecto
        self.cargador = cargador or CargadorResultados(
            ruta_tiempos=ruta_tiempos,
            ruta_operaciones=ruta_operaciones,
        )

    def graficar_tiempo_vs_tamano(
        self, df_tiempos: pd.DataFrame, ruta_salida: Path | str
    ) -> Path:
        """Genera un gráfico comparativo de Tamaño de entrada (n) vs Tiempo de ejecución.

        Args:
            df_tiempos: DataFrame con columnas ['tamano', 'caso', 'tiempo_segundos'].
            ruta_salida: Ruta de destino donde se guardará la imagen en disco.

        Returns:
            Path: Ruta resuelta de la imagen exportada.

        Raises:
            DatosInsuficientesError: Si el DataFrame está vacío o carece de columnas.
        """
        if df_tiempos.empty:
            raise DatosInsuficientesError("El DataFrame de tiempos está vacío.")

        ruta_salida = Path(ruta_salida)
        ruta_salida.parent.mkdir(parents=True, exist_ok=True)

        fig, ax = plt.subplots(figsize=(10, 6))

        # [LÍNEA CLAVE] Extracción de los escenarios evaluados para iteración de series
        casos_unicos = df_tiempos["caso"].unique()

        for caso in casos_unicos:
            datos_caso = df_tiempos[df_tiempos["caso"] == caso]
            ax.plot(
                datos_caso["tamano"],
                datos_caso["tiempo_segundos"],
                marker="o",
                label=str(caso),
            )

        # Configuración estética
        ax.set_title("Quick Sort: Tamaño de entrada vs Tiempo real")
        ax.set_xlabel("Tamaño de entrada (n)")
        ax.set_ylabel("Tiempo de ejecución (segundos)")
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.legend()

        # [LÍNEA CLAVE] Guardado en alta resolución y liberación de memoria
        fig.savefig(ruta_salida, dpi=300, bbox_inches="tight")
        plt.close(fig)
        return ruta_salida

    def graficar_n_vs_operaciones(
        self, df_operaciones: pd.DataFrame, ruta_salida: Path | str
    ) -> Path:
        """Genera un gráfico de Tamaño de entrada (n) frente a Número de Comparaciones.

        Args:
            df_operaciones: DataFrame con ['tamano', 'caso', 'comparaciones'].
            ruta_salida: Destino de la figura generada.

        Returns:
            Path: Ruta de la imagen guardada.

        Raises:
            DatosInsuficientesError: Si el DataFrame está vacío.
        """
        if df_operaciones.empty:
            raise DatosInsuficientesError("El DataFrame de operaciones está vacío.")

        ruta_salida = Path(ruta_salida)
        ruta_salida.parent.mkdir(parents=True, exist_ok=True)

        fig, ax = plt.subplots(figsize=(10, 6))
        casos_unicos = df_operaciones["caso"].unique()

        for caso in casos_unicos:
            datos_caso = df_operaciones[df_operaciones["caso"] == caso]
            ax.plot(
                datos_caso["tamano"],
                datos_caso["comparaciones"],
                marker="o",
                label=str(caso),
            )

        # [LÍNEA CLAVE] Formateo con separador de miles para legibilidad de grandes cifras
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
        ax.set_title("Quick Sort: Tamaño (n) frente a Operaciones")
        ax.set_xlabel("Tamaño de la entrada (n)")
        ax.set_ylabel("Número de Operaciones (comparaciones)")
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.legend()

        fig.savefig(ruta_salida, dpi=300, bbox_inches="tight")
        plt.close(fig)
        return ruta_salida

    def graficar_exp_vs_teoria(
        self, df_tiempos: pd.DataFrame, ruta_salida: Path | str
    ) -> Path:
        """Compara tiempos empíricos con curvas asintóticas teóricas O(n^2) y O(n log n).

        Calcula constantes empíricas de escala k utilizando el punto experimental
        máximo analizado:
        - Peor Caso: k_peor = t_max / (n_max^2)
        - Promedio: k_prom = t_max / (n_max * log2(n_max))

        Args:
            df_tiempos: DataFrame con columnas 'caso', 'tamano', 'tiempo_segundos'.
            ruta_salida: Ruta de la figura a exportar.

        Returns:
            Path: Ruta de la figura guardada.

        Raises:
            DatosInsuficientesError: Si faltan datos de 'Peor Caso' o 'Promedio'.
        """
        if df_tiempos.empty:
            raise DatosInsuficientesError("El DataFrame de tiempos está vacío.")

        ruta_salida = Path(ruta_salida)
        ruta_salida.parent.mkdir(parents=True, exist_ok=True)

        df_peor = df_tiempos[df_tiempos["caso"] == "Peor Caso"]
        df_prom = df_tiempos[df_tiempos["caso"] == "Promedio"]

        if df_peor.empty or df_prom.empty:
            raise DatosInsuficientesError(
                "Se requieren registros tanto de 'Peor Caso' como de 'Promedio'."
            )

        fig, (ax_peor, ax_prom) = plt.subplots(1, 2, figsize=(14, 6))

        n_min = float(df_tiempos["tamano"].min())
        n_max = float(df_tiempos["tamano"].max())

        # [LÍNEA CLAVE] Espacio muestral continuo para graficar curvas teóricas suaves
        n_teorico = np.linspace(n_min, n_max, 200)

        # ─── Peor caso: Ajuste asintótico O(n^2) ───
        t_max_peor_series = df_peor.loc[
            df_peor["tamano"] == int(n_max), "tiempo_segundos"
        ]
        if t_max_peor_series.empty:
            t_max_peor = float(df_peor["tiempo_segundos"].iloc[-1])
        else:
            t_max_peor = float(t_max_peor_series.values[0])

        # [LÍNEA CLAVE] Constante de proporcionalidad k: t = k * n^2  =>  k = t / n^2
        k_peor = t_max_peor / (n_max**2)

        ax_peor.plot(
            df_peor["tamano"],
            df_peor["tiempo_segundos"],
            marker="o",
            label="Experimental",
        )
        ax_peor.plot(
            n_teorico,
            k_peor * (n_teorico**2),
            label="Teórico O(n²)",
        )
        ax_peor.set_title("Quick Sort: Peor caso")
        ax_peor.set_xlabel("Tamaño de la entrada (n)")
        ax_peor.set_ylabel("Tiempo (segundos)")
        ax_peor.grid(True, linestyle="--", alpha=0.6)
        ax_peor.legend()

        # ─── Caso promedio: Ajuste asintótico O(n log n) ───
        t_max_prom_series = df_prom.loc[
            df_prom["tamano"] == int(n_max), "tiempo_segundos"
        ]
        if t_max_prom_series.empty:
            t_max_prom = float(df_prom["tiempo_segundos"].iloc[-1])
        else:
            t_max_prom = float(t_max_prom_series.values[0])

        # [LÍNEA CLAVE] Constante de proporcionalidad k: t = k * (n * log2(n))
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
        ax_prom.set_title("Quick Sort: Caso promedio")
        ax_prom.set_xlabel("Tamaño de la entrada (n)")
        ax_prom.set_ylabel("Tiempo (segundos)")
        ax_prom.grid(True, linestyle="--", alpha=0.6)
        ax_prom.legend()

        fig.savefig(ruta_salida, dpi=300, bbox_inches="tight")
        plt.close(fig)
        return ruta_salida
