"""Configuración central para experimentos y rutas del proyecto Quick Sort.

Este módulo encapsula los parámetros empíricos del benchmark (tamaños de entrada,
repeticiones por caso) y centraliza las rutas del sistema de archivos, garantizando
inmutabilidad y cumplimiento del principio de responsabilidad única (SRP).
"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class ConfiguracionExperimento:
    """Representa la configuración inmutable para el benchmark de Quick Sort.

    Attributes:
        tamanos: Secuencia inmutable con los tamaños de entrada (n) a evaluar.
        repeticiones: Número de iteraciones por cada tamaño y escenario para reducir
            el ruido del planificador del sistema operativo.
        ruta_tiempos_csv: Ubicación en disco para exportar los tiempos empíricos.
        ruta_operaciones_csv: Ubicación en disco para exportar el conteo de operaciones.
        directorio_graficas: Carpeta donde se guardarán las figuras generadas.
    """

    # Tamaños de prueba seleccionados para capturar transiciones asintóticas
    tamanos: tuple[int, ...] = (100, 200, 500, 1000, 2000, 10000)

    # Cantidad de repeticiones para calcular medias o medianas estadísticas confiables
    repeticiones: int = 10

    # Rutas por defecto del sistema de archivos normalizadas con pathlib
    ruta_tiempos_csv: Path = field(
        default_factory=lambda: Path("output/resultados/csv/tiempos.csv")
    )
    ruta_operaciones_csv: Path = field(
        default_factory=lambda: Path("output/resultados/csv/operaciones.csv")
    )
    directorio_graficas: Path = field(
        default_factory=lambda: Path("output/resultados/graficas")
    )

    def __post_init__(self) -> None:
        """Valida que los parámetros de configuración sean consistentes y positivos.

        Raises:
            ValueError: Si repeticiones es menor o igual a 0 o algún tamaño es inválido.
        """
        # Validación defensiva: previene estados inválidos antes de ejecutar benchmarks costosos
        if self.repeticiones <= 0:
            raise ValueError(
                f"El número de repeticiones debe ser positivo, recibido: {self.repeticiones}"
            )

        if not self.tamanos or any(n <= 0 for n in self.tamanos):
            raise ValueError(
                f"Los tamaños de entrada deben ser enteros positivos, recibido: {self.tamanos}"
            )
