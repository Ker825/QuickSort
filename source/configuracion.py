from dataclasses import dataclass


@dataclass(frozen=True)
class ConfiguracionExperimento:
    tamanos: tuple[int, ...] = (100, 200, 500, 1000, 2000)
    repeticiones: int = 30
