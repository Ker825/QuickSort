from dataclasses import dataclass


@dataclass(frozen=True)
class ConfiguracionExperimento:
    """Clase que representa la configuración del experimento de Quick Sort."""

    # tamaños de entrada a probar [listas de enteros]
    tamanos: tuple[int, ...] = (100, 200, 500, 1000, 2000)

    # cantidad de repeticiones por tamaño y caso
    repeticiones: int = 10
