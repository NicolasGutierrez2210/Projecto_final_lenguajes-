# Generated from grammar/DaZeParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .DaZeParser import DaZeParser
else:
    from DaZeParser import DaZeParser

# This class defines a complete listener for a parse tree produced by DaZeParser.
class DaZeParserListener(ParseTreeListener):

    # Enter a parse tree produced by DaZeParser#programa.
    def enterPrograma(self, ctx:DaZeParser.ProgramaContext):
        pass

    # Exit a parse tree produced by DaZeParser#programa.
    def exitPrograma(self, ctx:DaZeParser.ProgramaContext):
        pass


    # Enter a parse tree produced by DaZeParser#sentencia.
    def enterSentencia(self, ctx:DaZeParser.SentenciaContext):
        pass

    # Exit a parse tree produced by DaZeParser#sentencia.
    def exitSentencia(self, ctx:DaZeParser.SentenciaContext):
        pass


    # Enter a parse tree produced by DaZeParser#asignacion.
    def enterAsignacion(self, ctx:DaZeParser.AsignacionContext):
        pass

    # Exit a parse tree produced by DaZeParser#asignacion.
    def exitAsignacion(self, ctx:DaZeParser.AsignacionContext):
        pass


    # Enter a parse tree produced by DaZeParser#asignacion_indexada.
    def enterAsignacion_indexada(self, ctx:DaZeParser.Asignacion_indexadaContext):
        pass

    # Exit a parse tree produced by DaZeParser#asignacion_indexada.
    def exitAsignacion_indexada(self, ctx:DaZeParser.Asignacion_indexadaContext):
        pass


    # Enter a parse tree produced by DaZeParser#bucle_mientras_stmt.
    def enterBucle_mientras_stmt(self, ctx:DaZeParser.Bucle_mientras_stmtContext):
        pass

    # Exit a parse tree produced by DaZeParser#bucle_mientras_stmt.
    def exitBucle_mientras_stmt(self, ctx:DaZeParser.Bucle_mientras_stmtContext):
        pass


    # Enter a parse tree produced by DaZeParser#bucle_para_stmt.
    def enterBucle_para_stmt(self, ctx:DaZeParser.Bucle_para_stmtContext):
        pass

    # Exit a parse tree produced by DaZeParser#bucle_para_stmt.
    def exitBucle_para_stmt(self, ctx:DaZeParser.Bucle_para_stmtContext):
        pass


    # Enter a parse tree produced by DaZeParser#pipeline_stmt.
    def enterPipeline_stmt(self, ctx:DaZeParser.Pipeline_stmtContext):
        pass

    # Exit a parse tree produced by DaZeParser#pipeline_stmt.
    def exitPipeline_stmt(self, ctx:DaZeParser.Pipeline_stmtContext):
        pass


    # Enter a parse tree produced by DaZeParser#llamada_stmt.
    def enterLlamada_stmt(self, ctx:DaZeParser.Llamada_stmtContext):
        pass

    # Exit a parse tree produced by DaZeParser#llamada_stmt.
    def exitLlamada_stmt(self, ctx:DaZeParser.Llamada_stmtContext):
        pass


    # Enter a parse tree produced by DaZeParser#graficar_stmt.
    def enterGraficar_stmt(self, ctx:DaZeParser.Graficar_stmtContext):
        pass

    # Exit a parse tree produced by DaZeParser#graficar_stmt.
    def exitGraficar_stmt(self, ctx:DaZeParser.Graficar_stmtContext):
        pass


    # Enter a parse tree produced by DaZeParser#tipo_grafico.
    def enterTipo_grafico(self, ctx:DaZeParser.Tipo_graficoContext):
        pass

    # Exit a parse tree produced by DaZeParser#tipo_grafico.
    def exitTipo_grafico(self, ctx:DaZeParser.Tipo_graficoContext):
        pass


    # Enter a parse tree produced by DaZeParser#configuracion_grafico.
    def enterConfiguracion_grafico(self, ctx:DaZeParser.Configuracion_graficoContext):
        pass

    # Exit a parse tree produced by DaZeParser#configuracion_grafico.
    def exitConfiguracion_grafico(self, ctx:DaZeParser.Configuracion_graficoContext):
        pass


    # Enter a parse tree produced by DaZeParser#guardar_stmt.
    def enterGuardar_stmt(self, ctx:DaZeParser.Guardar_stmtContext):
        pass

    # Exit a parse tree produced by DaZeParser#guardar_stmt.
    def exitGuardar_stmt(self, ctx:DaZeParser.Guardar_stmtContext):
        pass


    # Enter a parse tree produced by DaZeParser#mostrar_stmt.
    def enterMostrar_stmt(self, ctx:DaZeParser.Mostrar_stmtContext):
        pass

    # Exit a parse tree produced by DaZeParser#mostrar_stmt.
    def exitMostrar_stmt(self, ctx:DaZeParser.Mostrar_stmtContext):
        pass


    # Enter a parse tree produced by DaZeParser#si_stmt.
    def enterSi_stmt(self, ctx:DaZeParser.Si_stmtContext):
        pass

    # Exit a parse tree produced by DaZeParser#si_stmt.
    def exitSi_stmt(self, ctx:DaZeParser.Si_stmtContext):
        pass


    # Enter a parse tree produced by DaZeParser#funcion_stmt.
    def enterFuncion_stmt(self, ctx:DaZeParser.Funcion_stmtContext):
        pass

    # Exit a parse tree produced by DaZeParser#funcion_stmt.
    def exitFuncion_stmt(self, ctx:DaZeParser.Funcion_stmtContext):
        pass


    # Enter a parse tree produced by DaZeParser#retornar_stmt.
    def enterRetornar_stmt(self, ctx:DaZeParser.Retornar_stmtContext):
        pass

    # Exit a parse tree produced by DaZeParser#retornar_stmt.
    def exitRetornar_stmt(self, ctx:DaZeParser.Retornar_stmtContext):
        pass


    # Enter a parse tree produced by DaZeParser#lista_parametros.
    def enterLista_parametros(self, ctx:DaZeParser.Lista_parametrosContext):
        pass

    # Exit a parse tree produced by DaZeParser#lista_parametros.
    def exitLista_parametros(self, ctx:DaZeParser.Lista_parametrosContext):
        pass


    # Enter a parse tree produced by DaZeParser#operacion_pipeline.
    def enterOperacion_pipeline(self, ctx:DaZeParser.Operacion_pipelineContext):
        pass

    # Exit a parse tree produced by DaZeParser#operacion_pipeline.
    def exitOperacion_pipeline(self, ctx:DaZeParser.Operacion_pipelineContext):
        pass


    # Enter a parse tree produced by DaZeParser#op_convocar.
    def enterOp_convocar(self, ctx:DaZeParser.Op_convocarContext):
        pass

    # Exit a parse tree produced by DaZeParser#op_convocar.
    def exitOp_convocar(self, ctx:DaZeParser.Op_convocarContext):
        pass


    # Enter a parse tree produced by DaZeParser#op_descartar.
    def enterOp_descartar(self, ctx:DaZeParser.Op_descartarContext):
        pass

    # Exit a parse tree produced by DaZeParser#op_descartar.
    def exitOp_descartar(self, ctx:DaZeParser.Op_descartarContext):
        pass


    # Enter a parse tree produced by DaZeParser#op_contratar.
    def enterOp_contratar(self, ctx:DaZeParser.Op_contratarContext):
        pass

    # Exit a parse tree produced by DaZeParser#op_contratar.
    def exitOp_contratar(self, ctx:DaZeParser.Op_contratarContext):
        pass


    # Enter a parse tree produced by DaZeParser#op_rebautizar.
    def enterOp_rebautizar(self, ctx:DaZeParser.Op_rebautizarContext):
        pass

    # Exit a parse tree produced by DaZeParser#op_rebautizar.
    def exitOp_rebautizar(self, ctx:DaZeParser.Op_rebautizarContext):
        pass


    # Enter a parse tree produced by DaZeParser#op_clasificar.
    def enterOp_clasificar(self, ctx:DaZeParser.Op_clasificarContext):
        pass

    # Exit a parse tree produced by DaZeParser#op_clasificar.
    def exitOp_clasificar(self, ctx:DaZeParser.Op_clasificarContext):
        pass


    # Enter a parse tree produced by DaZeParser#op_alinear.
    def enterOp_alinear(self, ctx:DaZeParser.Op_alinearContext):
        pass

    # Exit a parse tree produced by DaZeParser#op_alinear.
    def exitOp_alinear(self, ctx:DaZeParser.Op_alinearContext):
        pass


    # Enter a parse tree produced by DaZeParser#op_balance.
    def enterOp_balance(self, ctx:DaZeParser.Op_balanceContext):
        pass

    # Exit a parse tree produced by DaZeParser#op_balance.
    def exitOp_balance(self, ctx:DaZeParser.Op_balanceContext):
        pass


    # Enter a parse tree produced by DaZeParser#op_reemplazar_bajas.
    def enterOp_reemplazar_bajas(self, ctx:DaZeParser.Op_reemplazar_bajasContext):
        pass

    # Exit a parse tree produced by DaZeParser#op_reemplazar_bajas.
    def exitOp_reemplazar_bajas(self, ctx:DaZeParser.Op_reemplazar_bajasContext):
        pass


    # Enter a parse tree produced by DaZeParser#op_depurar_plantilla.
    def enterOp_depurar_plantilla(self, ctx:DaZeParser.Op_depurar_plantillaContext):
        pass

    # Exit a parse tree produced by DaZeParser#op_depurar_plantilla.
    def exitOp_depurar_plantilla(self, ctx:DaZeParser.Op_depurar_plantillaContext):
        pass


    # Enter a parse tree produced by DaZeParser#op_top.
    def enterOp_top(self, ctx:DaZeParser.Op_topContext):
        pass

    # Exit a parse tree produced by DaZeParser#op_top.
    def exitOp_top(self, ctx:DaZeParser.Op_topContext):
        pass


    # Enter a parse tree produced by DaZeParser#op_personalizada.
    def enterOp_personalizada(self, ctx:DaZeParser.Op_personalizadaContext):
        pass

    # Exit a parse tree produced by DaZeParser#op_personalizada.
    def exitOp_personalizada(self, ctx:DaZeParser.Op_personalizadaContext):
        pass


    # Enter a parse tree produced by DaZeParser#argumentos_ordenar.
    def enterArgumentos_ordenar(self, ctx:DaZeParser.Argumentos_ordenarContext):
        pass

    # Exit a parse tree produced by DaZeParser#argumentos_ordenar.
    def exitArgumentos_ordenar(self, ctx:DaZeParser.Argumentos_ordenarContext):
        pass


    # Enter a parse tree produced by DaZeParser#argumentos_agrupar.
    def enterArgumentos_agrupar(self, ctx:DaZeParser.Argumentos_agruparContext):
        pass

    # Exit a parse tree produced by DaZeParser#argumentos_agrupar.
    def exitArgumentos_agrupar(self, ctx:DaZeParser.Argumentos_agruparContext):
        pass


    # Enter a parse tree produced by DaZeParser#lista_columnas.
    def enterLista_columnas(self, ctx:DaZeParser.Lista_columnasContext):
        pass

    # Exit a parse tree produced by DaZeParser#lista_columnas.
    def exitLista_columnas(self, ctx:DaZeParser.Lista_columnasContext):
        pass


    # Enter a parse tree produced by DaZeParser#lista_nombres_columna.
    def enterLista_nombres_columna(self, ctx:DaZeParser.Lista_nombres_columnaContext):
        pass

    # Exit a parse tree produced by DaZeParser#lista_nombres_columna.
    def exitLista_nombres_columna(self, ctx:DaZeParser.Lista_nombres_columnaContext):
        pass


    # Enter a parse tree produced by DaZeParser#nombre_columna.
    def enterNombre_columna(self, ctx:DaZeParser.Nombre_columnaContext):
        pass

    # Exit a parse tree produced by DaZeParser#nombre_columna.
    def exitNombre_columna(self, ctx:DaZeParser.Nombre_columnaContext):
        pass


    # Enter a parse tree produced by DaZeParser#lista_asignaciones.
    def enterLista_asignaciones(self, ctx:DaZeParser.Lista_asignacionesContext):
        pass

    # Exit a parse tree produced by DaZeParser#lista_asignaciones.
    def exitLista_asignaciones(self, ctx:DaZeParser.Lista_asignacionesContext):
        pass


    # Enter a parse tree produced by DaZeParser#asignacion_par.
    def enterAsignacion_par(self, ctx:DaZeParser.Asignacion_parContext):
        pass

    # Exit a parse tree produced by DaZeParser#asignacion_par.
    def exitAsignacion_par(self, ctx:DaZeParser.Asignacion_parContext):
        pass


    # Enter a parse tree produced by DaZeParser#lista_resumen.
    def enterLista_resumen(self, ctx:DaZeParser.Lista_resumenContext):
        pass

    # Exit a parse tree produced by DaZeParser#lista_resumen.
    def exitLista_resumen(self, ctx:DaZeParser.Lista_resumenContext):
        pass


    # Enter a parse tree produced by DaZeParser#resumen_par.
    def enterResumen_par(self, ctx:DaZeParser.Resumen_parContext):
        pass

    # Exit a parse tree produced by DaZeParser#resumen_par.
    def exitResumen_par(self, ctx:DaZeParser.Resumen_parContext):
        pass


    # Enter a parse tree produced by DaZeParser#funcion_agregacion.
    def enterFuncion_agregacion(self, ctx:DaZeParser.Funcion_agregacionContext):
        pass

    # Exit a parse tree produced by DaZeParser#funcion_agregacion.
    def exitFuncion_agregacion(self, ctx:DaZeParser.Funcion_agregacionContext):
        pass


    # Enter a parse tree produced by DaZeParser#argumentos_con_nombre.
    def enterArgumentos_con_nombre(self, ctx:DaZeParser.Argumentos_con_nombreContext):
        pass

    # Exit a parse tree produced by DaZeParser#argumentos_con_nombre.
    def exitArgumentos_con_nombre(self, ctx:DaZeParser.Argumentos_con_nombreContext):
        pass


    # Enter a parse tree produced by DaZeParser#argumento_con_nombre.
    def enterArgumento_con_nombre(self, ctx:DaZeParser.Argumento_con_nombreContext):
        pass

    # Exit a parse tree produced by DaZeParser#argumento_con_nombre.
    def exitArgumento_con_nombre(self, ctx:DaZeParser.Argumento_con_nombreContext):
        pass


    # Enter a parse tree produced by DaZeParser#lista_argumentos.
    def enterLista_argumentos(self, ctx:DaZeParser.Lista_argumentosContext):
        pass

    # Exit a parse tree produced by DaZeParser#lista_argumentos.
    def exitLista_argumentos(self, ctx:DaZeParser.Lista_argumentosContext):
        pass


    # Enter a parse tree produced by DaZeParser#argumento.
    def enterArgumento(self, ctx:DaZeParser.ArgumentoContext):
        pass

    # Exit a parse tree produced by DaZeParser#argumento.
    def exitArgumento(self, ctx:DaZeParser.ArgumentoContext):
        pass


    # Enter a parse tree produced by DaZeParser#ExprAgrupacion.
    def enterExprAgrupacion(self, ctx:DaZeParser.ExprAgrupacionContext):
        pass

    # Exit a parse tree produced by DaZeParser#ExprAgrupacion.
    def exitExprAgrupacion(self, ctx:DaZeParser.ExprAgrupacionContext):
        pass


    # Enter a parse tree produced by DaZeParser#ExprEntero.
    def enterExprEntero(self, ctx:DaZeParser.ExprEnteroContext):
        pass

    # Exit a parse tree produced by DaZeParser#ExprEntero.
    def exitExprEntero(self, ctx:DaZeParser.ExprEnteroContext):
        pass


    # Enter a parse tree produced by DaZeParser#ExprMulDivMod.
    def enterExprMulDivMod(self, ctx:DaZeParser.ExprMulDivModContext):
        pass

    # Exit a parse tree produced by DaZeParser#ExprMulDivMod.
    def exitExprMulDivMod(self, ctx:DaZeParser.ExprMulDivModContext):
        pass


    # Enter a parse tree produced by DaZeParser#ExprRelacional.
    def enterExprRelacional(self, ctx:DaZeParser.ExprRelacionalContext):
        pass

    # Exit a parse tree produced by DaZeParser#ExprRelacional.
    def exitExprRelacional(self, ctx:DaZeParser.ExprRelacionalContext):
        pass


    # Enter a parse tree produced by DaZeParser#ExprIgualdad.
    def enterExprIgualdad(self, ctx:DaZeParser.ExprIgualdadContext):
        pass

    # Exit a parse tree produced by DaZeParser#ExprIgualdad.
    def exitExprIgualdad(self, ctx:DaZeParser.ExprIgualdadContext):
        pass


    # Enter a parse tree produced by DaZeParser#ExprDiccionario.
    def enterExprDiccionario(self, ctx:DaZeParser.ExprDiccionarioContext):
        pass

    # Exit a parse tree produced by DaZeParser#ExprDiccionario.
    def exitExprDiccionario(self, ctx:DaZeParser.ExprDiccionarioContext):
        pass


    # Enter a parse tree produced by DaZeParser#ExprCadena.
    def enterExprCadena(self, ctx:DaZeParser.ExprCadenaContext):
        pass

    # Exit a parse tree produced by DaZeParser#ExprCadena.
    def exitExprCadena(self, ctx:DaZeParser.ExprCadenaContext):
        pass


    # Enter a parse tree produced by DaZeParser#ExprIdentificador.
    def enterExprIdentificador(self, ctx:DaZeParser.ExprIdentificadorContext):
        pass

    # Exit a parse tree produced by DaZeParser#ExprIdentificador.
    def exitExprIdentificador(self, ctx:DaZeParser.ExprIdentificadorContext):
        pass


    # Enter a parse tree produced by DaZeParser#ExprPotencia.
    def enterExprPotencia(self, ctx:DaZeParser.ExprPotenciaContext):
        pass

    # Exit a parse tree produced by DaZeParser#ExprPotencia.
    def exitExprPotencia(self, ctx:DaZeParser.ExprPotenciaContext):
        pass


    # Enter a parse tree produced by DaZeParser#ExprUnaria.
    def enterExprUnaria(self, ctx:DaZeParser.ExprUnariaContext):
        pass

    # Exit a parse tree produced by DaZeParser#ExprUnaria.
    def exitExprUnaria(self, ctx:DaZeParser.ExprUnariaContext):
        pass


    # Enter a parse tree produced by DaZeParser#ExprLogicaY.
    def enterExprLogicaY(self, ctx:DaZeParser.ExprLogicaYContext):
        pass

    # Exit a parse tree produced by DaZeParser#ExprLogicaY.
    def exitExprLogicaY(self, ctx:DaZeParser.ExprLogicaYContext):
        pass


    # Enter a parse tree produced by DaZeParser#ExprLlamada.
    def enterExprLlamada(self, ctx:DaZeParser.ExprLlamadaContext):
        pass

    # Exit a parse tree produced by DaZeParser#ExprLlamada.
    def exitExprLlamada(self, ctx:DaZeParser.ExprLlamadaContext):
        pass


    # Enter a parse tree produced by DaZeParser#ExprLista.
    def enterExprLista(self, ctx:DaZeParser.ExprListaContext):
        pass

    # Exit a parse tree produced by DaZeParser#ExprLista.
    def exitExprLista(self, ctx:DaZeParser.ExprListaContext):
        pass


    # Enter a parse tree produced by DaZeParser#ExprSumaResta.
    def enterExprSumaResta(self, ctx:DaZeParser.ExprSumaRestaContext):
        pass

    # Exit a parse tree produced by DaZeParser#ExprSumaResta.
    def exitExprSumaResta(self, ctx:DaZeParser.ExprSumaRestaContext):
        pass


    # Enter a parse tree produced by DaZeParser#ExprLogicaO.
    def enterExprLogicaO(self, ctx:DaZeParser.ExprLogicaOContext):
        pass

    # Exit a parse tree produced by DaZeParser#ExprLogicaO.
    def exitExprLogicaO(self, ctx:DaZeParser.ExprLogicaOContext):
        pass


    # Enter a parse tree produced by DaZeParser#ExprDecimal.
    def enterExprDecimal(self, ctx:DaZeParser.ExprDecimalContext):
        pass

    # Exit a parse tree produced by DaZeParser#ExprDecimal.
    def exitExprDecimal(self, ctx:DaZeParser.ExprDecimalContext):
        pass


    # Enter a parse tree produced by DaZeParser#ExprFalso.
    def enterExprFalso(self, ctx:DaZeParser.ExprFalsoContext):
        pass

    # Exit a parse tree produced by DaZeParser#ExprFalso.
    def exitExprFalso(self, ctx:DaZeParser.ExprFalsoContext):
        pass


    # Enter a parse tree produced by DaZeParser#ExprVerdadero.
    def enterExprVerdadero(self, ctx:DaZeParser.ExprVerdaderoContext):
        pass

    # Exit a parse tree produced by DaZeParser#ExprVerdadero.
    def exitExprVerdadero(self, ctx:DaZeParser.ExprVerdaderoContext):
        pass


    # Enter a parse tree produced by DaZeParser#ExprNulo.
    def enterExprNulo(self, ctx:DaZeParser.ExprNuloContext):
        pass

    # Exit a parse tree produced by DaZeParser#ExprNulo.
    def exitExprNulo(self, ctx:DaZeParser.ExprNuloContext):
        pass


    # Enter a parse tree produced by DaZeParser#ExprIndexacion.
    def enterExprIndexacion(self, ctx:DaZeParser.ExprIndexacionContext):
        pass

    # Exit a parse tree produced by DaZeParser#ExprIndexacion.
    def exitExprIndexacion(self, ctx:DaZeParser.ExprIndexacionContext):
        pass


    # Enter a parse tree produced by DaZeParser#ExprFichar.
    def enterExprFichar(self, ctx:DaZeParser.ExprFicharContext):
        pass

    # Exit a parse tree produced by DaZeParser#ExprFichar.
    def exitExprFichar(self, ctx:DaZeParser.ExprFicharContext):
        pass


    # Enter a parse tree produced by DaZeParser#lista_expr.
    def enterLista_expr(self, ctx:DaZeParser.Lista_exprContext):
        pass

    # Exit a parse tree produced by DaZeParser#lista_expr.
    def exitLista_expr(self, ctx:DaZeParser.Lista_exprContext):
        pass


    # Enter a parse tree produced by DaZeParser#lista_diccionario.
    def enterLista_diccionario(self, ctx:DaZeParser.Lista_diccionarioContext):
        pass

    # Exit a parse tree produced by DaZeParser#lista_diccionario.
    def exitLista_diccionario(self, ctx:DaZeParser.Lista_diccionarioContext):
        pass


    # Enter a parse tree produced by DaZeParser#par_diccionario.
    def enterPar_diccionario(self, ctx:DaZeParser.Par_diccionarioContext):
        pass

    # Exit a parse tree produced by DaZeParser#par_diccionario.
    def exitPar_diccionario(self, ctx:DaZeParser.Par_diccionarioContext):
        pass


    # Enter a parse tree produced by DaZeParser#identificador.
    def enterIdentificador(self, ctx:DaZeParser.IdentificadorContext):
        pass

    # Exit a parse tree produced by DaZeParser#identificador.
    def exitIdentificador(self, ctx:DaZeParser.IdentificadorContext):
        pass



del DaZeParser