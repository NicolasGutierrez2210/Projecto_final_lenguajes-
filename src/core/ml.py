"""
Modulo de Machine Learning y Metodos Numericos Puros para DaZe.
Implementado desde cero sin dependencias externas (sin scikit-learn ni numpy).
"""

def raiz_babilonica(x, iteraciones=15):
    """Calculo de raiz cuadrada pura por Newton-Raphson."""
    if x < 0:
        return float('nan')
    if x == 0:
        return 0.0
    estimacion = x / 2.0 if x > 1.0 else 1.0
    for _ in range(iteraciones):
        estimacion = 0.5 * (estimacion + x / estimacion)
    return estimacion


def distancia_euclidiana(p1, p2):
    """Calcula la distancia euclidiana D-dimensional entre dos puntos."""
    if len(p1) != len(p2):
        raise ValueError("Los vectores deben tener la misma dimension.")
    suma_cuadrados = sum((float(a) - float(b)) ** 2 for a, b in zip(p1, p2))
    return raiz_babilonica(suma_cuadrados)


def correlacion_pearson(x, y):
    """
    Coeficiente de correlacion de Pearson (r).
    Retorna un valor entre -1.0 y 1.0 cuantificando la relacion lineal.
    """
    n = len(x)
    if n != len(y) or n < 2:
        return 0.0

    media_x = sum(x) / n
    media_y = sum(y) / n

    numerador = sum((xi - media_x) * (yi - media_y) for xi, yi in zip(x, y))
    denom_x = sum((xi - media_x) ** 2 for xi in x)
    denom_y = sum((yi - media_y) ** 2 for yi in y)

    denominador = raiz_babilonica(denom_x * denom_y)
    if denominador == 0.0:
        return 0.0

    return numerador / denominador


class RegresionLineal:
    """
    Modelo de Regresion Lineal Simple (y = m*x + b).
    Calculado por Minimos Cuadrados Ordinarios y optimizable por Descenso de Gradiente.
    """
    def __init__(self):
        self.m = 0.0  # Pendiente
        self.b = 0.0  # Intercepto
        self.r2 = 0.0 # Coeficiente de determinacion R^2
        self.entrenado = False

    def ajustar(self, x, y):
        """Ajuste analitico por Minimos Cuadrados (formula cerrada)."""
        n = len(x)
        if n != len(y) or n < 2:
            raise ValueError("Se requieren al menos dos observaciones validas.")

        media_x = sum(x) / n
        media_y = sum(y) / n

        numerador = sum((xi - media_x) * (yi - media_y) for xi, yi in zip(x, y))
        denominador = sum((xi - media_x) ** 2 for xi in x)

        if denominador == 0.0:
            raise ZeroDivisionError("Varianza de X es cero; no se puede ajustar la recta.")

        self.m = numerador / denominador
        self.b = media_y - (self.m * media_x)

        # Calculo de R^2
        ss_tot = sum((yi - media_y) ** 2 for yi in y)
        ss_res = sum((yi - self.predecir(xi)) ** 2 for xi, yi in zip(x, y))
        self.r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 1.0
        self.entrenado = True
        return self

    def ajustar_gradiente(self, x, y, lr=0.0001, epocas=1000):
        """Ajuste numerico mediante Descenso de Gradiente."""
        n = len(x)
        self.m = 0.0
        self.b = 0.0
        for _ in range(epocas):
            grad_m = 0.0
            grad_b = 0.0
            for xi, yi in zip(x, y):
                error = (self.m * xi + self.b) - yi
                grad_m += error * xi
                grad_b += error
            self.m -= (2.0 / n) * grad_m * lr
            self.b -= (2.0 / n) * grad_b * lr
        self.entrenado = True
        return self

    def predecir(self, x_val):
        """Estima el valor de y para una entrada o lista de entradas."""
        if isinstance(x_val, list):
            return [round(self.m * xi + self.b, 4) for xi in x_val]
        return round(self.m * x_val + self.b, 4)


class KMeans:
    """
    Algoritmo de Agrupamiento K-Means (K-Medias) desde cero.
    Segmenta datos multidimensionales sin etiquetas usando distancia euclidiana.
    """
    def __init__(self, k=2, max_iter=100):
        self.k = k
        self.max_iter = max_iter
        self.centroides = []
        self.etiquetas = []

    def ajustar(self, datos):
        """
        datos: Lista de puntos, donde cada punto es [x1, x2, ...] o un escalar.
        """
        if not datos:
            return self

        # Normalizar entradas si son escalares a listas [x]
        matriz = [p if isinstance(p, list) else [float(p)] for p in datos]
        n_muestras = len(matriz)
        dim = len(matriz[0])

        if self.k > n_muestras:
            raise ValueError("K no puede ser mayor a la cantidad de datos.")

        # Inicializacion determinista de centroides dispersos
        paso = max(1, n_muestras // self.k)
        self.centroides = [list(matriz[min(i * paso, n_muestras - 1)]) for i in range(self.k)]

        for _ in range(self.max_iter):
            # 1. Asignacion de clusters
            nuevas_etiquetas = []
            for punto in matriz:
                distancias = [distancia_euclidiana(punto, c) for c in self.centroides]
                cluster_cercano = distancias.index(min(distancias))
                nuevas_etiquetas.append(cluster_cercano)

            # 2. Recalculo de centroides (promedio por coordenada)
            nuevos_centroides = []
            for j in range(self.k):
                puntos_cluster = [matriz[idx] for idx, etiqueta in enumerate(nuevas_etiquetas) if etiqueta == j]
                if puntos_cluster:
                    centroide_promedio = [
                        sum(p[d] for p in puntos_cluster) / len(puntos_cluster)
                        for d in range(dim)
                    ]
                else:
                    centroide_promedio = self.centroides[j]
                nuevos_centroides.append(centroide_promedio)

            # Comprobar convergencia
            diferencia = sum(
                distancia_euclidiana(c_ant, c_nuev)
                for c_ant, c_nuev in zip(self.centroides, nuevos_centroides)
            )
            self.centroides = nuevos_centroides
            self.etiquetas = nuevas_etiquetas

            if diferencia < 1e-4:
                break

        return self

    def predecir(self, punto):
        """Asigna un nuevo punto al cluster mas cercano."""
        p = punto if isinstance(punto, list) else [float(punto)]
        distancias = [distancia_euclidiana(p, c) for c in self.centroides]
        return distancias.index(min(distancias))
