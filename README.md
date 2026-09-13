# Quick Sort — Análisis y visualización

Implementación y experimentación del algoritmo **Quick Sort**, orientada al análisis de su comportamiento mediante diferentes tamaños de entrada y la visualización de los resultados obtenidos.

El proyecto incluye la implementación del algoritmo, generación de datos para los experimentos, recopilación de métricas y generación de gráficas.

## 📁 Estructura del proyecto

```text
Quick_Sort/
├── documents/                  # Documentación teórica y material de apoyo
├── presentation/               # Diapositivas y recursos de exposición
├── output/
│   ├── anything/               # Salidas auxiliares
│   └── resultados/
│       ├── cvs/                # Métricas exportadas (.csv)
│       │   └── .gitkeep
│       └── graficas/           # Visualizaciones generadas (.png)
│           └── .gitkeep
├── source/
│   ├── algoritmo/              # Lógica de Quick Sort y métricas
│   ├── experimento/            # Generación de datos y ejecución de experimentos
│   └── graphics/               # Generación de visualizaciones
├── main.py                     # Punto de entrada del programa
├── pyproject.toml              # Configuración y dependencias del proyecto
├── uv.lock                     # Bloqueo determinista de dependencias
└── README.md                   # Documentación del proyecto
```

## ⚙️ Requisitos

* **Python:** 3.12 o superior
* **Gestor de paquetes:** [uv](https://docs.astral.sh/uv/)
* **Dependencias principales:**

  * Matplotlib
  * Pandas

## 🚀 Instalación

### Clonar el repositorio

```bash
git clone https://github.com/Ker825/QuickSort.git
cd QuickSort
```

### Instalación con uv

Se recomienda utilizar `uv`, ya que el proyecto incluye `pyproject.toml` y `uv.lock`.

```bash
uv sync
```

Esto crea el entorno virtual e instala las dependencias definidas por el proyecto.

### Instalación con pip

Como alternativa, se puede utilizar un entorno virtual convencional:

```bash
python3 -m venv .venv
```

#### Linux / macOS

```bash
source .venv/bin/activate
```

#### Windows

```powershell
.venv\Scripts\activate
```

Después, instalar las dependencias:

```bash
pip install matplotlib pandas
```

## ▶️ Ejecución

### Con uv

```bash
uv run main.py
```

### Con Python

Si el entorno virtual está activado:

```bash
python main.py
```

## 📊 Salidas generadas

Al finalizar la ejecución, los resultados se almacenan automáticamente en sus respectivas rutas dentro de `output/resultados/`.

### Tablas de datos

Los datos experimentales se almacenan en formato `.csv` dentro de:

```text
output/resultados/cvs/
```

Se generan los siguientes archivos:

* **`tiempos.csv`**: medición del tiempo de ejecución para cada tamaño de muestra ($N$).
* **`operaciones.csv`**: recuento total de comparaciones e intercambios realizados durante la ejecución del algoritmo.

### Gráficas de rendimiento

Las visualizaciones se almacenan en formato `.png` dentro de:

```text
output/resultados/graficas/
```

Se generan las siguientes gráficas:

* **`grafica_1_tiempo_vs_tamano.png`**: comportamiento del tiempo de ejecución frente al tamaño del arreglo.
* **`grafica_2_n_vs_operaciones.png`**: número de operaciones elementales realizadas en función del tamaño de entrada $N$.
* **`grafica_3_experimental_vs_teorico.png`**: comparación entre el comportamiento experimental del algoritmo y la curva teórica correspondiente a $O(n \log n)$.

En conjunto, estas salidas permiten analizar experimentalmente el comportamiento de **Quick Sort** y contrastarlo con su complejidad temporal teórica.

## 🧩 Organización del código

El código fuente se divide en módulos según su responsabilidad:

### `source/algoritmo/`

Contiene la lógica relacionada con **Quick Sort**, incluyendo las operaciones necesarias para el algoritmo y el registro de métricas.

### `source/experimento/`

Se encarga de preparar y ejecutar los experimentos, incluyendo la generación de datos y la coordinación de las pruebas.

### `source/graphics/`

Contiene la lógica relacionada con la lectura de resultados y la generación de las gráficas.

Esta separación busca mantener una estructura modular y facilitar el mantenimiento del proyecto.

## 📄 Documentación

La documentación teórica y el material utilizado durante el desarrollo se encuentran en:

```text
documents/
```

Los recursos destinados a la exposición del proyecto se encuentran en:

```text
presentation/
```

## 📝 Licencia

Este proyecto se encuentra disponible para fines académicos y educativos.
