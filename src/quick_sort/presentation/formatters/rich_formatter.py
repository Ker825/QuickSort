"""Formateadores y componentes visuales basados en Rich para la presentación en terminal.

Aplica el Principio de Responsabilidad Única (SRP): aísla la construcción de paneles,
árboles, tablas y estilos visuales de la lógica de ordenamiento y control de flujo.
"""

from typing import Any

from rich import box
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from quick_sort.domain.models.metricas import MetricasQuickSort
from quick_sort.domain.models.nodo_recursion import NodoRecursion


class RichVisualFormatter:
    """Fábrica de componentes visuales avanzados para la consola con Rich."""

    @staticmethod
    def crear_banner_principal() -> Panel:
        """Construye un banner de bienvenida estilizado con bordes redondeados."""
        texto = Text()
        texto.append(
            "DEMOSTRACIÓN DIDÁCTICA Y VISUAL: QUICK SORT\n", style="bold yellow"
        )
        texto.append(
            "Análisis estructural del algoritmo de ordenamiento Divide & Conquista",
            style="italic cyan",
        )
        return Panel(
            texto,
            box=box.DOUBLE,
            border_style="bright_blue",
            padding=(1, 2),
        )

    @staticmethod
    def crear_panel_explicacion() -> Panel:
        """Crea el panel conceptual con los 5 pasos fundamentales del algoritmo."""
        cuerpo = (
            "[bold cyan]¿CÓMO OPERA EL ALGORITMO QUICK SORT?[/bold cyan]\n\n"
            "  [bold yellow]1. Selección de Pivote:[/bold yellow] Se escoge un elemento "
            "(en esta implementación, el primero de la sublista: [code]lista[inicio][/code]).\n"
            "  [bold yellow]2. Partición Bifurcada:[/bold yellow] Dos punteros convergen "
            "intercambiando valores hasta ubicar los menores a la izquierda y mayores a la derecha.\n"
            "  [bold yellow]3. Posicionamiento Final:[/bold yellow] El pivote se asienta "
            "en su índice ordenado definitivo; [italic green]¡nunca vuelve a moverse![/italic green]\n"
            "  [bold yellow]4. Subdivisión Recursiva:[/bold yellow] Se repite el proceso "
            "de forma independiente sobre las particiones izquierda y derecha.\n"
            "  [bold yellow]5. Caso Base Inmediato:[/bold yellow] Si la sublista tiene "
            "0 o 1 elementos, por definición ya está ordenada y no requiere trabajo."
        )
        return Panel(
            cuerpo,
            title="[bold white on blue] Fundamentos Algorítmicos [/bold white on blue]",
            box=box.ROUNDED,
            border_style="cyan",
            padding=(1, 2),
        )

    @staticmethod
    def construir_arbol_recursion(nodo: NodoRecursion) -> Tree:
        """Transforma recursivamente la jerarquía de llamadas en un árbol estilizado de Rich.

        Args:
            nodo: Nodo raíz o subárbol de llamadas a representar.

        Returns:
            Tree: Componente imprimible de Rich con colores contextuales e iconografía.
        """
        # Renderizado diferenciado para Caso Base (hojas del árbol)
        if nodo.es_caso_base:
            etiqueta_hoja = (
                f"[dim]Sublista:[/dim] [white]{nodo.sublista}[/white]\n"
                "  [bold green]CASO BASE[/bold green] "
                "[dim green](0 o 1 elementos → trivialmente ordenada)[/dim green]"
            )
            return Tree(etiqueta_hoja, guide_style="bright_green")

        # Resaltado del pivote y metadatos de partición para nodos activos
        etiqueta_nodo = (
            f"[bold]Sublista:[/bold] [yellow]{nodo.sublista}[/yellow]\n"
            f"  [bold gold1]Pivote:[/bold gold1] [bold white on dark_goldenrod] {nodo.pivote} [/] "
            f"[dim]|[/dim] [bold cyan]Índice Final:[/bold cyan] [bold white]{nodo.posicion_pivote}[/bold white]\n"
            f"  [bold green]Estado tras partición:[/bold green] [white]{nodo.resultado}[/white]"
        )

        arbol = Tree(etiqueta_nodo, guide_style="bright_cyan")

        # Rama izquierda: partición de elementos menores o iguales al pivote
        if nodo.izquierda is not None:
            rama_izq = arbol.add(
                "[bold bright_blue]◀ Partición Izquierda[/bold bright_blue] "
                "[dim](elementos ≤ pivote)[/dim]",
                guide_style="bright_blue",
            )
            subarbol_izq = RichVisualFormatter.construir_arbol_recursion(nodo.izquierda)
            rama_izq.children.append(subarbol_izq)

        # Rama derecha: partición de elementos mayores o iguales al pivote
        if nodo.derecha is not None:
            rama_der = arbol.add(
                "[bold bright_magenta]Partición Derecha ▶[/bold bright_magenta] "
                "[dim](elementos ≥ pivote)[/dim]",
                guide_style="bright_magenta",
            )
            subarbol_der = RichVisualFormatter.construir_arbol_recursion(nodo.derecha)
            rama_der.children.append(subarbol_der)

        return arbol

    @staticmethod
    def crear_tabla_metricas(
        metricas: MetricasQuickSort,
        profundidad_maxima: int,
    ) -> Table:
        """Genera una tabla elegante con las métricas operacionales de una corrida.

        Args:
            metricas: Métricas contadas durante el ordenamiento.
            profundidad_maxima: Profundidad máxima alcanzada en el árbol de llamadas.

        Returns:
            Table: Tabla de Rich formateada con estilos y cabeceras.
        """
        tabla = Table(
            title="Métricas Operacionales de la Ejecución",
            title_style="bold magenta",
            box=box.ROUNDED,
            header_style="bold bright_white on dark_magenta",
            border_style="magenta",
        )

        tabla.add_column("Comparaciones", justify="right", style="cyan")
        tabla.add_column("Intercambios", justify="right", style="yellow")
        tabla.add_column("Iteraciones", justify="right", style="green")
        tabla.add_column("Llamadas Recursivas", justify="right", style="blue")
        tabla.add_column("Profundidad", justify="right", style="red")
        tabla.add_column("Total Ops", justify="right", style="bold white")

        tabla.add_row(
            f"{metricas.comparaciones:,}",
            f"{metricas.intercambios:,}",
            f"{metricas.iteraciones:,}",
            f"{metricas.llamadas_recursivas:,}",
            str(profundidad_maxima),
            f"{metricas.total_operaciones:,}",
        )
        return tabla

    @staticmethod
    def crear_panel_resultado(
        nombre_caso: str,
        original: list[int],
        ordenada: list[int],
    ) -> Panel:
        """Crea el panel de verificación con la lista inicial y su versión ordenada."""
        contenido = (
            f"[bold cyan]Lista Original (n={len(original)}):[/bold cyan] [dim]{original}[/dim]\n"
            f"[bold green]Lista Ordenada In-Place:[/bold green] [bold white]{ordenada}[/bold white]"
        )
        return Panel(
            contenido,
            title=f"[bold green]Verificación: {nombre_caso}[/bold green]",
            box=box.ROUNDED,
            border_style="green",
        )

    @staticmethod
    def crear_tabla_comparativa_resumen(filas: list[dict[str, Any]]) -> Table:
        """Construye la gran tabla comparativa consolidando todos los escenarios evaluados.

        Args:
            filas: Lista de diccionarios con las métricas acumuladas de cada caso.

        Returns:
            Table: Tabla comparativa de resumen con colores distintivos por columna.
        """
        tabla = Table(
            title="Comparativa Global de Escenarios (Mejor vs Promedio vs Peor)",
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

        for f in filas:
            tabla.add_row(
                str(f["caso"]),
                str(f["n"]),
                str(f["comparaciones"]),
                str(f["intercambios"]),
                str(f["llamadas"]),
                str(f["profundidad"]),
                str(f["complejidad"]),
            )

        return tabla

    @staticmethod
    def crear_panel_conclusiones() -> Panel:
        """Crea el panel de conclusiones teóricas y claves de aprendizaje."""
        conclusiones = (
            "[bold green]CLAVES ASINTÓTICAS DE QUICK SORT:[/bold green]\n\n"
            "• [bold cyan]Mejor Caso O(n log n):[/bold cyan] Se logra cuando el pivote "
            "divide la lista en particiones aproximadamente iguales (árbol balanceado de altura log₂ n).\n"
            "• [bold yellow]Caso Promedio O(n log n):[/bold yellow] En datos aleatorios, "
            "incluso particiones 90-10 mantienen la complejidad asintótica logarítmica-lineal.\n"
            "• [bold red]Peor Caso O(n²):[/bold red] Ocurre cuando el pivote elegido es "
            "sistemáticamente el elemento mínimo o máximo (lista ya ordenada), degenerando en O(n) niveles recursivos."
        )
        return Panel(
            conclusiones,
            title="[bold yellow] Síntesis Didáctica [/bold yellow]",
            box=box.ROUNDED,
            border_style="gold1",
            padding=(1, 2),
        )
