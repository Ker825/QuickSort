from pathlib import Path

from source.algoritmo.quick_sort import QuickSort
from source.experimento.cvs_writer import CsvWriter
from source.experimento.data_generator import DataGenerator
from source.experimento.experiment_runner import ExperimentRunner
from source.graphics.graficador import Graficador
from source.graphics.visualizador_csv import CargadorResultados


def main():
    ruta_tiempos = Path("output/resultados/cvs/tiempos.csv")
    ruta_operaciones = Path("output/resultados/cvs/operaciones.csv")
    directorio_graficas = Path("output/resultados/graficas")
    directorio_graficas.mkdir(parents=True, exist_ok=True)

    tamanos = [100, 200, 500, 1000, 2000]
    repeticiones = 30

    instrumentador = QuickSort()
    runner = ExperimentRunner(sorter=instrumentador)

    # 1. Caso Favorable (Mejor Caso)
    runner.ejecutar_caso(
        "Mejor Caso", DataGenerator.generar_mejor_caso, tamanos, repeticiones
    )

    # 2. Caso Promedio (Aleatorio)
    runner.ejecutar_caso(
        "Promedio", DataGenerator.generar_caso_promedio, tamanos, repeticiones
    )

    # 3. Peor Caso (Ordenado)
    runner.ejecutar_caso(
        "Peor Caso", DataGenerator.generar_peor_caso, tamanos, repeticiones
    )

    # 4. Guardar archivos finales
    cvs_writter = CsvWriter()
    cvs_writter.guardar_csv(runner)

    cargador = CargadorResultados(ruta_tiempos, ruta_operaciones)
    df_tiempos = cargador.cargar_tiempos_agrupados(usar_mediana=False)
    df_operaciones = cargador.cargar_operaciones_agrupadas(usar_mediana=False)

    print("Datos agrupados listos para graficar:")
    print(df_tiempos)

    # 2. Generar y guardar la figura
    graficador = Graficador()
    ruta_salida = directorio_graficas / "grafica_1_tiempo_vs_tamano.png"
    ruta_salida2 = directorio_graficas / "grafica_2_n_vs_operaciones.png"
    ruta_salida3 = directorio_graficas / "grafica_3_experimental_vs_teorico.png"

    graficador.graficar_tiempo_vs_tamano(df_tiempos, ruta_salida)

    graficador.graficar_n_vs_operaciones(df_operaciones, ruta_salida2)

    graficador.graficar_exp_vs_teoria(df_tiempos, ruta_salida3)

    print(
        f"Gráfica generada exitosamente en: \n| {ruta_salida} | \n| {ruta_salida2} | \n| {ruta_salida2} |"  # noqa: E501
    )


if __name__ == "__main__":
    main()
