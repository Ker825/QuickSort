"""Punto de entrada principal para el pipeline de benchmarking de Quick Sort.

Ejecuta el benchmark en los tres escenarios asintóticos (Mejor, Promedio, Peor),
exporta las mediciones crudas a CSV, realiza el procesamiento estadístico ETL y
genera las gráficas comparativas con Matplotlib.
"""

import sys
from pathlib import Path

# Asegura que el directorio 'src' esté en sys.path al invocar el script directamente
_src_path = str(Path(__file__).resolve().parent / "src")
if _src_path not in sys.path:
    sys.path.insert(0, _src_path)

from quick_sort.presentation.cli.benchmark_cli import ejecutar_benchmark_cli


def main() -> None:
    """Función de entrada para la ejecución del benchmark completo."""
    ejecutar_benchmark_cli()


if __name__ == "__main__":
    main()
