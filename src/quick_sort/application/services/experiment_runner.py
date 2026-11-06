"""Orquestador de pruebas de rendimiento y recolección de métricas empíricas.

Aplica el Principio de Responsabilidad Única (SRP) y de Inversión de Dependencias (DIP):
coordina benchmarks sobre cualquier implementación que cumpla `SorterProtocol`, aislando
la medición temporal con `time.perf_counter` del almacenamiento y la presentación.
"""

import sys
import time
from collections.abc import Sequence

from quick_sort.domain.models.registro_operacion import RegistroOperacion
from quick_sort.domain.models.registro_tiempo import RegistroTiempo
from quick_sort.domain.protocols import (
    GeneradorDatosFn,
    ProgresoCallback,
    SorterProtocol,
)

__all__ = ["ExperimentRunner", "ProgresoCallback"]

# [LÍNEA CLAVE] CPython limita el call stack a 1000 frames por defecto.
# En el peor caso de Quick Sort, la recursión degenera a profundidad O(n).
# Para soportar n = 10_000 en el peor caso sin desbordar el stack, elevamos el límite a 50_000.
sys.setrecursionlimit(50_000)


class ExperimentRunner:
    """Ejecutor de benchmarks comparativos sobre algoritmos de ordenamiento.

    Attributes:
        sorter (SorterProtocol): Instancia del algoritmo inyectada (DIP).
        registros_tiempos (list[RegistroTiempo]): Mediciones cronometradas por corrida.
        registros_operaciones (list[RegistroOperacion]): Operaciones contadas por corrida.
    """

    def __init__(self, sorter: SorterProtocol) -> None:
        """Inicializa el runner inyectando la estrategia de ordenamiento.

        Args:
            sorter (SorterProtocol): Implementación del algoritmo a evaluar.
        """
        # [LÍNEA CLAVE] Inyección de dependencias (DIP): depende del protocolo, no de la clase concreta
        self.sorter = sorter
        self.registros_tiempos: list[RegistroTiempo] = []
        self.registros_operaciones: list[RegistroOperacion] = []

    def limpiar_resultados(self) -> None:
        """Elimina los registros almacenados en memoria."""
        self.registros_tiempos.clear()
        self.registros_operaciones.clear()

    def ejecutar_caso(
        self,
        nombre_caso: str,
        generador_fn: GeneradorDatosFn,
        tamanos: Sequence[int],
        repeticiones: int = 10,
        al_iterar: ProgresoCallback | None = None,
    ) -> None:
        """Ejecuta una batería de benchmarks para un escenario sobre múltiples tamaños.

        Flujo metodológico por cada repetición de tamaño n:
        1. Genera los datos sintéticos de prueba con `generador_fn(n)`.
        2. Clona la lista para aislar la mutación in-place del generador.
        3. Reinicia los contadores operacionales del sorter.
        4. Mide estrictamente el intervalo de ordenamiento con `time.perf_counter()`.
        5. Emite telemetría mediante el callback desacoplado `al_iterar`.
        6. Persiste los resultados como Value Objects inmutables en memoria.

        Args:
            nombre_caso: Etiqueta descriptiva del escenario (ej. 'Mejor Caso', 'Peor Caso').
            generador_fn: Función fábrica generadora del arreglo de prueba.
            tamanos: Colección de longitudes de entrada a evaluar secuencialmente.
            repeticiones: Iteraciones por tamaño para promediar variabilidad ambiental.
            al_iterar: Callback opcional de telemetría hacia la interfaz de usuario.
        """
        for n in tamanos:
            for rep in range(1, repeticiones + 1):
                # [LÍNEA CLAVE] Generación externa al cronómetro: excluye el tiempo de CPU del generador
                datos_base = generador_fn(n)

                # [LÍNEA CLAVE] Copia superficial: Quick Sort muta el arreglo in-place
                datos_prueba = datos_base.copy()

                # [LÍNEA CLAVE] Reseteo de métricas para garantizar idempotencia entre corridas
                self.sorter.reiniciar_metricas()

                # [LÍNEA CLAVE] perf_counter: reloj monotónico de hardware inmune a ajustes de reloj del sistema
                inicio = time.perf_counter()
                self.sorter.ordenar(datos_prueba, 0, len(datos_prueba) - 1)
                fin = time.perf_counter()

                duracion = fin - inicio

                # [LÍNEA CLAVE] Telemetría desacoplada: notifica avance a la UI sin depender de Rich/print
                if al_iterar is not None:
                    al_iterar(nombre_caso, n, rep, repeticiones)

                # Persistencia en memoria estructurada
                self.registros_tiempos.append(
                    RegistroTiempo(
                        tamano=n,
                        caso=nombre_caso,
                        repeticion=rep,
                        tiempo_segundos=duracion,
                    )
                )

                metricas_actuales = self.sorter.metricas
                self.registros_operaciones.append(
                    RegistroOperacion(
                        tamano=n,
                        caso=nombre_caso,
                        repeticion=rep,
                        comparaciones=metricas_actuales.comparaciones,
                        intercambios=metricas_actuales.intercambios,
                        iteraciones=metricas_actuales.iteraciones,
                        llamadas_recursivas=metricas_actuales.llamadas_recursivas,
                    )
                )
