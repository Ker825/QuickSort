from pathlib import Path

from rich.console import Console
from rich.panel import Panel

from source.algoritmo.quick_sort import QuickSort
from source.configuracion import ConfiguracionExperimento
from source.experimento.csv_writer import CsvWriter
from source.experimento.data_generator import DataGenerator
from source.experimento.experiment_runner import ExperimentRunner
from source.graphics.graficador import Graficador
from source.graphics.visualizador_csv import CargadorResultados

console = Console()


def notificar_progreso(caso: str, n: int, rep: int, total_reps: int) -> None:
    console.print(
        f"[#768df5]Ejecutando[/#768df5] [bold]{caso}[/bold] | "
        f"[#768df5]n=[/#768df5][#89ca79]{n} [/#89ca79]| [#768df5]repetición[/#768df5] [#89ca79]{rep}/{total_reps}[/#89ca79]"  # noqa: E501
    )


def main() -> None:
    config = ConfiguracionExperimento()
    ruta_tiempos = Path("output/resultados/csv/tiempos.csv")
    ruta_operaciones = Path("output/resultados/csv/operaciones.csv")
    directorio_graficas = Path("output/resultados/graficas")
    directorio_graficas.mkdir(parents=True, exist_ok=True)

    instrumentador = QuickSort()
    runner = ExperimentRunner(sorter=instrumentador)

    console.rule("[bold fa6464]1. Ejecución de Benchmarks[/bold fa6464]")

    with console.status("[cyan]Ejecutando benchmarks de QuickSort...[/cyan]"):
        # Se ejecuta el mejor caso, que es cuando la lista ya está ordenada de manera ascendente # noqa: E501
        runner.ejecutar_caso(
            "Mejor Caso",
            DataGenerator.generar_mejor_caso,
            list(config.tamanos),
            config.repeticiones,
            al_iterar=notificar_progreso,
        )  # noqa: E501

        # Se ejecuta el caso promedio, que es cuando la lista está desordenada de manera aleatoria # noqa: E501
        runner.ejecutar_caso(
            "Promedio",
            DataGenerator.generar_caso_promedio,
            list(config.tamanos),
            config.repeticiones,
            al_iterar=notificar_progreso,
        )  # noqa: E501

        # Se ejecuta el peor caso, que es cuando la lista está ordenada de manera inversa # noqa: E501
        runner.ejecutar_caso(
            "Peor Caso",
            DataGenerator.generar_peor_caso,
            list(config.tamanos),
            config.repeticiones,
            al_iterar=notificar_progreso,
        )  # noqa: E501

    console.print("[#89ca79]Benchmarks finalizados con éxito.[/#89ca79]")

    console.rule("[bold #fa6464]2. Generación de CSVs[/bold #fa6464]")
    # 4. Guardar archivos finales
    csv_writer = CsvWriter()
    csv_writer.guardar_csv(runner)

    cargador = CargadorResultados(ruta_tiempos, ruta_operaciones)
    df_tiempos = cargador.cargar_tiempos_agrupados(usar_mediana=False)
    df_operaciones = cargador.cargar_operaciones_agrupadas(usar_mediana=False)

    console.print("Datos agrupados listos para graficar:")
    console.print(df_tiempos)

    # 2. Generar y guardar la figura
    graficador = Graficador()
    ruta_salida = directorio_graficas / "grafica_1_tiempo_vs_tamano.png"
    ruta_salida2 = directorio_graficas / "grafica_2_n_vs_operaciones.png"
    ruta_salida3 = directorio_graficas / "grafica_3_experimental_vs_teorico.png"

    graficador.graficar_tiempo_vs_tamano(df_tiempos, ruta_salida)

    graficador.graficar_n_vs_operaciones(df_operaciones, ruta_salida2)

    graficador.graficar_exp_vs_teoria(df_tiempos, ruta_salida3)

    resumen_rutas = (
        f"[bold #fa6464]Tiempos vs Tamaño:[/bold #fa6464] {ruta_salida}\n"
        f"[bold #fa6464]Operaciones vs N:[/bold #fa6464] {ruta_salida2}\n"
        f"[bold #fa6464]Teoría vs Práctica:[/bold #fa6464] {ruta_salida3}"
    )

    console.print(
        Panel(
            resumen_rutas,
            title="[bold #89ca79]Gráficas Exportadas[/bold #89ca79]",
            expand=False,
        )
    )


if __name__ == "__main__":
    main()
