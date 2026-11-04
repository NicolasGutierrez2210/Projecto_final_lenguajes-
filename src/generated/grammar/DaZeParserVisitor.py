# Generated from grammar/DaZeParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .DaZeParser import DaZeParser
else:
    from DaZeParser import DaZeParser

# This class defines a complete generic visitor for a parse tree produced by DaZeParser.

class DaZeParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by DaZeParser#programa.
    def visitPrograma(self, ctx:DaZeParser.ProgramaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#sentencia.
    def visitSentencia(self, ctx:DaZeParser.SentenciaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#asignacion.
    def visitAsignacion(self, ctx:DaZeParser.AsignacionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#asignacion_indexada.
    def visitAsignacion_indexada(self, ctx:DaZeParser.Asignacion_indexadaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#bucle_mientras_stmt.
    def visitBucle_mientras_stmt(self, ctx:DaZeParser.Bucle_mientras_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#bucle_para_stmt.
    def visitBucle_para_stmt(self, ctx:DaZeParser.Bucle_para_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#pipeline_stmt.
    def visitPipeline_stmt(self, ctx:DaZeParser.Pipeline_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#llamada_stmt.
    def visitLlamada_stmt(self, ctx:DaZeParser.Llamada_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#graficar_stmt.
    def visitGraficar_stmt(self, ctx:DaZeParser.Graficar_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#tipo_grafico.
    def visitTipo_grafico(self, ctx:DaZeParser.Tipo_graficoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#configuracion_grafico.
    def visitConfiguracion_grafico(self, ctx:DaZeParser.Configuracion_graficoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#guardar_stmt.
    def visitGuardar_stmt(self, ctx:DaZeParser.Guardar_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#mostrar_stmt.
    def visitMostrar_stmt(self, ctx:DaZeParser.Mostrar_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#si_stmt.
    def visitSi_stmt(self, ctx:DaZeParser.Si_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#funcion_stmt.
    def visitFuncion_stmt(self, ctx:DaZeParser.Funcion_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#retornar_stmt.
    def visitRetornar_stmt(self, ctx:DaZeParser.Retornar_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#lista_parametros.
    def visitLista_parametros(self, ctx:DaZeParser.Lista_parametrosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#operacion_pipeline.
    def visitOperacion_pipeline(self, ctx:DaZeParser.Operacion_pipelineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#op_convocar.
    def visitOp_convocar(self, ctx:DaZeParser.Op_convocarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#op_descartar.
    def visitOp_descartar(self, ctx:DaZeParser.Op_descartarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#op_contratar.
    def visitOp_contratar(self, ctx:DaZeParser.Op_contratarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#op_rebautizar.
    def visitOp_rebautizar(self, ctx:DaZeParser.Op_rebautizarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#op_clasificar.
    def visitOp_clasificar(self, ctx:DaZeParser.Op_clasificarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#op_alinear.
    def visitOp_alinear(self, ctx:DaZeParser.Op_alinearContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#op_balance.
    def visitOp_balance(self, ctx:DaZeParser.Op_balanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#op_reemplazar_bajas.
    def visitOp_reemplazar_bajas(self, ctx:DaZeParser.Op_reemplazar_bajasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#op_depurar_plantilla.
    def visitOp_depurar_plantilla(self, ctx:DaZeParser.Op_depurar_plantillaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#op_top.
    def visitOp_top(self, ctx:DaZeParser.Op_topContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#op_personalizada.
    def visitOp_personalizada(self, ctx:DaZeParser.Op_personalizadaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#argumentos_ordenar.
    def visitArgumentos_ordenar(self, ctx:DaZeParser.Argumentos_ordenarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#argumentos_agrupar.
    def visitArgumentos_agrupar(self, ctx:DaZeParser.Argumentos_agruparContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#lista_columnas.
    def visitLista_columnas(self, ctx:DaZeParser.Lista_columnasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#lista_nombres_columna.
    def visitLista_nombres_columna(self, ctx:DaZeParser.Lista_nombres_columnaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#nombre_columna.
    def visitNombre_columna(self, ctx:DaZeParser.Nombre_columnaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#lista_asignaciones.
    def visitLista_asignaciones(self, ctx:DaZeParser.Lista_asignacionesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#asignacion_par.
    def visitAsignacion_par(self, ctx:DaZeParser.Asignacion_parContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#lista_resumen.
    def visitLista_resumen(self, ctx:DaZeParser.Lista_resumenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#resumen_par.
    def visitResumen_par(self, ctx:DaZeParser.Resumen_parContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#funcion_agregacion.
    def visitFuncion_agregacion(self, ctx:DaZeParser.Funcion_agregacionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#argumentos_con_nombre.
    def visitArgumentos_con_nombre(self, ctx:DaZeParser.Argumentos_con_nombreContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#argumento_con_nombre.
    def visitArgumento_con_nombre(self, ctx:DaZeParser.Argumento_con_nombreContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#lista_argumentos.
    def visitLista_argumentos(self, ctx:DaZeParser.Lista_argumentosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#argumento.
    def visitArgumento(self, ctx:DaZeParser.ArgumentoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#ExprAgrupacion.
    def visitExprAgrupacion(self, ctx:DaZeParser.ExprAgrupacionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#ExprEntero.
    def visitExprEntero(self, ctx:DaZeParser.ExprEnteroContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#ExprMulDivMod.
    def visitExprMulDivMod(self, ctx:DaZeParser.ExprMulDivModContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#ExprRelacional.
    def visitExprRelacional(self, ctx:DaZeParser.ExprRelacionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#ExprIgualdad.
    def visitExprIgualdad(self, ctx:DaZeParser.ExprIgualdadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#ExprDiccionario.
    def visitExprDiccionario(self, ctx:DaZeParser.ExprDiccionarioContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#ExprCadena.
    def visitExprCadena(self, ctx:DaZeParser.ExprCadenaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#ExprIdentificador.
    def visitExprIdentificador(self, ctx:DaZeParser.ExprIdentificadorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#ExprPotencia.
    def visitExprPotencia(self, ctx:DaZeParser.ExprPotenciaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#ExprUnaria.
    def visitExprUnaria(self, ctx:DaZeParser.ExprUnariaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#ExprLogicaY.
    def visitExprLogicaY(self, ctx:DaZeParser.ExprLogicaYContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#ExprLlamada.
    def visitExprLlamada(self, ctx:DaZeParser.ExprLlamadaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#ExprLista.
    def visitExprLista(self, ctx:DaZeParser.ExprListaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#ExprSumaResta.
    def visitExprSumaResta(self, ctx:DaZeParser.ExprSumaRestaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#ExprLogicaO.
    def visitExprLogicaO(self, ctx:DaZeParser.ExprLogicaOContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#ExprDecimal.
    def visitExprDecimal(self, ctx:DaZeParser.ExprDecimalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#ExprFalso.
    def visitExprFalso(self, ctx:DaZeParser.ExprFalsoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#ExprVerdadero.
    def visitExprVerdadero(self, ctx:DaZeParser.ExprVerdaderoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#ExprNulo.
    def visitExprNulo(self, ctx:DaZeParser.ExprNuloContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#ExprIndexacion.
    def visitExprIndexacion(self, ctx:DaZeParser.ExprIndexacionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#ExprFichar.
    def visitExprFichar(self, ctx:DaZeParser.ExprFicharContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#lista_expr.
    def visitLista_expr(self, ctx:DaZeParser.Lista_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#lista_diccionario.
    def visitLista_diccionario(self, ctx:DaZeParser.Lista_diccionarioContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#par_diccionario.
    def visitPar_diccionario(self, ctx:DaZeParser.Par_diccionarioContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DaZeParser#identificador.
    def visitIdentificador(self, ctx:DaZeParser.IdentificadorContext):
        return self.visitChildren(ctx)



del DaZeParser