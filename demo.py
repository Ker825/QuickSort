from rich.console import Console
from rich.table import Table

from source.algoritmo.quick_sort import QuickSort


def demostrar_funcionamiento() -> None:
    console = Console()
    console.rule("[bold cyan]DEMOSTRACION VISUAL: QUICK SORT[/bold cyan]")

    casos_demo = {
        "Caso Promedio (Desordenado)": [34, 7, 23, 32, 5, 62, 12, 18],
        "Peor Caso (Ya Ordenado)": [3, 8, 12, 15, 20, 25, 30],
        "Mejor Caso (Pivote Mediana)": [15, 8, 3, 12, 25, 20, 30],
    }

    tabla = Table(title="Metricas de Ejecucion", header_style="bold magenta")
    tabla.add_column("Caso", style="cyan", no_wrap=True)
    tabla.add_column("Original", style="dim")
    tabla.add_column("Ordenada", style="green")
    tabla.add_column("Comparaciones", justify="right", style="yellow")
    tabla.add_column("Intercambios", justify="right", style="yellow")
    tabla.add_column("Recursiones", justify="right", style="yellow")

    sorter = QuickSort()

    for nombre, lista_original in casos_demo.items():
        lista_trabajo = lista_original.copy()
        sorter.reiniciar_metricas()

        sorter.ordenar(lista_trabajo, 0, len(lista_trabajo) - 1)
        assert lista_trabajo == sorted(lista_original), "Error de ordenamiento"

        m = sorter.metricas
        tabla.add_row(
            nombre,
            str(lista_original),
            str(lista_trabajo),
            str(m.comparaciones),
            str(m.intercambios),
            str(m.llamadas_recursivas),
        )

    console.print(tabla)
    console.rule(style="cyan")


if __name__ == "__main__":
    demostrar_funcionamiento()
