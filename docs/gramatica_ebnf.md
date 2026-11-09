# Gramatica EBNF de DaZe - Sports Analytics DSL

A continuacion se presenta la especificacion sintactica formal de DaZe adaptada al dominio deportivo en formato EBNF (Extended Backus-Naur Form).

```ebnf
programa            ::= { sentencia } EOF ;

sentencia           ::= asignacion
                      | asignacion_indexada
                      | bucle_mientras_stmt
                      | bucle_para_stmt
                      | pipeline_stmt
                      | graficar_stmt
                      | guardar_stmt
                      | mostrar_stmt
                      | si_stmt
                      | funcion_stmt
                      | retornar_stmt
                      | llamada_stmt ;

asignacion          ::= identificador '=' expr [ ';' ] ;

asignacion_indexada ::= identificador '[' expr ']' '=' expr [ ';' ] ;

bucle_mientras_stmt ::= 'en_juego' '(' expr ')' '{' { sentencia } '}' [ ';' ] ;

bucle_para_stmt     ::= 'ronda' '(' identificador 'en' expr ')' '{' { sentencia } '}' [ ';' ] ;

pipeline_stmt       ::= [ identificador '=' ] expr { '|>' operacion_pipeline }+ [ ';' ] ;

llamada_stmt        ::= identificador '(' [ lista_argumentos ] ')' [ ';' ] ;

graficar_stmt       ::= 'pizarra' tipo_grafico '(' expr ')' '{' { configuracion_grafico } '}' [ ';' ]
                      | 'pizarra' tipo_grafico '(' expr ')' [ ';' ] ;

tipo_grafico        ::= 'barras' | 'lineas' | 'histograma' | 'dispersion' | 'caja' ;

configuracion_grafico ::= identificador '=' expr [ ';' ] ;

guardar_stmt        ::= 'archivar' '(' expr ',' 'en' '=' CADENA [ ',' argumentos_con_nombre ] ')' [ ';' ]
                      | 'archivar' '(' expr ',' CADENA [ ',' argumentos_con_nombre ] ')' [ ';' ]
                      | 'archivar' expr 'en' CADENA [ 'como' identificador ] [ ';' ] ;

mostrar_stmt        ::= 'proyectar' '(' expr ')' [ ';' ] ;

si_stmt             ::= 'si' '(' expr ')' '{' { sentencia } '}' [ 'sino' '{' { sentencia } '}' ] [ ';' ] ;

funcion_stmt        ::= 'tactica' identificador '(' [ lista_parametros ] ')' '{' { sentencia } '}' [ ';' ] ;

retornar_stmt       ::= 'resultado' [ expr ] [ ';' ] ;

lista_parametros    ::= identificador { ',' identificador } ;

operacion_pipeline  ::= op_convocar
                      | op_descartar
                      | op_contratar
                      | op_rebautizar
                      | op_clasificar
                      | op_alinear
                      | op_balance
                      | op_reemplazar_bajas
                      | op_depurar_plantilla
                      | op_top
                      | op_personalizada ;

op_convocar         ::= 'convocar' '(' lista_columnas ')' ;
op_descartar        ::= 'descartar' '(' expr ')' | 'descartar' 'donde' expr ;
op_contratar        ::= 'contratar' '(' lista_asignaciones ')' ;
op_rebautizar       ::= 'rebautizar' '(' lista_asignaciones ')' ;
op_clasificar       ::= 'clasificar' '(' argumentos_ordenar ')' ;
op_alinear          ::= 'alinear' '(' argumentos_agrupar ')' | 'alinear' 'por' [ '[' ] lista_columnas [ ']' ] ;
op_balance          ::= 'balance' '(' lista_resumen ')' ;
op_reemplazar_bajas ::= ( 'sanear' | 'recuperar' | 'reemplazar_bajas' ) '(' argumentos_con_nombre ')' ;
op_depurar_plantilla ::= ( 'depurar' | 'limpiar' | 'depurar_plantilla' ) '(' [ argumentos_con_nombre | lista_columnas ] ')' ;
op_top              ::= 'top' '(' ENTERO ')' ;
op_personalizada    ::= identificador '(' [ lista_argumentos ] ')' ;

argumentos_ordenar  ::= lista_argumentos ;
argumentos_agrupar  ::= lista_argumentos ;

lista_columnas      ::= '[' [ lista_nombres_columna ] ']' | lista_nombres_columna ;
lista_nombres_columna ::= nombre_columna { ',' nombre_columna } ;
nombre_columna      ::= identificador | CADENA ;

lista_asignaciones  ::= asignacion_par { ',' asignacion_par } ;
asignacion_par      ::= identificador '=' expr ;

lista_resumen       ::= resumen_par { ',' resumen_par } ;
resumen_par         ::= identificador '=' ( funcion_agregacion | expr ) ;

funcion_agregacion  ::= ( 'contar' | 'conteo' ) '(' ')'
                      | ( 'suma' | 'media' | 'promedio' | 'mediana' | 'minimo' | 'min' | 'maximo' | 'max' | 'desviar' | 'desviacion' | 'desv_std' ) '(' ( identificador | CADENA ) ')' ;

argumentos_con_nombre ::= argumento_con_nombre { ',' argumento_con_nombre } ;
argumento_con_nombre  ::= identificador '=' expr ;

lista_argumentos    ::= argumento { ',' argumento } ;
argumento           ::= identificador '=' expr | expr ;

expr                ::= expr ( '^' | '**' ) expr
                      | ( '+' | '-' | 'no' | 'not' | '!' ) expr
                      | expr ( '*' | '/' | '%' ) expr
                      | expr ( '+' | '-' ) expr
                      | expr ( '>' | '<' | '>=' | '<=' ) expr
                      | expr ( '==' | '!=' ) expr
                      | expr ( 'y' | 'and' | '&&' ) expr
                      | expr ( 'o' | 'or' | '||' ) expr
                      | 'fichar' '(' CADENA [ ',' argumentos_con_nombre ] ')'
                      | identificador '(' [ lista_argumentos ] ')'
                      | expr '[' expr ']'
                      | '{' [ lista_diccionario ] '}'
                      | '[' [ lista_expr ] ']'
                      | '(' expr ')'
                      | identificador
                      | ENTERO
                      | DECIMAL
                      | CADENA
                      | ( 'verdadero' | 'true' )
                      | ( 'falso' | 'false' )
                      | ( 'nulo' | 'null' ) ;

lista_diccionario   ::= par_diccionario { ',' par_diccionario } ;
par_diccionario     ::= ( identificador | CADENA ) ':' expr ;

lista_expr          ::= expr { ',' expr } ;

identificador       ::= ID | PALABRA_CLAVE_PERMITIDA ;
```
