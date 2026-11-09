"""
Módulo de Machine Learning y Métodos Numéricos Puros para DaZe.
Implementado sin dependencias externas (sin numpy, scipy ni scikit-learn).
"""

def _raiz(n, tolerancia=1e-12):
    """Raíz cuadrada por algoritmo iterativo de Newton-Raphson."""
    if n < 0:
        raise ValueError("No se puede calcular raíz de número negativo")
    if n == 0:
        return 0.0
    x = n / 2.0 if n >= 1 else 1.0
    for _ in range(100):
        sig = 0.5 * (x + n / x)
        if abs(x - sig) < tolerancia:
            return sig
        x = sig
    return x


def correlacion_pearson(x, y):
    """Calcula el coeficiente de correlación r de Pearson en [-1.0, 1.0]."""
    if len(x) != len(y) or len(x) < 2:
        return 0.0
    n = len(x)
    media_x = sum(x) / n
    media_y = sum(y) / n

    num = sum((xi - media_x) * (yi - media_y) for xi, yi in zip(x, y))
    den_x = sum((xi - media_x) ** 2 for xi in x)
    den_y = sum((yi - media_y) ** 2 for yi in y)

    denominador = _raiz(den_x * den_y)
    if denominador == 0:
        return 0.0
    return num / denominador

# Alias de correlación
correlacion = correlacion_pearson


class RegresionLineal:
    """Modelo de regresión lineal simple (y = mx + b) por MCO."""
    def __init__(self):
        self.m = 0.0
        self.b = 0.0
        self.r2 = 0.0

    def __getitem__(self, clave):
        if hasattr(self, clave):
            return getattr(self, clave)
        raise KeyError(clave)

    def ajustar(self, x, y):
        n = len(x)
        if n < 2 or n != len(y):
            raise ValueError("Se requieren al menos 2 pares de datos para ajustar regresión.")

        media_x = sum(x) / n
        media_y = sum(y) / n

        num = sum((xi - media_x) * (yi - media_y) for xi, yi in zip(x, y))
        den = sum((xi - media_x) ** 2 for xi in x)

        self.m = (num / den) if den != 0 else 0.0
        self.b = media_y - (self.m * media_x)

        ss_tot = sum((yi - media_y) ** 2 for yi in y)
        ss_res = sum((yi - (self.m * xi + self.b)) ** 2 for xi, yi in zip(x, y))
        if ss_tot == 0:
            self.r2 = 1.0 if ss_res == 0 else 0.0
        else:
            self.r2 = max(0.0, min(1.0, 1.0 - (ss_res / ss_tot)))

        return self

    def predecir(self, x_val):
        return self.m * x_val + self.b


def regresion_lineal(x, y):
    """Ajusta una regresión lineal simple y retorna métricas en un diccionario."""
    modelo = RegresionLineal()
    modelo.ajustar(x, y)
    return {
        "m": modelo.m,
        "b": modelo.b,
        "r2": modelo.r2,
        "modelo": modelo
    }


def predecir_regresion(modelo, x_val):
    """Estima el valor de y para un x_val dado a partir de un modelo de regresión."""
    if isinstance(modelo, dict):
        if "m" in modelo and "b" in modelo:
            return modelo["m"] * x_val + modelo["b"]
        elif "modelo" in modelo:
            return modelo["modelo"].predecir(x_val)
    elif hasattr(modelo, "predecir"):
        return modelo.predecir(x_val)
    raise ValueError("Objeto de modelo no válido para inferencia")


class KMeans:
    """Algoritmo de clustering no supervisado en D dimensiones."""
    def __init__(self, k=2, max_iter=20):
        self.k = k
        self.max_iter = max_iter
        self.centroides = []
        self.etiquetas = []

    def __getitem__(self, clave):
        if hasattr(self, clave):
            return getattr(self, clave)
        raise KeyError(clave)

    def _distancia_euclidiana(self, p1, p2):
        return _raiz(sum((a - b) ** 2 for a, b in zip(p1, p2)))

    def ajustar(self, datos):
        if not datos or self.k <= 0:
            return self

        k = min(self.k, len(datos))
        self.centroides = [list(datos[i]) for i in range(k)]
        self.etiquetas = [0] * len(datos)
        dim = len(datos[0])

        for _ in range(self.max_iter):
            nuevas_etiquetas = []
            for punto in datos:
                distancias = [self._distancia_euclidiana(punto, c) for c in self.centroides]
                min_idx = distancias.index(min(distancias))
                nuevas_etiquetas.append(min_idx)

            clusters = {i: [] for i in range(k)}
            for idx, c_idx in enumerate(nuevas_etiquetas):
                clusters[c_idx].append(datos[idx])

            nuevos_centroides = []
            for i in range(k):
                if clusters[i]:
                    n_puntos = len(clusters[i])
                    nuevo_c = [sum(p[d] for p in clusters[i]) / n_puntos for d in range(dim)]
                else:
                    nuevo_c = self.centroides[i]
                nuevos_centroides.append(nuevo_c)

            self.centroides = nuevos_centroides
            if nuevas_etiquetas == self.etiquetas:
                break
            self.etiquetas = nuevas_etiquetas

        return self


def agrupar_kmedias(datos, k=2, max_iter=20):
    """Ejecuta agrupamiento K-Means y retorna centroides y etiquetas."""
    km = KMeans(k=k, max_iter=max_iter)
    km.ajustar(datos)
    return {
        "centroides": km.centroides,
        "etiquetas": km.etiquetas,
        "modelo": km
    }
