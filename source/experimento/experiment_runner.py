import sys
import time
from collections.abc import Callable

from source.algoritmo.quick_sort import QuickSort

from .models.registro_operacion import RegistroOperacion
from .models.registro_tiempo import RegistroTiempo

# Prevenir RecursionError en el peor caso para n >= 1000
sys.setrecursionlimit(50_000)


class ExperimentRunner:
    """Orquestador de pruebas de rendimiento y recolección de métricas."""

    def __init__(self, sorter: QuickSort) -> None:
        self.sorter = sorter

        self.registros_tiempos: list[RegistroTiempo] = []
        self.registros_operaciones: list[RegistroOperacion] = []

    def ejecutar_caso(
        self,
        nombre_caso: str,
        generador_fn: Callable[[int], list[int]],
        tamanos: list[int],
        repeticiones: int = 10,
    ) -> None:
        """
        Ejecuta la suite para un caso específico a través de distintos tamaños n.
        """
        for n in tamanos:
            for rep in range(1, repeticiones + 1):
                # 1. Generar y clonar datos fuera del temporizador
                datos_base = generador_fn(n)
                datos_prueba = datos_base.copy()

                # 2. Reiniciar métricas antes de ejecutar
                self.sorter.reiniciar_metricas()

                # 3. Medir estrictamente la llamada del algoritmo
                inicio = time.perf_counter()
                self.sorter.ordenar(datos_prueba, 0, len(datos_prueba) - 1)
                fin = time.perf_counter()

                duracion = fin - inicio

                print(
                    f"Ejecutando {nombre_caso} para n={n} (repetición {rep}/{repeticiones})..."
                )

                # 4. Almacenar resultados
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
