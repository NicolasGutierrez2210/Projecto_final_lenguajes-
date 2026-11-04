"""
Modulo de calculos estadisticos descriptivos para DaZe.
Implementacion pura sin dependencias de la libreria math.
"""
from typing import Iterable, List, Any, Union
from .matematica import raiz_cuadrada


def _es_nan(val: Any) -> bool:
    return isinstance(val, float) and (val != val)


def _limpiar_numeros(valores: Iterable[Any]) -> List[Union[int, float]]:
    limpios: List[Union[int, float]] = []
    for val in valores:
        if val is None or val == "":
            continue
        if isinstance(val, (int, float)):
            if not _es_nan(val):
                limpios.append(val)
        elif isinstance(val, str):
            val_strip = val.strip()
            if not val_strip:
                continue
            try:
                if "." in val_strip:
                    limpios.append(float(val_strip))
                else:
                    limpios.append(int(val_strip))
            except ValueError:
                pass
    return limpios


def suma(valores: Iterable[Any]) -> Union[int, float]:
    nums = _limpiar_numeros(valores)
    if not nums:
        return 0
    total = sum(nums)
    if isinstance(total, float):
        return round(total, 4)
    return total


def contar(valores: Iterable[Any] = None) -> int:
    if valores is None:
        return 0
    count = 0
    for val in valores:
        if val is not None and val != "":
            if _es_nan(val):
                continue
            count += 1
    return count


def media(valores: Iterable[Any]) -> float:
    nums = _limpiar_numeros(valores)
    if not nums:
        return 0.0
    return round(sum(nums) / len(nums), 4)


def mediana(valores: Iterable[Any]) -> Union[int, float]:
    nums = _limpiar_numeros(valores)
    if not nums:
        return 0.0
    nums.sort()
    n = len(nums)
    mitad = n // 2
    if n % 2 == 1:
        return nums[mitad]
    else:
        prom = (nums[mitad - 1] + nums[mitad]) / 2.0
        return round(prom, 4)


def minimo(valores: Iterable[Any]) -> Union[int, float]:
    nums = _limpiar_numeros(valores)
    if not nums:
        return 0.0
    return min(nums)


def maximo(valores: Iterable[Any]) -> Union[int, float]:
    nums = _limpiar_numeros(valores)
    if not nums:
        return 0.0
    return max(nums)


def desviar(valores: Iterable[Any], muestral: bool = True) -> float:
    nums = _limpiar_numeros(valores)
    n = len(nums)
    if n <= 1:
        return 0.0
    prom = sum(nums) / n
    varianza_suma = sum((x - prom) ** 2 for x in nums)
    divisor = (n - 1) if (muestral and n > 1) else n
    return round(raiz_cuadrada(varianza_suma / divisor), 4)
