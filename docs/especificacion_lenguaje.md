# Especificación Formal del Lenguaje DaZe (.dz) - Sports Analytics DSL

## 1. Delimitación del Dominio y Casos de Uso

DaZe es un lenguaje de dominio específico (*Domain-Specific Language*, DSL) diseñado para modelar flujos de trabajo reproducibles en analítica deportiva, preparación y evaluación de plantillas de atletas, simulaciones tácticas, modelos predictivos de rendimiento y especificación declarativa de pizarras visuales. El lenguaje combina una sintaxis declarativa basada en tuberías o *pipelines* (`|>`) con estructuras imperativas temáticas (`en_juego`, `ronda`), estructuras de datos lineales nativas en memoria, algoritmos de Machine Learning desarrollados desde primeros principios matemáticos y un entorno de ejecución desacoplado de dependencias externas.

### Perfil de Usuarios
* **Analistas de Rendimiento Deportivo y Preparadores Físicos**: Profesionales que requieren transformar telemetría GPS, métricas biomecánicas y estadísticas de partidos de manera compacta, reproducible y estructurada.
* **Directores Técnicos y Cuerpos Técnicos**: Equipos multidisciplinarios que diseñan convocatorias, simulan escenarios de sustitución y evalúan planes tácticos mediante un vocabulario directo de su área de conocimiento.
* **Científicos de Datos en Deportes**: Desarrolladores que construyen modelos predictivos (regresión, correlación) y segmentación no supervisada (agrupamiento de perfiles de jugadores) sin lidiar con la sobrecarga sintáctica de lenguajes de propósito general.

### Entradas y Salidas del Sistema
* **Entradas**:
  * Archivos estructurados en formato CSV con métricas de rendimiento deportivo (delimitadores configurables y soporte de encabezados).
  * Literales escalares (enteros, decimales, texto, booleanos).
  * Colecciones indexables (listas unidimensionales, matrices multidimensionales y diccionarios clave-valor).
  * Estructuras de datos lineales en memoria (pilas y colas).
* **Salidas**:
  * Tablas transformadas y consolidadas exportables físicamente a formato CSV (`archivar`).
  * Proyecciones tabulares y literales formateados en la terminal estándar (`proyectar`).
  * Especificaciones declarativas para renderizado de representaciones gráficas (`pizarra`).
  * Respuestas evaluadas dinámicamente en una consola interactiva en vivo (REPL).

### Restricciones Fundamentales de Diseño
1. **Principio de Inmutabilidad en Tuberías**: Toda operación encadenada mediante el operador `|>` es no destructiva. Recibe una tabla de datos inicial y genera una nueva colección derivada en memoria sin alterar el estado de la tabla original.
2. **Entorno de Cómputo Autónomo (*Zero-Dependency Core*)**: Todo el procesamiento tabular (`racoons`), las funciones estadísticas (`estadistica`), las estructuras lineales (`estructuras`), los algoritmos numéricos (`matematica`) y los modelos de Machine Learning (`ml`) operan exclusivamente en código Python puro sin librerías externas (`pandas`, `numpy`, `scikit-learn`, `scipy` o el módulo estándar `math`).
3. **Aproximaciones Numéricas Determinísticas**: Todos los cálculos trigonométricos y raíces operan bajo Series de Taylor y el método de Newton-Raphson / Babilónico con cotas de convergencia estricta.

---

## 2. Tipos de Datos y Literales

El sistema de tipos de DaZe es dinámico con verificación semántica en tiempo de ejecución. Los tipos nativos reconocidos son:

| Tipo | Identificador Semántico | Descripción | Sintaxis y Literales de Ejemplo |
| :--- | :--- | :--- | :--- |
| **Entero** | `ENTERO` | Valores numéricos enteros con signo | `10`, `0`, `-5` |
| **Decimal** | `DECIMAL` | Valores de punto flotante de precisión estándar | `3.1416`, `0.05`, `99.9` |
| **Cadena** | `CADENA` | Secuencias de texto delimitadas por comillas simples o dobles | `"plantilla.csv"`, `'Delantero'` |
| **Booleano** | `BOOLEANO` | Literales para evaluación de verdad lógica | `verdadero`, `falso`, `true`, `false` |
| **Nulo** | `NULO` | Representación formal de dato faltante o ausencia de registro | `nulo`, `null` |
| **Lista / Arreglo** | `LISTA` | Secuencia ordenada de elementos indexable y mutable por corchetes | `[10, 20, 30]`, `["A", "B"]` |
| **Matriz** | `LISTA` | Arreglo bidimensional compuesto por listas anidadas | `[[1, 0], [0, 1]]` |
| **Diccionario** | `DICCIONARIO` | Colección asociativa de pares clave-valor indexable por clave | `{"nombre": "Vinicius", "goles": 21}` |
| **Pila** | `PILA` | Estructura lineal de acceso LIFO (*Last In, First Out*) | Instanciada mediante `pila()` |
| **Cola** | `COLA` | Estructura lineal de acceso FIFO (*First In, First Out*) | Instanciada mediante `cola()` |
| **Tabla** | `TABLA` | Estructura bidimensional con esquema de columnas y tipos asociados | Obtenida por `fichar(...)` o tuberías `\|>` |

---

## 3. Operadores y Precedencia

La gramática resuelve la precedencia de operadores mediante recursión por la izquierda en la regla sintáctica `expr`, garantizando el orden matemático universal de evaluación:

### 3.1. Operadores de Acceso, Indexación y Potencia
* **Indexación y Mutación Directa**: Corchetes `[]` para consulta (`lista[i]`, `dict[clave]`) y asignación puntual (`lista[i] = nuevo_valor`, `dict[clave] = nuevo_valor`).
* **Potenciación**: `^` o `**` (asociatividad a derecha; máxima precedencia aritmética).

### 3.2. Operadores Unarios y Aritméticos
* **Operadores Unarios**: Prefijos `+`, `-`, y negación lógica `no` / `not` / `!`.
* **Multiplicativos**: Multiplicación `*`, división `/`, y módulo residual `%`.
* **Aditivos**: Suma `+` y resta `-` (la suma concatena cadenas y colecciones).

### 3.3. Operadores Relacionales y de Igualdad
* **Comparación**: Menor `<`, menor o igual `<=`, mayor `>`, mayor o igual `>=`.
* **Igualdad Estricta**: Igualdad `==` y diferencia `!=`.

### 3.4. Operadores Lógicos y de Tubería
* **Conjunción Lógica**: `y`, `and`, `&&`.
* **Disyunción Lógica**: `o`, `or`, `||`.
* **Operador de Tubería (*Pipeline*)**: `|>` (conecta secuencialmente la salida de un nodo con la entrada del siguiente).

---

## 4. Catálogo de Instrucciones y Palabras Reservadas

### 4.1. Carga, Exportación y Proyección
* **`fichar(ruta, ...)`**: Carga una plantilla de datos desde el disco. Admite argumentos nombrados opcionales (`separador`, `encabezado`).
  ```daze
  datos = fichar("datos/plantilla_temporada.csv", separador=",", encabezado=verdadero);
  ```
* **`archivar(tabla, en=ruta, ...)`**: Exporta una estructura tabular a un archivo físico CSV en disco, creando automáticamente los directorios necesarios.
  ```daze
  archivar(resumen, en="salidas/resumen_posiciones.csv", separador=",");
  ```
* **`proyectar(expr)`**: Imprime en consola cualquier literal, tabla con alineación ASCII, arreglo, diccionario o valor evaluado.
  ```daze
  proyectar("Resultado del analisis:");
  proyectar(titulares);
  ```

### 4.2. Operaciones de Tubería o Pipeline (`|>`)
Las transformaciones tabulares se componen encadenando operaciones mediante `|>`:
* **`convocar(...)`**: Proyecta únicamente las columnas indicadas en el orden especificado.
* **`descartar(...)`**: Filtra filas mediante una expresión booleana o la cláusula `donde`.
* **`contratar(...)`**: Deriva o agrega nuevas columnas calculadas a partir de expresiones.
* **`rebautizar(...)`**: Renombra atributos existentes mediante pares de asignación.
* **`clasificar(...)`**: Ordena filas de acuerdo con una o más columnas (`descendente=verdadero` o `ascendente=verdadero`).
* **`alinear(...)`**: Particiona la tabla en grupos tácticos aislados (*GroupBy*).
* **`balance(...)`**: Aplica funciones de resumen descriptivo (`suma`, `media`, `mediana`, `minimo`, `maximo`, `desv_std`, `contar`) sobre grupos o sobre la tabla completa.
* **`sanear(...)`** (o `reemplazar_bajas`): Imputa valores nulos o faltantes en columnas específicas.
* **`depurar(...)`** (o `depurar_plantilla`): Deduplica registros repetidos en la plantilla.
* **`top(n)`**: Conserva únicamente los primeros $n$ registros destacados.

### 4.3. Estructuras de Control, Bucles Temáticos y Modularidad
* **`en_juego (condicion) { ... }`**: Bucle condicional temático (*while*) para simulaciones continuas o decrementos iterativos.
  ```daze
  minutos_restantes = 5;
  en_juego (minutos_restantes > 0) {
      proyectar(minutos_restantes);
      minutos_restantes = minutos_restantes - 1;
  }
  ```
* **`ronda (iterador en coleccion) { ... }`**: Bucle temático de recorrido (*for-in*) sobre arreglos, listas o filas de una tabla.
  ```daze
  goles_temporada = [2, 1, 3, 0];
  ronda (g en goles_temporada) {
      proyectar(g);
  }
  ```
* **`si (condicion) { ... } sino { ... }`**: Bifurcación condicional evaluada en tiempo de ejecución.
* **`tactica nombre(p1, p2, ...) { ... }`**: Declara un bloque funcional reutilizable con ámbito local aislado.
* **`resultado expr;`**: Emite el valor de retorno de una táctica hacia el llamador.

### 4.4. Estructuras de Datos Lineales Nativas
* **Pila (`Pila` - LIFO)**:
  * `pila()`: Inicializa una nueva instancia de pila vacía.
  * `apilar(p, elemento)`: Inserta un elemento en el tope de la estructura.
  * `desapilar(p)`: Remueve y extrae el elemento superior.
  * `tope(p)`: Inspecciona el elemento superior sin extraerlo.
* **Cola (`Cola` - FIFO)**:
  * `cola()`: Inicializa una nueva instancia de cola vacía.
  * `encolar(c, elemento)`: Encola un elemento al final de la fila.
  * `desencolar(c)`: Desencola y extrae el elemento del frente.
  * `frente(c)`: Inspecciona el primer elemento en turno sin removerlo.
* **Operación Compartida**:
  * `longitud(coleccion)`: Retorna la cardinalidad de arreglos, diccionarios, pilas y colas.

### 4.5. Motor Matemático Puro (Algoritmos Nativos)
Cálculos implementados desde cero sin recurrir a la librería estándar `math`:
* **`raiz(x)`** / **`sqrt(x)`**: Raíz cuadrada por aproximación iterativa de Newton-Raphson / Método Babilónico:
  $$x_{k+1} = \frac{1}{2} \left( x_k + \frac{n}{x_k} \right)$$
* **`seno(x)`**: Aproximación trigonométrica de precisión por Series de Taylor con reducción modular a $[-\pi, \pi]$:
  $$\sin(x) = \sum_{k=0}^{12} \frac{(-1)^k}{(2k+1)!} x^{2k+1}$$
* **`coseno(x)`**: Evaluación trigonométrica por Series de Taylor:
  $$\cos(x) = \sum_{k=0}^{12} \frac{(-1)^k}{(2k)!} x^{2k}$$
* **`tangente(x)`**: Razón analítica $\frac{\sin(x)}{\cos(x)}$ con control de división por cero.
* **`potencia(base, exp)`**: Exponenciación pura compatible con exponentes enteros positivos y negativos.
* **`abs(x)`**: Magnitud escalar absoluta.

### 4.6. Declaración de Pizarras Visuales
* **`pizarra tipo(tabla) { config }`**: Especifica formalmente representaciones gráficas (`barras`, `lineas`, `histograma`, `dispersion`, `caja`), validando tipos de datos, columnas y rutas de salida antes del renderizado.
  ```daze
  pizarra barras(resumen_posiciones) {
      eje_x = posicion;
      eje_y = goles_totales;
      titulo = "Goles por Posicion";
      color = "azul";
      guardar = "salidas/goles_posicion.png";
  }
  ```

### 4.7. Machine Learning y Métodos Numéricos Avanzados
Funciones nativas integradas al intérprete implementadas desde cero sin `scikit-learn` ni `numpy`:
* **`correlacion(x, y)`**: Coeficiente de correlación lineal de Pearson ($r \in [-1.0, 1.0]$) entre dos variables físicas continuas:
  $$r = \frac{\sum_{i=1}^N (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^N (x_i - \bar{x})^2} \cdot \sqrt{\sum_{i=1}^N (y_i - \bar{y})^2}}$$
* **`regresion_lineal(x, y)`**: Ajuste de un modelo de regresión lineal simple ($y = mx + b$) mediante **Mínimos Cuadrados Ordinarios (MCO)**:
  $$m = \frac{\sum_{i=1}^N (x_i - \bar{x})(y_i - \bar{y})}{\sum_{i=1}^N (x_i - \bar{x})^2}, \quad b = \bar{y} - m\bar{x}$$
  Retorna un diccionario asociativo con los siguientes campos:
  * `"m"`: Pendiente calculada de la recta.
  * `"b"`: Intercepto con el eje $Y$.
  * `"r2"`: Coeficiente de determinación ($R^2 = 1 - \frac{\text{SS}_{\text{res}}}{\text{SS}_{\text{tot}}}$).
* **`predecir_regresion(modelo, valor)`** / **`predecir(modelo, valor)`**: Inferencia analítica para calcular $\hat{y} = mx + b$ sobre un escalar o una lista de valores futuros.
* **`agrupar_kmedias(datos, k)`**: Algoritmo de agrupamiento no supervisado (*K-Means*) en espacios multidimensionales basado en **Distancia Euclidiana** pura:
  $$d(p, q) = \sqrt{\sum_{j=1}^D (p_j - q_j)^2}$$
  Retorna un diccionario asociativo con:
  * `"centroides"`: Lista con las coordenadas multidimensionales de cada centroide convergido.
  * `"etiquetas"`: Lista de asignación de cluster ($0, 1, \dots, k-1$) para cada muestra de entrada.

### 4.8. Interfaz de Ejecución y Consola Interactiva (REPL)
DaZe provee dos modos de interacción a través del comando `./daze` o `src/cli.py`:
1. **Modo Interactivo (REPL - *Read-Eval-Print Loop*)**:
   Al invocar `./daze` sin argumentos, se inicializa un shell interactivo con prompt `daze> `. Mantiene una única `TablaSimbolos` persistente en memoria entre instrucciones sucesivas y detecta llaves abiertas para habilitar edición multilínea (`...   `).
   * **`simbolos`**: Lista todas las variables, tablas y estructuras activas en el entorno.
   * **`limpiar`** / **`clear`**: Limpia la pantalla de la terminal.
   * **`ayuda`** / **`help`**: Despliega la referencia rápida de sintaxis y comandos.
   * **`salir`** / **`exit`**: Cierra la sesión interactiva.
2. **Modo por Lotes (Batch)**:
   Ejecuta programas completos pasándole el archivo como parámetro: `python3 src/cli.py script.dz`.

---

## 5. Ejemplos de Integración Completa

### 5.1. Manejo de Estructuras de Datos Lineales y Bucles
```daze
# Uso de Pilas y Colas nativas
estrategias = pila();
apilar(estrategias, "Bloque Bajo");
apilar(estrategias, "Presion Alta");

estrategia_activa = tope(estrategias);
proyectar("Estrategia activa en el tope:");
proyectar(estrategia_activa);

# Modificacion y recorrido de arreglos
notas_rendimiento = [80, 85, 90];
notas_rendimiento[0] = 95;

ronda (n en notas_rendimiento) {
    proyectar(n);
}
```

### 5.2. Pipeline Tabular y Cálculo Matemático Puro
```daze
plantilla = fichar("datos/plantilla_temporada.csv", separador=",", encabezado=verdadero);

titulares = plantilla
    |> convocar(nombre, minutos, goles, asistencias)
    |> descartar(minutos > 0)
    |> contratar(
        contribucion = goles + asistencias,
        desviacion_estimada = raiz(contribucion)
    )
    |> clasificar(por=[contribucion], descendente=verdadero)
    |> top(5);

proyectar("Top 5 jugadores por contribucion:");
proyectar(titulares);
```

### 5.3. Modelos Predictivos y Agrupamiento con Machine Learning
```daze
# 1. Evaluacion de asociacion lineal
minutos_jugados = [120, 340, 500, 750, 900, 1100, 1300];
goles_marcados  = [1, 3, 4, 7, 8, 11, 14];

r = correlacion(minutos_jugados, goles_marcados);
proyectar("Coeficiente de correlacion de Pearson:");
proyectar(r);

# 2. Ajuste de regresion lineal (MCO) y prediccion
modelo = regresion_lineal(minutos_jugados, goles_marcados);
proyectar("Pendiente:");
proyectar(modelo["m"]);
proyectar("Intercepto:");
proyectar(modelo["b"]);
proyectar("Bondad de ajuste R^2:");
proyectar(modelo["r2"]);

goles_esperados = predecir_regresion(modelo, 950);
proyectar("Goles esperados para 950 minutos:");
proyectar(goles_esperados);

# 3. Agrupamiento no supervisado K-Means (k=2)
# Muestra de perfiles de jugadores en 2D: [minutos, goles]
vectores_atletas = [
    [100, 1],   [150, 0],   [200, 1],    # Perfil 0: Suplentes / Pocos minutos
    [1100, 12], [1200, 15], [1300, 14]   # Perfil 1: Titulares goleadores
];

clusters = agrupar_kmedias(vectores_atletas, 2);
proyectar("Centroides convergidos:");
proyectar(clusters["centroides"]);
proyectar("Etiquetas asignadas por cluster:");
proyectar(clusters["etiquetas"]);
```
