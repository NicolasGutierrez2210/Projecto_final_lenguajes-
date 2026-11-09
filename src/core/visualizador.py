import os
import struct
import zlib

def _empaquetar_png(ancho, alto, pixeles):
    """Genera los bytes de un archivo PNG válido usando únicamente zlib estándar."""
    header = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('>IIBBBBB', ancho, alto, 8, 2, 0, 0, 0)
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data)
    ihdr = struct.pack('>I', len(ihdr_data)) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)

    raw_data = bytearray()
    for y in range(alto):
        raw_data.append(0)  # Filtro PNG 0: None
        for x in range(ancho):
            r, g, b = pixeles[y][x]
            raw_data.extend((r, g, b))

    comprimido = zlib.compress(bytes(raw_data), level=6)
    idat_crc = zlib.crc32(b'IDAT' + comprimido)
    idat = struct.pack('>I', len(comprimido)) + b'IDAT' + comprimido + struct.pack('>I', idat_crc)

    iend_crc = zlib.crc32(b'IEND')
    iend = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc)
    return header + ihdr + idat + iend


class CanvasPNG:
    """Lienzo gráfico 2D en memoria para trazado de primitivas geométricas."""
    def __init__(self, ancho=640, alto=420, color_fondo=(250, 250, 252)):
        self.ancho = ancho
        self.alto = alto
        self.pixeles = [[color_fondo for _ in range(ancho)] for _ in range(alto)]

    def set_pixel(self, x, y, color):
        if 0 <= x < self.ancho and 0 <= y < self.alto:
            self.pixeles[y][x] = color

    def rectangulo(self, x1, y1, x2, y2, color):
        xa, xb = max(0, min(x1, x2)), min(self.ancho - 1, max(x1, x2))
        ya, yb = max(0, min(y1, y2)), min(self.alto - 1, max(y1, y2))
        for y in range(ya, yb + 1):
            for x in range(xa, xb + 1):
                self.pixeles[y][x] = color

    def linea(self, x0, y0, x1, y1, color):
        """Algoritmo de Bresenham para trazar líneas de ejes y curvas."""
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.set_pixel(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circulo(self, cx, cy, radio, color):
        for y in range(cy - radio, cy + radio + 1):
            for x in range(cx - radio, cx + radio + 1):
                if (x - cx) ** 2 + (y - cy) ** 2 <= radio ** 2:
                    self.set_pixel(x, y, color)

    def guardar(self, ruta):
        os.makedirs(os.path.dirname(ruta) or ".", exist_ok=True)
        datos_png = _empaquetar_png(self.ancho, self.alto, self.pixeles)
        with open(ruta, "wb") as f:
            f.write(datos_png)


def _obtener_rgb(nombre_color):
    colores = {
        "azul": (41, 128, 185),
        "royalblue": (41, 128, 185),
        "rojo": (231, 76, 60),
        "crimson": (231, 76, 60),
        "verde": (39, 174, 96),
        "seagreen": (39, 174, 96),
        "naranja": (230, 126, 34),
        "darkorange": (230, 126, 34),
        "morado": (142, 68, 173)
    }
    return colores.get(nombre_color.lower(), (52, 73, 94))


def renderizar_pizarra_nativa(tipo, filas, config):
    """
    Renderiza el gráfico de forma dual:
    1. Gráfico en consola en caracteres ASCII/Unicode.
    2. Archivo físico .png mediante CanvasPNG nativo sin librerías externas.
    """
    eje_x = config.get("eje_x", "").strip("'\"")
    eje_y = config.get("eje_y", "").strip("'\"")
    titulo = config.get("titulo", f"Pizarra {tipo.capitalize()}").strip("'\"")
    color_nombre = config.get("color", "azul").strip("'\"")
    salida = config.get("guardar", f"salidas/pizarra_{tipo}.png").strip("'\"")
    color_rgb = _obtener_rgb(color_nombre)

    # 1. RENDERIZADO EN CONSOLA (ASCII)
    print(f"\n\033[1;36m┌────────────────────────────────────────────────────────┐\033[0m")
    print(f"\033[1;36m│ [PIZARRA {tipo.upper()}] {titulo[:42]:<42} │\033[0m")
    print(f"\033[1;36m└────────────────────────────────────────────────────────┘\033[0m")

    canvas = CanvasPNG(ancho=640, alto=420)
    # Dibujar marco y ejes del gráfico
    canvas.rectangulo(50, 40, 600, 370, (255, 255, 255))
    canvas.linea(70, 350, 580, 350, (40, 40, 40))   # Eje X
    canvas.linea(70, 60, 70, 350, (40, 40, 40))     # Eje Y

    if tipo == "barras":
        etiquetas = [str(f.get(eje_x, f"Item {i+1}")) for i, f in enumerate(filas)]
        valores = [float(f.get(eje_y, 0)) for f in filas]
        max_v = max(valores) if valores and max(valores) > 0 else 1.0

        for i, (etq, val) in enumerate(zip(etiquetas, valores)):
            long_barra = int((val / max_v) * 28)
            barra_ascii = "█" * long_barra
            print(f"  {etq:>14} │ {barra_ascii} {val}")

        # Trazado en PNG
        n = max(1, len(valores))
        ancho_barra = min(60, int(460 / n) - 15)
        paso = int(480 / n)
        for i, val in enumerate(valores):
            altura = int((val / max_v) * 260)
            x0 = 85 + (i * paso)
            y0 = 349 - altura
            canvas.rectangulo(x0, y0, x0 + ancho_barra, 349, color_rgb)

    elif tipo == "dispersion":
        vx = [float(f.get(eje_x, 0)) for f in filas]
        vy = [float(f.get(eje_y, 0)) for f in filas]
        min_x, max_x = (min(vx), max(vx)) if vx else (0, 1)
        min_y, max_y = (min(vy), max(vy)) if vy else (0, 1)
        rango_x = (max_x - min_x) if max_x != min_x else 1.0
        rango_y = (max_y - min_y) if max_y != min_y else 1.0

        print(f"  Puntos proyectados (Total: {len(vx)} registros):")
        for i in range(min(5, len(vx))):
            print(f"    • ({eje_x}: {vx[i]}, {eje_y}: {vy[i]})")
        if len(vx) > 5:
            print(f"    ... [{len(vx) - 5} puntos adicionales procesados]")

        # Trazado en PNG
        for x, y in zip(vx, vy):
            px = int(80 + ((x - min_x) / rango_x) * 480)
            py = int(340 - ((y - min_y) / rango_y) * 260)
            canvas.circulo(px, py, 4, color_rgb)

    elif tipo == "histograma":
        col = eje_x if eje_x else eje_y
        vals = [float(f.get(col, 0)) for f in filas]
        min_v, max_v = (min(vals), max(vals)) if vals else (0, 1)
        bins = 5
        ancho_bin = (max_v - min_v) / bins if max_v != min_v else 1.0
        conteos = [0] * bins

        for v in vals:
            idx = int((v - min_v) / ancho_bin)
            if idx >= bins:
                idx = bins - 1
            conteos[idx] += 1

        max_c = max(conteos) if conteos and max(conteos) > 0 else 1
        for b in range(bins):
            r0 = min_v + b * ancho_bin
            r1 = r0 + ancho_bin
            barra_ascii = "▓" * int((conteos[b] / max_c) * 25)
            print(f"  [{r0:>5.1f} - {r1:>5.1f}] │ {barra_ascii} ({conteos[b]})")

        # Trazado en PNG
        paso = int(480 / bins)
        for b in range(bins):
            altura = int((conteos[b] / max_c) * 260)
            x0 = 85 + b * paso
            y0 = 349 - altura
            canvas.rectangulo(x0, y0, x0 + paso - 10, 349, color_rgb)

    elif tipo in ("lineas", "caja"):
        etiquetas = [str(f.get(eje_x, f"P{i+1}")) for i, f in enumerate(filas)]
        valores = [float(f.get(eje_y, 0)) for f in filas]
        max_v = max(valores) if valores and max(valores) > 0 else 1.0

        for etq, val in zip(etiquetas, valores):
            punto = "─" * int((val / max_v) * 25) + "●"
            print(f"  {etq:>14} │ {punto} {val}")

        # Trazado en PNG
        puntos = []
        paso = int(480 / max(1, len(valores) - 1)) if len(valores) > 1 else 240
        for i, val in enumerate(valores):
            px = 80 + i * paso
            py = int(340 - (val / max_v) * 260)
            puntos.append((px, py))
            canvas.circulo(px, py, 3, (30, 30, 30))

        for i in range(len(puntos) - 1):
            canvas.linea(puntos[i][0], puntos[i][1], puntos[i+1][0], puntos[i+1][1], color_rgb)

    # 2. GUARDAR ARCHIVO PNG FÍSICO
    canvas.guardar(salida)
    print(f"\033[1;32m✓ Pizarra '{tipo}' generada con éxito (PNG puro sin librerías): {salida}\033[0m\n")
