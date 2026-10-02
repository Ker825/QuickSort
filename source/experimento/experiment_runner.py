import sys
import time
from collections.abc import Callable

from source.algoritmo.quick_sort import QuickSort

from .models.registro_operacion import RegistroOperacion
from .models.registro_tiempo import RegistroTiempo

# CPython tiene un limite por defecto de 1000 frames en el call stack.
# En el peor caso (pivote desbalanceado), Quick Sort degrada a recursividad O(n),
# por lo que entradas n >= 1000 generarian RecursionError sin este ajuste.
sys.setrecursionlimit(50_000)

# Alias de tipo para desacoplar UI/logs del orquestador:
# Firma: (nombre_caso, n, repeticion_actual, total_repeticiones) -> None
ProgresoCallback = Callable[[str, int, int, int], None]


class ExperimentRunner:
    """Orquestador de pruebas de rendimiento y recoleccion de metricas empiricas.

    Aplica el Principio de Responsabilidad Unica (SRP): coordina la ejecucion
    de benchmarks sobre el algoritmo, aislando la medicion temporal y el conteo
    de operaciones elementales sin acoplarse al almacenamiento (CSV) ni a la
    presentacion grafica.

    Attributes:
        sorter (QuickSort): Instancia del algoritmo que implementa la logica
            de ordenamiento y el rastreo interno de metricas.
        registros_tiempos (list[RegistroTiempo]): Historico estructurado de
            tiempos medidos por corrida.
        registros_operaciones (list[RegistroOperacion]): Historico estructurado
            de operaciones computacionales registradas por corrida.
    """

    def __init__(self, sorter: QuickSort) -> None:
        """Inicializa el corredor inyectando la estrategia de ordenamiento.

        Args:
            sorter (QuickSort): Instancia del algoritmo a evaluar.
        """
        self.sorter = sorter
        self.registros_tiempos: list[RegistroTiempo] = []
        self.registros_operaciones: list[RegistroOperacion] = []

    def ejecutar_caso(
        self,
        nombre_caso: str,
        generador_fn: Callable[[int], list[int]],
        tamanos: list[int],
        repeticiones: int = 10,
        al_iterar: ProgresoCallback | None = None,
    ) -> None:
        """Ejecuta una bateria de pruebas para un escenario especifico sobre multiples tamanos.

        Para cada tamano `n` y cada repeticion:
        1. Genera un arreglo base y extrae una copia para preservar la entrada original.
        2. Limpia los contadores internos del algoritmo para garantizar idempotencia.
        3. Mide con precision nanometrica exclusivamente la ejecucion del ordenamiento.
        4. Notifica el avance via callback y persiste los resultados como modelos inmutables.

        Args:
            nombre_caso (str): Etiqueta descriptiva del escenario (e.g. 'Mejor Caso', 'Peor Caso').
            generador_fn (Callable[[int], list[int]]): Fabrica que genera la lista de prueba de tamano n.
            tamanos (list[int]): Lista de longitudes n a evaluar secuencialmente.
            repeticiones (int, optional): Veces que se repite la medicion por tamano para mitigar ruido termico/OS. Defaults to 10.
            al_iterar (ProgresoCallback | None, optional): Callback opcional invocado tras cada corrida. Defaults to None.
        """  # noqa: E501
        for n in tamanos:
            for rep in range(1, repeticiones + 1):
                # Generacion previa al temporizador: aisla el tiempo de CPU consumido por # noqa: E501
                # el generador pseudoaleatorio o la asignacion de memoria inicial.
                datos_base = generador_fn(n)
                # Clonacion superficial requerida: Quick Sort ordena in-place y muta el arreglo. # noqa: E501
                datos_prueba = datos_base.copy()

                # Resetea contadores para evitar acumulacion entre ejecuciones consecutivas. # noqa: E501
                self.sorter.reiniciar_metricas()

                # perf_counter utiliza un reloj monotonico de hardware insensible a ajustes NTP. # noqa: E501
                # Se enmarca estrictamente la llamada de ordenamiento para evitar ruido de fondo. # noqa: E501
                inicio = time.perf_counter()
                self.sorter.ordenar(datos_prueba, 0, len(datos_prueba) - 1)
                fin = time.perf_counter()

                duracion = fin - inicio

                # Delegacion de telemetria sin acoplar librerias de terminal (tqdm, logging, print). # noqa: E501
                if al_iterar:
                    al_iterar(nombre_caso, n, rep, repeticiones)

                # Persistencia en memoria usando Value Objects/DTOs tipados
                self.registros_tiempos.append(
                    RegistroTiempo(
                        tamano=n,
                        caso=nombre_caso,
                        repeticion=rep,
                        tiempo_segundos=duracion,
                    )
                )

                self.registros_operaciones.append(
                    RegistroOperacion(
                        tamano=n,
                        caso=nombre_caso,
                        repeticion=rep,
                        comparaciones=self.sorter.metricas.comparaciones,
                        intercambios=self.sorter.metricas.intercambios,
                        iteraciones=self.sorter.metricas.iteraciones,
                        llamadas_recursivas=self.sorter.metricas.llamadas_recursivas,
                    )
                )
