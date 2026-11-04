lexer grammar DaZeLexer;

// Palabras reservadas principales (Dominio Deportivo)
FICHAR: 'fichar';
ARCHIVAR: 'archivar';
CONVOCAR: 'convocar';
DESCARTAR: 'descartar';
CONTRATAR: 'contratar';
REBAUTIZAR: 'rebautizar';
CLASIFICAR: 'clasificar';
ALINEAR: 'alinear';
BALANCE: 'balance';
REEMPLAZAR_BAJAS: 'sanear' | 'recuperar' | 'reemplazar_bajas';
DEPURAR_PLANTILLA: 'depurar' | 'limpiar' | 'depurar_plantilla';
TOP: 'top';
PIZARRA: 'pizarra';
PROYECTAR: 'proyectar';
RESULTADO: 'resultado';
TACTICA: 'tactica';
SI: 'si';
SINO: 'sino';

// Ciclos y estructuras (Corte 3)
EN_JUEGO: 'en_juego';
RONDA: 'ronda';

// Modificadores y conectores
EN: 'en';
POR: 'por';
DONDE: 'donde';
COMO: 'como';
ASCENDENTE: 'ascendente';
DESCENDENTE: 'descendente';

// Funciones de agregacion
CONTAR: 'contar' | 'conteo';
SUMA: 'suma';
MEDIA: 'media' | 'promedio';
MEDIANA: 'mediana';
MINIMO: 'minimo' | 'min';
MAXIMO: 'maximo' | 'max';
DESV_STD: 'desviar' | 'desviacion' | 'desv_std';

// Tipos de graficos
BARRAS: 'barras';
LINEAS: 'lineas';
HISTOGRAMA: 'histograma';
DISPERSION: 'dispersion';
CAJA: 'caja';

// Literales logicos y especiales
VERDADERO: 'verdadero' | 'true';
FALSO: 'falso' | 'false';
NULO: 'nulo' | 'null';

// Operadores logicos
Y: 'y' | 'and' | '&&';
O: 'o' | 'or' | '||';
NO: 'no' | 'not' | '!';

// Operadores de pipeline y asignacion
PIPE: '|>';
ASIGNAR: '=';

// Operadores relacionales
IGUAL_IGUAL: '==';
DIFERENTE: '!=';
MAYOR_IGUAL: '>=';
MENOR_IGUAL: '<=';
MAYOR: '>';
MENOR: '<';

// Operadores aritmeticos
POT: '^' | '**';
MAS: '+';
MENOS: '-';
MULT: '*';
DIV: '/';
MOD: '%';

// Delimitadores y puntuacion
LPAREN: '(';
RPAREN: ')';
LBRACK: '[';
RBRACK: ']';
LBRACE: '{';
RBRACE: '}';
COMA: ',';
PUNTO_Y_COMA: ';';
DOS_PUNTOS: ':';

// Literales y tokens complejos
DECIMAL: [0-9]+ '.' [0-9]+;
ENTERO: [0-9]+;
CADENA: '"' (~["\\\r\n] | '\\' .)* '"' | '\'' (~['\\\r\n] | '\\' .)* '\'';
ID: [a-zA-Z_][a-zA-Z0-9_]*;

// Comentarios y espacios
COMENTARIO_LINEA: ('#' | '//') ~[\r\n]* -> skip;
COMENTARIO_BLOQUE: '/*' .*? '*/' -> skip;
WS: [ \t\r\n]+ -> skip;
