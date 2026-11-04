from typing import Dict, Any, Optional, List
from src.core.racoons import Tabla
from src.core.estructuras import Pila, Cola


class Simbolo:
    def __init__(
        self,
        nombre: str,
        tipo: str,
        valor: Any = None,
        esquema: Optional[List[str]] = None,
        linea: int = 0,
        columna: int = 0,
    ):
        self.nombre = nombre
        self.tipo = tipo
        self.valor = valor
        self.esquema = esquema or ([] if not isinstance(valor, Tabla) else list(valor.columnas))
        self.linea = linea
        self.columna = columna

    def actualizar(self, nuevo_valor: Any, nuevo_tipo: Optional[str] = None):
        self.valor = nuevo_valor
        if nuevo_tipo:
            self.tipo = nuevo_tipo
        elif isinstance(nuevo_valor, Tabla):
            self.tipo = "TABLA"
            self.esquema = list(nuevo_valor.columnas)
        elif isinstance(nuevo_valor, (int, float)):
            self.tipo = "NUMERO"
        elif isinstance(nuevo_valor, str):
            self.tipo = "CADENA"
        elif isinstance(nuevo_valor, bool):
            self.tipo = "BOOLEANO"
        elif isinstance(nuevo_valor, list):
            self.tipo = "LISTA"
        elif isinstance(nuevo_valor, dict):
            self.tipo = "DICCIONARIO"
        elif isinstance(nuevo_valor, Pila):
            self.tipo = "PILA"
        elif isinstance(nuevo_valor, Cola):
            self.tipo = "COLA"

    def __repr__(self) -> str:
        esquema_info = f", cols={self.esquema}" if self.esquema else ""
        return f"<Simbolo {self.nombre}: {self.tipo}{esquema_info}>"


class TablaSimbolos:
    def __init__(self, padre: Optional["TablaSimbolos"] = None, nombre_ambito: str = "global"):
        self.padre = padre
        self.nombre_ambito = nombre_ambito
        self.simbolos: Dict[str, Simbolo] = {}

    def definir(
        self,
        nombre: str,
        valor: Any,
        tipo: Optional[str] = None,
        linea: int = 0,
        columna: int = 0,
    ) -> Simbolo:
        tipo_final = tipo or self._deducir_tipo(valor)
        esquema = list(valor.columnas) if isinstance(valor, Tabla) else None

        simbolo = Simbolo(
            nombre=nombre,
            tipo=tipo_final,
            valor=valor,
            esquema=esquema,
            linea=linea,
            columna=columna,
        )
        self.simbolos[nombre] = simbolo
        return simbolo

    def actualizar(self, nombre: str, valor: Any, tipo: Optional[str] = None) -> bool:
        if nombre in self.simbolos:
            self.simbolos[nombre].actualizar(valor, tipo)
            return True
        if self.padre:
            return self.padre.actualizar(nombre, valor, tipo)
        return False

    def obtener(self, nombre: str) -> Optional[Simbolo]:
        if nombre in self.simbolos:
            return self.simbolos[nombre]
        if self.padre:
            return self.padre.obtener(nombre)
        return None

    def existe(self, nombre: str) -> bool:
        return self.obtener(nombre) is not None

    def crear_ambito_hijo(self, nombre: str = "local") -> "TablaSimbolos":
        return TablaSimbolos(padre=self, nombre_ambito=nombre)

    def _deducir_tipo(self, valor: Any) -> str:
        if isinstance(valor, Tabla):
            return "TABLA"
        elif isinstance(valor, bool):
            return "BOOLEANO"
        elif isinstance(valor, (int, float)):
            return "NUMERO"
        elif isinstance(valor, str):
            return "CADENA"
        elif isinstance(valor, list):
            return "LISTA"
        elif isinstance(valor, dict):
            return "DICCIONARIO"
        elif isinstance(valor, Pila):
            return "PILA"
        elif isinstance(valor, Cola):
            return "COLA"
        elif callable(valor):
            return "TACTICA"
        elif valor is None:
            return "NULO"
        return "DESCONOCIDO"
