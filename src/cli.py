import os
import sys

# 1. Asegurar ruta raíz del proyecto
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

try:
    import readline
except ImportError:
    pass

from antlr4 import InputStream, CommonTokenStream
from src.generated.DaZeLexer import DaZeLexer
from src.generated.DaZeParser import DaZeParser
from src.errors import DaZeErrorListener
from src.semantic.visitor import DaZeSemanticVisitor

# 2. Importación robusta del visualizador de árbol
def renderizar_arbol(tree, parser):
    try:
        import src.tree_viewer as tv
        for fn in ["imprimir_arbol_consola", "print_tree", "imprimir_arbol", "render_tree"]:
            if hasattr(tv, fn):
                f = getattr(tv, fn)
                try:
                    return f(tree, parser)
                except TypeError:
                    return f(tree)
        print(tree.toStringTree(recog=parser))
    except Exception:
        print(tree.toStringTree(recog=parser))

BANNER = """
╔══════════════════════════════════════════════════════════════════════╗
║                 DaZe: Sports Analytics DSL - v1.0.0                  ║
║                  Consola Interactiva (REPL Oficial)                  ║
║   Escribe código DaZe, 'ayuda' para comandos o 'salir' para terminar ║
╚══════════════════════════════════════════════════════════════════════╝"""

def ejecutar_bloque(codigo_fuente, visitor):
    codigo_limpio = codigo_fuente.strip()
    if not codigo_limpio:
        return

    input_stream = InputStream(codigo_fuente)
    lexer = DaZeLexer(input_stream)
    error_listener = DaZeErrorListener()
    lexer.removeErrorListeners()
    lexer.addErrorListener(error_listener)

    token_stream = CommonTokenStream(lexer)
    parser = DaZeParser(token_stream)
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)

    tree = parser.programa()

    if error_listener.has_errors():
        for err in error_listener.get_errors():
            print(f"[Error {err.error_type}] Línea {err.line}:{err.column} -> {err.message}")
        return

    try:
        resultado = visitor.visit(tree)
        if resultado is not None and not codigo_limpio.endswith(";"):
            print(f"=> {resultado}")
    except Exception as e:
        print(f"[Error Semántico] {str(e)}")

def iniciar_repl():
    print(BANNER)
    visitor = DaZeSemanticVisitor()
    buffer_codigo = []
    nivel_llaves = 0

    while True:
        try:
            prompt = "daze> " if nivel_llaves == 0 else "...   "
            linea = input(prompt)
            linea_limpia = linea.strip()

            if nivel_llaves == 0:
                if linea_limpia in ("salir", "exit", "quit"):
                    print("Cerrando sesión de DaZe. ¡Hasta pronto!")
                    break

                if linea_limpia in ("limpiar", "clear"):
                    os.system("clear" if os.name != "nt" else "cls")
                    print(BANNER)
                    continue

                if linea_limpia in ("ayuda", "help"):
                    print("""
Comandos de la consola:
  salir / exit      : Cierra la consola interactiva.
  limpiar / clear   : Limpia la pantalla de la terminal.
  simbolos          : Lista las variables y tablas cargadas en memoria.
  ayuda / help      : Muestra este menú de ayuda.

Instrucciones admitidas:
  - Asignaciones:     minutos = 90;
  - Proyección:       proyectar("Hola mundo");
  - Matemáticas:      r = raiz(144);  sen = seno(1.57);
  - Estructuras:      p = pila();  apilar(p, "Messi");
  - Bucles:           en_juego (i < 3) { ... }
  - Machine Learning: mod = regresion_lineal([1,2,3], [2,4,6]);
""")
                    continue

                if linea_limpia == "simbolos":
                    print("--- Símbolos en Memoria ---")
                    ts = getattr(visitor, "tabla_simbolos", None)
                    if ts and hasattr(ts, "simbolos"):
                        for k, v in ts.simbolos.items():
                            print(f"  • {k}: {v}")
                    else:
                        print("  (Ámbito global vacío)")
                    continue

            nivel_llaves += linea.count("{") - linea.count("}")
            buffer_codigo.append(linea)

            if nivel_llaves <= 0:
                codigo_a_ejecutar = chr(10).join(buffer_codigo)
                ejecutar_bloque(codigo_a_ejecutar, visitor)
                buffer_codigo = []
                nivel_llaves = 0

        except KeyboardInterrupt:
            print(chr(10) + "(Entrada cancelada. Escribe 'salir' para terminar)")
            buffer_codigo = []
            nivel_llaves = 0
        except EOFError:
            print(chr(10) + "Cerrando sesión de DaZe.")
            break

def main():
    if len(sys.argv) == 1:
        iniciar_repl()
        return

    args = sys.argv[1:]
    solo_check = "--check" in args
    ver_tokens = "--tokens" in args
    ver_arbol = "--tree" in args

    archivos = [a for a in args if not a.startswith("--")]

    if not archivos:
        iniciar_repl()
        return

    ruta_archivo = archivos[0]
    if not os.path.exists(ruta_archivo):
        print(f"Error: No se encontró el archivo '{ruta_archivo}'")
        sys.exit(1)

    with open(ruta_archivo, "r", encoding="utf-8") as f:
        codigo = f.read()

    input_stream = InputStream(codigo)
    lexer = DaZeLexer(input_stream)

    if ver_tokens:
        token_stream = CommonTokenStream(lexer)
        token_stream.fill()
        for tok in token_stream.tokens:
            print(tok)
        return

    error_listener = DaZeErrorListener()
    lexer.removeErrorListeners()
    lexer.addErrorListener(error_listener)

    token_stream = CommonTokenStream(lexer)
    parser = DaZeParser(token_stream)
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)

    tree = parser.programa()

    if error_listener.has_errors():
        for err in error_listener.get_errors():
            print(f"[Error {err.error_type}] Línea {err.line}:{err.column} -> {err.message}")
        sys.exit(1)

    if solo_check:
        print(f"✓ El archivo '{ruta_archivo}' es sintácticamente válido.")
        return

    if ver_arbol:
        renderizar_arbol(tree, parser)
        return

    visitor = DaZeSemanticVisitor()
    visitor.visit(tree)
    print(f"✓ Ejecución completada con éxito para '{ruta_archivo}'.")

if __name__ == "__main__":
    main()
