# DaZe: DSL para Analítica Deportiva (Sports Analytics DSL)

Este repositorio contiene la especificación formal, diseño algorítmico e implementación completa de **DaZe** (`.dz`), un lenguaje de dominio específico (*Domain-Specific Language*, DSL) concebido para modelar flujos de trabajo reproducibles en analítica de rendimiento deportivo, simulación táctica, preparación de plantillas de atletas, modelado predictivo y especificación declarativa de pizarras visuales.

El objetivo central de DaZe es proporcionar a analistas de rendimiento, preparadores físicos y directores técnicos una sintaxis declarativa, formal y contextualizada en el deporte mediante *pipelines* secuenciales (`|>`), ciclos imperativos temáticos (`en_juego`, `ronda`), estructuras de datos lineales nativas en memoria, algoritmos de Machine Learning desarrollados desde primeros principios matemáticos y un motor gráfico autónomo, eliminando dependencias de librerías de terceros como `pandas`, `numpy`, `scikit-learn`, `matplotlib` o la biblioteca estándar `math`.

El compilador/intérprete utiliza **ANTLR4** en el *front-end* (análisis léxico y sintáctico) y **Python 3.11+** en el *back-end* para el análisis semántico y la ejecución interpretada mediante el patrón de diseño **Visitor**, apoyado en una **Tabla de Símbolos** jerárquica con soporte de múltiples ámbitos y tipos de datos nativos.

---

## 1. Filosofía y Principios de Diseño

1. **Cero Dependencias de Cómputo y Graficación Externa (*Zero-Dependency Core*)**:
   El motor numérico, el procesamiento tabular, las estructuras de datos, los modelos de Machine Learning y el trazador de imágenes PNG han sido construidos desde cero en Python puro dentro del paquete `src/core/`. El único requisito externo del proyecto es el runtime oficial de ANTLR4 (`antlr4-python3-runtime`) para la etapa de generación de árboles sintácticos.
2. **Inmutabilidad Tabular en Tuberías (`|>`)**:
   Inspirado en paradigmas funcionales modernos (Elixir, F# y el ecosistema Tidyverse de R), cada transformación en una tubería recibe una plantilla de datos y genera una nueva colección derivada en memoria sin mutar destructivamente el estado de la tabla original.
3. **Dualidad de Renderizado Visual (Consola + PNG Binario Autónomo)**:
   Las sentencias `pizarra` ejecutan un renderizado simultáneo: trazan diagramas en arte ASCII/Unicode directamente en la terminal para inspección inmediata y empaquetan físicamente archivos `.png` válidos compatibles con cualquier visor mediante manipulación de bytes y compresión DEFLATE nativa (`zlib`).
4. **Vocabulario Formal de Dominio**:
   Se sustituyen los términos genéricos de bases de datos por la terminología de dirección técnica y analítica deportiva:
   - `fichar`: Carga de datos de plantilla desde archivos CSV.
   - `archivar`: Persistencia física y exportación tabular a disco.
   - `convocar`: Proyección selectiva de variables y columnas clave.
   - `descartar`: Filtrado condicional de registros basado en predicados lógicos.
   - `contratar`: Mutación e incorporación de nuevas métricas calculadas.
   - `clasificar`: Ordenamiento múltiple por métricas de rendimiento.
   - `alinear`: Segmentación y particionamiento por grupos tácticos (*GroupBy*).
   - `balance`: Agregaciones y resúmenes descriptivos sobre grupos o tablas.
   - `pizarra`: Declaración y especificación gráfica de representaciones visuales.
   - `tactica`: Definición de subrutinas modulares con ámbito local.
   - `en_juego` / `ronda`: Bucles imperativos temáticos (*while* y *for-in*).

---

## 2. Arquitectura de Librerías Nativas (`src/core/`)

Toda la lógica de procesamiento reside en módulos propios desacoplados:

### 2.1. `racoons (Tabla y GrupoTabla)` (`src/core/racoons.py`)
Estructura de datos tabular bidimensional en memoria diseñada para manipular colecciones de registros sin `pandas`:
- **`csvread(ruta, separador=',', encabezado=verdadero)`**: Lectura de archivos delimitados mediante el módulo nativo `csv` de Python con inferencia automática de tipos (`ENTERO`, `DECIMAL`, `BOOLEANO`, `CADENA` y `NULO`).
- **`csvsave(ruta, separador=',')`**: Exportación física a disco con aseguramiento y creación recursiva de directorios de destino.
- **`convocar(columnas)`**: Proyección de subconjuntos de columnas con validación estricta de esquemas.
- **`descartar(condicion)`**: Evaluación booleana fila por fila para aislar atletas o eventos que cumplan determinados criterios.
- **`contratar(columnas_dict)`**: Derivación de nuevos indicadores atléticos a partir de expresiones aritméticas evaluadas dinámicamente.
- **`rebautizar(mapeo)`**: Renombrado determinístico de atributos.
- **`clasificar(columnas, descendente)`**: Algoritmo de ordenamiento estable ascendente o descendente por una o más claves.
- **`alinear(columnas_grupo)`**: Particionamiento de la tabla en subgrupos aislados (`GrupoTabla`) según claves discretas (ej. posición, club).
- **`balance(agregaciones)`**: Computación multivariable de métricas agregadas por grupo o sobre la tabla global.
- **`sanear(reemplazos)` / `reemplazar_bajas`**: Imputación de valores faltantes o nulos por valores por defecto.
- **`depurar(columnas)` / `depurar_plantilla`**: Deduplicación de registros en la plantilla.
- **`top(n)`**: Truncamiento de los primeros $n$ registros destacados.
- **`mostrar(limite=10)`**: Renderizado visual por consola con alineación de columnas y bordes en texto ASCII.

### 2.2. Motor Matemático Puro (`src/core/matematica.py`)
Módulo algorítmico implementado sin recurrir a la librería estándar `math`:
- **`raiz_cuadrada(x)` / `raiz(x)`**: Aproximación iterativa de Newton-Raphson / Método Babilónico:
  $$x_{k+1} = \frac{1}{2} \left( x_k + \frac{n}{x_k} \right)$$
  Calculado con cota de tolerancia de convergencia de $10^{-12}$.
- **`seno(x)`**: Evaluación trigonométrica de precisión mediante Series de Taylor con normalización modular al intervalo $[-\pi, \pi]$:
  $$\sin(x) = \sum_{k=0}^{12} \frac{(-1)^k}{(2k+1)!} x^{2k+1}$$
- **`coseno(x)`**: Evaluación trigonométrica por Series de Taylor:
  $$\cos(x) = \sum_{k=0}^{12} \frac{(-1)^k}{(2k)!} x^{2k}$$
- **`tangente(x)`**: Razón analítica $\frac{\sin(x)}{\cos(x)}$ con control de singularidades y división por cero.
- **`potencia(base, exp)`**: Exponenciación entera positiva, negativa y fraccionaria pura.
- **`valor_absoluto(x)` / `abs(x)`**: Magnitud escalar absoluta.

### 2.3. Estadística Descriptiva (`src/core/estadistica.py`)
Métricas descriptivas desacopladas que operan sobre secuencias numéricas ignorando valores nulos o corruptos:
- **`suma(valores)`**: Acumulación aritmética determinística.
- **`media(valores)`**: Promedio aritmético ($\bar{x} = \frac{1}{N}\sum x_i$).
- **`mediana(valores)`**: Valor central de la serie ordenada (o promedio de las dos posiciones medias si $N$ es par).
- **`minimo(valores)`** y **`maximo(valores)`**: Detección de extremos en colecciones.
- **`desviar(valores)` / `desv_std`**: Desviación estándar muestral utilizando la raíz cuadrada babilónica pura:
  $$s = \sqrt{\frac{1}{N-1}\sum_{i=1}^{N} (x_i - \bar{x})^2}$$
- **`contar(valores)`**: Conteo de registros válidos.

### 2.4. Estructuras de Datos Lineales y Colecciones (`src/core/estructuras.py`)
Estructuras nativas integradas al sistema de tipos y tabla de símbolos de DaZe:
- **`Pila` (LIFO - *Last In, First Out*)**:
  - `pila()`: Instanciación de una pila vacía.
  - `apilar(p, elemento)`: Inserción en el tope de la estructura.
  - `desapilar(p)`: Extracción destructiva del elemento superior.
  - `tope(p)`: Consulta del elemento en la cima sin remoción.
- **`Cola` (FIFO - *First In, First Out*)**:
  - `cola()`: Instanciación de una cola vacía.
  - `encolar(c, elemento)`: Inserción al final de la fila.
  - `desencolar(c)`: Extracción destructiva del elemento al frente.
  - `frente(c)`: Consulta del primer elemento sin remoción.
- **Arreglos y Matrices**: Literales `[10, 20, 30]`, matrices bidimensionales `[[1, 0], [0, 1]]`, indexación por corchetes `arr[i]` y mutación directa `arr[i] = nuevo_valor`.
- **Diccionarios Asociativos**: Literales asociativos `{"nombre": "Vinicius", "goles": 21}`, lectura por clave `dict[clave]` y mutación `dict[clave] = nuevo_valor`.
- **Operaciones Compartidas**: `longitud(coleccion)` para consultar la cardinalidad de arreglos, diccionarios, pilas y colas.

### 2.5. Machine Learning y Métodos Numéricos Puros (`src/core/ml.py`)
Biblioteca de modelos predictivos y aprendizaje no supervisado construida desde cero sin `scikit-learn` ni `numpy`:
- **`correlacion_pearson(x, y)` / `correlacion(x, y)`**:
  Calcula el coeficiente de correlación lineal de Pearson ($r \in [-1.0, 1.0]$) entre dos variables continuas:
  $$r = \frac{\sum_{i=1}^N (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^N (x_i - \bar{x})^2} \cdot \sqrt{\sum_{i=1}^N (y_i - \bar{y})^2}}$$
- **`RegresionLineal` / `regresion_lineal(x, y)`**:
  Modelo de regresión lineal simple ($y = mx + b$):
  - **Ajuste Analítico por Mínimos Cuadrados Ordinarios (MCO)**:
    $$m = \frac{\sum_{i=1}^N (x_i - \bar{x})(y_i - \bar{y})}{\sum_{i=1}^N (x_i - \bar{x})^2}, \quad b = \bar{y} - m\bar{x}$$
  - **Bondad de Ajuste ($R^2$)**: Coeficiente de determinación que cuantifica la proporción de varianza explicada:
    $$R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$$
  - **Inferencia (`predecir_regresion(modelo, x)` / `predecir`)**: Estima valores escalares o listas de proyecciones futuras.
- **`KMeans` / `agrupar_kmedias(datos, k)`**:
  Algoritmo de agrupamiento no supervisado (*Clustering*) para segmentar perfiles de atletas sin etiquetas:
  - Distancia euclidiana multidimensional pura:
    $$d(p, q) = \sqrt{\sum_{k=1}^D (p_k - q_k)^2}$$
  - Asignación dinámica a los centroides más cercanos.
  - Recálculo iterativo de centroides como la coordenada media de cada cluster.

### 2.6. Motor Visual Nativo PNG y ASCII (`src/core/visualizador.py`)
Generador gráfico autónomo desacoplado de `matplotlib`:
- **Rasterizador 2D Nativo (`CanvasPNG`)**: Lienzo en memoria que implementa el algoritmo de Bresenham para trazar líneas de ejes y curvas, polígonos de barras y círculos de dispersión.
- **Codificador Binario PNG**: Empaqueta los bloques estándar `IHDR`, `IDAT` y `IEND` calculando sumas de redundancia cíclica (`CRC32`) y comprimiendo los canales RGB con el módulo estándar `zlib`.
- **Renderizador Dual**: Imprime gráficos en caracteres ASCII (`█`, `▓`, `●`) en la consola estándar y exporta el archivo físico `.png` en disco.

---

## 3. Infraestructura de Compilación y Ejecución

### 3.1. Front-End (ANTLR4)
- **`grammar/DaZeLexer.g4`**: Definición léxica. Transforma el código fuente en tokens atómicos (palabras reservadas deportivas, literales numéricos, cadenas, operadores relacionales y delimitadores). Incluye la directiva `-> skip` para descartar espacios en blanco y comentarios (`#` y `/* ... */`).
- **`grammar/DaZeParser.g4`**: Gramática libre de contexto. Valida la estructura jerárquica de sentencias, bucles, asignaciones, tuberías (`|>`) y resuelve la precedencia de operadores mediante recursividad izquierda:
  $$\text{Potencia } (\hat{}, **) \longrightarrow \text{Unarios } (+, -, \text{no}) \longrightarrow \text{Multiplicativos } (*, /, \%) \longrightarrow \text{Aditivos } (+, -) \longrightarrow \text{Relacionales } (==, !=, <, >, <=, >=) \longrightarrow \text{Lógicos } (\text{y}, \text{o})$$

### 3.2. Tabla de Símbolos y Ámbitos (`src/semantic/tabla_simbolos.py`)
Maneja la visibilidad de identificadores mediante una estructura jerárquica de entornos:
- **Ámbito Global**: Mantiene las tablas cargadas con `fichar`, los resultados de pipelines y las variables generales.
- **Ámbitos Locales**: Se crean dinámicamente al invocar funciones (`tactica`), aislando parámetros y variables locales del entorno global.
- **Tipado Dinámico**: Asocia cada variable a su tipo nativo (`ENTERO`, `DECIMAL`, `CADENA`, `BOOLEANO`, `TABLA`, `PILA`, `COLA`, `LISTA`, `DICCIONARIO`).

### 3.3. Intérprete Semántico (`src/semantic/visitor.py`)
Implementa el patrón de diseño **Visitor** sobre el árbol sintáctico (AST):
- Evalúa expresiones aritméticas, lógicas y relacionales.
- Enlaza en tiempo de ejecución las columnas de una tabla para que las expresiones dentro de `descartar` o `contratar` resuelvan directamente los campos del registro.
- Controla el flujo de ejecución en bifurcaciones `si`/`sino` y ciclos `en_juego`/`ronda`.
- Gestiona el retorno de subrutinas con la palabra clave `resultado`.
- Despacha las llamadas a funciones nativas matemáticas, de estructuras de datos, de Machine Learning puro y generación de pizarras.

### 3.4. Consola Interactiva (REPL) y CLI (`src/cli.py` & `./daze`)
El archivo `src/cli.py` ofrece dos modalidades de uso:
1. **Consola Interactiva en Vivo (REPL Oficial)**:
   Al ejecutar `./daze` o `python3 src/cli.py` sin argumentos, se inicializa un shell interactivo (`daze> `) que:
   - Mantiene una única instancia de `TablaSimbolos` y `Visitor` en memoria a lo largo de toda la sesión.
   - Permite ingresar código multilínea controlando la apertura y cierre de llaves (`{ ... }`), permitiendo definir tácticas y pizarras en vivo.
   - Dispone de comandos de sesión: `ayuda`, `limpiar`, `simbolos` y `salir`.
2. **Modo por Lotes (Batch)**:
   Ejecución directa de scripts `.dz` desde la terminal de comandos (`python3 src/cli.py script.dz`).

---

## 4. Estructura del Repositorio

```text
proyecto_lenguajes/
|-- grammar/
|   |-- DaZeLexer.g4          # Definición léxica: tokens deportivos, operadores y literales
|   |-- DaZeParser.g4         # Definición sintáctica: sentencias, pipelines, bucles y estructuras
|-- src/
|   |-- __init__.py           # Fachada de compilación y parseo
|   |-- cli.py                # Interfaz de línea de comandos (CLI) y Consola Interactiva (REPL)
|   |-- errors.py             # Listener de errores léxicos y sintácticos en español
|   |-- tree_viewer.py        # Visualizador jerárquico del árbol sintáctico (CST/AST)
|   |-- core/                 # Librerías nativas en Python puro (Cero dependencias externas)
|   |   |-- racoons.py        # Motor de DataFrames propio (Tabla y GrupoTabla)
|   |   |-- matematica.py     # Newton-Raphson, Series de Taylor y métodos numéricos
|   |   |-- estadistica.py    # Estadística descriptiva pura desacoplada
|   |   |-- estructuras.py    # Estructuras de datos lineales: Pila (LIFO) y Cola (FIFO)
|   |   |-- ml.py             # Machine Learning puro: Pearson, Regresión Lineal y K-Means
|   |   |-- visualizador.py   # Motor visual nativo: CanvasPNG binario puro y ASCII art
|   |-- semantic/             # Análisis semántico y evaluación en tiempo de ejecución
|   |   |-- tabla_simbolos.py # Tabla de símbolos con soporte de ámbitos y tipos
|   |   |-- visitor.py        # Intérprete semántico basado en el patrón Visitor
|   |-- generated/            # Clases autogeneradas por ANTLR4
|       |-- DaZeLexer.py
|       |-- DaZeParser.py
|       |-- DaZeParserVisitor.py
|       |-- DaZeParserListener.py
|-- docs/
|   |-- especificacion_lenguaje.md  # Catálogo formal de tipos, operadores e instrucciones
|   |-- gramatica_ebnf.md          # Especificación formal en notación EBNF
|   |-- caso_estudio.md            # Informe técnico integral de los 8 puntos evaluados
|-- datos/
|   |-- rendimiento_jugadores.csv  # Dataset oficial de 15 futbolistas profesionales
|   |-- plantilla_temporada.csv    # Dataset general de plantilla
|-- salidas/                       # Directorio de persistencia física de resultados
|   |-- resumen_posiciones.csv     # Tabla consolidada de agregaciones por posición
|   |-- 1_goles_por_posicion.png   # Pizarra de Barras generada sin librerías
|   |-- 2_dispersion_minutos_contribucion.png # Pizarra de Dispersión
|   |-- 3_histograma_minutos.png   # Pizarra de Histograma
|   |-- 4_lineas_top_ofensivo.png  # Pizarra de Líneas
|-- examples/
|   |-- demo_estructuras.dz   # Prueba integral de arreglos, diccionarios, pilas y bucles
|   |-- correcto_ventas.dz    # Pipeline de analítica de rendimiento deportivo
|   |-- correcto_estudiantes.dz # Procesamiento de métricas formativas en cantera
|   |-- correcto_sensores.dz  # Monitoreo de telemetría de chalecos GPS
|   |-- incorrecto_sintaxis.dz# Casos con errores sintácticos intencionales para diagnóstico
|   |-- incorrecto_lexico.dz  # Casos con caracteres inválidos para prueba de errores
|-- caso_estudio.dz           # Script maestro ejecutable del caso de estudio (Corte 3)
|-- prueba_ml.dz              # Demostración integral de Machine Learning puro en DaZe
|-- tests/
|   |-- test_lexer.py         # Pruebas unitarias del analizador léxico
|   |-- test_parser.py        # Pruebas unitarias sintácticas y precedencia
|   |-- test_errors.py        # Pruebas de captura de errores léxicos y sintácticos
|   |-- test_core_tabla.py    # Pruebas unitarias del motor racoons
|   |-- test_estadistica.py   # Pruebas unitarias de estadística pura
|   |-- test_interpreter.py   # Pruebas de evaluación semántica del visitor
|   |-- test_semantic.py      # Pruebas de tabla de símbolos y chequeo de tipos
|   |-- test_corte3.py        # Pruebas de ML puro, visualizador binario y pizarras
|-- daze                      # Script ejecutable de acceso directo a la consola interactiva
|-- requirements.txt          # Dependencia única del runtime: antlr4-python3-runtime
|-- .gitignore                # Reglas de exclusión para Git
|-- README.md                 # Documentación técnica principal del proyecto
```

---

## 5. Sintaxis y Capacidades del Lenguaje

### 5.1. Carga, Persistencia y Proyección
```daze
# Carga de plantilla desde archivo CSV con delimitador configurable
plantilla = fichar("datos/rendimiento_jugadores.csv", separador=",", encabezado=verdadero);

# Impresión en consola de cadenas, tablas o expresiones evaluadas
proyectar("Plantilla cargada exitosamente.");
proyectar(plantilla);

# Exportación de la tabla resultante a disco
archivar(plantilla, en="salidas/plantilla_respaldo.csv", separador=",");
```

### 5.2. Estructuras de Datos Lineales y Colecciones
```daze
# 1. Arreglos e indexación por corchetes
dorsales = [10, 7, 9, 8];
dorsales[1] = 11;
proyectar(dorsales[1]); # Imprime 11

# 2. Matrices bidimensionales
formacion_tactica = [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
];

# 3. Diccionarios asociativos
ficha_jugador = {
    "nombre": "Vinicius Jr",
    "posicion": "Delantero",
    "goles": 21
};
ficha_jugador["goles"] = 22;
proyectar(ficha_jugador["goles"]);

# 4. Pila nativa (LIFO)
estrategias = pila();
apilar(estrategias, "Bloque Bajo");
apilar(estrategias, "Presion Alta");
estrategia_activa = tope(estrategias);
proyectar(estrategia_activa); # "Presion Alta"
desapilar(estrategias);

# 5. Cola nativa (FIFO)
orden_penaltis = cola();
encolar(orden_penaltis, "Jugador A");
encolar(orden_penaltis, "Jugador B");
tirador_actual = frente(orden_penaltis);
proyectar(tirador_actual); # "Jugador A"
desencolar(orden_penaltis);
```

### 5.3. Ciclos Temáticos Imperativos
```daze
# Bucle condicional (while) temático
minutos_restantes = 3;
en_juego (minutos_restantes > 0) {
    proyectar(minutos_restantes);
    minutos_restantes = minutos_restantes - 1;
}

# Bucle de recorrido (for-in) sobre arreglos o colecciones
goles_ronda = [1, 2, 0, 3];
ronda (g en goles_ronda) {
    proyectar(g);
}
```

### 5.4. Subrutinas (`tactica`) y Condicionales (`si` / `sino`)
```daze
tactica evaluar_fatiga(frecuencia_cardiaca, distancia_km) {
    si (frecuencia_cardiaca > 185 y distancia_km > 10.0) {
        proyectar("Alerta: Sobrecarga cardiovascular detectada.");
        resultado 1;
    } sino {
        proyectar("Rango aerobico estable.");
        resultado 0;
    }
}

alerta = evaluar_fatiga(188, 11.2);
```

### 5.5. Tuberías de Transformación Tabular (`|>`)
```daze
titulares = plantilla
    |> convocar(dorsal, nombre, posicion, minutos, goles, asistencias)
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
        mediana_minutos = mediana(minutos),
        desv_rendimiento = desv_std(rendimiento),
        total_convocados = contar()
    );

archivar(resumen_posiciones, en="salidas/resumen_posiciones.csv", separador=",");
```

### 5.6. Motor Numérico y Funciones Matemáticas Puras
```daze
# Raíz cuadrada por aproximación Newton-Raphson pura
hipotenusa = raiz(64);
proyectar(hipotenusa); # 8.0

# Funciones trigonométricas por Series de Taylor
angulo_radianes = 1.047197; # ~60 grados
s = seno(angulo_radianes);
c = coseno(angulo_radianes);
proyectar(s);
proyectar(c);

# Exponenciación
pot = potencia(2, 8); # 256
```

### 5.7. Machine Learning y Métodos Predictivos Puros
```daze
# 1. Asociación Lineal: Coeficiente de Correlación de Pearson (r)
minutos = [120, 340, 500, 750, 900, 1100, 1300];
goles   = [1, 3, 4, 7, 8, 11, 14];

r = correlacion(minutos, goles);
proyectar("Correlacion de Pearson (minutos vs goles):");
proyectar(r);

# 2. Modelo Predictivo: Regresión Lineal Simple (y = m*x + b) por MCO
modelo = regresion_lineal(minutos, goles);
proyectar("Pendiente calculada (m):");
proyectar(modelo["m"]);
proyectar("Intercepto calculado (b):");
proyectar(modelo["b"]);
proyectar("Bondad de ajuste (R^2):");
proyectar(modelo["r2"]);

# Inferencia de goles para un jugador con 950 minutos disputados
prediccion_950 = predecir_regresion(modelo, 950);
proyectar("Goles estimados para 950 minutos:");
proyectar(prediccion_950);

# 3. Aprendizaje No Supervisado: K-Means Clustering (k=2) con Distancia Euclidiana
vectores_plantilla = [
    [100, 1],   [150, 0],   [200, 1],    # Suplentes con pocos minutos
    [1100, 12], [1200, 15], [1300, 14]   # Titulares goleadores
];

clusters = agrupar_kmedias(vectores_plantilla, 2);
proyectar("Centroides calculados:");
proyectar(clusters["centroides"]);
proyectar("Etiquetas asignadas por cluster:");
proyectar(clusters["etiquetas"]);
```

### 5.8. Declaración y Renderizado de Pizarras Visuales
```daze
pizarra barras(resumen_posiciones) {
    eje_x = "posicion";
    eje_y = "goles_totales";
    titulo = "Goles Totales por Posicion";
    color = "royalblue";
    guardar = "salidas/goles_por_posicion.png";
}

pizarra dispersion(titulares) {
    eje_x = "minutos";
    eje_y = "rendimiento";
    titulo = "Rendimiento vs Minutos Disputados";
    color = "crimson";
    guardar = "salidas/dispersion_rendimiento.png";
}
```

---

## 6. Caso de Estudio Oficial (Corte 3)

El caso de estudio modela el desempeño físico-táctico de una plantilla de 15 futbolistas profesionales de élite internacional (`datos/rendimiento_jugadores.csv`). El script maestro `caso_estudio.dz` ejecuta el flujo completo cubriendo los 8 puntos estipulados por la guía docente:

1. **Ingesta y Limpieza**: Carga del dataset y filtrado condicional mediante `descartar(minutos >= 800)`.
2. **Derivación de Indicadores**: Cálculo de contribución ofensiva ($\text{goles} + \text{asistencias}$), promedio de gol por partido completo y desgaste aeróbico por minuto.
3. **Agregación Descriptiva**: Agrupación táctica por línea (`alinear(por=[posicion])`) computando sumas, promedios, medianas y desviaciones estándar babilónicas puras.
4. **Machine Learning Aplicado**:
   - Correlación de Pearson ($r \approx 0.5246$) entre minutos y producción goleadora.
   - Ajuste por MCO ($m = 0.0217$, $b = -17.298$, $R^2 = 0.2752$) y proyección de $4.42$ goles para $1000$ minutos.
   - Segmentación K-Means ($k=3$) en perfiles de titulares determinantes, volantes mixtos y bloque bajo defensivo.
5. **Generación de las 4 Pizarras Físicas**:
   - `salidas/1_goles_por_posicion.png` (Barras)
   - `salidas/2_dispersion_minutos_contribucion.png` (Dispersión)
   - `salidas/3_histograma_minutos.png` (Histograma)
   - `salidas/4_lineas_top_ofensivo.png` (Líneas)

---

## 7. Guía de Ejecución y Pruebas (Linux / AWS EC2)

### 7.1. Requisitos Previos e Instalación
- Python 3.11 o superior y `pip`.
- Entorno de ejecución en Linux (Ubuntu, Debian o Amazon Linux 2023 en AWS EC2).

```bash
git clone https://github.com/NicolasGutierrez2210/Projecto_final_lenguajes-.git
cd Projecto_final_lenguajes-

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### 7.2. Ejecución del Caso de Estudio Integral
Para ejecutar el script del caso de estudio de principio a fin:

```bash
python3 src/cli.py caso_estudio.dz
```

Comprobar los archivos y gráficos generados:
```bash
ls -lh salidas/
cat salidas/resumen_posiciones.csv
```

### 7.3. Uso de la Consola Interactiva (REPL Oficial)
Para interactuar en vivo con el compilador manteniendo el estado en memoria:

```bash
./daze
```

Comandos en una sola línea o bloques multilínea compatibles:
```daze
daze> datos = fichar("datos/rendimiento_jugadores.csv");
daze> pizarra barras(datos) { eje_x = "posicion"; eje_y = "goles"; guardar = "salidas/pizarra_consola.png"; }
daze> salir
```

### 7.4. Ejecución de la Batería Completa de Pruebas Unitarias
Para correr las 45 pruebas automatizadas (Cortes 1, 2 y 3):

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

*Salida esperada:* `Ran 45 tests in ...s` finalizando en `OK`.

---

## 8. Manejo de Errores y Diagnóstico

El módulo `src/errors.py` implementa `DaZeErrorListener`, el cual sustituye los emisores de excepciones por defecto de ANTLR para ofrecer diagnósticos comprensibles en español:
- **Errores Léxicos**: Detecta caracteres que no pertenecen al alfabeto del lenguaje (ej. `@`, `$`) indicando la línea y columna exacta.
- **Errores Sintácticos**: Identifica tokens fuera de contexto o estructuras gramaticales incompletas (ej. punto y coma faltante, asignaciones truncadas o paréntesis desbalanceados), comunicando con precisión qué elemento se esperaba encontrar.
