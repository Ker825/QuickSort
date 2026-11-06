"""Demostración visual e interactiva del algoritmo Quick Sort utilizando Rich.

Este módulo ilustra paso a paso la mecánica de partición, la selección del pivote,
la recursión simétrica (Divide y Vencerás) y las diferencias asintóticas entre el
Mejor Caso, el Caso Promedio y el Peor Caso mediante árboles jerárquicos y tablas
estilizadas en la terminal.
"""

import sys
from pathlib import Path
from typing import Any

# Asegura que el directorio 'src' esté en sys.path al invocar el script directamente
_src_path = str(Path(__file__).resolve().parent / "src")
if _src_path not in sys.path:
    sys.path.insert(0, _src_path)

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from quick_sort.application.services.quick_sort_visual import QuickSortVisual
from quick_sort.domain.models.nodo_recursion import NodoRecursion

# Instancia central de Console para renderizado con Rich en la terminal
console = Console()


def mostrar_explicacion() -> None:
    """Muestra una tarjeta explicativa en la consola con el fundamento teórico de Quick Sort.

    Explica la estrategia de Divide y Vencerás y los cinco pasos fundamentales
    que sigue el algoritmo para ordenar una secuencia de números.
    """
    # Construcción de texto formateado con Rich Markup para destacar conceptos
    texto_explicativo = (
        "[bold cyan]¿CÓMO FUNCIONA EL ALGORITMO QUICK SORT?[/bold cyan]\n\n"
        "[bold yellow]1. Selección del Pivote:[/bold yellow] Se elige un elemento base "
        "(en esta implementación, el primer elemento del segmento).\n"
        "[bold yellow]2. Partición Convergente:[/bold yellow] Dos punteros avanzan y retroceden "
        "intercambiando valores hasta segregar menores y mayores.\n"
        "[bold yellow]3. Asentamiento Definitivo:[/bold yellow] El pivote se posiciona en "
        "su índice ordenado final; [italic green]¡su posición queda fija para siempre![/italic green]\n"
        "[bold yellow]4. Divide y Vencerás:[/bold yellow] Se invoca recursivamente el proceso "
        "en las particiones izquierda y derecha.\n"
        "[bold yellow]5. Caso Base Trivial:[/bold yellow] Si una sublista tiene 0 o 1 elementos, "
        "ya está ordenada por definición y la recursión se detiene."
    )

    # Presentación en Panel con esquinas redondeadas y padding armónico
    console.print(
        Panel(
            texto_explicativo,
            title="[bold white on blue] Fundamentos Algorítmicos [/bold white on blue]",
            box=box.ROUNDED,
            border_style="cyan",
            padding=(1, 2),
        )
    )


def construir_arbol(
    nodo: NodoRecursion,
    nivel: int = 0,
) -> Tree:
    """Convierte un NodoRecursion en un árbol jerárquico imprimible con Rich.

    Recorre recursivamente los nodos de la llamada de Quick Sort, identificando
    las hojas (casos base) y las ramas bifurcadas (particiones izquierda y derecha),
    asignando colores temáticos y estilos de guía visual.

    Args:
        nodo: Nodo actual en el árbol de recursión de Quick Sort.
        nivel: Nivel de profundidad en la jerarquía (0 para la raíz).

    Returns:
        Tree: Estructura visual de árbol lista para imprimirse en la terminal.
    """
    # Identificación del Caso Base: sublistas con tamaño <= 1
    if nodo.es_caso_base:
        etiqueta_caso_base = (
            f"[dim]Sublista:[/dim] [white]{nodo.sublista}[/white]\n"
            "  [bold green]CASO BASE[/bold green] "
            "[dim green](0 o 1 elementos → ya está ordenada)[/dim green]"
        )
        return Tree(etiqueta_caso_base, guide_style="bright_green")

    # Resaltado del Pivote y posición final para nodos de partición
    etiqueta_particion = (
        f"[bold]Sublista:[/bold] [yellow]{nodo.sublista}[/yellow]\n"
        f"  [bold gold1]Pivote:[/bold gold1] [bold white on dark_goldenrod] {nodo.pivote} [/] "
        f"[dim]|[/dim] [bold cyan]Índice Final:[/bold cyan] [bold white]{nodo.posicion_pivote}[/bold white]\n"
        f"  [bold green]Resultado tras partición:[/bold green] [white]{nodo.resultado}[/white]"
    )

    arbol = Tree(etiqueta_particion, guide_style="bright_cyan")

    # Recursión y agregación de la rama izquierda (valores <= pivote)
    if nodo.izquierda is not None:
        rama_izquierda = arbol.add(
            "[bold bright_blue]◀ Partición Izquierda[/bold bright_blue] "
            "[dim](elementos ≤ pivote)[/dim]",
            guide_style="bright_blue",
        )
        subarbol_izq = construir_arbol(nodo.izquierda, nivel + 1)
        rama_izquierda.children.append(subarbol_izq)

    # Recursión y agregación de la rama derecha (valores >= pivote)
    if nodo.derecha is not None:
        rama_derecha = arbol.add(
            "[bold bright_magenta]Partición Derecha ▶[/bold bright_magenta] "
            "[dim](elementos ≥ pivote)[/dim]",
            guide_style="bright_magenta",
        )
        subarbol_der = construir_arbol(nodo.derecha, nivel + 1)
        rama_derecha.children.append(subarbol_der)

    return arbol


def mostrar_metricas(sorter: QuickSortVisual) -> None:
    """Muestra una tabla estilizada de Rich con las métricas registradas en la ejecución.

    Args:
        sorter: Instancia de QuickSortVisual tras haber completado el ordenamiento.
    """
    metricas = sorter.metricas
    raiz = sorter.obtener_arbol()
    profundidad = raiz.calcular_profundidad_maxima() if raiz else 0

    # Tabla con cabeceras estilizadas, alineación numérica y caja redondeada
    tabla = Table(
        title="Métricas Operacionales de Ejecución",
        title_style="bold magenta",
        box=box.ROUNDED,
        header_style="bold bright_white on dark_magenta",
        border_style="magenta",
    )

    tabla.add_column("Comparaciones", justify="right", style="cyan")
    tabla.add_column("Intercambios", justify="right", style="yellow")
    tabla.add_column("Iteraciones", justify="right", style="green")
    tabla.add_column("Recursiones", justify="right", style="blue")
    tabla.add_column("Profundidad", justify="right", style="red")
    tabla.add_column("Total Ops", justify="right", style="bold white")

    # Formateo con separador de miles para facilitar la lectura
    tabla.add_row(
        f"{metricas.comparaciones:,}",
        f"{metricas.intercambios:,}",
        f"{metricas.iteraciones:,}",
        f"{metricas.llamadas_recursivas:,}",
        str(profundidad),
        f"{metricas.total_operaciones:,}",
    )

    console.print(tabla)


def demostrar_caso(
    nombre: str,
    lista_original: list[int],
    complejidad_teorica: str = "O(n log n)",
) -> dict[str, Any]:
    """Ejecuta y visualiza un caso individual de demostración en consola.

    Flujo de ejecución:
    1. Despliega un separador temático con Rule de Rich.
    2. Clona la lista y ejecuta el ordenamiento con instrumentación de árbol.
    3. Verifica mediante aserción la exactitud del resultado frente a `sorted()`.
    4. Renderiza el árbol jerárquico de llamadas.
    5. Muestra el panel con la lista original y la lista ordenada.
    6. Muestra la tabla de métricas operacionales.

    Args:
        nombre: Título descriptivo del escenario.
        lista_original: Arreglo inicial de enteros a procesar.
        complejidad_teorica: Notación asintótica teórica del caso.

    Returns:
        dict[str, Any]: Resumen cuantitativo para la comparativa final.
    """
    console.print()
    console.print(Rule(f"[bold cyan]▶ Escenario: {nombre}[/bold cyan]", style="cyan"))

    # Copia superficial para proteger la lista original de mutaciones in-place
    lista_trabajo = lista_original.copy()

    # Ejecución del algoritmo instrumentado para captura de árbol
    sorter = QuickSortVisual()
    sorter.ordenar(
        lista_trabajo,
        0,
        len(lista_trabajo) - 1,
    )

    # Verificación de invariante algorítmica: la lista debe quedar estrictamente ordenada
    assert lista_trabajo == sorted(lista_original), (
        "La lista no coincide con sorted(lista_original)"
    )

    # Despliegue del árbol de recursión
    console.print()
    console.print("[bold yellow]Árbol Jerárquico de Recursión:[/bold yellow]")

    raiz = sorter.obtener_arbol()
    profundidad_maxima = 0
    if raiz is not None:
        profundidad_maxima = raiz.calcular_profundidad_maxima()
        arbol = construir_arbol(raiz)
        console.print(arbol)

    console.print()

    # Panel comparativo de estado inicial vs estado final
    console.print(
        Panel(
            f"[bold cyan]Lista Original (n={len(lista_original)}):[/bold cyan] [dim]{lista_original}[/dim]\n"
            f"[bold green]Lista Ordenada In-Place:[/bold green] [bold white]{lista_trabajo}[/bold white]",
            title="[bold green]Verificación de Ordenamiento[/bold green]",
            box=box.ROUNDED,
            border_style="green",
        )
    )

    console.print()

    # Despliegue de métricas
    mostrar_metricas(sorter)

    return {
        "caso": nombre,
        "n": len(lista_original),
        "comparaciones": sorter.metricas.comparaciones,
        "intercambios": sorter.metricas.intercambios,
        "recursiones": sorter.metricas.llamadas_recursivas,
        "profundidad": profundidad_maxima,
        "complejidad": complejidad_teorica,
    }


def mostrar_resumen_comparativo(resumen_casos: list[dict[str, Any]]) -> None:
    """Despliega una tabla consolidada comparando todos los casos ejecutados.

    Args:
        resumen_casos: Lista de diccionarios con las métricas de cada escenario.
    """
    tabla = Table(
        title="Resumen Comparativo de Escenarios (Mejor vs Promedio vs Peor)",
        title_style="bold yellow",
        box=box.DOUBLE_EDGE,
        header_style="bold white on navy_blue",
        border_style="bright_blue",
    )

    tabla.add_column("Escenario", style="bold cyan")
    tabla.add_column("n", justify="right", style="white")
    tabla.add_column("Comp.", justify="right", style="bright_cyan")
    tabla.add_column("Swaps", justify="right", style="yellow")
    tabla.add_column("Llamadas", justify="right", style="bright_magenta")
    tabla.add_column("Prof.", justify="right", style="red")
    tabla.add_column("Complejidad", justify="center", style="bold green")

    for fila in resumen_casos:
        tabla.add_row(
            str(fila["caso"]),
            str(fila["n"]),
            f"{fila['comparaciones']:,}",
            f"{fila['intercambios']:,}",
            f"{fila['recursiones']:,}",
            str(fila["profundidad"]),
            str(fila["complejidad"]),
        )

    console.print(tabla)


def demostrar_funcionamiento() -> None:
    """Ejecuta la demostración interactiva completa en la terminal."""
    # Limpieza de la terminal para brindar máxima legibilidad y foco visual
    console.clear()

    # Banner superior
    banner = Text()
    banner.append("DEMOSTRACIÓN VISUAL Y DIDÁCTICA: QUICK SORT\n", style="bold yellow")
    banner.append(
        "Inspección gráfica del árbol de partición y análisis de complejidad",
        style="italic cyan",
    )
    console.print(
        Panel(banner, box=box.DOUBLE, border_style="bright_blue", padding=(1, 2))
    )
    console.print()

    # 1. Panel de explicación teórica
    mostrar_explicacion()

    # 2. Catálogo de escenarios didácticos para comparar los extremos asintóticos
    casos_demo: list[tuple[str, list[int], str]] = [
        (
            "Caso Favorable / Mejor Caso (Balanceado)",
            [15, 8, 3, 12, 25, 20, 30],
            "O(n log n)",
        ),
        (
            "Caso Promedio (Distribución Desordenada)",
            [34, 7, 23, 32, 5, 62, 12, 18],
            "O(n log n)",
        ),
        (
            "Peor Caso (Lista Ya Ordenada - Degenerada)",
            [3, 8, 12, 15, 20, 25, 30],
            "O(n²)",
        ),
    ]

    resumen_filas: list[dict[str, Any]] = []
    for nombre, lista, complejidad in casos_demo:
        fila = demostrar_caso(nombre, lista, complejidad)
        resumen_filas.append(fila)

    # 3. Gran tabla comparativa final
    console.print()
    console.print(Rule("[bold gold1]BALANCE COMPARATIVO[/bold gold1]", style="gold1"))
    console.print()
    mostrar_resumen_comparativo(resumen_filas)

    # 4. Panel didáctico de conclusiones clave
    console.print()
    console.print(
        Panel(
            "[bold]Puntos Clave para Recordar:[/bold]\n\n"
            "• [bold cyan]Invariante del Pivote:[/bold cyan] Cada partición sitúa al pivote "
            "en su posición final definitiva e inmutable.\n"
            "• [bold green]Partición Equilibrada (Mejor Caso):[/bold green] El pivote divide "
            "la lista en mitades similares, produciendo un árbol de altura log₂ n y costo O(n log n).\n"
            "• [bold red]Partición Degenerada (Peor Caso):[/bold red] Con una lista ya ordenada, "
            "el pivote extremo genera particiones de tamaño 0 y n - 1, colapsando el árbol a profundidad n y costo O(n²).",
            title="[bold yellow]¿Qué debemos recordar?[/bold yellow]",
            box=box.ROUNDED,
            border_style="gold1",
            padding=(1, 2),
        )
    )
    console.print()


if __name__ == "__main__":
    demostrar_funcionamiento()
