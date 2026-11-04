"""
Estructuras de datos nativas para DaZe (Corte 3).
"""

class Pila:
    """Estructura LIFO (Last In, First Out)."""
    def __init__(self):
        self._datos = []

    def apilar(self, elem):
        self._datos.append(elem)

    def desapilar(self):
        if self.esta_vacia():
            raise IndexError("Intento de desapilar en una pila vacia.")
        return self._datos.pop()

    def tope(self):
        return None if self.esta_vacia() else self._datos[-1]

    def esta_vacia(self):
        return len(self._datos) == 0

    def __len__(self):
        return len(self._datos)

    def __repr__(self):
        return f"Pila({self._datos})"


class Cola:
    """Estructura FIFO (First In, First Out)."""
    def __init__(self):
        self._datos = []

    def encolar(self, elem):
        self._datos.append(elem)

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("Intento de desencolar en una cola vacia.")
        return self._datos.pop(0)

    def frente(self):
        return None if self.esta_vacia() else self._datos[0]

    def esta_vacia(self):
        return len(self._datos) == 0

    def __len__(self):
        return len(self._datos)

    def __repr__(self):
        return f"Cola({self._datos})"
