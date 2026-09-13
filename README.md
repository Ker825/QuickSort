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
── source/
│   ├── algoritmo/              # Lógica de Quick Sort y métricas
  ├── experimento/            # Generación de datos y ejecución de experimentos
│   └── graphics/               # Generación de visualizaciones
├── test/
│   ├──test_data_generator.py
│   └──test/test_quick_sort.py
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

## 🧠 Sobre Quick Sort
Quick Sort es un algoritmo de ordenamiento basado en la estrategia de divide y vencerás.

Su funcionamiento general consiste en:

Seleccionar un elemento de la lista como pivote.
Reorganizar los elementos alrededor del pivote.
Aplicar el mismo procedimiento de forma recursiva a las particiones resultantes.
Continuar hasta que las particiones tengan uno o ningún elemento.

En esta implementación se utiliza el primer elemento de cada sublista como pivote.

La elección del pivote influye directamente en el rendimiento del algoritmo. Cuando el pivote divide la entrada en particiones aproximadamente iguales, el algoritmo presenta un comportamiento de:

``$$ O(n \log n) $$``

Sin embargo, cuando el pivote genera particiones muy desbalanceadas, el número de operaciones puede crecer hasta:

``O(n2)``



En este proyecto se estudian tres situaciones:

* **`Mejor Caso:`** se generan datos buscando que el primer elemento de cada partición sea un pivote cercano a la mediana, produciendo particiones aproximadamente equilibradas.



* **`Caso promedio:`** se utilizan datos generados aleatoriamente para representar una distribución sin un patrón de orden específico.

* **`Peor caso:`** se utiliza una lista ordenada de forma ascendente. Debido a que el primer elemento es utilizado como pivote, las particiones resultan altamente desbalanceadas.


## Complejidad espacial
```
La implementación ordena la lista en el mismo arreglo (in-place), por lo que no necesita crear otra lista completa para almacenar el resultado.

Sin embargo, Quick Sort utiliza memoria adicional debido a las llamadas recursivas:

Caso promedio/mejor caso: aproximadamente $O(\log n)$.
Peor caso: puede llegar hasta $O(n)$ debido a la profundidad de la recursión.

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

## 🧪 Experimentos
Los experimentos se realizan utilizando diferentes tamaños de entrada y varias repeticiones para cada tamaño.

Actualmente se utilizan los siguientes tamaños:

* **`100`**
* **`200`**
* **`500`**
* **`1000`**
* **`2000`**

Cada tamaño se ejecuta varias veces para obtener mediciones que permitan comparar el comportamiento del algoritmo.

Para cada ejecución se registran diferentes métricas, entre ellas:

Tiempo de ejecución.
Comparaciones.
Intercambios.
Iteraciones.
Llamadas recursivas.

El tiempo se mide utilizando **`time.perf_counter()`**, y la generación de los datos se realiza antes de iniciar la medición para evitar que el tiempo necesario para generar las entradas afecte al resultado del algoritmo.

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
