from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.tree import Tree

from source.demo.models.nodo_recursion import NodoRecursion
from source.demo.quick_sort_visual import QuickSortVisual

console = Console()


def mostrar_explicacion() -> None:
    """Muestra una explicación breve de cómo funciona Quick Sort."""

    texto = (
        "[bold cyan]¿CÓMO FUNCIONA QUICK SORT?[/bold cyan]\n\n"
        "[bold]1.[/bold] Elegimos un elemento como [yellow]pivote[/yellow].\n"
        "[bold]2.[/bold] Particionamos la lista alrededor del pivote.\n"
        "[bold]3.[/bold] El pivote queda en su posición definitiva.\n"
        "[bold]4.[/bold] Repetimos el proceso con las dos particiones.\n"
        "[bold]5.[/bold] La recursión termina cuando una sublista "
        "tiene 0 o 1 elementos."
    )

    console.print(
        Panel(
            texto,
            title="Quick Sort",
            border_style="cyan",
        )
    )


def construir_arbol(
    nodo: NodoRecursion,
    nivel: int = 0,
) -> Tree:
    """Convierte un NodoRecursion en un árbol de Rich."""

    if nodo.es_caso_base:
        texto = (
            f"[dim]Sublista: {nodo.sublista}[/dim]\n"
            "[bold green]✓ CASO BASE[/bold green]\n"
            "[green]0 o 1 elementos → ya está ordenada[/green]"
        )

        return Tree(texto)

    texto = (
        f"[bold]Sublista:[/bold] {nodo.sublista}\n"
        f"[yellow]Pivote:[/yellow] {nodo.pivote}\n"
        f"[cyan]Posición final del pivote (índice):[/cyan] "
        f"{nodo.posicion_pivote}\n"
        f"[green]Resultado:[/green] {nodo.resultado}"
    )

    arbol = Tree(texto)

    if nodo.izquierda is not None:
        izquierda = construir_arbol(nodo.izquierda, nivel + 1)

        arbol.add(
            Tree(
                "[bold blue]Izquierda[/bold blue] "
                "[dim](partición anterior al pivote)[/dim]"
            )
        )

        # Recuperamos el último nodo añadido para agregar
        # el árbol correspondiente.
        rama_izquierda = arbol.children[-1]
        rama_izquierda.children.append(izquierda)

    if nodo.derecha is not None:
        derecha = construir_arbol(nodo.derecha, nivel + 1)

        arbol.add(
            Tree(
                "[bold magenta]Derecha[/bold magenta] "
                "[dim](partición posterior al pivote)[/dim]"
            )
        )

        rama_derecha = arbol.children[-1]
        rama_derecha.children.append(derecha)

    return arbol


def mostrar_metricas(sorter: QuickSortVisual) -> None:
    """Muestra las métricas obtenidas durante la ejecución."""

    metricas = sorter.metricas

    tabla = Table(
        title="Métricas de Ejecución",
        header_style="bold magenta",
    )

    tabla.add_column("Comparaciones", justify="right")
    tabla.add_column("Intercambios", justify="right")
    tabla.add_column("Iteraciones", justify="right")
    tabla.add_column("Recursiones", justify="right")

    tabla.add_row(
        str(metricas.comparaciones),
        str(metricas.intercambios),
        str(metricas.iteraciones),
        str(metricas.llamadas_recursivas),
    )

    console.print(tabla)


def demostrar_caso(
    nombre: str,
    lista_original: list[int],
) -> None:
    """Ejecuta y muestra un caso de demostración."""

    console.print()
    console.print(Rule(f"[bold cyan]{nombre}[/bold cyan]"))

    lista_trabajo = lista_original.copy()

    sorter = QuickSortVisual()

    sorter.ordenar(
        lista_trabajo,
        0,
        len(lista_trabajo) - 1,
    )

    assert lista_trabajo == sorted(lista_original)

    console.print()
    console.print("[bold cyan]Árbol de recursión[/bold cyan]")

    raiz = sorter.obtener_arbol()

    if raiz is not None:
        arbol = construir_arbol(raiz)
        console.print(arbol)

    console.print()

    console.print(
        Panel(
            f"[bold]Lista original:[/bold] {lista_original}\n"
            f"[bold green]Lista ordenada:[/bold green] "
            f"{lista_trabajo}",
            title="Resultado final",
            border_style="green",
        )
    )

    console.print()

    mostrar_metricas(sorter)


def demostrar_funcionamiento() -> None:
    """Ejecuta la demostración completa."""

    console.clear()

    console.print(Rule("[bold cyan]DEMOSTRACIÓN VISUAL: QUICK SORT[/bold cyan]"))

    mostrar_explicacion()

    casos_demo = {
        "Caso Promedio (Desordenado)": [34, 7, 23, 32, 5, 62, 12, 18],
        "Peor Caso (Ya Ordenado)": [3, 8, 12, 15, 20, 25, 30],
        "Caso Favorable (Balanceado)": [15, 8, 3, 12, 25, 20, 30],
    }

    for nombre, lista in casos_demo.items():
        demostrar_caso(nombre, lista)

    console.print()
    console.print(
        Panel(
            "[bold]Idea clave:[/bold]\n\n"
            "Cada llamada de Quick Sort coloca un pivote "
            "en su posición definitiva y después repite "
            "el mismo proceso sobre las particiones restantes.",
            title="¿Qué debemos recordar?",
            border_style="cyan",
        )
    )


if __name__ == "__main__":
    demostrar_funcionamiento()
