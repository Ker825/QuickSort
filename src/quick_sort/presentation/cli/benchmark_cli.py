"""CLI para la orquestación y presentación en terminal del benchmark completo.

Aplica el Principio de Responsabilidad Única (SRP): integra el runner de experimentos,
la persistencia CSV, la carga de datos agrupados y la generación de gráficos Matplotlib,
presentando el progreso con componentes Rich.
"""

from collections.abc import Sequence

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from quick_sort.application.services.data_generator import DataGenerator
from quick_sort.application.services.experiment_runner import ExperimentRunner
from quick_sort.application.services.quick_sort import QuickSort
from quick_sort.core.config import ConfiguracionExperimento
from quick_sort.infrastructure.storage.csv_loader import CargadorResultados
from quick_sort.infrastructure.storage.csv_writer import CsvWriter
from quick_sort.infrastructure.visualization.graficador import Graficador

console = Console()


def notificar_progreso(caso: str, n: int, rep: int, total_reps: int) -> None:
    """Callback de telemetría para mostrar en terminal el avance de cada corrida."""
    console.print(
        f"[#768df5]Ejecutando[/#768df5] [bold]{caso}[/bold] | "
        f"[#768df5]n=[/#768df5][#89ca79]{n:<6}[/#89ca79] | "
        f"[#768df5]repetición[/#768df5] [#89ca79]{rep}/{total_reps}[/#89ca79]"
    )


def ejecutar_benchmark_cli(
    config: ConfiguracionExperimento | None = None,
    tamanos_personalizados: Sequence[int] | None = None,
) -> None:
    """Ejecuta el pipeline completo de benchmarking, persistencia CSV y generación de figuras.

    Args:
        config: Configuración de parámetros y rutas (usa defaults si es None).
        tamanos_personalizados: Lista opcional para sobreescribir los tamaños de prueba.
    """
    config_activa = config or ConfiguracionExperimento()
    tamanos = list(tamanos_personalizados or config_activa.tamanos)

    directorio_csv = config_activa.ruta_tiempos_csv.parent
    directorio_graficas = config_activa.directorio_graficas
    directorio_graficas.mkdir(parents=True, exist_ok=True)

    # 1. Instanciación desacoplada del algoritmo y del runner (DIP)
    instrumentador = QuickSort()
    runner = ExperimentRunner(sorter=instrumentador)

    console.rule("[bold #fa6464]1. Ejecución de Benchmarks de QuickSort[/bold #fa6464]")

    with console.status("[cyan]Ejecutando benchmarks de QuickSort...[/cyan]"):
        # Evaluación del Mejor Caso: particiones balanceadas O(n log n)
        runner.ejecutar_caso(
            "Mejor Caso",
            DataGenerator.generar_mejor_caso,
            tamanos,
            config_activa.repeticiones,
            al_iterar=notificar_progreso,
        )

        # Evaluación del Caso Promedio: distribución uniforme O(n log n)
        runner.ejecutar_caso(
            "Promedio",
            DataGenerator.generar_caso_promedio,
            tamanos,
            config_activa.repeticiones,
            al_iterar=notificar_progreso,
        )

        # Evaluación del Peor Caso: partición degenerada O(n^2)
        runner.ejecutar_caso(
            "Peor Caso",
            DataGenerator.generar_peor_caso,
            tamanos,
            config_activa.repeticiones,
            al_iterar=notificar_progreso,
        )

    console.print("[bold #89ca79]Benchmarks finalizados con éxito.[/bold #89ca79]")

    # 2. Persistencia en archivos CSV
    console.rule("[bold #fa6464]2. Exportación de Resultados CSV[/bold #fa6464]")
    csv_writer = CsvWriter(directorio_salida=directorio_csv)
    ruta_tiempos, ruta_operaciones = csv_writer.guardar_csv(runner)
    console.print(
        f"[cyan]Archivos generados:[/cyan]\n  • {ruta_tiempos}\n  • {ruta_operaciones}"
    )

    # 3. Transformación ETL y agregación de métricas
    cargador = CargadorResultados(ruta_tiempos, ruta_operaciones)
    df_tiempos = cargador.cargar_tiempos_agrupados(usar_mediana=False)
    df_operaciones = cargador.cargar_operaciones_agrupadas(usar_mediana=False)

    # Mostrar tabla resumen con Rich
    tabla_tiempos = Table(
        title="Tiempos Medios Agrupados",
        box=box.SIMPLE_HEAD,
        header_style="bold magenta",
    )
    for col in df_tiempos.columns:
        tabla_tiempos.add_column(str(col))
    for _, fila in df_tiempos.iterrows():
        tabla_tiempos.add_row(*[str(val) for val in fila.values])
    console.print(tabla_tiempos)

    # 4. Generación y exportación de figuras gráficas con Matplotlib
    console.rule("[bold #fa6464]3. Renderizado y Guardado de Gráficas[/bold #fa6464]")
    graficador = Graficador(cargador=cargador)

    ruta_salida1 = directorio_graficas / "grafica_1_tiempo_vs_tamano.png"
    ruta_salida2 = directorio_graficas / "grafica_2_n_vs_operaciones.png"
    ruta_salida3 = directorio_graficas / "grafica_3_experimental_vs_teorico.png"

    graficador.graficar_tiempo_vs_tamano(df_tiempos, ruta_salida1)
    graficador.graficar_n_vs_operaciones(df_operaciones, ruta_salida2)
    graficador.graficar_exp_vs_teoria(df_tiempos, ruta_salida3)

    resumen_rutas = (
        f"[bold #fa6464]Tiempos vs Tamaño:[/bold #fa6464] {ruta_salida1}\n"
        f"[bold #fa6464]Operaciones vs N:[/bold #fa6464] {ruta_salida2}\n"
        f"[bold #fa6464]Teoría vs Práctica:[/bold #fa6464] {ruta_salida3}"
    )

    console.print(
        Panel(
            resumen_rutas,
            title="[bold #89ca79]Gráficas Exportadas Exitosamente[/bold #89ca79]",
            box=box.ROUNDED,
            expand=False,
        )
    )
