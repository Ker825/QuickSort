from source.algoritmo.quick_sort import QuickSort


def demostrar_funcionamiento() -> None:
    print("=" * 60)
    print("DEMOSTRACION VISUAL: QUICK SORT")
    print("=" * 60)

    casos_demo = {
        "Caso Promedio (Desordenado)": [34, 7, 23, 32, 5, 62, 12, 18],
        "Peor Caso (Ya Ordenado)": [3, 8, 12, 15, 20, 25, 30],
        "Mejor Caso (Pivote Mediana)": [15, 8, 3, 12, 25, 20, 30],
    }

    sorter = QuickSort()

    for nombre, lista_original in casos_demo.items():
        lista_trabajo = lista_original.copy()
        sorter.reiniciar_metricas()  # Reiniciar métricas antes de cada iteración

        print(f"\n--- {nombre} ---")
        print(f"Original: {lista_trabajo}")

        sorter.ordenar(lista_trabajo, 0, len(lista_trabajo) - 1)

        print(f"Ordenada: {lista_trabajo}")
        assert lista_trabajo == sorted(lista_original), "Error de ordenamiento"

        # Expone el registro de operaciones de la iteración actual
        m = sorter.metricas
        print(
            f"Metricas: Comparaciones={m.comparaciones} | "
            f"Intercambios={m.intercambios} | "
            f"Llamadas recursivas={m.llamadas_recursivas} | "
        )

    print("\n" + "=" * 60)


demostrar_funcionamiento()
