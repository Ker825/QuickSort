"""Controlador de la interfaz de consola interactiva para la demostración visual con Rich.

Aplica el Principio de Responsabilidad Única (SRP): orquesta la ejecución didáctica
de los casos representativos de Quick Sort, delegando la presentación visual en
`RichVisualFormatter`.
"""

from typing import Any

from rich.console import Console
from rich.rule import Rule

from quick_sort.application.services.quick_sort_visual import QuickSortVisual
from quick_sort.presentation.formatters.rich_formatter import RichVisualFormatter

# Instancia central de consola para la salida estándar
console = Console()

# Catálogo de casos didácticos diseñados para contrastar los comportamientos asintóticos
CASOS_DEMOSTRACION: list[dict[str, Any]] = [
    {
        "nombre": "Caso Favorable / Mejor Caso (Balanceado)",
        "datos": [15, 8, 3, 12, 25, 20, 30],
        "complejidad": "O(n log n)",
        "color": "green",
    },
    {
        "nombre": "Caso Promedio (Distribución Aleatoria)",
        "datos": [34, 7, 23, 32, 5, 62, 12, 18],
        "complejidad": "O(n log n)",
        "color": "cyan",
    },
    {
        "nombre": "Peor Caso (Lista Ya Ordenada - Degenerada)",
        "datos": [3, 8, 12, 15, 20, 25, 30],
        "complejidad": "O(n²)",
        "color": "red",
    },
]


def demostrar_caso(
    nombre: str,
    lista_original: list[int],
    complejidad_teorica: str,
    consola: Console,
) -> dict[str, Any]:
    """Ejecuta un caso individual de demostración, renderizando su árbol y métricas.

    Args:
        nombre: Título del escenario a demostrar.
        lista_original: Arreglo inicial de enteros sin modificar.
        complejidad_teorica: Notación asintótica correspondiente.
        consola: Instancia de Console para renderizar la salida de Rich.

    Returns:
        dict[str, Any]: Métricas acumuladas del caso para el resumen global.
    """
    consola.print()
    consola.print(Rule(f"[bold cyan]▶ Escenario: {nombre}[/bold cyan]", style="cyan"))

    # [LÍNEA CLAVE] Clonación para preservar la lista original intacta ante mutaciones in-place
    lista_trabajo = lista_original.copy()

    # [LÍNEA CLAVE] Instanciación del ordenador instrumentado con árbol de llamadas
    sorter = QuickSortVisual()
    sorter.ordenar(lista_trabajo, 0, len(lista_trabajo) - 1)

    # Verificación estricta de invariante de ordenamiento
    assert lista_trabajo == sorted(lista_original), (
        "Error: el resultado no coincide con sorted()"
    )

    # [LÍNEA CLAVE] Construcción y renderizado del árbol jerárquico de recursión
    consola.print()
    consola.print("[bold yellow]Jerarquía del Árbol de Recursión:[/bold yellow]")

    raiz = sorter.obtener_arbol()
    profundidad_maxima = 0
    if raiz is not None:
        profundidad_maxima = raiz.calcular_profundidad_maxima()
        arbol_rich = RichVisualFormatter.construir_arbol_recursion(raiz)
        consola.print(arbol_rich)

    consola.print()

    # Renderizado del panel de verificación con entrada vs salida
    panel_resultado = RichVisualFormatter.crear_panel_resultado(
        nombre, lista_original, lista_trabajo
    )
    consola.print(panel_resultado)

    consola.print()

    # Renderizado de la tabla de métricas operacionales detalladas
    tabla_metricas = RichVisualFormatter.crear_tabla_metricas(
        sorter.metricas, profundidad_maxima
    )
    consola.print(tabla_metricas)

    # Retorna un resumen para la tabla comparativa final
    return {
        "caso": nombre,
        "n": len(lista_original),
        "comparaciones": sorter.metricas.comparaciones,
        "intercambios": sorter.metricas.intercambios,
        "llamadas": sorter.metricas.llamadas_recursivas,
        "profundidad": profundidad_maxima,
        "complejidad": complejidad_teorica,
    }


def ejecutar_demostracion(consola: Console | None = None) -> None:
    """Orquesta el flujo integral de la demostración visual con Rich en terminal.

    Pasos ejecutados:
    1. Limpieza de pantalla y despliegue del banner principal.
    2. Panel explicativo con la teoría fundamental de Quick Sort.
    3. Batería de escenarios didácticos (Mejor Caso, Caso Promedio, Peor Caso).
    4. Gran tabla comparativa resumen con análisis asintótico cruzado.
    5. Panel de síntesis con las conclusiones esenciales.

    Args:
        consola: Instancia opcional de Console de Rich (usa la global si es None).
    """
    c = consola or console

    # [LÍNEA CLAVE] Limpieza de terminal para una presentación inmersiva
    c.clear()

    # 1. Despliegue de banners explicativos
    c.print(RichVisualFormatter.crear_banner_principal())
    c.print()
    c.print(RichVisualFormatter.crear_panel_explicacion())

    # 2. Iteración y ejecución de cada escenario de prueba
    resumen_filas: list[dict[str, Any]] = []
    for caso_cfg in CASOS_DEMOSTRACION:
        metricas_caso = demostrar_caso(
            nombre=caso_cfg["nombre"],
            lista_original=caso_cfg["datos"],
            complejidad_teorica=caso_cfg["complejidad"],
            consola=c,
        )
        resumen_filas.append(metricas_caso)

    # 3. Despliegue de la tabla comparativa resumen
    c.print()
    c.print(Rule("[bold gold1]RESUMEN COMPARATIVO FINAL[/bold gold1]", style="gold1"))
    c.print()
    c.print(RichVisualFormatter.crear_tabla_comparativa_resumen(resumen_filas))

    # 4. Despliegue de conclusiones teóricas
    c.print()
    c.print(RichVisualFormatter.crear_panel_conclusiones())
    c.print()
