from src.core.ml import correlacion_pearson, RegresionLineal, KMeans
from src.core.estructuras import Pila, Cola
import src.core.matematica as mate
import os
import sys
from typing import Any, Dict, List, Optional, Union
from antlr4 import ParserRuleContext

from src.generated.DaZeParser import DaZeParser
from src.generated.DaZeParserVisitor import DaZeParserVisitor
from src.core.racoons import Tabla, GrupoTabla
from src.semantic.tabla_simbolos import TablaSimbolos, Simbolo
from src.errors import SemanticError, DiagnosticError


class ReturnSignal(Exception):
    """Senal de retorno de flujo para la instruccion 'resultado' en tacticas."""
    def __init__(self, valor: Any):
        self.valor = valor


class TacticaDefinicion:
    """Representa una funcion definida por el usuario en DaZe."""
    def __init__(self, nombre: str, parametros: List[str], sentencias_ctx: List[Any], linea: int = 0):
        self.nombre = nombre
        self.parametros = parametros
        self.sentencias_ctx = sentencias_ctx
        self.linea = linea

    def __repr__(self):
        return f"<Tactica {self.nombre}({', '.join(self.parametros)})>"


class DaZeSemanticVisitor(DaZeParserVisitor):
    """
    Visitor para la comprobacion semantica y la ejecucion de flujos de datos en DaZe.
    Recorre el AST generado por ANTLR4 y procesa instrucciones utilizando el motor nativo Tabla.
    """

    def __init__(self, tabla_simbolos: Optional[TablaSimbolos] = None, base_dir: Optional[str] = None):
        super().__init__()
        self.tabla_simbolos = tabla_simbolos or TablaSimbolos()
        self.base_dir = base_dir or os.getcwd()
        self.contexto_fila: Optional[Dict[str, Any]] = None
        self.errores_semanticos: List[DiagnosticError] = []
        self._registrar_funciones_nativas()

    def _registrar_funciones_nativas(self):
        nativas = {
            "raiz": mate.raiz_cuadrada,
            "sqrt": mate.raiz_cuadrada,
            "seno": mate.seno,
            "coseno": mate.coseno,
            "tangente": mate.tangente,
            "abs": mate.valor_absoluto,
            "potencia": mate.potencia,
            "maximo": mate.maximo_coleccion,
            "minimo": mate.minimo_coleccion,
            "promedio": mate.promedio_coleccion,
            "pila": lambda: Pila(),
            "cola": lambda: Cola(),
            "apilar": lambda p, x: p.apilar(x) if isinstance(p, Pila) else self._err_tipo("Pila", p),
            "desapilar": lambda p: p.desapilar() if isinstance(p, Pila) else self._err_tipo("Pila", p),
            "tope": lambda p: p.tope() if isinstance(p, Pila) else self._err_tipo("Pila", p),
            "encolar": lambda c, x: c.encolar(x) if isinstance(c, Cola) else self._err_tipo("Cola", c),
            "desencolar": lambda c: c.desencolar() if isinstance(c, Cola) else self._err_tipo("Cola", c),
            "frente": lambda c: c.frente() if isinstance(c, Cola) else self._err_tipo("Cola", c),
            "longitud": lambda col: len(col),
        }
        for nombre, func in nativas.items():
            self.tabla_simbolos.definir(nombre, func, tipo="TACTICA")

    def _err_tipo(self, esperado: str, recibido: Any):
        raise TypeError(f"Se esperaba una estructura '{esperado}', pero se recibio '{type(recibido).__name__}'.")

    def _resolver_ruta(self, ruta: str) -> str:
        if os.path.isabs(ruta):
            return ruta
        # 1. Probar relativa al directorio base especificado
        candidato_base = os.path.normpath(os.path.join(self.base_dir, ruta))
        if os.path.exists(candidato_base):
            return candidato_base
        # 2. Probar relativa al directorio padre del script (ej. si el script esta en examples/)
        candidato_padre = os.path.normpath(os.path.join(self.base_dir, "..", ruta))
        if os.path.exists(candidato_padre):
            return candidato_padre
        # 3. Probar relativa al cwd
        candidato_cwd = os.path.normpath(os.path.join(os.getcwd(), ruta))
        if os.path.exists(candidato_cwd):
            return candidato_cwd
        # 4. Probar en subdirectorio Proyecto_lenguajes si estamos un nivel arriba
        candidato_sub = os.path.normpath(os.path.join(os.getcwd(), "Proyecto_lenguajes", ruta))
        if os.path.exists(candidato_sub):
            return candidato_sub
        return candidato_base

    def _error(self, mensaje: str, ctx: ParserRuleContext, simbolo: Optional[str] = None) -> SemanticError:
        linea = ctx.start.line if (ctx and hasattr(ctx, "start") and ctx.start) else 0
        columna = ctx.start.column if (ctx and hasattr(ctx, "start") and ctx.start) else 0
        err = SemanticError(message=mensaje, line=linea, column=columna, offending_symbol=simbolo)
        self.errores_semanticos.append(err.to_diagnostic())
        return err

    # -------------------------------------------------------------
    # Programa y Sentencias
    # -------------------------------------------------------------

    def visitPrograma(self, ctx: DaZeParser.ProgramaContext):
        resultado_ultimo = None
        for sentencia in ctx.sentencia():
            try:
                resultado_ultimo = self.visit(sentencia)
            except SemanticError:
                # El error ya fue registrado en self.errores_semanticos
                continue
        return resultado_ultimo

    def visitSentencia(self, ctx: DaZeParser.SentenciaContext):
        return self.visitChildren(ctx)

    def visitAsignacion(self, ctx: DaZeParser.AsignacionContext):
        id_nombre = ctx.identificador().getText()
        valor = self.visit(ctx.expr())
        linea = ctx.start.line
        columna = ctx.start.column

        if self.tabla_simbolos.existe(id_nombre):
            self.tabla_simbolos.actualizar(id_nombre, valor)
        else:
            self.tabla_simbolos.definir(id_nombre, valor, linea=linea, columna=columna)

        return valor

    # -------------------------------------------------------------
    # Pipelines (|>)
    # -------------------------------------------------------------

    def visitPipeline_stmt(self, ctx: DaZeParser.Pipeline_stmtContext):
        # 1. Obtener la fuente de datos inicial
        valor_fuente = self.visit(ctx.expr())
        if not isinstance(valor_fuente, (Tabla, GrupoTabla)):
            raise self._error(
                f"El inicio del pipeline debe ser una tabla o conjunto de datos, se recibio '{type(valor_fuente).__name__}'.",
                ctx.expr(),
                ctx.expr().getText(),
            )

        tabla_actual = valor_fuente

        # 2. Encadenar cada operacion del pipeline
        for op_ctx in ctx.operacion_pipeline():
            tabla_actual = self._ejecutar_operacion_pipeline(op_ctx, tabla_actual)

        # 3. Si tiene asignacion final (ej. resultado = datos |> ...)
        if ctx.identificador():
            nombre_destino = ctx.identificador().getText()
            linea = ctx.start.line
            columna = ctx.start.column
            if self.tabla_simbolos.existe(nombre_destino):
                self.tabla_simbolos.actualizar(nombre_destino, tabla_actual)
            else:
                self.tabla_simbolos.definir(nombre_destino, tabla_actual, linea=linea, columna=columna)

        return tabla_actual

    def _ejecutar_operacion_pipeline(self, op_ctx: DaZeParser.Operacion_pipelineContext, tabla: Union[Tabla, GrupoTabla]) -> Union[Tabla, GrupoTabla]:
        hijo = op_ctx.getChild(0)

        if isinstance(hijo, DaZeParser.Op_convocarContext):
            return self._aplicar_convocar(hijo, tabla)
        elif isinstance(hijo, DaZeParser.Op_descartarContext):
            return self._aplicar_descartar(hijo, tabla)
        elif isinstance(hijo, DaZeParser.Op_contratarContext):
            return self._aplicar_contratar(hijo, tabla)
        elif isinstance(hijo, DaZeParser.Op_rebautizarContext):
            return self._aplicar_rebautizar(hijo, tabla)
        elif isinstance(hijo, DaZeParser.Op_clasificarContext):
            return self._aplicar_clasificar(hijo, tabla)
        elif isinstance(hijo, DaZeParser.Op_alinearContext):
            return self._aplicar_alinear(hijo, tabla)
        elif isinstance(hijo, DaZeParser.Op_balanceContext):
            return self._aplicar_balance(hijo, tabla)
        elif isinstance(hijo, DaZeParser.Op_reemplazar_bajasContext):
            return self._aplicar_sanear(hijo, tabla)
        elif isinstance(hijo, DaZeParser.Op_depurar_plantillaContext):
            return self._aplicar_depurar(hijo, tabla)
        elif isinstance(hijo, DaZeParser.Op_topContext):
            return self._aplicar_top(hijo, tabla)
        elif isinstance(hijo, DaZeParser.Op_personalizadaContext):
            return self._aplicar_personalizada(hijo, tabla)
        else:
            raise self._error(f"Operacion de pipeline desconocida: '{op_ctx.getText()}'", op_ctx)

    def _extraer_lista_columnas(self, ctx_cols: DaZeParser.Lista_columnasContext) -> List[str]:
        cols = []
        if not ctx_cols:
            return cols
        if ctx_cols.lista_nombres_columna():
            for item in ctx_cols.lista_nombres_columna().nombre_columna():
                txt = item.getText()
                if (txt.startswith('"') and txt.endswith('"')) or (txt.startswith("'") and txt.endswith("'")):
                    txt = txt[1:-1]
                cols.append(txt)
        return cols

    def _aplicar_convocar(self, ctx: DaZeParser.Op_convocarContext, tabla: Union[Tabla, GrupoTabla]) -> Tabla:
        if isinstance(tabla, GrupoTabla):
            tabla = tabla.tabla_origen

        cols = self._extraer_lista_columnas(ctx.lista_columnas())
        # Validar existencia de cada columna
        for col in cols:
            if col not in tabla.columnas:
                raise self._error(
                    f"La columna '{col}' no existe en la plantilla deportiva. Disponibles: {', '.join(tabla.columnas)}",
                    ctx,
                    col,
                )
        return tabla.convocar(cols)

    def _aplicar_descartar(self, ctx: DaZeParser.Op_descartarContext, tabla: Union[Tabla, GrupoTabla]) -> Tabla:
        if isinstance(tabla, GrupoTabla):
            tabla = tabla.tabla_origen

        expr_ctx = ctx.expr()

        def predicado(fila: Dict[str, Any]) -> bool:
            self.contexto_fila = fila
            try:
                res = self.visit(expr_ctx)
                return bool(res)
            finally:
                self.contexto_fila = None

        return tabla.descartar(predicado)

    def _aplicar_contratar(self, ctx: DaZeParser.Op_contratarContext, tabla: Union[Tabla, GrupoTabla]) -> Tabla:
        if isinstance(tabla, GrupoTabla):
            tabla = tabla.tabla_origen

        nuevas_columnas: Dict[str, Any] = {}
        for asignacion_par in ctx.lista_asignaciones().asignacion_par():
            nombre_col = asignacion_par.identificador().getText()
            expr_ctx = asignacion_par.expr()

            def calculador(fila: Dict[str, Any], e_ctx=expr_ctx) -> Any:
                self.contexto_fila = fila
                try:
                    return self.visit(e_ctx)
                finally:
                    self.contexto_fila = None

            nuevas_columnas[nombre_col] = calculador

        return tabla.contratar(nuevas_columnas)

    def _aplicar_rebautizar(self, ctx: DaZeParser.Op_rebautizarContext, tabla: Union[Tabla, GrupoTabla]) -> Tabla:
        if isinstance(tabla, GrupoTabla):
            tabla = tabla.tabla_origen

        mapeo: Dict[str, str] = {}
        for asignacion_par in ctx.lista_asignaciones().asignacion_par():
            col_vieja = asignacion_par.identificador().getText()
            nuevo_nombre_val = self.visit(asignacion_par.expr())
            if not isinstance(nuevo_nombre_val, str):
                nuevo_nombre_val = str(nuevo_nombre_val)

            if col_vieja not in tabla.columnas:
                raise self._error(
                    f"No se puede rebautizar la columna inexistente '{col_vieja}'.",
                    ctx,
                    col_vieja,
                )
            mapeo[col_vieja] = nuevo_nombre_val

        return tabla.rebautizar(mapeo)

    def _extraer_nombres_columnas_de_expr(self, expr_ctx) -> List[str]:
        if isinstance(expr_ctx, DaZeParser.ExprIdentificadorContext):
            return [expr_ctx.identificador().getText()]
        elif isinstance(expr_ctx, DaZeParser.ExprCadenaContext):
            return [expr_ctx.CADENA().getText().strip('"\'')]
        elif isinstance(expr_ctx, DaZeParser.ExprListaContext):
            res = []
            if expr_ctx.lista_expr():
                for sub_e in expr_ctx.lista_expr().expr():
                    res.extend(self._extraer_nombres_columnas_de_expr(sub_e))
            return res
        elif isinstance(expr_ctx, DaZeParser.ExprAgrupacionContext):
            return self._extraer_nombres_columnas_de_expr(expr_ctx.expr())
        else:
            try:
                val = self.visit(expr_ctx)
                if isinstance(val, list):
                    return [str(v) for v in val]
                elif val is not None:
                    return [str(val)]
            except Exception:
                pass
            return [expr_ctx.getText()]

    def _aplicar_clasificar(self, ctx: DaZeParser.Op_clasificarContext, tabla: Union[Tabla, GrupoTabla]) -> Tabla:
        if isinstance(tabla, GrupoTabla):
            tabla = tabla.tabla_origen

        cols_orden: List[str] = []
        descendente = False

        args_ctx = ctx.argumentos_ordenar().lista_argumentos()
        for arg in args_ctx.argumento():
            if arg.identificador() and arg.expr():
                clave = arg.identificador().getText().lower()
                if clave in ("por", "columnas", "columna"):
                    cols_orden.extend(self._extraer_nombres_columnas_de_expr(arg.expr()))
                elif clave in ("descendente", "desc"):
                    descendente = bool(self.visit(arg.expr()))
                elif clave in ("ascendente", "asc"):
                    descendente = not bool(self.visit(arg.expr()))
            else:
                cols_orden.extend(self._extraer_nombres_columnas_de_expr(arg.expr()))

        if not cols_orden:
            raise self._error("La operacion 'clasificar' requiere al menos una columna para ordenar.", ctx)

        for c in cols_orden:
            if c not in tabla.columnas:
                raise self._error(f"Columna de ordenamiento '{c}' no existe en la plantilla.", ctx, c)

        return tabla.clasificar(cols_orden, descendente=descendente)

    def _aplicar_alinear(self, ctx: DaZeParser.Op_alinearContext, tabla: Union[Tabla, GrupoTabla]) -> GrupoTabla:
        if isinstance(tabla, GrupoTabla):
            tabla = tabla.tabla_origen

        cols_grupo: List[str] = []

        if ctx.argumentos_agrupar():
            args_ctx = ctx.argumentos_agrupar().lista_argumentos()
            for arg in args_ctx.argumento():
                if arg.identificador() and arg.expr():
                    clave = arg.identificador().getText().lower()
                    if clave in ("por", "columnas", "columna"):
                        cols_grupo.extend(self._extraer_nombres_columnas_de_expr(arg.expr()))
                else:
                    cols_grupo.extend(self._extraer_nombres_columnas_de_expr(arg.expr()))
        elif ctx.lista_columnas():
            cols_grupo = self._extraer_lista_columnas(ctx.lista_columnas())

        if not cols_grupo:
            raise self._error("La operacion 'alinear' requiere especificar las columnas de agrupacion.", ctx)

        for c in cols_grupo:
            if c not in tabla.columnas:
                raise self._error(f"Columna de agrupacion '{c}' no existe en la plantilla.", ctx, c)

        return tabla.alinear(cols_grupo)

    def _aplicar_balance(self, ctx: DaZeParser.Op_balanceContext, tabla: Union[Tabla, GrupoTabla]) -> Tabla:
        agregaciones: Dict[str, tuple] = {}

        for item_resumen in ctx.lista_resumen().resumen_par():
            nombre_salida = item_resumen.identificador().getText()

            if item_resumen.funcion_agregacion():
                f_ctx = item_resumen.funcion_agregacion()
                nombre_func = f_ctx.getChild(0).getText().lower()

                # 'contar()' no necesita columna obligatoria
                if f_ctx.identificador():
                    col_origen = f_ctx.identificador().getText()
                elif f_ctx.CADENA():
                    col_origen = f_ctx.CADENA().getText().strip('"\'')
                else:
                    col_origen = None

                tabla_ref = tabla.tabla_origen if isinstance(tabla, GrupoTabla) else tabla
                if col_origen and col_origen not in tabla_ref.columnas:
                    raise self._error(
                        f"Columna '{col_origen}' no encontrada para agregacion '{nombre_func}'.",
                        item_resumen,
                        col_origen,
                    )

                agregaciones[nombre_salida] = (nombre_func, col_origen)
            else:
                val = self.visit(item_resumen.expr())
                # Asignacion constante o expresion evaluada
                agregaciones[nombre_salida] = ("constante", val)

        return tabla.balance(agregaciones)

    def _aplicar_sanear(self, ctx: DaZeParser.Op_reemplazar_bajasContext, tabla: Union[Tabla, GrupoTabla]) -> Tabla:
        if isinstance(tabla, GrupoTabla):
            tabla = tabla.tabla_origen

        reemplazos: Dict[str, Any] = {}
        for arg in ctx.argumentos_con_nombre().argumento_con_nombre():
            col = arg.identificador().getText()
            val = self.visit(arg.expr())
            reemplazos[col] = val

        return tabla.sanear(reemplazos)

    def _aplicar_depurar(self, ctx: DaZeParser.Op_depurar_plantillaContext, tabla: Union[Tabla, GrupoTabla]) -> Tabla:
        if isinstance(tabla, GrupoTabla):
            tabla = tabla.tabla_origen

        cols = None
        if ctx.lista_columnas():
            cols = self._extraer_lista_columnas(ctx.lista_columnas())
        return tabla.depurar(cols)

    def _aplicar_top(self, ctx: DaZeParser.Op_topContext, tabla: Union[Tabla, GrupoTabla]) -> Tabla:
        if isinstance(tabla, GrupoTabla):
            tabla = tabla.tabla_origen
        n = int(ctx.ENTERO().getText())
        return tabla.top(n)

    def _aplicar_personalizada(self, ctx: DaZeParser.Op_personalizadaContext, tabla: Union[Tabla, GrupoTabla]) -> Any:
        nombre = ctx.identificador().getText()
        simbolo = self.tabla_simbolos.obtener(nombre)
        if not simbolo or not isinstance(simbolo.valor, TacticaDefinicion):
            raise self._error(f"No existe una tactica o funcion llamada '{nombre}' para encadenar en pipeline.", ctx, nombre)

        args_evaluados = [tabla]
        if ctx.lista_argumentos():
            for arg in ctx.lista_argumentos().argumento():
                args_evaluados.append(self.visit(arg.expr()))

        return self._ejecutar_tactica(simbolo.valor, args_evaluados, ctx)

    # -------------------------------------------------------------
    # Sentencias de Carga, Guardado y Visualizacion
    # -------------------------------------------------------------

    def visitExprFichar(self, ctx: DaZeParser.ExprFicharContext):
        ruta_rel = ctx.CADENA().getText().strip('"\'')
        ruta = self._resolver_ruta(ruta_rel)

        separador = ","
        encabezado = True

        if ctx.argumentos_con_nombre():
            for arg in ctx.argumentos_con_nombre().argumento_con_nombre():
                clave = arg.identificador().getText().lower()
                val = self.visit(arg.expr())
                if clave in ("separador", "sep", "delimitador"):
                    separador = str(val)
                elif clave in ("encabezado", "header"):
                    encabezado = bool(val)

        try:
            return Tabla.csvread(ruta, separador=separador, encabezado=encabezado)
        except Exception as e:
            raise self._error(f"Error cargando archivo con 'fichar': {str(e)}", ctx, ruta_rel)

    def visitGuardar_stmt(self, ctx: DaZeParser.Guardar_stmtContext):
        valor_tabla = self.visit(ctx.expr())
        if isinstance(valor_tabla, GrupoTabla):
            valor_tabla = valor_tabla.tabla_origen
        if not isinstance(valor_tabla, Tabla):
            raise self._error("La instruccion 'archivar' requiere una tabla deportiva valida como primer argumento.", ctx)

        ruta_texto = ctx.CADENA().getText().strip('"\'')
        if os.path.basename(self.base_dir) == "examples" and not os.path.isabs(ruta_texto):
            ruta = os.path.normpath(os.path.join(self.base_dir, "..", ruta_texto))
        else:
            ruta = os.path.normpath(os.path.join(self.base_dir, ruta_texto))

        separador = ","
        if ctx.argumentos_con_nombre():
            for arg in ctx.argumentos_con_nombre().argumento_con_nombre():
                clave = arg.identificador().getText().lower()
                val = self.visit(arg.expr())
                if clave in ("separador", "sep", "delimitador"):
                    separador = str(val)

        try:
            valor_tabla.csvsave(ruta, separador=separador)
            print(f"[Archivado] Tabla guardada exitosamente en '{ruta}' ({len(valor_tabla)} registros)")
        except Exception as e:
            raise self._error(f"Error al archivar tabla en '{ruta}': {str(e)}", ctx, ruta_texto)

        return valor_tabla

    def visitMostrar_stmt(self, ctx: DaZeParser.Mostrar_stmtContext):
        valor = self.visit(ctx.expr())
        if isinstance(valor, Tabla):
            print(valor.mostrar())
        elif isinstance(valor, GrupoTabla):
            print(valor.tabla_origen.mostrar())
        else:
            print(valor)
        return valor

    def visitGraficar_stmt(self, ctx: DaZeParser.Graficar_stmtContext):
        # Validacion semantica de la declaracion de visualizacion
        tipo = ctx.tipo_grafico().getText()
        valor_tabla = self.visit(ctx.expr())
        if isinstance(valor_tabla, GrupoTabla):
            valor_tabla = valor_tabla.tabla_origen

        if not isinstance(valor_tabla, Tabla):
            raise self._error(f"La declaracion de pizarra '{tipo}' requiere una tabla deportiva valida.", ctx.expr())

        # Validar propiedades configuradas dentro del bloque
        configs: Dict[str, Any] = {}
        for c_ctx in ctx.configuracion_grafico():
            clave = c_ctx.identificador().getText()
            expr_c = c_ctx.expr()
            if isinstance(expr_c, DaZeParser.ExprIdentificadorContext):
                val_txt = expr_c.identificador().getText()
                if val_txt in valor_tabla.columnas:
                    val = val_txt
                else:
                    simbolo = self.tabla_simbolos.obtener(val_txt)
                    val = simbolo.valor if simbolo else val_txt
            else:
                val = self.visit(expr_c)
            configs[clave] = val

        for eje in ("eje_x", "eje_y", "x", "y"):
            if eje in configs:
                col_name = str(configs[eje])
                if col_name not in valor_tabla.columnas:
                    # Advertencia / comprobacion semantica
                    raise self._error(
                        f"En la pizarra '{tipo}', la columna '{col_name}' especificada en '{eje}' no existe en la plantilla.",
                        ctx,
                        col_name,
                    )

        print(f"[Pizarra] Especificacion validada para grafico '{tipo}' ({len(valor_tabla)} registros disponibles)")
        return configs

    # -------------------------------------------------------------
    # Estructuras de Control y Funciones (Tactica)
    # -------------------------------------------------------------

    def visitSi_stmt(self, ctx: DaZeParser.Si_stmtContext):
        condicion = self.visit(ctx.expr())
        bloques = ctx.sentencia()

        # En la gramatica: si (expr) { sentencia* } (sino { sentencia* })?
        if ctx.SINO():
            # Buscar donde termina el bloque si y empieza el bloque sino
            # Podemos inspeccionar el arbol sintactico directamente
            sentencias_si = []
            sentencias_sino = []
            en_sino = False
            for i in range(ctx.getChildCount()):
                hijo = ctx.getChild(i)
                if hijo.getText() == "sino":
                    en_sino = True
                elif isinstance(hijo, DaZeParser.SentenciaContext):
                    if en_sino:
                        sentencias_sino.append(hijo)
                    else:
                        sentencias_si.append(hijo)

            objetivo = sentencias_si if bool(condicion) else sentencias_sino
        else:
            objetivo = bloques if bool(condicion) else []

        resultado = None
        for s in objetivo:
            resultado = self.visit(s)
        return resultado

    def visitFuncion_stmt(self, ctx: DaZeParser.Funcion_stmtContext):
        nombre = ctx.identificador().getText()
        params = []
        if ctx.lista_parametros():
            for p in ctx.lista_parametros().identificador():
                params.append(p.getText())

        tactica_obj = TacticaDefinicion(
            nombre=nombre,
            parametros=params,
            sentencias_ctx=ctx.sentencia(),
            linea=ctx.start.line,
        )
        self.tabla_simbolos.definir(nombre, tactica_obj, tipo="TACTICA", linea=ctx.start.line, columna=ctx.start.column)
        return tactica_obj

    def visitRetornar_stmt(self, ctx: DaZeParser.Retornar_stmtContext):
        val = self.visit(ctx.expr()) if ctx.expr() else None
        raise ReturnSignal(val)

    def visitLlamada_stmt(self, ctx: DaZeParser.Llamada_stmtContext):
        nombre = ctx.identificador().getText()

        args_evaluados = []
        if ctx.lista_argumentos():
            for arg in ctx.lista_argumentos().argumento():
                args_evaluados.append(self.visit(arg.expr()))

        if nombre == "proyectar":
            for val in args_evaluados:
                if isinstance(val, Tabla):
                    print(val.mostrar())
                elif isinstance(val, GrupoTabla):
                    print(val.tabla_origen.mostrar())
                else:
                    print(val)
            return args_evaluados[-1] if args_evaluados else None

        if nombre == "archivar" and args_evaluados:
            tabla_val = args_evaluados[0]
            if isinstance(tabla_val, GrupoTabla):
                tabla_val = tabla_val.tabla_origen
            if not isinstance(tabla_val, Tabla):
                raise self._error("La funcion 'archivar' requiere una tabla valida.", ctx)
            ruta_texto = str(args_evaluados[1]) if len(args_evaluados) > 1 else "salidas/exportacion.csv"
            if os.path.basename(self.base_dir) == "examples" and not os.path.isabs(ruta_texto):
                ruta = os.path.normpath(os.path.join(self.base_dir, "..", ruta_texto))
            else:
                ruta = os.path.normpath(os.path.join(self.base_dir, ruta_texto))
            tabla_val.csvsave(ruta)
            print(f"[Archivado] Tabla guardada exitosamente en '{ruta}' ({len(tabla_val)} registros)")
            return tabla_val

        simbolo = self.tabla_simbolos.obtener(nombre)
        if not simbolo:
            raise self._error(f"Tactica o funcion '{nombre}' no declarada.", ctx, nombre)

        if isinstance(simbolo.valor, TacticaDefinicion):
            return self._ejecutar_tactica(simbolo.valor, args_evaluados, ctx)
        elif callable(simbolo.valor):
            return simbolo.valor(*args_evaluados)
        else:
            raise self._error(f"'{nombre}' no es ejecutable como tactica o funcion.", ctx, nombre)

    def _ejecutar_tactica(self, tactica: TacticaDefinicion, argumentos: List[Any], ctx: ParserRuleContext) -> Any:
        if len(argumentos) != len(tactica.parametros):
            raise self._error(
                f"La tactica '{tactica.nombre}' esperaba {len(tactica.parametros)} parametros ({', '.join(tactica.parametros)}), pero recibio {len(argumentos)}.",
                ctx,
                tactica.nombre,
            )

        # Crear nuevo ambito local
        ambito_anterior = self.tabla_simbolos
        self.tabla_simbolos = self.tabla_simbolos.crear_ambito_hijo(f"tactica_{tactica.nombre}")

        for param_nombre, valor in zip(tactica.parametros, argumentos):
            self.tabla_simbolos.definir(param_nombre, valor)

        resultado = None
        try:
            for s in tactica.sentencias_ctx:
                self.visit(s)
        except ReturnSignal as ret:
            resultado = ret.valor
        finally:
            self.tabla_simbolos = ambito_anterior

        return resultado

    # -------------------------------------------------------------
    # Evaluacion de Expresiones
    # -------------------------------------------------------------

    def visitExprIdentificador(self, ctx: DaZeParser.ExprIdentificadorContext):
        nombre = ctx.identificador().getText()

        # 1. Si estamos dentro de la evaluacion de una fila de tabla
        if self.contexto_fila is not None and nombre in self.contexto_fila:
            return self.contexto_fila[nombre]

        # 2. Buscar en la tabla de simbolos
        simbolo = self.tabla_simbolos.obtener(nombre)
        if simbolo is not None:
            return simbolo.valor

        # 3. Si estabamos en fila pero la columna no existe
        if self.contexto_fila is not None:
            raise self._error(
                f"La columna '{nombre}' no existe en el registro actual de la plantilla deportiva.",
                ctx,
                nombre,
            )

        raise self._error(f"Variable o identificador '{nombre}' no ha sido declarado.", ctx, nombre)

    def visitExprEntero(self, ctx: DaZeParser.ExprEnteroContext):
        return int(ctx.ENTERO().getText())

    def visitExprDecimal(self, ctx: DaZeParser.ExprDecimalContext):
        return float(ctx.DECIMAL().getText())

    def visitExprCadena(self, ctx: DaZeParser.ExprCadenaContext):
        txt = ctx.CADENA().getText()
        return txt[1:-1]

    def visitExprVerdadero(self, ctx: DaZeParser.ExprVerdaderoContext):
        return True

    def visitExprFalso(self, ctx: DaZeParser.ExprFalsoContext):
        return False

    def visitExprNulo(self, ctx: DaZeParser.ExprNuloContext):
        return None

    def visitExprAgrupacion(self, ctx: DaZeParser.ExprAgrupacionContext):
        return self.visit(ctx.expr())

    def visitExprLista(self, ctx: DaZeParser.ExprListaContext):
        elementos = []
        if ctx.lista_expr():
            for e in ctx.lista_expr().expr():
                elementos.append(self.visit(e))
        return elementos

    def visitExprPotencia(self, ctx: DaZeParser.ExprPotenciaContext):
        base = self.visit(ctx.expr(0))
        exponente = self.visit(ctx.expr(1))
        if not isinstance(base, (int, float)) or not isinstance(exponente, (int, float)):
            raise self._error(f"La operacion de potencia requiere numeros, se recibio {type(base).__name__} y {type(exponente).__name__}.", ctx)
        return base ** exponente

    def visitExprUnaria(self, ctx: DaZeParser.ExprUnariaContext):
        val = self.visit(ctx.expr())
        op = ctx.getChild(0).getText().lower()
        if op == "-":
            if not isinstance(val, (int, float)):
                raise self._error(f"Operador unario '-' no aplicable a tipo {type(val).__name__}.", ctx)
            return -val
        elif op == "+":
            return val
        elif op in ("no", "not", "!"):
            return not bool(val)
        return val

    def visitExprMulDivMod(self, ctx: DaZeParser.ExprMulDivModContext):
        izq = self.visit(ctx.expr(0))
        der = self.visit(ctx.expr(1))
        op = ctx.getChild(1).getText()

        if izq is None or der is None:
            return None

        if op == "*":
            if isinstance(izq, (int, float)) and isinstance(der, (int, float)):
                return izq * der
            elif isinstance(izq, str) and isinstance(der, int):
                return izq * der
            raise self._error(f"Multiplicacion invalida entre {type(izq).__name__} y {type(der).__name__}.", ctx)
        elif op == "/":
            if not isinstance(izq, (int, float)) or not isinstance(der, (int, float)):
                raise self._error(f"Division requiere operandos numericos, recibidos {type(izq).__name__} y {type(der).__name__}.", ctx)
            if der == 0:
                raise self._error("Division por cero no permitida en calculos de rendimiento.", ctx)
            return izq / der
        elif op == "%":
            if not isinstance(izq, (int, float)) or not isinstance(der, (int, float)):
                raise self._error(f"Modulo '%' requiere operandos numericos, recibidos {type(izq).__name__} y {type(der).__name__}.", ctx)
            return izq % der
        return None

    def visitExprSumaResta(self, ctx: DaZeParser.ExprSumaRestaContext):
        izq = self.visit(ctx.expr(0))
        der = self.visit(ctx.expr(1))
        op = ctx.getChild(1).getText()

        if op == "+":
            if isinstance(izq, (int, float)) and isinstance(der, (int, float)):
                return izq + der
            elif isinstance(izq, str) or isinstance(der, str):
                return f"{izq if izq is not None else ''}{der if der is not None else ''}"
            elif isinstance(izq, list) and isinstance(der, list):
                return izq + der
            raise self._error(f"Operacion suma no permitida entre {type(izq).__name__} y {type(der).__name__}.", ctx)
        elif op == "-":
            if not isinstance(izq, (int, float)) or not isinstance(der, (int, float)):
                raise self._error(f"Operacion resta requiere operandos numericos, recibidos {type(izq).__name__} y {type(der).__name__}.", ctx)
            return izq - der
        return None

    def visitExprRelacional(self, ctx: DaZeParser.ExprRelacionalContext):
        izq = self.visit(ctx.expr(0))
        der = self.visit(ctx.expr(1))
        op = ctx.getChild(1).getText()

        if izq is None or der is None:
            return False

        try:
            if op == ">":
                return izq > der
            elif op == "<":
                return izq < der
            elif op == ">=":
                return izq >= der
            elif op == "<=":
                return izq <= der
        except TypeError as e:
            raise self._error(f"Comparacion relacional invalida entre {type(izq).__name__} y {type(der).__name__}.", ctx)
        return False

    def visitExprIgualdad(self, ctx: DaZeParser.ExprIgualdadContext):
        izq = self.visit(ctx.expr(0))
        der = self.visit(ctx.expr(1))
        op = ctx.getChild(1).getText()

        if op == "==":
            return izq == der
        elif op == "!=":
            return izq != der
        return False

    def visitExprLogicaY(self, ctx: DaZeParser.ExprLogicaYContext):
        izq = self.visit(ctx.expr(0))
        if not bool(izq):
            return False
        der = self.visit(ctx.expr(1))
        return bool(der)

    def visitExprLogicaO(self, ctx: DaZeParser.ExprLogicaOContext):
        izq = self.visit(ctx.expr(0))
        if bool(izq):
            return True
        der = self.visit(ctx.expr(1))
        return bool(der)

    def visitExprLlamada(self, ctx: DaZeParser.ExprLlamadaContext):
        nombre = ctx.identificador().getText()
        # --- MACHINE LEARNING PURO (CORTE 3) ---
        if nombre in ("correlacion", "regresion_lineal", "predecir_regresion", "predecir", "agrupar_kmedias"):
            _ml_args = []
            if hasattr(ctx, "lista_argumentos") and ctx.lista_argumentos():
                for _a in ctx.lista_argumentos().argumento():
                    _expr = _a.expr() if hasattr(_a, "expr") and _a.expr() else _a
                    _ml_args.append(self.visit(_expr))

            if nombre == "correlacion":
                if len(_ml_args) != 2:
                    raise Exception("correlacion() requiere 2 listas: correlacion(x, y)")
                return correlacion_pearson(_ml_args[0], _ml_args[1])

            if nombre == "regresion_lineal":
                if len(_ml_args) != 2:
                    raise Exception("regresion_lineal() requiere 2 listas: regresion_lineal(x, y)")
                modelo = RegresionLineal().ajustar(_ml_args[0], _ml_args[1])
                return {
                    "m": modelo.m,
                    "b": modelo.b,
                    "r2": modelo.r2,
                    "_modelo": modelo
                }

            if nombre in ("predecir_regresion", "predecir"):
                if len(_ml_args) != 2:
                    raise Exception("predecir_regresion() requiere el modelo y el valor: predecir(mod, x)")
                mod = _ml_args[0]
                val = _ml_args[1]
                if isinstance(mod, dict) and "_modelo" in mod:
                    return mod["_modelo"].predecir(val)
                if isinstance(mod, dict) and "m" in mod and "b" in mod:
                    if isinstance(val, list):
                        return [round(mod["m"] * v + mod["b"], 4) for v in val]
                    return round(mod["m"] * val + mod["b"], 4)
                raise Exception("El primer argumento debe ser un modelo entrenado de regresion.")

            if nombre == "agrupar_kmedias":
                if len(_ml_args) < 2:
                    raise Exception("agrupar_kmedias() requiere datos y valor k: agrupar_kmedias(datos, k)")
                datos = _ml_args[0]
                k = int(_ml_args[1])
                km = KMeans(k=k, max_iter=60).ajustar(datos)
                return {
                    "centroides": km.centroides,
                    "etiquetas": km.etiquetas
                }

        simbolo = self.tabla_simbolos.obtener(nombre)
        if not simbolo:
            raise self._error(f"Tactica o funcion '{nombre}' no declarada.", ctx, nombre)

        args_evaluados = []
        if ctx.lista_argumentos():
            for arg in ctx.lista_argumentos().argumento():
                args_evaluados.append(self.visit(arg.expr()))

        if isinstance(simbolo.valor, TacticaDefinicion):
            return self._ejecutar_tactica(simbolo.valor, args_evaluados, ctx)
        elif callable(simbolo.valor):
            return simbolo.valor(*args_evaluados)
        else:
            raise self._error(f"'{nombre}' no es ejecutable como funcion.", ctx, nombre)



    # -------------------------------------------------------------
    # Metodos del Corte 3 (Ciclos, Arreglos y Diccionarios)
    # -------------------------------------------------------------

    def visitAsignacion_indexada(self, ctx: DaZeParser.Asignacion_indexadaContext):
        id_nombre = ctx.identificador().getText()
        simbolo = self.tabla_simbolos.obtener(id_nombre)
        if not simbolo:
            raise self._error(f"Variable '{id_nombre}' no declarada.", ctx, id_nombre)

        contenedor = simbolo.valor
        indice = self.visit(ctx.expr(0))
        nuevo_valor = self.visit(ctx.expr(1))

        if isinstance(contenedor, list):
            if not isinstance(indice, int):
                raise self._error(f"El indice debe ser entero, recibido '{type(indice).__name__}'.", ctx)
            if indice < 0 or indice >= len(contenedor):
                raise self._error(f"Indice {indice} fuera de rango para lista de tamano {len(contenedor)}.", ctx)
            contenedor[indice] = nuevo_valor
        elif isinstance(contenedor, dict):
            contenedor[indice] = nuevo_valor
        else:
            raise self._error(f"El tipo '{type(contenedor).__name__}' no admite asignacion por indice.", ctx)
        return nuevo_valor

    def visitBucle_mientras_stmt(self, ctx: DaZeParser.Bucle_mientras_stmtContext):
        resultado = None
        while bool(self.visit(ctx.expr())):
            for s in ctx.sentencia():
                resultado = self.visit(s)
        return resultado

    def visitBucle_para_stmt(self, ctx: DaZeParser.Bucle_para_stmtContext):
        var_iterador = ctx.identificador().getText()
        coleccion = self.visit(ctx.expr())

        if isinstance(coleccion, (Tabla, GrupoTabla)):
            iterable = coleccion.filas if isinstance(coleccion, Tabla) else coleccion.tabla_origen.filas
        elif isinstance(coleccion, (list, tuple)):
            iterable = coleccion
        elif isinstance(coleccion, dict):
            iterable = list(coleccion.keys())
        else:
            raise self._error(f"No se puede iterar en 'ronda' sobre tipo '{type(coleccion).__name__}'.", ctx.expr())

        resultado = None
        for elemento in iterable:
            if self.tabla_simbolos.existe(var_iterador):
                self.tabla_simbolos.actualizar(var_iterador, elemento)
            else:
                self.tabla_simbolos.definir(var_iterador, elemento)

            for s in ctx.sentencia():
                resultado = self.visit(s)
        return resultado

    def visitExprDiccionario(self, ctx: DaZeParser.ExprDiccionarioContext):
        d = {}
        if ctx.lista_diccionario():
            for p in ctx.lista_diccionario().par_diccionario():
                clave_raw = p.getChild(0).getText()
                if (clave_raw.startswith('"') and clave_raw.endswith('"')) or (clave_raw.startswith("'") and clave_raw.endswith("'")):
                    clave = clave_raw[1:-1]
                else:
                    clave = clave_raw
                d[clave] = self.visit(p.expr())
        return d

    def visitExprIndexacion(self, ctx: DaZeParser.ExprIndexacionContext):
        contenedor = self.visit(ctx.expr(0))
        indice = self.visit(ctx.expr(1))

        if isinstance(contenedor, list):
            if not isinstance(indice, int):
                raise self._error(f"El indice debe ser entero, recibido '{type(indice).__name__}'.", ctx)
            if indice < 0 or indice >= len(contenedor):
                raise self._error(f"Indice {indice} fuera de rango para lista de longitud {len(contenedor)}.", ctx)
            return contenedor[indice]
        elif isinstance(contenedor, dict):
            if indice not in contenedor:
                raise self._error(f"Clave '{indice}' no existe en el diccionario.", ctx)
            return contenedor[indice]
        raise self._error(f"El tipo '{type(contenedor).__name__}' no admite acceso por corchetes.", ctx)

def ejecutar_codigo(codigo: str, base_dir: Optional[str] = None):
    from src import parse_code
    tree, parser, errores_sintacticos = parse_code(codigo)
    if errores_sintacticos:
        return None, errores_sintacticos

    visitor = DaZeSemanticVisitor(base_dir=base_dir)
    try:
        resultado = visitor.visit(tree)
    except SemanticError:
        pass

    todos_errores = errores_sintacticos + visitor.errores_semanticos
    return visitor, todos_errores


def ejecutar_archivo(ruta_archivo: str):
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"No existe el archivo '{ruta_archivo}'")

    with open(ruta_archivo, "r", encoding="utf-8") as f:
        codigo = f.read()

    base_dir = os.path.dirname(os.path.abspath(ruta_archivo))
    return ejecutar_codigo(codigo, base_dir=base_dir)
