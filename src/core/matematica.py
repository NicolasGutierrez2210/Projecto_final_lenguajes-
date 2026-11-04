"""
Modulo matematico de DaZe (Corte 3).
Implementacion desde cero sin dependencias de la libreria math.
"""

PI = 3.141592653589793

def valor_absoluto(n):
    return -n if n < 0 else n

def factorial(n):
    if n < 0:
        raise ValueError("No existe factorial de un numero negativo.")
    res = 1
    for i in range(2, int(n) + 1):
        res *= i
    return res

def potencia(base, exp):
    if exp == 0:
        return 1.0
    res = 1.0
    exp_pos = int(valor_absoluto(exp))
    for _ in range(exp_pos):
        res *= base
    return (1.0 / res) if exp < 0 else res

def normalizar_angulo(radianes):
    dos_pi = 2.0 * PI
    while radianes > PI:
        radianes -= dos_pi
    while radianes < -PI:
        radianes += dos_pi
    return radianes

def raiz_cuadrada(n, tolerancia=1e-7, max_iter=1000):
    """Metodo de Newton-Raphson / Babilonico."""
    if n < 0:
        raise ValueError("Error matematico: no existe raiz real de numero negativo.")
    if n == 0 or n == 1:
        return float(n)
    x = n / 2.0
    for _ in range(max_iter):
        siguiente = 0.5 * (x + (n / x))
        if valor_absoluto(siguiente - x) < tolerancia:
            return round(siguiente, 6)
        x = siguiente
    return round(x, 6)

def seno(x, terminos=12):
    x_norm = normalizar_angulo(x)
    res = 0.0
    for n in range(terminos):
        signo = -1 if (n % 2 == 1) else 1
        exp = (2 * n) + 1
        res += signo * (potencia(x_norm, exp) / factorial(exp))
    return round(res, 6)

def coseno(x, terminos=12):
    x_norm = normalizar_angulo(x)
    res = 0.0
    for n in range(terminos):
        signo = -1 if (n % 2 == 1) else 1
        exp = 2 * n
        res += signo * (potencia(x_norm, exp) / factorial(exp))
    return round(res, 6)

def tangente(x):
    cos_val = coseno(x)
    if valor_absoluto(cos_val) < 1e-6:
        raise ZeroDivisionError("Tangente indefinida (coseno cercano a cero).")
    return round(seno(x) / cos_val, 6)

def maximo_coleccion(lista):
    if not lista:
        raise ValueError("Lista vacia.")
    m = lista[0]
    for x in lista[1:]:
        if x > m:
            m = x
    return m

def minimo_coleccion(lista):
    if not lista:
        raise ValueError("Lista vacia.")
    m = lista[0]
    for x in lista[1:]:
        if x < m:
            m = x
    return m

def promedio_coleccion(lista):
    if not lista:
        raise ValueError("Lista vacia.")
    suma = 0.0
    for x in lista:
        suma += x
    return round(suma / len(lista), 4)
