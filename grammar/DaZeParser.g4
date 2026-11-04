parser grammar DaZeParser;

options { tokenVocab=DaZeLexer; }

programa
    : sentencia* EOF
    ;

sentencia
    : asignacion_indexada
    | asignacion
    | bucle_mientras_stmt
    | bucle_para_stmt
    | pipeline_stmt
    | graficar_stmt
    | guardar_stmt
    | mostrar_stmt
    | si_stmt
    | funcion_stmt
    | retornar_stmt
    | llamada_stmt
    ;

asignacion
    : identificador ASIGNAR expr PUNTO_Y_COMA?
    ;

asignacion_indexada
    : identificador LBRACK expr RBRACK ASIGNAR expr PUNTO_Y_COMA?
    ;

bucle_mientras_stmt
    : EN_JUEGO LPAREN expr RPAREN LBRACE sentencia* RBRACE PUNTO_Y_COMA?
    ;

bucle_para_stmt
    : RONDA LPAREN identificador EN expr RPAREN LBRACE sentencia* RBRACE PUNTO_Y_COMA?
    ;

pipeline_stmt
    : (identificador ASIGNAR)? expr (PIPE operacion_pipeline)+ PUNTO_Y_COMA?
    ;

llamada_stmt
    : identificador LPAREN lista_argumentos? RPAREN PUNTO_Y_COMA?
    ;

graficar_stmt
    : PIZARRA tipo_grafico LPAREN expr RPAREN LBRACE configuracion_grafico* RBRACE PUNTO_Y_COMA?
    | PIZARRA tipo_grafico LPAREN expr RPAREN PUNTO_Y_COMA?
    ;

tipo_grafico
    : BARRAS
    | LINEAS
    | HISTOGRAMA
    | DISPERSION
    | CAJA
    ;

configuracion_grafico
    : identificador ASIGNAR expr PUNTO_Y_COMA?
    ;

guardar_stmt
    : ARCHIVAR LPAREN expr COMA EN ASIGNAR CADENA (COMA argumentos_con_nombre)? RPAREN PUNTO_Y_COMA?
    | ARCHIVAR LPAREN expr COMA CADENA (COMA argumentos_con_nombre)? RPAREN PUNTO_Y_COMA?
    | ARCHIVAR expr EN CADENA (COMO identificador)? PUNTO_Y_COMA?
    ;

mostrar_stmt
    : PROYECTAR LPAREN expr RPAREN PUNTO_Y_COMA?
    ;

si_stmt
    : SI LPAREN expr RPAREN LBRACE sentencia* RBRACE (SINO LBRACE sentencia* RBRACE)? PUNTO_Y_COMA?
    ;

funcion_stmt
    : TACTICA identificador LPAREN lista_parametros? RPAREN LBRACE sentencia* RBRACE PUNTO_Y_COMA?
    ;

retornar_stmt
    : RESULTADO expr? PUNTO_Y_COMA?
    ;

lista_parametros
    : identificador (COMA identificador)*
    ;

operacion_pipeline
    : op_convocar
    | op_descartar
    | op_contratar
    | op_rebautizar
    | op_clasificar
    | op_alinear
    | op_balance
    | op_reemplazar_bajas
    | op_depurar_plantilla
    | op_top
    | op_personalizada
    ;

op_convocar
    : CONVOCAR LPAREN lista_columnas RPAREN
    ;

op_descartar
    : DESCARTAR LPAREN expr RPAREN
    | DESCARTAR DONDE expr
    ;

op_contratar
    : CONTRATAR LPAREN lista_asignaciones RPAREN
    ;

op_rebautizar
    : REBAUTIZAR LPAREN lista_asignaciones RPAREN
    ;

op_clasificar
    : CLASIFICAR LPAREN argumentos_ordenar RPAREN
    ;

op_alinear
    : ALINEAR LPAREN argumentos_agrupar RPAREN
    | ALINEAR POR LBRACK lista_columnas RBRACK
    | ALINEAR POR lista_columnas
    ;

op_balance
    : BALANCE LPAREN lista_resumen RPAREN
    ;

op_reemplazar_bajas
    : REEMPLAZAR_BAJAS LPAREN argumentos_con_nombre RPAREN
    ;

op_depurar_plantilla
    : DEPURAR_PLANTILLA LPAREN (argumentos_con_nombre | lista_columnas)? RPAREN
    ;

op_top
    : TOP LPAREN ENTERO RPAREN
    ;

op_personalizada
    : identificador LPAREN lista_argumentos? RPAREN
    ;

argumentos_ordenar
    : lista_argumentos
    ;

argumentos_agrupar
    : lista_argumentos
    ;

lista_columnas
    : LBRACK lista_nombres_columna? RBRACK
    | lista_nombres_columna
    ;

lista_nombres_columna
    : nombre_columna (COMA nombre_columna)*
    ;

nombre_columna
    : identificador
    | CADENA
    ;

lista_asignaciones
    : asignacion_par (COMA asignacion_par)*
    ;

asignacion_par
    : identificador ASIGNAR expr
    ;

lista_resumen
    : resumen_par (COMA resumen_par)*
    ;

resumen_par
    : identificador ASIGNAR (funcion_agregacion | expr)
    ;

funcion_agregacion
    : CONTAR LPAREN RPAREN
    | (SUMA | MEDIA | MEDIANA | MINIMO | MAXIMO | DESV_STD) LPAREN (identificador | CADENA) RPAREN
    ;

argumentos_con_nombre
    : argumento_con_nombre (COMA argumento_con_nombre)*
    ;

argumento_con_nombre
    : identificador ASIGNAR expr
    ;

lista_argumentos
    : argumento (COMA argumento)*
    ;

argumento
    : identificador ASIGNAR expr
    | expr
    ;

expr
    : expr POT expr                                             # ExprPotencia
    | (MAS | MENOS | NO) expr                                   # ExprUnaria
    | expr (MULT | DIV | MOD) expr                              # ExprMulDivMod
    | expr (MAS | MENOS) expr                                   # ExprSumaResta
    | expr (MAYOR | MENOR | MAYOR_IGUAL | MENOR_IGUAL) expr      # ExprRelacional
    | expr (IGUAL_IGUAL | DIFERENTE) expr                       # ExprIgualdad
    | expr Y expr                                               # ExprLogicaY
    | expr O expr                                               # ExprLogicaO
    | FICHAR LPAREN CADENA (COMA argumentos_con_nombre)? RPAREN # ExprFichar
    | identificador LPAREN lista_argumentos? RPAREN             # ExprLlamada
    | expr LBRACK expr RBRACK                                   # ExprIndexacion
    | LBRACK lista_expr? RBRACK                                 # ExprLista
    | LBRACE lista_diccionario? RBRACE                          # ExprDiccionario
    | LPAREN expr RPAREN                                        # ExprAgrupacion
    | identificador                                             # ExprIdentificador
    | ENTERO                                                    # ExprEntero
    | DECIMAL                                                   # ExprDecimal
    | CADENA                                                    # ExprCadena
    | VERDADERO                                                 # ExprVerdadero
    | FALSO                                                     # ExprFalso
    | NULO                                                      # ExprNulo
    ;

lista_expr
    : expr (COMA expr)*
    ;

lista_diccionario
    : par_diccionario (COMA par_diccionario)*
    ;

par_diccionario
    : (identificador | CADENA | ENTERO) DOS_PUNTOS expr
    ;

identificador
    : ID
    | Y
    | O
    | NO
    | POR
    | EN
    | COMO
    | DONDE
    | ASCENDENTE
    | DESCENDENTE
    | MAXIMO
    | MINIMO
    | MEDIA
    | MEDIANA
    | SUMA
    | CONTAR
    | DESV_STD
    | BARRAS
    | LINEAS
    | HISTOGRAMA
    | DISPERSION
    | CAJA
    | ARCHIVAR
    | FICHAR
    | CONVOCAR
    | DESCARTAR
    | CONTRATAR
    | REBAUTIZAR
    | CLASIFICAR
    | ALINEAR
    | BALANCE
    | REEMPLAZAR_BAJAS
    | DEPURAR_PLANTILLA
    | TOP
    | PIZARRA
    | PROYECTAR
    | RESULTADO
    | TACTICA
    | EN_JUEGO
    | RONDA
    ;
