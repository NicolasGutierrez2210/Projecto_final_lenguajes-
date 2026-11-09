# DaZe: DSL para Analítica Deportiva (Sports Analytics DSL)

Este repositorio contiene la implementación completa de **DaZe** (`.dz`), un lenguaje de dominio específico diseñado para modelar flujos reproducibles de análisis de datos deportivos, preparación de plantillas de atletas, simulaciones tácticas, modelos de predicción y generación de pizarras de rendimiento.

El objetivo de DaZe es que los analistas de rendimiento, preparadores físicos y directores técnicos puedan transformar y analizar datos de forma declarativa mediante *pipelines* secuenciales (`|>`), estructuras de datos en memoria, ciclos imperativos y algoritmos de Machine Learning construidos para el dominio deportivo, garantizando un entorno de ejecución desacoplado de dependencias externas pesadas.

El proyecto utiliza **ANTLR4** para el *front-end* (análisis léxico y sintáctico) y **Python 3.11+** para el análisis semántico y la ejecución interpretada mediante el patrón de diseño **Visitor** sobre una **Tabla de Símbolos** jerárquica con soporte de ámbitos.

---

## Arquitectura de Librerías Nativas (`src/core/`)

Para garantizar la autonomía del lenguaje y cumplir estrictamente con los lineamientos de diseño algorítmico, **no se utilizan bibliotecas externas como `pandas`, `numpy`, `scikit-learn` o el módulo estándar `math`**. Todas las estructuras y motores de cálculo han sido construidos desde cero en Python puro dentro de `src/core/`:

### 1. `racoons (Tabla)` (`src/core/racoons.py`)
Estructura tabular bidimensional nativa para la manipulación inmutable de datos deportivos:
- **`csvread(ruta, separador=',', encabezado=verdadero)`**: Lectura de archivos CSV con inferencia automática de tipos (enteros, decimales, booleanos y valores nulos).
- **`csvsave(ruta, separador=',')`**: Exportación de tablas a disco asegurando la creación recursiva de directorios.
- **`convocar(columnas)`**: Proyección selectiva de atributos, validando su existencia en el esquema.
- **`descartar(condicion)`**: Filtrado condicional no destructivo de registros.
- **`contratar(columnas_dict)`**: Derivación y cálculo de nuevas métricas mediante expresiones aritméticas.
- **`rebautizar(mapeo)`**: Renombrado de variables existentes.
- **`clasificar(columnas, descendente)`**: Ordenamiento múltiple de registros en orden ascendente o descendente.
- **`alinear(columnas_grupo)`**: Particionamiento y agrupación de registros (*GroupBy*).
- **`balance(agregaciones)`**: Resumen estadístico multivariable sobre grupos o tablas globales.
- **`sanear(reemplazos)`**: Imputación de datos faltantes o bajas médicas.
- **`depurar(columnas)`**: Deduplicación de registros en la plantilla.
- **`top(n)`**: Truncamiento de los primeros $n$ registros destacados.
- **`mostrar(limite=10)`**: Renderizado tabular en consola con bordes ASCII alineados.

### 2. Motor Matemático Puro (`src/core/matematica.py`)
Módulo algorítmico implementado sin dependencias de la librería estándar `math`:
- **`raiz_cuadrada(x)` / `raiz(x)`**: Algoritmo iterativo de Newton-Raphson / Babilónico ($x_{k+1} = \frac{1}{2}(x_k + \frac{n}{x_k})$) con tolerancia de $10^{-12}$.
- **`seno(x)` y `coseno(x)`**: Aproximación trigonométrica de alta precisión mediante Series de Taylor con normalización modular al rango $[-\pi, \pi]$.
- **`tangente(x)`**: Razón trigonométrica con control de asíntotas y división por cero.
- **`potencia(base, exp)`**: Exponenciación entera positiva, negativa y fraccionaria pura.
- **`valor_absoluto(x)` / `abs(x)`**: Magnitud escalar.

### 3. Estadística Descriptiva (`src/core/estadistica.py`)
Operaciones descriptivas desacopladas que operan sobre colecciones e iterables:
- **`suma(valores)`**: Sumatoria ignorando registros nulos o inválidos.
- **`media(valores)`**: Promedio aritmético.
- **`mediana(valores)`**: Valor central tras ordenamiento determinístico.
- **`minimo(valores)`** y **`maximo(valores)`**: Extremos de la serie.
- **`desviar(valores)` / `desv_std`**: Desviación estándar muestral utilizando la raíz cuadrada babilónica pura.
- **`contar(valores)`**: Conteo de registros válidos.

### 4. Estructuras de Datos Lineales (`src/core/estructuras.py`)
Estructuras nativas integradas al sistema de tipos de DaZe:
- **`Pila` (LIFO)**:
  - `pila()`: Inicialización en memoria.
  - `apilar(p, elemento)`: Inserción en el tope.
  - `desapilar(p)`: Extracción destructiva del tope.
  - `tope(p)`: Inspección del valor superior sin remoción.
- **`Cola` (FIFO)**:
  - `cola()`: Inicialización en memoria.
  - `encolar(c, elemento)`: Inserción al final de la fila.
  - `desencolar(c)`: Extracción destructiva del frente.
  - `frente(c)`: Inspección del primer elemento en turno.
- **Operaciones Compartidas**: `longitud(coleccion)` para consultar el tamaño de arreglos, pilas y colas.

### 5. Motor de Machine Learning y Métodos Numéricos (`src/core/ml.py`)
Modelos predictivos y algoritmos de agrupamiento construidos desde cero en Python puro:
- **`correlacion_pearson(x, y)` / `correlacion(x, y)`**: Coeficiente de correlación lineal de Pearson ($r \in [-1.0, 1.0]$) implementado mediante sumatorias de desvíos y raíz babilónica para cuantificar la asociación física entre variables (ej. minutos vs. goles).
- **`RegresionLineal` / `regresion_lineal(x, y)`**: Modelo de regresión lineal simple ($y = mx + b$).
  - Ajuste analítico de parámetros ($m, b$) mediante **Mínimos Cuadrados Ordinarios**.
  - Optimización numérica alternativa mediante **Descenso de Gradiente** (`ajustar_gradiente`).
  - Cálculo de la métrica de bondad de ajuste o coeficiente de determinación ($R^2$).
  - Método de inferencia (`predecir` / `predecir_regresion`) para estimar rendimiento futuro.
- **`KMeans` / `agrupar_kmedias(datos, k)`**: Algoritmo de agrupamiento no supervisado (*Clustering*).
  - Cálculo de distancias en espacios $D$-dimensionales mediante **Distancia Euclidiana** pura.
  - Asignación dinámica de clusters y convergencia iterativa de centroides por coordenadas medias.
  - Segmentación automática de jugadores según perfiles atléticos y tácticos sin etiquetas previas.

---

## Estructura del Repositorio

```text
proyecto_lenguajes/
|-- grammar/
|   |-- DaZeLexer.g4          # Definicion lexica: palabras clave deportivas, operadores y literales
|   |-- DaZeParser.g4         # Definicion sintactica: sentencias, bucles, arreglos y pipelines
|-- src/
|   |-- __init__.py           # Fachada de compilacion y parseo
|   |-- cli.py                # Interfaz de linea de comandos (CLI) y modo interactivo (REPL)
|   |-- errors.py             # Listener de errores lexicos y sintacticos en espanol
|   |-- tree_viewer.py        # Visualizador jerarquico del arbol sintactico (CST/AST)
|   |-- core/                 # Librerias nativas en Python puro (Cero dependencias)
|   |   |-- racoons.py        # Motor de DataFrames (Tabla y GrupoTabla)
|   |   |-- matematica.py     # Newton-Raphson, Series de Taylor y algoritmos puros
|   |   |-- estadistica.py    # Metricas descriptivas independientes de math
|   |   |-- estructuras.py    # Implementacion de Pila (LIFO) y Cola (FIFO)
|   |   |-- ml.py             # Machine Learning puro: Pearson, Regresion Lineal y K-Means
|   |-- semantic/             # Evaluacion semantica y tiempo de ejecucion
|   |   |-- tabla_simbolos.py # Tabla de simbolos con soporte de ambitos y tipos
|   |   |-- visitor.py        # Evaluador semantico e interprete del arbol AST
|   |-- generated/            # Clases autogeneradas por ANTLR4
|       |-- DaZeLexer.py
|       |-- DaZeParser.py
|       |-- DaZeParserVisitor.py
|       |-- DaZeParserListener.py
|-- docs/
|   |-- especificacion_lenguaje.md  # Catalogo formal de tipos, operadores e instrucciones
|   |-- gramatica_ebnf.md          # Especificacion sintactica en formato EBNF
|-- examples/
|   |-- demo_estructuras.dz   # Prueba integral de arreglos, diccionarios, pilas, colas y bucles
|   |-- correcto_ventas.dz    # Pipeline de rendimiento de jugadores del primer equipo
|   |-- correcto_estudiantes.dz # Evaluacion y metricas en divisiones menores
|   |-- correcto_sensores.dz  # Telemetria GPS y deteccion de fatiga cardiovascular
|   |-- incorrecto_sintaxis.dz# Casos de prueba con errores intencionales
|   |-- incorrecto_lexico.dz  # Casos con caracteres invalidos
|-- prueba_ml.dz              # Demostracion integral de Machine Learning en DaZe
|-- tests/
|   |-- test_lexer.py         # Pruebas unitarias del analizador lexico
|   |-- test_parser.py        # Pruebas unitarias de parsing y precedencia
|   |-- test_errors.py        # Pruebas de captura de errores y diagnostico
|-- requirements.txt          # Dependencia unica del runtime: antlr4-python3-runtime
|-- .gitignore                # Reglas de exclusion de control de versiones
|-- README.md                 # Documentacion tecnica principal
```

---

## Sintaxis y Capacidades del Lenguaje

### 1. Carga, Asignación y Proyección
```daze
plantilla = fichar("datos/plantilla_temporada.csv", separador=",", encabezado=verdadero);
proyectar("Plantilla cargada exitosamente.");
```

### 2. Estructuras de Datos (Arreglos, Diccionarios, Pilas y Colas)
DaZe cuenta con soporte de literales, indexación y mutación por corchetes `[]`:
```daze
# Arreglos y matrices bidimensionales
dorsales = [10, 7, 9];
dorsales[1] = 11;

matriz_tactica = [
    [1, 0],
    [0, 1]
];

# Diccionarios asociativos
ficha = {
    "nombre": "Kylian",
    "goles": 24
};
proyectar(ficha["goles"]);

# Pilas y Colas nativas
estrategias = pila();
apilar(estrategias, "Presion Alta");
estrategia_activa = tope(estrategias);

turnos = cola();
encolar(turnos, "Jugador 1");
desencolar(turnos);
```

### 3. Ciclos Temáticos Imperativos
- **`en_juego (condicion) { ... }`**: Bucle condicional (*while*) para simulaciones continuas o decrementos iterativos.
- **`ronda (elemento en coleccion) { ... }`**: Bucle de recorrido (*for-in*) sobre arreglos, listas y tablas.
```daze
contador = 3;
en_juego (contador > 0) {
    proyectar(contador);
    contador = contador - 1;
}

ronda (num en dorsales) {
    proyectar(num);
}
```

### 4. Pipelines de Transformación Tabular (`|>`)
```daze
titulares = plantilla
    |> convocar(dorsal, club, posicion, minutos, goles, asistencias)
    |> descartar(minutos > 0 y goles >= 0)
    |> contratar(
        contribucion = goles + asistencias,
        promedio_gol = (goles * 90) / minutos,
        rendimiento = (contribucion * 1.5) + (minutos / 100)
    )
    |> clasificar(por=[rendimiento], descendente=verdadero)
    |> top(11);

resumen_posiciones = titulares
    |> alinear(por=[posicion])
    |> balance(
        goles_totales = suma(goles),
        media_asistencias = media(asistencias),
        total_convocados = contar()
    );

archivar(resumen_posiciones, en="salidas/resumen_posiciones.csv", separador=",");
```

### 5. Cálculo Matemático Puro
```daze
angulo = 1.047; # ~60 grados en radianes
val_seno = seno(angulo);
hipotenusa = raiz(64);
proyectar(hipotenusa); # 8.0
```

### 6. Machine Learning y Métricas Predictivas Puras
```daze
# 1. Asociacion lineal entre minutos jugados y goles marcados
minutos = [120, 340, 500, 750, 900, 1100, 1300];
goles   = [1, 3, 4, 7, 8, 11, 14];

r = correlacion(minutos, goles);
proyectar(r); # ~0.9916

# 2. Entrenamiento de Regresion Lineal Simple (y = m*x + b)
modelo = regresion_lineal(minutos, goles);
proyectar(modelo["m"]);  # Pendiente calculada
proyectar(modelo["b"]);  # Intercepto calculado
proyectar(modelo["r2"]); # Coeficiente R^2

# Prediccion de goles esperados para 950 minutos
goles_estimados = predecir_regresion(modelo, 950);
proyectar(goles_estimados); # ~9.39 goles

# 3. Agrupamiento no supervisado K-Means (k=2) sobre vectores [minutos, goles]
perfiles = [
    [100, 1], [150, 0], [200, 1],      # Suplentes
    [1100, 12], [1200, 15], [1300, 14] # Titulares
];
clusters = agrupar_kmedias(perfiles, 2);
proyectar(clusters["centroides"]);
proyectar(clusters["etiquetas"]); # [0, 0, 0, 1, 1, 1]
```

### 7. Pizarras Visuales Declarativas
```daze
pizarra barras(resumen_posiciones) {
    eje_x = posicion;
    eje_y = goles_totales;
    titulo = "Goles Totales por Posicion";
    color = "azul";
    guardar = "salidas/goles_por_posicion.png";
}
```

---

## Guía de Ejecución y Pruebas

### 1. Requisitos Previos
- Python 3.11 o superior.
- Java JRE 11+ (requerido únicamente si se recompilan las gramáticas `.g4` de ANTLR).

### 2. Instalación
```bash
git clone https://github.com/NicolasGutierrez2210/Projecto_final_lenguajes-.git
cd Projecto_final_lenguajes-
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Ejecución de Programas
Para ejecutar un archivo con el intérprete semántico:
```bash
python3 src/cli.py prueba_ml.dz
python3 src/cli.py examples/demo_estructuras.dz
python3 src/cli.py examples/correcto_ventas.dz
```

Opciones de análisis y diagnóstico adicionales:
```bash
# Solo validar sintaxis sin ejecutar
python3 src/cli.py --check prueba_ml.dz

# Visualizar el stream de tokens del Lexer
python3 src/cli.py --tokens prueba_ml.dz

# Ver el arbol sintactico concreto (CST) en formato jerarquico
python3 src/cli.py --tree prueba_ml.dz
```

### 4. Batería de Pruebas Automatizadas
Para ejecutar toda la suite de pruebas unitarias:
```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```
