# Especificación del Lenguaje DaZe (.dz) - Sports Analytics DSL

## 1. Delimitación del Dominio y Casos de Uso

DaZe es un lenguaje de dominio específico (DSL) diseñado para modelar flujos de trabajo reproducibles en analítica deportiva, simulación táctica, preparación de plantillas de atletas y especificación declarativa de pizarras visuales. El lenguaje combina una sintaxis funcional/declarativa basada en tuberías o *pipelines* (`|>`) con estructuras imperativas temáticas (`en_juego`, `ronda`), estructuras de datos lineales nativas en memoria y un motor numérico implementado desde cero sin dependencias de librerías externas.

### Perfil de Usuarios
- Analistas de rendimiento deportivo, preparadores físicos, directores técnicos y cuerpos técnicos multidisciplinarios.
- Desarrolladores e investigadores que procesan telemetría GPS, métricas biomecánicas, estadísticas de partidos y modelos determinísticos de manera compacta, reproducible y legible.

### Entradas y Salidas
- **Entradas**: Archivos tabulares en formato CSV con métricas de rendimiento deportivo (configuración de delimitadores y presencia de encabezados), literales escalares, colecciones indexables y estructuras lineales en memoria.
- **Salidas**: Tablas transformadas y consolidadas exportables a CSV, proyecciones en consola mediante `proyectar`, especificaciones declarativas de representaciones gráficas para pizarras tácticas y estructuras de datos procesadas.

### Restricciones de Diseño
- Toda transformación dentro de una tubería (`|>`) respeta el principio de inmutabilidad tabular: recibe una plantilla de datos y deriva una nueva transformación sin alterar destructivamente los estados anteriores.
- Todos los cálculos trigonométricos y numéricos operan exclusivamente sobre algoritmos nativos (Series de Taylor y método iterativo de Newton-Raphson / Babilónico), garantizando independencia de la biblioteca estándar `math`.

---

## 2. Tipos de Datos y Literales

| Tipo | Descripción | Sintaxis / Ejemplos |
|---|---|---|
| Entero | Valores numéricos enteros de precisión estándar | `10`, `0`, `-5` |
| Decimal | Valores numéricos en punto flotante | `3.1416`, `0.05`, `99.9` |
| Cadena | Texto delimitado por comillas simples o dobles | `"plantilla.csv"`, `'Delantero'` |
| Booleano | Literales de lógica booleana | `verdadero`, `falso`, `true`, `false` |
| Nulo | Representación formal de dato faltante o ausencia de registro | `nulo`, `null` |
| Lista / Arreglo | Secuencia ordenada de elementos indexable y mutable por `[]` | `[10, 20, 30]`, `["A", "B"]` |
| Diccionario | Colección asociativa de pares clave-valor indexable por clave | `{"nombre": "Kylian", "goles": 24}` |
| Pila | Estructura lineal LIFO (*Last In, First Out*) | `pila()` |
| Cola | Estructura lineal FIFO (*First In, First Out*) | `cola()` |
| Tabla | Colección tabular estructurada cargada o derivada de un *pipeline* | Resultado de `fichar(...)` o `\|>` |

---

## 3. Operadores y Precedencia

### 3.1. Operadores de Acceso, Indexación y Potencia
- **Indexación y Mutación**: Corchetes `[]` para consulta (`lista[i]`, `dict[clave]`) y asignación destructiva puntual (`lista[i] = nuevo_valor`, `dict[clave] = nuevo_valor`).
- **Potencia**: `^` o `**` (asociatividad a derecha).

### 3.2. Operadores Unarios y Aritméticos
- **Unarios**: Prefijos `+`, `-`, y negación lógica `no` / `not` / `!`.
- **Multiplicativos**: Multiplicación `*`, división `/`, módulo `%`.
- **Aditivos**: Suma `+`, resta `-` (el operador `+` concatena cadenas y colecciones homogéneas).

### 3.3. Operadores Relacionales y de Igualdad
- **Comparación**: Menor `<`, menor o igual `<=`, mayor `>`, mayor o igual `>=`.
- **Igualdad**: Igualdad estricta `==`, diferencia `!=`.

### 3.4. Operadores Lógicos
- **Conjunción**: `y`, `and`, `&&`.
- **Disyunción**: `o`, `or`, `||`.

---

## 4. Catálogo de Instrucciones y Palabras Reservadas

### 4.1. Carga, Exportación y Salida
- **`fichar(ruta, ...)`**: Carga una plantilla de datos desde el disco. Admite parámetros opcionales con nombre (`separador`, `encabezado`).
  ```daze
  datos = fichar("datos/plantilla_temporada.csv", separador=",", encabezado=verdadero);
  ```
- **`archivar(tabla, en=ruta, ...)`**: Exporta una estructura tabular a un archivo CSV en disco.
  ```daze
  archivar(resumen, en="salidas/resumen_posiciones.csv", separador=",");
  ```
- **`proyectar(expr)`**: Imprime literales, tablas formateadas, estructuras de datos o expresiones en consola.
  ```daze
  proyectar("Resultado del analisis:");
  proyectar(titulares);
  ```

### 4.2. Operaciones de Pipeline (`|>`)
Las transformaciones se componen secuencialmente conectando una tabla mediante el operador de tubería `|>`:
- **`convocar(...)`**: Selecciona y proyecta un subconjunto de columnas relevantes de la plantilla.
- **`descartar(...)`**: Filtra filas mediante expresiones lógicas o la cláusula `donde`.
- **`contratar(...)`**: Incorpora nuevas métricas o columnas calculadas a la plantilla.
- **`rebautizar(...)`**: Renombra columnas existentes mediante pares de asignación.
- **`clasificar(...)`**: Ordena registros según columnas (`descendente=verdadero` o `ascendente=verdadero`).
- **`alinear(...)`**: Agrupa registros por una o varias columnas clave (*Group By*).
- **`balance(...)`**: Aplica funciones de agregación (`suma`, `media`, `mediana`, `minimo`, `maximo`, `desv_std`, `contar`) sobre grupos o tablas globales.
- **`sanear(...)`** (o `reemplazar_bajas`): Imputa valores nulos o faltantes en columnas específicas.
- **`depurar(...)`** (o `depurar_plantilla`): Deduplica registros basados en un conjunto de atributos.
- **`top(n)`**: Conserva únicamente los primeros $n$ registros de la plantilla.
- **Operaciones personalizadas**: Ejecución de tácticas creadas por el usuario dentro del pipeline.

### 4.3. Estructuras de Control, Ciclos y Subrutinas
- **`en_juego (condicion) { ... }`**: Bucle condicional temático (*while*) para simulaciones y algoritmos iterativos.
  ```daze
  contador = 1;
  en_juego (contador <= 5) {
      proyectar(contador);
      contador = contador + 1;
  }
  ```
- **`ronda (iterador en coleccion) { ... }`**: Bucle temático de recorrido (*for-in*) sobre arreglos, llaves de diccionarios o filas tabulares.
  ```daze
  tiempos = [10, 20, 30];
  ronda (t en tiempos) {
      proyectar(t);
  }
  ```
- **`si (condicion) { ... } sino { ... }`**: Estructura de bifurcación condicional.
- **`tactica nombre(params) { ... }`**: Declara un bloque funcional reutilizable con ámbito local.
- **`resultado expr;`**: Emite el valor de retorno de una táctica.

### 4.4. Estructuras de Datos Lineales Nativas
- **Pila (LIFO)**:
  - `pila()`: Inicializa una nueva instancia de pila vacía.
  - `apilar(p, elemento)`: Inserta un elemento en el tope de la pila.
  - `desapilar(p)`: Remueve y extrae el elemento en el tope.
  - `tope(p)`: Consulta el elemento en la cima sin extraerlo.
- **Cola (FIFO)**:
  - `cola()`: Inicializa una nueva instancia de cola vacía.
  - `encolar(c, elemento)`: Encola un elemento al final.
  - `desencolar(c)`: Desencola y extrae el elemento al frente.
  - `frente(c)`: Consulta el primer elemento sin extraerlo.
- **Operaciones compartidas**:
  - `longitud(coleccion)`: Retorna la cantidad de elementos presentes en una lista, pila o cola.

### 4.5. Motor Matemático Puro (Algoritmos Nativos)
Funciones integradas que operan sin recurrir al módulo `math`:
- **`raiz(x)`** / **`sqrt(x)`**: Raíz cuadrada calculada por el método iterativo de Newton-Raphson / Babilónico:
  $$x_{k+1} = \frac{1}{2}\left(x_k + \frac{n}{x_k}\right)$$
- **`seno(x)`**: Evaluación trigonométrica mediante aproximación por Series de Taylor con normalización modular a $[-\pi, \pi]$:
  $$\sin(x) = \sum_{n=0}^{k} \frac{(-1)^n}{(2n+1)!} x^{2n+1}$$
- **`coseno(x)`**: Evaluación trigonométrica mediante Series de Taylor:
  $$\cos(x) = \sum_{n=0}^{k} \frac{(-1)^n}{(2n)!} x^{2n}$$
- **`tangente(x)`**: Razón entre seno y coseno con control de división por cero e indeterminaciones.
- **`potencia(base, exp)`**: Cálculo de exponenciación pura con soporte para exponentes enteros positivos y negativos.
- **`abs(x)`**: Valor absoluto de un escalar.
- **`promedio(lista)`**: Media aritmética calculada sobre una colección iterable.
- **`minimo(lista)`** / **`maximo(lista)`**: Extremos numéricos de una colección.

### 4.6. Declaración de Pizarras Visuales
- **`pizarra tipo(tabla) { config }`**: Especifica formalmente representaciones gráficas (`barras`, `lineas`, `histograma`, `dispersion`, `caja`), validando tipos, ejes y configuraciones asociadas antes del renderizado.

---

## 5. Ejemplos de Integración Completa

### 5.1. Análisis y Mutación de Estructuras
```daze
# Inicializacion y uso de estructuras de datos
tacticas_activas = pila();
apilar(tacticas_activas, "Bloque Bajo");
apilar(tacticas_activas, "Presion Alta");

estrategia_actual = tope(tacticas_activas);
proyectar("Estrategia activa en el tope:");
proyectar(estrategia_actual);

fila_rendimiento = [80, 85, 90];
fila_rendimiento[0] = 95;

ronda (nota en fila_rendimiento) {
    proyectar(nota);
}
```

### 5.2. Pipeline y Cálculo Numérico
```daze
# Carga y transformacion de plantilla con algoritmos puros
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
